import subprocess
import os
import glob
from pyrevit import script

def jarvis(installDir):
    out = script.get_output()
    out.print_html('<em>Jarvis</em> &mdash; updating ...')
    print(subprocess.check_output('cd {} & git pull --recurse-submodules'.format(installDir), stderr=subprocess.STDOUT, shell=True))
    
def extension(repo):
    status = subprocess.check_output('cd {} & git status --untracked-files=no --porcelain'.format(repo), stderr=subprocess.STDOUT, shell=True)
    if status:
        print('Skipped update &mdash; repository not clean! :flushed_face:')
    else:
        print(subprocess.check_output('cd {} & git pull'.format(repo), stderr=subprocess.STDOUT, shell=True))
    
def extensions(extensionsDir):
    out = script.get_output()
    for git in glob.glob('{}\\*\\.git'.format(extensionsDir)):
        out.print_html('<br>')
        repo = os.path.dirname(git)
        out.print_html('<em>{}</em> &mdash; updating ...'.format(os.path.basename(repo)))
        extension(repo)
        