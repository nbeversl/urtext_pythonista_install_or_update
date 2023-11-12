import os
import shutil
import urllib.request
import zipfile
import site

message = """
This script will download and install all the libraries needed to 
run Urtext in Pythonista. Existing copies of the libraries
will be erased and replaced. 

Do you want to proceed? (y/n)
"""
proceed = input(message)
if proceed.lower()[0] == 'y':
	this_phone_path = os.path.dirname(site.getuserbase())
	libraries = [
		'anytree',
		'dateutil',
		'sublemon',
		'thefuzz',
		'urtext',
		'urtext_pythonista',
		'six.py',
		'app_single_launch.py',
	]
	
	data = urllib.request.urlretrieve(
		'https://github.com/nbeversl/urtext_pythonista_install_or_update/archive/refs/heads/main.zip')
	filename = data[0]
	
	z=zipfile.ZipFile(filename)
	z.extractall()
	
	for l in libraries:
		source = os.path.abspath(
			os.path.join(
				os.getcwd(),
				# 'Documents',
				'urtext_pythonista_install_or_update-main',
				l))
		if os.path.exists(source):
			destination = os.path.abspath(
			os.path.join(
				this_phone_path,
				'Documents',
				'site-packages-3',
				l))
			if os.path.exists(destination):
				if os.path.isdir(destination):
					shutil.rmtree(destination)
				else:
					os.remove(destination)
			os.rename(source, destination)
			print('Installed or updated %s' % l)
		else:
			print('NO PATH %s' % source)
	shutil.rmtree(os.path.join(
		os.getcwd(),
		'urtext_pythonista_install_or_update-main'))
	print('Done!')
else:
	print('Ok.')

