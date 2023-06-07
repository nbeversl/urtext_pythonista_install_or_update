# Urtext Pythonista

This repository makes Urtext usable on iOS using the Pythonista 3 app (https://apps.apple.com/us/app/pythonista-3/id1085978097).

## Setup:

1. You must first get all of these files accessible within Pythonista on your iOS device. The easist way is:

	- download this repository as a .ZIP file from the device itself and save it inside iCloud (use "Save to Files")

	- in the Files app, uncompress the .ZIP file (click-hold and select "Uncompress"). You can then delete the .ZIP file.

	- move the uncompressed folder (`urtext_pythonista_deps-main`) into the Pythonista 3 folder by clicking the three dots at the top right, choose "Select", select the `urtext_pythonista_deps-main` folder, click the folder icon in the bottom toolbar, select the Pythonista 3 folder, and then click "Move" at the top right.

2. In the Pythonista 3 app, open the "iCloud" folder off the main menu and open `urtext_pythonista_deps-main` (this folder, which you just moved). Click the word "Edit" at the top right and and select all of the following folders AND files:

- anytree           
- dateutil
- sublemon
- thefuzz
- urtext
- urtext_pythonista 
- app_single_launch.py
- six.py 

Click the folder icon on the bottom left next to the trash can icon. In the "Move to..." dialog, select the folder `site-packages-3` under the `On this iPhone (or iPad)` folder.

If you have already followed these steps before and are updating, you will first have to delete the existing copies or you will see an error message.  

3. Do the same thing to move the launch script, `launch_urtext_pythonista.py` into the `On this iPhone (or iPad)` folder itself.

4. From the main menu, open up "This iPhone (or iPad)" menu and open `launch_urtext_pythonista.py` in the Pythonista 3 editor. Follow the usage instructions inside, which also explains how to set up a one-click launch using the Shortcuts app.

## Additional Information

This repository is a convenience only and may not contain the latest versions of all libraries/modules. Their source locations are below:

- anytree (https://github.com/c0fec0de/anytree)             
- dateutil (https://github.com/dateutil/dateutil)
- six (https://pypi.org/project/six/)
- sublemon (https://github.com/nbeversl/sublemon)
- thefuzz (https://github.com/seatgeek/thefuzz)
- urtext (https://github.com/nbeversl/urtext)
- urtext_pythonista (https://github.com/nbeversl/urtext_pythonista)
- app_single_launch (https://github.com/TPO-POMGOM/Pythonista-utilities/blob/master/app_single_launch.py)
