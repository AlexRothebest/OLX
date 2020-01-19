import os

import subprocess

if os.name == 'nt':
	get_pip_directory = os.getcwd() + '\get-pip.py'
	subprocess.call('python ' + get_pip_directory)

	requirements_directory = os.getcwd() + '\ '[0] + 'requirements.txt'
	subprocess.call('pip install -r ' + requirements_directory)
else:
	get_pip_directory = os.getcwd() + '\get-pip.py'
	subprocess.call('python3 ' + get_pip_directory)

	requirements_directory = os.getcwd() + '\ '[0] + 'requirements.txt'
	subprocess.call('pip3 install -r ' + requirements_directory)