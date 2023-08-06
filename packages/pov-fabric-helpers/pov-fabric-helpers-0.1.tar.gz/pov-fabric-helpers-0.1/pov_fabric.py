"""
Fabric helpers
"""

import sys
import posixpath
from pipes import quote  # TBD: use shlex.quote on Python 3.2+

from fabric.api import run, sudo, quiet, settings, cd, env, abort, task
from fabric.contrib.files import exists, append


#
# Command-line parsing
#

def asbool(v):
    """Convert value to boolean."""
    if isinstance(v, basestring):
        return v.lower() in ('yes', 'true', 'on', '1')
    else:
        return bool(v)


#
# System management helpers
#

def ensure_apt_not_outdated():
    """Make sure apt-get update was run within the last day."""
    if not run("find /var/lib/apt/lists -maxdepth 0 -mtime -1", quiet=True):
        sudo("apt-get update -qq")


def package_installed(package):
    """Check if the specified packages is installed."""
    # XXX: doing this in a loop is slow :(
    with quiet():
        status = run("dpkg-query -W --showformat='${Status}' %s" % package)
        return status == "install ok installed"


def install_packages(*packages, **kw):
    """Install system packages.

    You can use any of these styles::

        install_packages('foo bar')
        install_packages('foo', 'bar')
        install_packages(['foo', 'bar'])

    Keyword arguments:

    - ``missing_only`` (default: False) -- apt-get install only the missing
      packages.  This can be slower than just letting apt figure it out.

    - ``interactive`` (default: False) -- allow interactive prompts during
      package installation.

    """
    missing_only = kw.pop('missing_only', True)
    interactive = kw.pop('interactive', False)
    if kw:
        raise TypeError('unexpected keyword arguments: {}'
                        .format(', '.join(sorted(kw))))
    if len(packages) == 1 and not isinstance(packages[0], str):
        # handle lists and tuples
        packages = packages[0]
    if missing_only:
        packages = [p for p in packages if not package_installed(p)]
    if not packages:
        return
    ensure_apt_not_outdated()
    command = "apt-get install -qq -y %s" % " ".join(packages)
    if not interactive:
        command = "DEBIAN_FRONTEND=noninteractive " + command
    sudo(command)


def ensure_known_host(host_key, known_hosts='/root/.ssh/known_hosts'):
    """Make sure a host key exists in the known_hosts file.

    This is idempotent: running it again won't add the same key again.
    """
    if not exists(known_hosts, use_sudo=True):
        if not exists(posixpath.dirname(known_hosts), use_sudo=True):
            sudo('install -d -m700 %s' % posixpath.dirname(known_hosts))
        sudo('touch %s' % known_hosts)
    # Must use shell=True to work around Fabric bug, where it would fall
    # flat in contains() with an error ("sudo: export: command not
    # found") that is silently suppressed, resulting in always appending
    # the ssh key to /root/.ssh/known_hosts.  Probably because I use
    # `with settings(shell_env(LC_ALL='C.UTF-8')):`.
    append(known_hosts, host_key, use_sudo=True, shell=True)


def ensure_user(user):
    """Create a system user if it doesn't exist already.

    This is idempotent: running it again won't add the same user again.
    """
    with quiet():
        if run("id {user}".format(user=user)).succeeded:
            return
    with settings(sudo_user="root"):
        sudo("adduser --system --group --disabled-password --quiet %s" % user)


#
# Git
#

def git_clone(git_repo, work_dir, force=False):
    """Clone a git repository into work_dir.

    If work_dir exists and force is False (default), aborts.

    If work_dir exists and force is True, performs a 'git fetch' followed by
    'git reset origin/master'.

    Takes care to allow SSH agent forwarding to be used for authentication.

    Returns the commit hash of the version cloned.
    """
    # sudo removes SSH_AUTH_SOCK from the environment, so we can't make use of
    # the ssh agent forwarding unless we cunningly preserve the envvar and sudo
    # to root (because only root and the original user will be able to access
    # the socket)
    ssh_auth_sock = run("echo $SSH_AUTH_SOCK", quiet=True)
    if exists(posixpath.join(work_dir, '.git')) and force:
        with cd(work_dir):
            sudo("SSH_AUTH_SOCK={ssh_auth_sock} git fetch".format(
                ssh_auth_sock=ssh_auth_sock))
            sudo("git reset origin/master")
    else:
        sudo("SSH_AUTH_SOCK={ssh_auth_sock} git clone {git_repo} {work_dir}".format(
            ssh_auth_sock=ssh_auth_sock,
            git_repo=git_repo,
            work_dir=work_dir))
    with cd(work_dir):
        got_commit = sudo("git describe --always").strip()
    return got_commit


#
# PostgreSQL helper
#

def postgresql_user_exists(user):
    """Check if a postgresql user already exists."""
    out = sudo("psql -tAc \"SELECT 1 FROM pg_roles WHERE rolname = '%s'\"" % user,
               user='postgres', quiet=True)
    return bool(out)


