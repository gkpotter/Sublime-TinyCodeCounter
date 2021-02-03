import sublime
import sublime_plugin
import sys


package_name = 'TinyCodeCounter'
settings_file = 'TinyCodeCounter.sublime-settings'
settings = None


def plugin_loaded():
  from package_control import events

  if events.install(package_name):
      print('Installed %s!' % events.install(package_name))
  elif events.post_upgrade(package_name):
      print('Upgraded to %s!' % events.post_upgrade(package_name))

  # load settings
  global settings
  settings = sublime.load_settings(settings_file)


def plugin_unloaded():
  from package_control import events

  if events.pre_upgrade(package_name):
      print('Upgrading from %s!' % events.pre_upgrade(package_name))
  elif events.remove(package_name):
      print('Removing %s!' % events.remove(package_name))


if sys.version_info < (3,):
    plugin_loaded()
    unload_handler = plugin_unloaded


class charCounter(sublime_plugin.ViewEventListener):
	def __init__(self, view):
		self.view = view
		self.phantom_set = sublime.PhantomSet(view)
		
		global settings
		self.markers = settings.get('markers')
		self.char_limit = settings.get('char_limit')
		self.remove_newlines = settings.get('remove_newlines')
		self.colors = settings.get('colors')
		self.label = settings.get('label')
		self.zero_char = settings.get('zero_char')
		self.include_marker_line = settings.get('include_marker_line')

		self.just_copied = False

		self.update()


	@classmethod
	def is_applicable(cls, view_settings):
		syntax = view_settings.get('syntax')
		
		global settings
		languages = settings.get('languages')
		
		return any(language in syntax for language in languages)


	def update(self):
		phantoms = []
		
		# find the first marker
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
			offset = count - limit

			color = self.view.style_for_scope('comment')['foreground']
			offset_color = self.colors['over'] if count > limit else self.colors['under']

			style = """
				<style> 
					a {{ 
						text-decoration: none; 
						color: {color} 
					}} 

					#offset {{ 
					color: {offset_color} 
					}} 
				</style>
				""".format(color = color, offset_color = offset_color)

			text = """
				<a href=copy> 
					{label} {count} (<span id="offset">{plusminus}{offset}</span>){copied_msg}
				</a>
				""".format(
					label = self.label, 
					count = count, 
					plusminus = '+' if offset > 0 else self.zero_char if offset == 0 else '-', 
					offset = abs(offset) if offset != 0 else '',
					copied_msg = ' Copied!' if self.just_copied else '')

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