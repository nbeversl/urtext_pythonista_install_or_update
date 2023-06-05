from urtext_theme_light import urtext_theme_light
from objc_util import ObjCClass

urtext_theme_light_custom = urtext_theme_light

urtext_theme_light_custom['font'] = {
    'regular' :  ObjCClass('UIFont').fontWithName_size_('Fira Code', 12),
    'bold' :    ObjCClass('UIFont').fontWithName_size_('FiraCode-Bold', 12),
}