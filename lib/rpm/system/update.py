import subprocess
import os
import glob
from pyrevit import script
from rpm import config


class Update:
		
	@staticmethod
	def check(repo):  
		out = script.get_output()
		try:
			if not os.path.isdir(repo + '\\.git'):
				return False
			if not Update.remoteExists(repo):
				out.print_html('<br>Error: Remote of repository "{}" not found!'.format(os.path.basename(repo)))
				return False
			status = Update.git('fetch origin --dry-run', repo)
			if status:
				out.print_html('<br><b>{}</b> &mdash; updates available'.format(os.path.basename(repo)))			
				print(status)
				return True
		except:
			pass	
   		return False
		
	@staticmethod
	def checkExtensions():
		for repo in Update.getExtensionRepos():
			if Update.check(repo):
				return True
		return False
				
	@staticmethod
	def checkPyRevit():
		return Update.check(config.RPM_PYREVIT_DIR)    
		
	@staticmethod
	def git(cmd, repo):
		return subprocess.check_output('set GIT_TERMINAL_PROMPT=0 && git -c credential.helper= --git-dir={0}\\.git --work-tree={0} {1}'.format(repo, cmd), 
                                 	   stderr=subprocess.STDOUT, 
                                       shell=True, 
                                       cwd='C:\\')
		
	@staticmethod
	def getExtensionRepos():
		repos = []
		for git in glob.glob('{}\\*\\.git'.format(config.RPM_EXTENSIONS_DIR)):
			repos.append(os.path.dirname(git))
		return repos
				
	@staticmethod
	def pyRevit():
		os.system('{}\\updatePyRevit.bat {}'.format(os.path.dirname(__file__), config.RPM_PYREVIT_DIR))
	
	@staticmethod 
	def extension(repo):
		if not Update.remoteExists(repo):
			print('Error: Remote of repository "{}" not found!'.format(os.path.basename(repo)))
			return False
		status = Update.git('status --untracked-files=no --porcelain', repo)
		if status:
			print('Skipped update &mdash; repository not clean!')
		else:
			print(Update.git('pull', repo))
	
	@staticmethod
	def extensions():
		out = script.get_output()
		for repo in Update.getExtensionRepos():
			out.print_html('<br><b>{}</b> &mdash; updating ...'.format(os.path.basename(repo)))
			Update.extension(repo)
   
	@staticmethod
	def remoteExists(repo):
		url = Update.git('remote get-url --all origin', repo).rstrip()
		try:
			Update.git('ls-remote {}'.format(url), repo)
			return True
		except:
			return False