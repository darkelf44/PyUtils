"""Terminal database in Python

This information is based on the terminfo database from NCurses (db version
10.2.1), all credit goes to them.

This module only includes the "modern" terminals, meaning the ones that are
still being used, or emulated by modern operating systems. This means mostly
xterm and other terminal emulators, Linux and BDS consoles, and the VT-100/200
series as a fallback.

The TERM names used are almost identical to the terminfo onces, except the '.'
and '-' sings are replaced with '_', as they are not allowed in python names.

The terminals are put into modules based on their first letter, so the terminal
"xterm" is located in the "terminfo.x" module, and to import it you'd write
"import terminfo.x.xterm". Each terminal is a separate module and must be
imported individually.

The currenly supported terminals are:
	a) ansi, ansi80x25
	c) cons25
	d) dumb
	l) linux, linux_16color
	m) mach, mach_bold, mach_color, mach_gnu, mach_gnu_color, mintty
	n) nsterm, nsterm_256color
	p) pcansi
	r) rxvt, rxvt_basic
	s) screen, screen_256color, screen_256color_bce, screen_bce
	v) vt52, vt100, vt102, vt200, vt220
	w) wsvt25, wsvt25m
	x) xterm, xterm_16color, xterm_256color, xterm_color, xterm_mono, xterm_r5, xterm_r6, xterm_vt220, xterm_xfree86
	
Oh, and also hurd is supported for some reason. Not sure why though...

"""

import sys

class Terminal(object):
	'''Describes the capabilities of a single terminal type.'''

	# Terminal registry - stores the imported terminals
	registry = {}

	def __init__(self, names, use=(), **kwargs):
		# Inherit attributes
		for u in use:
			try:
				self.__dict__.update(Terminal.registry[u].__dict__)
			except KeyError:
				self.__dict__.update(__import__('terminfo.' + u[0], u).__dict__)
				
		# Override attributes
		self.__dict__.update(kwargs)
		# Register terminal
		for n in names:
			Terminal.registry[n] = self
			
class TerminalModule(Terminal):
	'''Terminal object designed to live in the module registry'''

	def __init__(self, names, use=(), **kwargs):
		# Initialize terminal
		Terminal.__init__(self, names, use, **kwargs)
		# Override module definition with terminal data
		for n in names:
			__import__('terminfo.' + n[0])
			sys.modules['terminfo.' + n[0] + '.' + n] = self
			setattr(sys.modules['terminfo.' + n[0]], n, self)
