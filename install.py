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
	dependencies = [
		'anytree',
		'dateutil',
		'thefuzz',
		'six.py',
		'app_single_launch.py',
	]
	libraries = {
		'sublemon' : 'https://github.com/nbeversl/sublemon/archive/refs/heads/master.zip',
		'urtext_pythonista' : 'https://github.com/nbeversl/urtext_pythonista/archive/refs/heads/master.zip',
		'urtext' : 'https://github.com/nbeversl/urtext/archive/refs/heads/master.zip'
	}
	
	data = urllib.request.urlretrieve(
		'https://github.com/nbeversl/urtext_pythonista_install_or_update/archive/refs/heads/main.zip')
	dependencies_filename = data[0]
	z = zipfile.ZipFile(dependencies_filename)
	z.extractall()

	for lib in libraries:
		library = urllib.request.urlretrieve(libraries[lib])
		library_filename = library[0]
		z = zipfile.ZipFile(library_filename)
		z.extractall(os.getcwd())
		existing_folder = os.path.join(os.getcwd(), lib+ '-master')
		target_folder = os.path.join(os.getcwd(), lib)
		if os.path.exists(target_folder):
			shutil.rmtree(target_folder)
		os.rename(existing_folder, target_folder)

	all_libraries = list(dependencies) 
	all_libraries.extend(list(libraries.keys()))
	
	for l in all_libraries:
		if l in dependencies:
			source = os.path.abspath(
				os.path.join(
					os.getcwd(),
					'urtext_pythonista_install_or_update-main',
					l))
		else:
			source = os.path.abspath(
				os.path.join(
					os.getcwd(),
					l))
		if os.path.exists(source):
			destination = os.path.abspath(
				os.path.join(
					this_phone_path,
					'Documents',
					'site-packages',
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
	launch_script_path = os.path.abspath(
		os.path.join(
			os.getcwd(),
			'urtext_pythonista_install_or_update-main',
			'launch_urtext_pythonista.py'))
	if os.path.exists(launch_script_path):
		os.remove(launch_script_path)
	os.rename(launch_script_path,
				os.path.join(
				this_phone_path,
				'Documents',
				'launch_urtext_pythonista.py'))
	shutil.rmtree(os.path.join(
		os.getcwd(),
		'urtext_pythonista_install_or_update-main'))
	print('Done!')
else:
	print('Ok.')