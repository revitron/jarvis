import subprocess
import os
import glob
from pyrevit import script
import constants


class Update:

    def __init__(self):
        Update.jarvis(constants.JRVS_DIR)
        Update.extensions(constants.JRVS_EXTENSIONS_DIR)
        
    @staticmethod
    def git(cmd, repo):
        return subprocess.check_output('git --git-dir={0}\\.git --work-tree={0} {1}'.format(repo, cmd), stderr=subprocess.STDOUT, shell=True)
        
    @staticmethod
    def jarvis(installDir):
        out = script.get_output()
        out.print_html('<em>Jarvis</em> &mdash; updating ...')
        print(Update.git('pull --recurse-submodules', installDir))
    
    @staticmethod 
    def extension(repo):
        status = Update.git('status --untracked-files=no --porcelain', repo)
        if status:
            print('Skipped update &mdash; repository not clean! :flushed_face:')
        else:
            print(Update.git('pull', repo))
    
    @staticmethod
    def extensions(extensionsDir):
        out = script.get_output()
        for git in glob.glob('{}\\*\\.git'.format(extensionsDir)):
            out.print_html('<br>')
            repo = os.path.dirname(git)
            out.print_html('<em>{}</em> &mdash; updating ...'.format(os.path.basename(repo)))
            Update.extension(repo)
        