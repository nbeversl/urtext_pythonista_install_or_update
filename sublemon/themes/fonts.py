from objc_util import ObjCClass

# examples

fonts = {
	'Courier New': ObjCClass('UIFont').fontWithName_size_('Courier New', 12),
	'Courier New Bold': ObjCClass('UIFont').fontWithName_size_('Courier New Bold', 12)
		
}
