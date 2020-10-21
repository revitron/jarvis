"""
Check for pyRevit core and extension updates and optionally install them. 
"""
from rpm.system.ui import UI
from pyrevit.coreutils.ribbon import ICON_LARGE

__context__ = 'zero-doc'

buttonCmp = None
scriptCmp = None

def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
	buttonCmp = ui_button_cmp
	scriptCmp = script_cmp
	updateButton(scriptCmp, buttonCmp, False)
	return True

def updateButton(script_cmp, ui_button_cmp, force = False):
	if UI.checkUpdates(force):
		ui_button_cmp.set_title('Install\nUpdates')
		update_icon = script_cmp.get_bundle_file('icon-has-updates.png')
		ui_button_cmp.set_icon(update_icon, icon_size=ICON_LARGE)

if __name__ == '__main__':
	updateButton(scriptCmp, buttonCmp, True)
	


