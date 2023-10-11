from objc_util import *

class SyntaxHighlighter:

	def __init__(self, syntax, theme):

		self.syntax = syntax(theme)
		self.theme = theme
		self.all_wrappers = []
		self.push_wrapper, self.pop_wrapper = get_push_pop_patterns(self.syntax.syntax)
		if self.push_wrapper:
			self.all_wrappers = [self.push_wrapper, self.pop_wrapper]

	@on_main_thread
	def setAttribs(self, tv, tvo, initial=False):

		current_text = tv.text
		str_obj = ObjCClass('NSMutableAttributedString').alloc().initWithString_(current_text)
		original_str_obj = ObjCClass('NSMutableAttributedString').alloc().initWithString_(current_text)  
		len_current_text = len(current_text)
		str_obj.addAttribute_value_range_(
			ObjCInstance(
				c_void_p.in_dll(c,'NSFontAttributeName')), 
			self.theme['font']['regular'], 
			NSRange(0,len_current_text))

		str_obj.addAttribute_value_range_(
			ObjCInstance(c_void_p.in_dll(c,'NSForegroundColorAttributeName')), 
			self.theme['foreground_color'],
			NSRange(0,len_current_text))

		nested_level = 0
		
		found_wrappers = find_wrappers(
			current_text, 
			self.all_wrappers)

		positions = sorted(found_wrappers.keys())
		len_wrappers = len(self.theme['wrappers'])

		for position in positions:
			# if the found wrapper is a push wrapper
			if self.push_wrapper.match(found_wrappers[position]):
				nested_level += 1
				if nested_level < len_wrappers:
					str_obj.addAttribute_value_range_(
					  ObjCInstance(c_void_p.in_dll(c,'NSForegroundColorAttributeName')),
					  self.theme['wrappers'][nested_level],
					  NSRange(position,1))
				continue
			
			if self.pop_wrapper.match(found_wrappers[position]):
				if nested_level < len_wrappers:
					str_obj.addAttribute_value_range_(
					  ObjCInstance(c_void_p.in_dll(c,'NSForegroundColorAttributeName')),
					  self.theme['wrappers'][nested_level],
					  NSRange(position,1))
				nested_level -= 1

		nest_colors(str_obj, current_text, 0, self.syntax.syntax)
		if initial or (str_obj != original_str_obj):
		  tvo.setAllowsEditingTextAttributes_(True)
		  tvo.setAttributedText_(str_obj)

def nest_colors(str_obj, current_text, offset, parse_patterns):
	
	for pattern in parse_patterns:

		if 'type' in pattern:
			continue # already done

		sre = pattern['pattern'].finditer(current_text)

		for m in sre:
			start, end = m.span()
			length = end-start
			
			if 'font' in pattern['self']: 
				  
			  str_obj.addAttribute_value_range_(
				ObjCInstance(c_void_p.in_dll(c,'NSFontAttributeName')), 
				pattern['self']['font'], 
				NSRange(start + offset,length))
			
			if 'color' in pattern['self']:
			  str_obj.addAttribute_value_range_(
				ObjCInstance(c_void_p.in_dll(c,'NSForegroundColorAttributeName')),
				pattern['self']['color'],
				NSRange(start + offset,length)
			  )

			if 'groups' in pattern:
				for g in pattern['groups']:
					group_start, group_end = m.span(g)
					group_length = group_end - group_start

					if 'font' in pattern['groups'][g]: 
						str_obj.addAttribute_value_range_(
						ObjCInstance(c_void_p.in_dll(c,'NSFontAttributeName')), 
						pattern['groups'][g]['font'], 
						NSRange(group_start + offset, group_length))

					if 'color' in pattern['groups'][g]:
					  	str_obj.addAttribute_value_range_(
						ObjCInstance(c_void_p.in_dll(c,'NSForegroundColorAttributeName')),
						pattern['groups'][g]['color'],
						NSRange(group_start + offset, group_length)
					  )
					
			if 'inside' in pattern:
				substring = current_text[start:end]
				nest_colors(str_obj, substring, start, pattern['inside'])

def get_push_pop_patterns(syntax):
	for p in syntax:
		if 'type' in p and p['type'] == 'push':
			push_wrapper = p['pattern'] 
			pop_wrapper = p['pop']['pattern']
			return (push_wrapper, pop_wrapper)
	return [None, None]

def find_wrappers(string, wrappers):
	found_wrappers = {}
	for w in wrappers:
		s = w.finditer(string)
		for item in s:
			found_wrappers[item.start()] = item.group()
	return found_wrappers
