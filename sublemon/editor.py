import os
import ui
import dialogs
import console
from objc_util import *
from sublemon.syntax_highlighter import SyntaxHighlighter
from sublemon.auto_completer import AutoCompleter
from sublemon.text_view_delegate import TextViewDelegate
from sublemon.layout import layout
from sublemon.settings import settings
from sublemon.base_editor_theme import base_editor_theme
from sublemon.plaintext_syntax import PlaintextSyntax
from sublemon.themes.theme_example import theme_light

class BaseEditor(ui.View):

	layout = layout
	name = "Base Editor"
	syntax = PlaintextSyntax

	def __init__(self, args):

		if 'theme' in args:
			self.theme = args['theme']
		else:
			self.theme = base_editor_theme
		self.theme_options = {}
		if 'themes' in args:
			for theme in args['themes']:
				self.theme_options[theme['name']] = theme
			if args['themes']:
				self.theme = args['themes'][0]	
		else:
			self.theme = theme_light

		self.current_open_file = None
		self.current_open_file_original_contents = None
		self.saved = None
		self.menu_options = {'Set Theme' : self.choose_theme}
		self.width, self.height = ui.get_screen_size()
		self.frame = (0, self.layout['text_view_distance_from_top'], self.width, self.height)
		self.init_text_view()
		self.setup_obj_instances()
		self.setup_autocomplete()
		self.set_theme(self.theme['name'])
		self.setup_syntax_highlighter()

	def show(self):
		self.present('fullscreen', hide_title_bar=True)
		self.tv.begin_editing()

	def setup_syntax_highlighter(self):
		self.syntax_highlighter = SyntaxHighlighter(
			self.syntax,
			self.theme)

	def setup_buttons(self, buttons):
		if not buttons:
			buttons= {
				'Open' : self.open_file,
				'Save' : self.save,
				'Save As...' : self.save_as,
				'↓' : self.hide_keyboard,
			}
		self._build_button_container(buttons)

	def setup_autocomplete(self):
		self.autoCompleter = AutoCompleter(
			self.width, self.height, self.layout, self.theme)
		self.add_subview(self.autoCompleter.search)
		self.add_subview(self.autoCompleter.dropDown)

	def open_file(self, filename, save_first=True):
		if save_first and self.current_open_file != filename:
		 	self.save(None)
		open_file = dialogs.pick_document()
		if open_file:
			contents = self.get_file_contents(open_file)
			self.tv.text=contents
			self.current_open_file = open_file
			self.current_open_file_original_contents = contents
			self.refresh_syntax_highlighting()

	def choose_theme(self, sender):
		self.autoCompleter.set_items(items=self.theme_options)
		self.autoCompleter.set_action(self.set_theme)
		self.autoCompleter.show()

	def set_theme(self, theme):
		self.theme = self.theme_options[theme]
		self.tvo.setBackgroundColor(self.theme['background_color'])
		if 'keyboard_appearance' in self.theme:
			self.tvo.setKeyboardAppearance_(self.theme['keyboard_appearance'])
		self.setup_syntax_highlighter()

	def init_text_view(self):
		self.tv = ui.TextView()
		self.tv.frame=(
			0, 
			0,
			self.width, 
			self.height)
		
		self.tv.width = self.width
		self.tv.delegate = TextViewDelegate(self)
		self.add_subview(self.tv)

	def _build_button_container(self, buttons):
		num_buttons = len(buttons)
		num_button_lines = 1
		button_space_per_line = self.width - self.layout['button_horizontal_spacing']
		button_width_with_spacing = int( button_space_per_line / num_buttons )
		while button_width_with_spacing < ( self.layout['min_button_width'] + self.layout['button_horizontal_spacing']):
			num_button_lines += 1
			button_width_with_spacing = int( 
					( button_space_per_line * num_button_lines ) / num_buttons 
					)
		button_width = button_width_with_spacing - self.layout['button_horizontal_spacing']

		button_x_position = self.layout['button_horizontal_spacing']
		button_y_position = self.layout['button_vertical_spacing']
		button_line = ui.View()
		button_line.flex = "WHLR"
		button_line.background_color = self.theme['button_line_background_color']
		button_line.height = self.layout['button_height'] * num_button_lines 
		button_line.height += self.layout['button_vertical_spacing'] * num_button_lines

		buttons_this_line = 1
		for button_character in buttons:
			new_button = ui.Button(title=button_character)
			new_button.action = buttons[button_character]
			new_button.corner_radius = self.layout['button_corner_radius']
			new_button.height = self.layout['button_height']
			new_button.tint_color = self.theme['button_tint_color']
			if button_x_position + button_width >= self.width :
				button_y_position += self.layout['button_height'] + self.layout['button_vertical_spacing']
				button_x_position = self.layout['button_horizontal_spacing']
			new_button.frame = (button_x_position, 
				button_y_position,
				button_width,
				self.layout['button_height'])
			button_line.add_subview(new_button)
			button_x_position += button_width + self.layout['button_horizontal_spacing']
			new_button.border_width = self.layout['button_border_width']
			new_button.border_color = self.theme['button_border_color']
			new_button.background_color = self.theme['button_background_color']

		self.add_subview(button_line)
		self.tvo.setInputAccessoryView_(ObjCInstance(button_line))

	def setup_obj_instances(self):
		self.tvo = ObjCInstance(self.tv)
		self.tvo.setAllowsEditingTextAttributes_(True)	

	def hide_keyboard(self, sender):
		self.tv.end_editing()

	def save_as(self, sender):
		self.current_open_file = console.input_alert(
			title='Filename',
			message='Note files will be saved in the Pythonista folder, also accessible via iCloud')
		self.save(None)

	def save(self, sender, save_as=True):
		if self.saved:
			return True
		if self.current_open_file:
			current_file_contents = self.get_file_contents(self.current_open_file)
			if self.current_open_file_original_contents != current_file_contents:
				ask = self.handle_changed_contents(self.current_open_file) 
				if ask != 'Overwrite (use current view)':
					return False
			contents = self.tv.text 
			with open(self.current_open_file, 'w', encoding='utf-8') as d:
				d.write(contents)
			self.saved = True
			self.current_open_file_original_contents = contents
			return True
		elif save_as:
			return self.save_as(None)
		return False

	def handle_changed_contents(self, filename):
		return dialogs.list_dialog(
			title='This File\'s Contents Changed.', 
			items=[
				'Overwrite (use current view)',
				'Discard (Keep contents on disk)',
			])

	def get_file_contents(self, filename):
		with open(filename, 'r', encoding='utf-8') as d:
			contents = d.read()
		return contents

	def refresh_syntax_highlighting(self, text=''):   
		self.syntax_highlighter.setAttribs(self.tv, self.tvo, self.theme)
