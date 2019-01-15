'''Elementary additions to standard Python'''

from __future__ import print_function
from __future__ import absolute_import

import sys, os, io

import types as _types
import zipfile as _zipfile

import os.path as _ospath
import ntpath as _ntpath
import posixpath as _posixpath

# ------------------------------------------------------------ #
#	Versioning 
# ------------------------------------------------------------ #

version = (0, 1, 2)
versionstring = '%d.%d.%d' % version


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
#	Utility functions
# ------------------------------------------------------------ #

@decorator
def scope(f):
	'''Assign the result of a function after its definition to create an enclosing scope'''
	# Execute scope
	result = f()
	
	# Inherit attributes
	for attr in scope.inherit:
		if hasattr(f, attr):
			setattr(result, attr, getattr(f, attr))
	
	# Return exports
	return f()
	
scope.inherit = ['__name__', '__doc__']


# ------------------------------------------------------------ #
#	Resource functions
# ------------------------------------------------------------ #

@namespace
class resource:

	# Resource only path - searched before sys.path
	path = []

	# Resource loader hooks - similar to sys.path_hooks
	loader_hooks = []

	# Resource loader cache - similar to sys.path_importer_cache
	loader_cache = {}

	def open(path, module=None, verbose=False):
		'''
		Open a resouce file
		
		Finds a resource file in sys.path similarly, how modules are found, and opens it. Works with both directories
		and archive files in sys.path. Relative paths work, like relative imports, it adds the parent module names to
		the path, but still the whole sys.path is searched.
		
		path - Path to the resource, separated with '/' characters. Absolute paths begin with a '/' character
		
		module - The module name for relative imports. Ignored with absolute imports.
		
		verbose - Not used
		
		Returns the resource stream, opened in binary mode. Use io.TextIOWrapper when reading text files to get a
		character stream from the result.
		'''
		
		# Get absolute path in a relative format
		if path.startswith('/'):
			path = path.lstrip('/')
		else:
			module = module or sys._getframe(1).f_globals['__name__']
			path = '/'.join([module.replace('.', '/'), path.lstrip('/')])
			
		# Search sys.path
		for base in (resource.path + sys.path):
			# Consult loader cache
			try:
				loader = None
				loader = resource.loader_cache[base]
			except KeyError:
				# Find loader for resource
				for cls in resource.loader_hooks:
					try:
						loader = cls(base)
						break
					except:
						pass
				# Save loader (even if its None)
				resource.loader_cache[base] = loader
				
			# Open resource
			if loader is not None:
				# Try opening the resource
				try:
					return loader.open(path)
				except:
					pass
			
			# System path are searched only, if the resource path is a valid, relative path on the system
			elif _ospath.isrelative(path):
				# Try to open the resource
				try:
					if not base:
						return io.open(os.path.normpath(path), 'rb')
					elif _ospath.isdir(base):
						return io.open(os.path.normpath(base + '/' + path), 'rb')
				except:
					pass
			
		# Not found
		raise IOError(2, 'Resource not found: %r' % path)
	
	def local_open(path):
		'''Works like resource.open, but the path is always interpreted as a relative path'''
		return resource.open(path.lstrip('/'), module=sys._getframe(1).f_globals['__name__'], verbose=verbose)

	def global_open(path):
		'''Works like resource.open, but the path is always interpreted as an absolute path'''
		return resource.open(_posixpath.join('/', path), verbose=verbose)
		
	def cleanup():
		'''Calls the cleanup method of all cached loaders, to free up cached resources'''
		for loader in resource.loader_cache.values():
			loader.cleanup()
	
	class ZipLoader(object):
		'''Resource loader hook for ZIP archives'''
		
		__slots__ = ('path', 'prefix')
		
		# ZipFile cache to avoid opening the same file multiple times
		zipfile_cache = {}
		
		def __init__(self, path):
			# Find filesystem prefix
			prefix, suffix = path, []
			while prefix and not _ospath.exists(prefix):
				prefix, part = _ospath.split(prefix)
				suffix.append(part)
				
			# Split the filesystem part from the archive part
			if _ospath.isfile(prefix):
				self.path, self.prefix = prefix, '/'.join(suffix)
			else:
				raise ImportError()
				
			# Open the zip file (to check if it's a zip file)
			try:
				self.file = self.zipfile_cache[self.path]
			except KeyError:
				self.zipfile_cache[self.path] = _zipfile.ZipFile(self.path, 'r')
			
		def open(self, path):
			# Open the zip file
			try:
				zfile = self.zipfile_cache[self.path]
			except KeyError:
				zfile = self.zipfile_cache[self.path] = _zipfile.ZipFile(self.path, 'r')
			
			# Add prefix
			if self.prefix:
				path = self.prefix + '/' + path
			
			# Return the resource
			return zfile.open(path, 'r')
				
		@classmethod
		def cleanup(cls):
			# Close all the open zip files, and empty the cache
			if cls.zipfile_cache:
				zipfiles, cls.zipfile_cache = cls.zipfile_cache, {}
				for zfile in zipfiles.values():
					zfile.close()
				
	# Register resource loaders
	loader_hooks += [ZipLoader]


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
_ospath.isabsolute = _ospath.isabs
_ospath.isrelative = _ospath_isrelative

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