def ensure_postgresql_user(user):
    """Create a PostgreSQL user if it doesn't exist already.

    This is idempotent: running it again won't add the same user again.
    """
    if not postgresql_user_exists(user):
        sudo("LC_ALL=C.UTF-8 createuser -DRS %s" % user, user='postgres')


def postgresql_db_exists(dbname):
    """Check if a PostgreSQL database already exists."""
    out = sudo("psql -tAc \"SELECT 1 FROM pg_database WHERE datname = '%s'\"" % dbname,
               user='postgres', quiet=True)
    return bool(out)


def ensure_postgresql_db(dbname, owner):
    """Create a PostgreSQL database if it doesn't exist already.

    This is idempotent: running it again won't create the database again.
    """
    if not postgresql_db_exists(dbname):
        sudo("LC_ALL=C.UTF-8 createdb -E utf-8 -T template0 -O %s %s" % (owner, dbname),
             user='postgres')


#
# pov-admin-tools
#

def changelog(message, append=False, optional=True):
    """Append a message to /root/Changelog, with a timestamped header.

    Depends on pov-admin-tools.  If it's not installed, skips the
    message (unless you say optional=False, in which case it aborts
    with an error).

    By default the message gets a timestamped header.  Use append=True
    to append to an existing message instead of starting a new one.
    """
    if exists('/usr/sbin/new-changelog-entry') or not optional:
        cmd = 'new-changelog-entry'
        if append:
            cmd += ' -a'
        cmd += ' ' + quote(message)
        sudo(cmd, user='root')


def changelog_append(message):
    """Append a message to /root/Changelog.

    Shortcut for changelog(message, append=True).
    """
    changelog(message, append=True)


#
# Instance management
#


class Instance(object):
    """Service instance configuration.

    Subclass to add more parameters, e.g. ::

        from pov_fabric import Instance as BaseInstance

        class Instance(BaseInstance):
            def __init__(self, name, host, home='/opt/project'):
                super(Instance, self).Instance.__init__(name, host)
                self.home = home

    Or use the ``with_params()`` classmethod.
    """

    def __init__(self, name, host, **kwargs):
        self.name = name
        self.host = host
        self.__dict__.update(kwargs)

    def _asdict(self):
        """Return the instance parameters as a dict.

        Useful for string formatting, e.g. ::

            print('{name} is on {host}'.format(**instance._asdict()))

        Mimics the API of ``collections.namedtuple``.
        """
        return self.__dict__

    REQUIRED = object()

    @classmethod
    def with_params(cls, **params):
        """Define an instance subclass

        Usage example::

            from pov_fabric import Instance

            Instance = Instance.with_params(
                required_arg1=Instance.REQUIRED,
                optional_arg1='default value',
                optional_arg2=None)

        """

        def __init__(self, name, host, **kw):
            super(new_cls, self).__init__(name, host)
            for k, v in params.items():
                if v is cls.REQUIRED and k not in kw:
                    raise TypeError(
                        "__init__() requires a keyword argument '{}'"
                        .format(k))
                setattr(self, k, v)
            for k, v in kw.items():
                if k not in params:
                    raise TypeError(
                        "__init__() got an unexpected keyword argument '{}'"
                        .format(k))
                setattr(self, k, v)
        new_cls = type('Instance', (cls, ), dict(__init__=__init__))
        return new_cls

    @classmethod
    def define(cls, *args, **kwargs):
        """Define an instance.

        Creates a new Instance object with the given constructor arguments,
        registers it in env.instances and defines an instance selector task.
        """
        instance = cls(*args, **kwargs)
        _define_instance(instance)
        _define_instance_task(instance.name, stacklevel=2)


def _define_instance(instance):
    """Define an instance.

    Instances are stored in the ``env.instances`` dictionary, which is created
    on demand.
    """
    if not hasattr(env, 'instances'):
        env.instances = {}
    if instance.name in env.instances:
        abort("Instance {name} is already defined.".format(name=instance.name))
    env.instances[instance.name] = instance


def _define_instance_task(name, stacklevel=1):
    """Define an instance task

    This task will set env.instance to the name of the task.
    """
    def fn():
        env.instance = name
    fn.__doc__ = """Select instance '%s' for subsequent tasks.""" % name
    instance_task = task(name=name)(fn)
    sys._getframe(stacklevel).f_globals[name.replace('-', '_')] = instance_task


def get_instance(instance_name=None):
    """Select the instance to operate on.

    Defaults to env.instance if instance_name is not specified.

    Aborts with a help message if the instance is not defined.
    """
    instances = sorted(getattr(env, 'instances', {}))
    if not instances:
        abort("There are no instances defined in env.instances.")
    if not instance_name:
        instance_name = getattr(env, 'instance', None)
    try:
        return env.instances[instance_name]
    except KeyError:
        abort("Please specify an instance ({known_instances}), e.g.\n\n"
              "  fab {instance} {command}".format(
                  known_instances=", ".join(instances),
                  instance=instances[0],
                  command=env.command))
