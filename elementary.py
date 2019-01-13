from __future__ import print_function
from __future__ import absolute_import

import sys, os, io

import types as _types
import zipfile as _zipfile
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

def open_local_resource(path, verbose=False):
	'''Open a resouce file, relative to the current module. The path is separated by '/' characters.'''
	base = sys._getframe(1).f_globals['__name__'].split('.')
	path = _posixpath.join(*base, path.lstrip('/'))
	return open_global_resource(path, verbose=verbose)
	
def open_global_resource(path, verbose=False):
	'''Open a resouce file, from a directory or archive in sys.path. The path is separated by '/' characters.'''
	path = path.lstrip('/')
	for base in sys.path:
		if not base:
			# Current directory
			filename = os.path.normpath('./' + path)
			if os.path.isfile(filename):
				return io.open(filename, 'rb')
		if os.path.isdir(base):
			# Normal directory
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
#	Export to builtins
# ------------------------------------------------------------ #

__builtins__['namespace'] = namespace

__builtins__['decorator'] = decorator
__builtins__['_if'] = _if
__builtins__['_try'] = _try
__builtins__['_raise'] = _raise

__builtins__['local_import'] = local_import
__builtins__['global_import'] = global_import

