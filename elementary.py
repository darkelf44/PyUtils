from __future__ import print_function
from __future__ import absolute_import

import sys, os, io

import types as _types
import zipfile as _zipfile

import os.path as _ospath
import ntpath as _ntpath
import posixpath as _posixpath

version = (0, 1, 1)
versionstr = '%d.%d.%d' % version

# ------------------------------------------------------------ #
#	Classes 
# ------------------------------------------------------------ #

class namespace:
	'''Works like a Lua table, or a javascript object. Can be used as decorator for classes'''

	def __init__(self, init=None):
		'''Converts any namespace like, or dictionary like object into a namespace'''

		if init is not None:
			try:
				namespaces = (type, _types.ClassType, _types.ModuleType)
			except:
				namespaces = (type, _types.ModuleType)
			
			if isinstance(init, namespaces):
				self.__dict__.update(init.__dict__)
			elif init is not None:
				self.__dict__.update(init)
	
	def __repr__(self):
		return 'namespace(%r)' % self.__dict__

# ------------------------------------------------------------ #
#	Keyword functions
# ------------------------------------------------------------ #

def decorator(f):
	'''Marks a function as a decorator'''
	return f

def _if(x, true, false=None):
	'''If statement as function'''
	if x:
		return true
	else:
		return false

def _try(f, filter=None, onexcept=None, onfinally=None):
	'''Try statement as function'''
	if not filter:
		# Try-finally statement
		try:
			return f()
		finally:
			return onfinally()
	else:
		# Try-except-finally statement 
		try:
			return f()
		except filter as e:
			if onexcept:
				return onexcept(e)
		finally:
			if onfinally:
				return onfinally()

def _raise(x):
	'''Raise statement as function'''
	raise x
	

# ------------------------------------------------------------ #
#	Import functions
# ------------------------------------------------------------ #

def local_import(name):
	'''Import a module, relative to the current module'''
	base = sys._getframe(1).f_globals['__name__'].split('.')
	name = str.split(name, '.')
	while name and not name[0]:
		base, name = base[:-1], name[1:]
	name = '.'.join(base + name)
	return global_import(name) if name else None

def global_import(name):
	'''Import a module, using absolute import'''
	__import__(name, None, None, None, 0)
	return sys.modules[name]

# ------------------------------------------------------------ #
#	Resource functions
# ------------------------------------------------------------ #

@namespace
class resource:

	def local_open(path, verbose=False):
		'''
		Open a resouce file, relative to the current module's path.
		
		Works like resource.global_open, except the path here is relative to the current module name (that's the module
		name and not the file name).
		
		path - Relative path to the resouce, separated with '/' characters.
		
		verbose - Print warnings to stderr, when finding oddities in sys.path
		
		Returns the resource stream, opened in binary mode. Use io.TextIOWrapper when reading text files to get a
		character stream from the result.
		'''
		base = sys._getframe(1).f_globals['__name__'].replace('.', '/')
		path = '/'.join([base, path.lstrip('/')])
		return resource.global_open(path, verbose=verbose)

	def global_open(path, verbose=False):
		'''
		Open a resouce file, with an absolute path, using sys.path.
		
		Finds a resource file in sys.path similarly, how modules are found, and opens it. Works with both directories
		and archive files in sys.path. The entries in sys.path are searched for the resource in the order they appear,
		but unlike when inporting, the parent directories don't need to be python modules (no need for __init__.py
		files), and can appear in multiple times in sys.path.
		
		path - Absolute path to the resouce, separated with '/' characters.
		
		verbose - Print warnings to stderr, when finding oddities in sys.path
		
		Returns the resource stream, opened in binary mode. Use io.TextIOWrapper when reading text files to get a
		character stream from the result.
		'''
		# Make the path relative
		path = path.lstrip('/')
		for base in sys.path:
			if not base:
				# Current directory
				if os.path.isrelative(path):
					filename = os.path.normpath(path)
					if os.path.isfile(filename):
						return io.open(filename, 'rb')
			elif os.path.isdir(base):
				# Normal directory
				if os.path.isrelative(path):
					filename = os.path.normpath(base + '/' + path)
					if os.path.isfile(filename):
						return io.open(filename, 'rb')
			elif os.path.isfile(base):
				# Archive File
				try:
					filename = _posixpath.normpath(path)
					with _zipfile.ZipFile(base, 'r') as zfile:
						try:
							return zfile.open(filename, 'r')
						except KeyError:
							pass
				except _zipfile.BadZipFile:
					if verbose:
						print('Warning: Entry in sys.path is not an archive nor a directory: %r' % base)
		# Resource not found
		raise FileNotFoundError('No such a resouce: %r' % path)

# ------------------------------------------------------------ #
#	Fixing stdio, stderr
# ------------------------------------------------------------ #

# Make sure standard streams are safe to write
if sys.version_info > (3, 0):
	if sys.stdout.encoding not in ('utf8', 'utf-8') and sys.stdout.errors == 'surrogateescape':
		_params = dict(encoding=sys.stdout.encoding, errors='replace', newline=sys.stdout.newlines, line_buffering=sys.stdout.line_buffering)
		sys.stdout = io.TextIOWrapper(sys.stdout.detach(), **_params)
		del _params
	if sys.stdout.encoding not in ('utf8', 'utf-8') and sys.stderr.errors == 'surrogateescape':
		_params = dict(encoding=sys.stderr.encoding, errors='replace', newline=sys.stderr.newlines, line_buffering=sys.stderr.line_buffering)
		sys.stderr = io.TextIOWrapper(sys.stderr.detach(), **_params)
		del _params

# ------------------------------------------------------------ #
#	Extending os.path
# ------------------------------------------------------------ #

def _ntpath_isabsulute(path):
	'''Checks if a path is fully absolute on windows (does not depend on eith the current directory or the current drive)'''
	return (_ntpath.splitdrive(path)[0] or _ntpath.splitunc(path)[0]) and _ntpath.isabs(path)
	
def _ntpath_isrelative(path):
	'''Checks if a path is fully relative on windows (relative and has no drive letter)'''
	return not _ntpath.splitdrive(path)[0] and not _ntpath.isabs(path)

def _ospath_isrelative(path):
	'''Test whether a path is relative'''
	return not _ospath.isabs(path)

# Ensure os.path.isabsolute and os.path.isrelative always exists
os.path.isabsolute = os.path.isabs
os.path.isrelative = _ospath_isrelative

# Deprecate ntpath.isabs
_ntpath.isabs.__doc__ = '''[Deprecated by elementary]: Use isabsolute or isrelative instead'''

# Update functions on ntpath
_ntpath.isabsolute = _ntpath_isabsulute
_ntpath.isrelative = _ntpath_isrelative

# ------------------------------------------------------------ #
#	Export to builtins
# ------------------------------------------------------------ #

__builtins__['namespace'] = namespace

__builtins__['decorator'] = decorator
__builtins__['_if'] = _if
__builtins__['_try'] = _try
__builtins__['_raise'] = _raise

__builtins__['local_import'] = local_import
__builtins__['global_import'] = global_import

