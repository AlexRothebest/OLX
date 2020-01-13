import os

import subprocess


get_pip_directory = os.getcwd() + '\get-pip.py'
subprocess.call('python ' + get_pip_directory)

requirements_directory = os.getcwd() + '\ '[0] + 'requirements.txt'
subprocess.call('pip install -r ' + requirements_directory)