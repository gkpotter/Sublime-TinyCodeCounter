import sublime
import sublime_plugin

class charCounter(sublime_plugin.ViewEventListener):
	SETTINGS_FILE = 'TinyCodeCounter.sublime-settings'
	settings = sublime.load_settings(SETTINGS_FILE)
	
	
	def __init__(self, view):
		self.view = view
		self.phantom_set = sublime.PhantomSet(view)
		
		self.markers = self.settings.get('markers')
		self.char_limit = self.settings.get('char_limit')
		self.remove_newlines = self.settings.get('remove_newlines')
		self.colors = self.settings.get('colors')
		self.label = self.settings.get('label')
		self.zero_char = self.settings.get('zero_char')
		self.include_marker_line = self.settings.get('include_marker_line')

		self.just_copied = False

		self.update()


	@classmethod
	def is_applicable(cls, view_settings):
		syntax = view_settings.get('syntax')
		languages = cls.settings.get('languages')
		
		if languages == None:
			cls.settings = sublime.load_settings(cls.SETTINGS_FILE)
			languages = cls.settings.get('languages')
		
		return any(language in syntax for language in languages)


	def update(self):
		phantoms = []
		
		# find first marker
		marker_start = -1
		for marker in self.markers:
			found_start = self.view.find(marker, 0).a
			if found_start > 0:
				if marker_start == -1:
					marker_start = found_start
				else:
					marker_start = min(found_start, marker_start)

		if marker_start > 0:
			code_region = self.view.line(marker_start)

			code = self.view.substr(sublime.Region(0,marker_start))
			code = code.replace(' ', '').replace('\t', '')

			if self.remove_newlines:
				code = code.replace('\n', '')

			if self.include_marker_line:
				# do not remove whitespace from marker_line except from the end
				marker_line = self.view.substr(sublime.Region(marker_start, code_region.b)).strip()
				code += marker_line

			count = len(code)
			limit = self.char_limit
			diff = count - limit

			color = self.view.style_for_scope('comment')['foreground']
			offset_color = self.colors['over'] if count > limit else self.colors['under']

			style = '<style> a {{ text-decoration: none; color: {} }} #offset {{ color: {} }} </style>'.format(
				color, 
				offset_color) 

			text = '<a href>{} {} (<span id="offset">{}{}</span>){}</a>'.format(
				self.label, 
				count, 
				'+' if diff > 0 else self.zero_char if diff == 0 else '-', 
				abs(diff) if diff != 0 else '',
				' Copied!' if self.just_copied else '')

			phantoms.append(sublime.Phantom(
				sublime.Region(marker_start),
				style + text,
				sublime.LAYOUT_BLOCK,
				lambda href: self.set_clipboard(code)))

		self.just_copied = False
		self.phantom_set.update(phantoms)


	def set_clipboard(self, code):
		if not self.just_copied:
			sublime.set_timeout(self.update, 1000)
			
			sublime.set_clipboard(code)
			self.just_copied = True
			self.update()


	def on_modified(self):
		self.update()


	def on_load(self):
		self.update()
