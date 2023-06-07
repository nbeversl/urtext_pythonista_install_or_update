import os 
from app_single_launch import AppSingleLaunch
from urtext_pythonista.urtext_pythonista import UrtextEditor

# Usage:
#
# 1. Move this file into the "This iPhone" folder of Pythonista 3
#
# 2. Set the `path` variable below to the location
#    of your Urtext project inside of the iCloud Drive/Pythonista 3
#    folder.
#
path = 'Urtext Projects/My Urtext Project' # (example)
#
# 3. For a single-step launch, using the iOS Shortcuts app,
#    create a shorcut that opens the URL:
#    pythonista://launch_urtext_pythonista.py?action=run
#
#    This can then be added to your iOS home screen.
#

app = AppSingleLaunch("Urtext Pythonista")
if not app.is_active():
    s = UrtextEditor({ 
        'path' : os.path.join(
            '/private/var/mobile/Library/Mobile Documents/iCloud~com~omz-software~Pythonista3/Documents/',
            path)
    })
    app.will_present(s.tv)
    s.show()
    
