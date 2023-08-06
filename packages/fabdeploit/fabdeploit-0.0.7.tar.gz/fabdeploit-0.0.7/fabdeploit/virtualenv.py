from __future__ import absolute_import
import fabric.api as fab
import posixpath
from .utils import _select_bin

# IDEA:
# Initialize a virtualenv using some REQUIREMENTS file. Then initialize a
# git repository in it. Create tags for every release made using
# "release/$COMMIT_SHA1" as tag name. This way we can revert to old versions
# inside the virtualenv as well.


def _env_bin(*commands):
    if 'deploy_env_path' in fab.env:
        return _select_bin(*commands, paths=[
            posixpath.join(fab.env.deploy_env_path, 'bin'),
            posixpath.join(fab.env.deploy_env_path, 'Scripts'),
        ])
    else:
        return _select_bin(*commands)


def create_commit(message=None, tag=None):
    import datetime
    
    fab.require('deploy_env_path')
    
    if not getattr(fab.env, 'deploy_env_history', False):
        return
    
    if message is None:
        message = datetime.datetime.now().isoformat()
    with fab.cd(fab.env.deploy_env_path):
        # (re) initialize
        fab.run('git init')
        # TODO: Make sure this is done right:        
        ## switch back to latest commit
        #fab.run('git checkout master')
        # addremove everything
        fab.run('git add -A')
        fab.run('git ls-files --deleted -z | xargs -r -0 git rm')
        # create commit (may fail if no changes happened)
        with fab.settings(warn_only=True):
            fab.run('git commit --allow-empty -m "%s"' % message)
        # create tag if wanted
        if tag:
            fab.run('git tag "%s"' % tag)


def init(force=False):
    from fabric.contrib import files
    
    fab.require('deploy_env_path')
    
    if not force and files.exists(fab.env.deploy_env_path):
        return
    
    download_path = posixpath.join(fab.env.deploy_env_path, 'download')
    download_virtualenv_path = posixpath.join(download_path, 'virtualenv')
    download_virtualenv_bin = posixpath.join(download_virtualenv_path, 'virtualenv.py')
    fab.run('mkdir -p "%s"' % download_path)
    fab.run('git clone --depth 1 --branch master https://github.com/pypa/virtualenv.git %s' % download_virtualenv_path)
    fab.run('%s "%s" --clear --no-site-packages "%s"' % (
        _select_bin('python2', 'python'),
        download_virtualenv_bin,
        fab.env.deploy_env_path,
    ))


def update():
    import datetime
    
    fab.require(
        'deploy_env_path',
        'deploy_env_requirements')
    
    fab.run('%s install -Ur "%s"' % (
        _env_bin('pip2', 'pip'),
        fab.env.deploy_env_requirements,
    ))


def switch_release(commit):
    fab.require('deploy_env_path')
    
    if not getattr(fab.env, 'deploy_env_history', False):
        fab.abort('Cannot switch to older version, git is not enabled for virtualenv (see env.deploy_env_history)')
    
    with fab.cd(fab.env.deploy_env_path):
        # see git.py on why we do checkout + reset
        fab.run('git checkout "%s"' % commit)
        fab.run('git reset --hard')

