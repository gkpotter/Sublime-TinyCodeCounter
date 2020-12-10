import sublime
import sublime_plugin

settings = sublime.load_settings('p5t.sublime-settings')

class CharCounter(sublime_plugin.ViewEventListener):
	def __init__(self, view):
		self.view = view
		self.phantom_set = sublime.PhantomSet(view)

		self.marker = settings.get('marker')
		self.char_limit = settings.get('char_limit')
		self.remove_newlines = settings.get('remove_newlines')
		self.update()

	@classmethod
	def is_applicable(cls, settings):
		syntax = settings.get('syntax')
		return 'JavaScript' in syntax

	def update(self):
		phantoms = []
		
		marker_region = self.view.find(self.marker,0)
		
		if marker_region.a > 0:
			code_region = self.view.line(marker_region.a)
		
			msg_start = code_region.a

			code = self.view.substr(sublime.Region(0,msg_start))
			code = code.replace(' ','').replace('\t','')

			if self.remove_newlines:
				code = code.replace('\n','')

			# do not remove whitespace from comment
			comment = self.view.substr(sublime.Region(msg_start,code_region.b)).strip()
			code += comment

			count = len(code)
			limit = self.char_limit
			diff = count-limit

			color = self.view.style_for_scope('comment')['foreground']

			style = ('<style>a{text-decoration:none;color:'
				+ str(color)
				+ '}#offset{color:'
				+ ('#f00'if count>limit else '#0f0') 
				+ '}</style>')
			
			text = ('<a href=copy>Char count: '
				+	str(count)
				+ ' (<span id="offset">'
				+ ('+' if diff > 0 else '' if diff == 0 else '-')
				+ str(abs(diff))
				+ '</span>)</a>')

			phantoms.append(sublime.Phantom(
				sublime.Region(msg_start),
				style + text,
				sublime.LAYOUT_BLOCK,
				lambda href: self.on_click(code)))

		self.phantom_set.update(phantoms)

	def on_click(self, code):
		print('Copied!')
		sublime.set_clipboard(code)

	def on_modified(self):
		self.update()
			