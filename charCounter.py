import sublime
import sublime_plugin

settings = sublime.load_settings('TinyCodeCounter.sublime-settings')
languages = settings.get('languages')

class charCounter(sublime_plugin.ViewEventListener):
	def __init__(self, view):
		self.view = view
		self.phantom_set = sublime.PhantomSet(view)

		self.markers = settings.get('markers')
		self.char_limit = settings.get('char_limit')
		self.remove_newlines = settings.get('remove_newlines')
		self.colors = settings.get('colors')
		self.label = settings.get('label')
		
		self.update()

	@classmethod
	def is_applicable(cls, settings):
		syntax = settings.get('syntax')
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
			print(marker_start)
			code_region = self.view.line(marker_start)

			code = self.view.substr(sublime.Region(0,marker_start))
			code = code.replace(' ', '').replace('\t', '')

			if self.remove_newlines:
				code = code.replace('\n', '')

			# do not remove whitespace from comment
			comment = self.view.substr(sublime.Region(marker_start, code_region.b)).strip()
			code += comment

			count = len(code)
			limit = self.char_limit
			diff = count-limit

			color = self.view.style_for_scope('comment')['foreground']

			style = ('<style>a{text-decoration:none;color:'
				+ str(color)
				+ '}#offset{color:'
				+ (self.colors['over'] if count > limit else self.colors['under'] ) 
				+ '}</style>')
			
			text = ('<a href=copy>'
				+ self.label
				+	str(count)
				+ ' (<span id="offset">'
				+ ('+' if diff > 0 else '' if diff == 0 else '-')
				+ str(abs(diff))
				+ '</span>)</a>')

			phantoms.append(sublime.Phantom(
				sublime.Region(marker_start),
				style + text,
				sublime.LAYOUT_BLOCK,
				lambda href: self.set_clipboard(code)))

		self.phantom_set.update(phantoms)

	def set_clipboard(self, code):
		print('Copied!')
		sublime.set_clipboard(code)

	def on_modified(self):
		self.update()
			