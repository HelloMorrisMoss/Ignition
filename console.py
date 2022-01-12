"""Code for use in the Ignition Designer's Script Console.

Functions
	recurse_find_code: called from within the console will return the code text itself as unicode.
	save_console_code: called from within the console will save the code text to a file.
	
"""


def recurse_find_code(comp=None, indent=0):
	"""Get the code from the Ignition Script Console where this is called as unicode."""
	
	import java
	import com.inductiveautomation.ignition.designer.gui.tools.CodeEditor
	
	
	# find the root
	if comp is None:
		comp = java.awt.KeyboardFocusManager.getCurrentKeyboardFocusManager().getFocusOwner().getRootPane()

	# iterate through descendent components to find the CodeEditor
	for kid in comp.getComponents():
		if isinstance(kid, com.inductiveautomation.ignition.designer.gui.tools.CodeEditor):
			# return the code
			return kid.text
		else:
			# dig deeper
			new_indent = indent + 1
			result = recurse_find_code(kid, new_indent)
			if result:
				return result
	return None


def save_console_code(save_path=None):
	"""Save Ignition Script Console code.
	
	Call this at the top of the code in anIgnition Designer Script Console to save the
	code automatically when run. Defaults to the user's home directory in a file named
	console_code.py
	
	:param save_path: str, the desired path to save the backup
	
	"""
	
	import os
	import java
	
	# default to a file in the user's home directory
	if not save_path:
		home_dir = java.lang.System.getProperty('user.home')
		save_path = os.path.join(home_dir, 'console_code.py')

	code_txt = recurse_find_code()
	with open(save_path, 'w') as save_file:
		save_file.write(code_txt)
