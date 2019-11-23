import sys, os, io
import re
import json
import ctypes
import weakref

# Library version
version = (1, 0, 0)
versionstring = '%d.%d.%d' % version

# Cross python support
str = type(u'')
bytes = type(b'')

# The type that python uses internally for names (This differs between 2 and 3)
istr = type('')

# ctypes.c_void_p is broken, use pointer instead
class pointer(ctypes.c_void_p):
	pass

# Exports
__all__ = ('Types', 'Library', 'Loader', 'load')

class Types(object):

	'''
		Types class - Building type systems
		
		Create a type system from a few basic types. You can register types by name, and you can query those types,
		plus also any of the types devired from those the type system knows. The types this system can derive are
		pointers, arrays and functions.
		
		For example, if you register a type "A", you can query "A*", "A**", "A[10]", "A, A -> A" and so on. The names
		of the derived type use the Universal Type System (TM).
		
		On its own this type system will construct types using the "ctypes" type system in python. But you can
		override this behaviour, by replacing the "_pointer", "_array", and "_function" methods, and replacing the
		built in types.
	'''
	
	CALLTYPES = {
		'@cdecl' : 'cdecl',
		'@stdcall' : 'stdcall',
	}
	
	TYPESETS = {
		# Standard C types
		'sdtc': {
			'void'   : None,
			'char'   : ctypes.c_char,
			'wchar'  : ctypes.c_wchar,
			'byte'   : ctypes.c_byte,
			'ubyte'  : ctypes.c_ubyte,
			'short'  : ctypes.c_short,
			'ushort' : ctypes.c_ushort,
			'int'    : ctypes.c_int,
			'uint'   : ctypes.c_uint,
			'long'   : ctypes.c_long,
			'ulong'  : ctypes.c_ulong,
			'longlong'  : ctypes.c_longlong,
			'ulonglong' : ctypes.c_ulonglong,
			'float'  : ctypes.c_float,
			'double' : ctypes.c_double
		},
		
		# Types from stddef.h
		'stddef': {
			'size_t'    : {4:ctypes.c_uint32, 8:ctypes.c_uint64}[ctypes.sizeof(ctypes.c_size_t)],
			'ptrdiff_t' : {4:ctypes.c_int32, 8:ctypes.c_int64}[ctypes.sizeof(pointer)]
		},
		
		# Types from stdint.h
		'stdint': {
			'int8_t'    : ctypes.c_int8,
			'int16_t'   : ctypes.c_int16,
			'int32_t'   : ctypes.c_int32,
			'int64_t'   : ctypes.c_int64,
			'uint8_t'   : ctypes.c_uint8,
			'uint16_t'  : ctypes.c_uint16,
			'uint32_t'  : ctypes.c_uint32,
			'uint64_t'  : ctypes.c_uint64,
			'intptr_t'  : {4:ctypes.c_int32, 8:ctypes.c_int64}[ctypes.sizeof(pointer)],
			'uintptr_t' : {4:ctypes.c_uint32, 8:ctypes.c_uint64}[ctypes.sizeof(pointer)]
		},
		
		# Simplified types
		'simple': {
			'N'   :	None,
			'P'   : ctypes.c_void_p,
			'C'  : ctypes.c_char,
			'CW' : ctypes.c_wchar,
			'S'  : ctypes.c_char_p,
			'SW' : ctypes.c_wchar_p,
			'IA'  : {4:ctypes.c_int32, 8:ctypes.c_int64}[ctypes.sizeof(pointer)],
			'IZ'  : {4:ctypes.c_int32, 8:ctypes.c_int64}[ctypes.sizeof(ctypes.c_size_t)],
			'I8'  : ctypes.c_int8,
			'I16' : ctypes.c_int16,
			'I32' : ctypes.c_int32,
			'I64' : ctypes.c_int64,
			'UA'  : {4:ctypes.c_uint32, 8:ctypes.c_uint64}[ctypes.sizeof(pointer)],
			'UZ'  : {4:ctypes.c_uint32, 8:ctypes.c_uint64}[ctypes.sizeof(ctypes.c_size_t)],
			'U8'  : ctypes.c_uint8,
			'U16' : ctypes.c_uint16,
			'U32' : ctypes.c_uint32,
			'U64' : ctypes.c_uint64,
			'F32' : ctypes.c_float,
			'F64' : ctypes.c_double
		}, 
	}

	def __init__(self, typesets='simple'):
		# Init
		self._list = {}
		self._cache = {}
		
		# Load type systems
		if not isinstance(typesets, tuple):
			typesets = tuple(name.strip() for name in typesets.split(','))
		for name in typesets:
			self._list.update(self.TYPESETS[name])
	
	def __getitem__(self, name):
		return self._list[name]
		
	def __setitem__(self, name, value):
		self._list[name] = value
		
	def find(self, name, namespace=None):
		'''Find a type by name, using an optional namespace object'''
		if namespace:
			try:
				return namespace[name]
			except KeyError:
				pass
		return self._list[name]
	
	def build(self, type, namespace=None):
		'''Build a complex type from other types, using an optonal namespace object.'''
		if type == '()':
			return None
		elif type == '...':
			return '...'
		else:
			op, nodes = type[0], type[1:]
			if op == '*':
				return self.build_pointer(self.build(nodes[0], namespace=namespace))
			elif op == '[]':
				return self.build_array(self.build(nodes[0], namespace=namespace), nodes[1])
			elif op == '->':
				return self.build_function(tuple(self.build(x, namespace=namespace) for x in nodes[0]), self.build(nodes[1], namespace=namespace), nodes[2])
			elif op == 'id':
				try:
					return self.find(nodes[0], namespace=namespace)
				except KeyError:
					raise Utils.dontchain(ValueError('Undefined type: %s' % nodes[0]))
			else:
				raise ValueError('Invalid operator: %s' % op)
	
	def build_pointer(self, type):
		'''Create type value for pointer'''
		return ctypes.POINTER(type)
	
	def build_array(self, type, length):
		'''Create type value for array'''
		return type * (length or 0)
	
	def build_function(self, params, result, calltype):
		'''Create type value for functions'''
		if '...' in params:
			# Vararg function
			result = self.build_function([], result, calltype)
			result.argtypes = None	# HACK: wiping argtypes creates an typeless function
			return result
		else:
			# Normal function
			calltype = calltype or 'cdecl'
			if calltype == 'cdecl':
				return ctypes.CFUNCTYPE(result, *params)
			elif calltype == 'stdcall':
				return ctypes.WINFUNCTYPE(result, *params)
			else:
				raise ValueError('calltype: Invalid value')
			
	@staticmethod
	def isident(text):
		return text and not text[:1].isdigit() and text.replace('_', '').isalnum()
		
	@staticmethod
	def isinteger(text):
		return text and text.isdigit()
		
	@classmethod
	def tokenize(cls, text):
		# List of symbols
		symbols = {'->', ',', '*', '...', '[', ']', '(', ')'}
		
		# Tokenize input the fast way
		for s in symbols:
			text = text.replace(s, ' %s ' % s)
		return text.split()
		
	@classmethod
	def parsetype(cls, text):
		#	Type ::=
		#		Expression
		#	|
		#		ExpressionList [ CallingConvention ] '->' ResultType
		#	|
		#		'(' [ ExpressionList ] ')' [ CallingConvention ] '->' ResultType
		#	
		#	Expression ::=
		#		IDENTIFIER [ '[' [ NUMBER ] ']' | '*' ] ...
		#	|
		#		'(' Type ')' [ '[' [ NUMBER ] ']' | '*' ] ...
		#
		#	ExpressionList ::= Expression [ ',' Expression ] ... [ '...' ]
		#	
		#	CallingConvention ::= '@' + IDENTIFIER
		#	ResultType ::= '(' ')' | Type
		
		def parse_type(pos):
			return parse_type_2(pos) or parse_type_1(pos) or parse_expr(pos)
		
		def parse_type_1(pos):
			# Type --> ExpressionList [ CallingConvention ] '->' ResultType
			try:
				l, pos = parse_expr_list(pos)
				c = parse_call_conv(pos)
				if c:
					c, pos = c
				_, pos = parse_tokens(pos, ['->'])
				r, pos = parse_result(pos)
				return ('->', tuple(l), r, c), pos
			except TypeError:
				return None
			
		def parse_type_2(pos):
			# Type --> '(' [ ExpressionList ] ')' [ CallingConvention ] '->' ResultType
			try:
				_, pos = parse_tokens(pos, ['('])
				l = parse_expr_list(pos)
				if l:
					l, pos = l
				_, pos = parse_tokens(pos, [')'])
				c = parse_call_conv(pos)
				if c:
					c, pos = c
				_, pos = parse_tokens(pos, ['->'])
				r, pos = parse_result(pos)
				l = l or ()
				return ('->', tuple(l), r, c), pos
			except TypeError:
				return None
			
		def parse_expr(pos):
			return parse_expr_2(pos) or parse_expr_1(pos)
			
		def parse_expr_1(pos):
			# Expression --> IDENTIFIER [ '[' [ NUMBER ] ']' | '*' ] ...
			try:
				i, pos = parse_ident(pos)
			except TypeError:
				return None
			t = ('id', i)
			x = parse_tokens(pos, ['*'], ('*', t)) or parse_expr_a(pos, t)
			while x:
				t, pos = x
				x = parse_tokens(pos, ['*'], ('*', t)) or parse_expr_a(pos, t)
			return t, pos

		def parse_expr_2(pos):
			# Expression --> '(' Type ')' [ '[' [ NUMBER ] ']' | '*' ] ...
			try:
				_, pos = parse_tokens(pos, ['('])
				t, pos = parse_type(pos)
				_, pos = parse_tokens(pos, [')'])
			except TypeError:
				return None
			x = parse_tokens(pos, ['*'], ('*', t)) or parse_expr_a(pos, t)
			while x:
				t, pos = x
				x = parse_tokens(pos, ['*'], ('*', t)) or parse_expr_a(pos, t)
			return t, pos
		
		def parse_expr_a(pos, t):
			# ??? --> [ '[' [ NUMBER ] ']'
			try:
				_, pos = parse_tokens(pos, ['['])
				n = parse_int(pos)
				if n:
					n, pos = n
				_, pos = parse_tokens(pos, [']'])
				return ('[]', t, n), pos
			except TypeError:
				return None
				
		def parse_expr_list(pos):
			# ExpressionList --> Expression [ ',' Expression ] ... [ '...' ]
			try:
				e, pos = parse_expr(pos)
			except TypeError:
				return None
			r = [e]
			try:
				c = parse_tokens(pos, [','])
				while c:
					c, pos = c
					e, pos = parse_expr(pos)
					r.append(e)
					c = parse_tokens(pos, [','])
				c = parse_tokens(pos, ['...'])
				if c:
					c, pos = c
					r.append('...')
				return r, pos
			except TypeError:
				return None
			
		def parse_call_conv(pos):
			# CallingConvention --> '@' + IDENTIFIER
			try:
				c, pos = parse_any(pos)
				return cls.CALLTYPES[c], pos
			except (TypeError, KeyError):
				return None
			
		def parse_result(pos):
			# ResultType --> '(' ')' | Type
			return parse_type(pos) or parse_tokens(pos, ['(', ')'], '()')
		
		def parse_any(pos):
			if pos >= expr_len:
				return None
			return expr[pos], pos + 1
		
		def parse_int(pos):
			if pos >= expr_len:
				return None
			r = expr[pos]
			if cls.isinteger(r):
				return r, pos + 1
			return None
			
		def parse_ident(pos):
			if pos >= expr_len:
				return None
			r = expr[pos]
			if cls.isident(r):
				return r, pos + 1
			return None
		
		def parse_tokens(pos, l, r=None):
			if pos >= expr_len:
				return None
			n = pos + len(l)
			if expr[pos:n] == l:
				return r, n
			return None
		
		# Tokenize the input
		expr = cls.tokenize(text)
		expr_len = len(expr)
		expr_err = None
		
		# Parse the type
		result = parse_type(0)
		if result:
			result, end = result
			if end != expr_len:
				raise ValueError('Syntax error: Unexpected input: %s' % expr[end])
			return result
		else:
			raise ValueError('Syntax error: Invalid expression!')

class Library(object):
	
	def __init__(self, loader, binary):
		self._loader = loader
		self._binary = binary
		self._delayed = {}
		
	def __getattr__(self, name):
		# Do not resolve reserved names
		if not name.startswith('_') or name.startswith('_u_'):
			# Unescape attribute name
			attrname = name
			if attrname.startswith('_u_'):
				name = attrname[2:]
				
			try:
				# Resolve delayed export
				result = self._loader.load_delayed(self, self._delayed[name])
				
				# Move to attributes
				del self._delayed[name]
				self.__dict__[attrname] = result
				return result
			except KeyError:
				pass
				
		# Raise AttributeError
		return object.__getattribute__(self, attrname)
		
	def __getitem__(self, name):
		# Escape names starting with underscore
		attrname = '_u' * name.startswith('_') + name
		
		# Lookup in dictionary
		try:
			return self.__dict__[attrname]
		except KeyError:
			pass
		
		# Resolve delayed export
		result = self._loader.load_delayed(self, self._delayed[name])
		
		# Move to attributes
		del self._delayed[name]
		self.__dict__[attrname] = result
		return result
		
	def __setitem__(self, name, value):
		# Escape names starting with underscore
		if name.startswith('_'):
			name = '_u' + name
	
		# Set value in object
		self.__dict__[name] = value

class Loader(object):
	# File format version of the library descriptor JSON
	FORMAT_VERSION = 2

	# Path for loading dlls
	path = ['.'] + list(sys.path)
	# Extensions of the library binary
	extensions = ['dlib'] + {'nt': ['dll'], 'posix': ['so']}.get(os.name, [])
	# Binary cache to avoid loading a library multiple times
	binary_cache = weakref.WeakValueDictionary()

	def __init__(self, path=None, extensions=None, types=None):
		# Public dlls are cached by the loader. Loaders do not share caches
		self.cache = {}
		
		# Set path and extensions
		if path is not None:
			self.path = path
		if extensions is not None:
			self.extensions = extensions
		
		# Create type system with default type sets
		self.types = types or Types(typesets='simple')
	
	def load(self, filename, binary=None, delayed=False, private=False):
		# Normalize filename
		filename = os.path.abspath(filename)
	
		# Load from cache
		if not private:
			library = self.cache.get(filename)
			if library is not None:
				return library
				
		# Load library descriptor json with comments removed
		with io.open(filename, 'r', encoding='utf-8') as file:
			config = json.loads(re.sub(r'^[ \t]*#.*$', '', file.read(), flags=re.MULTILINE))
			
		# Validate file format
		if config['type'] != 'library':
			raise ValueError('"{filename}": Value of "type" need to be "{expected}"!'.format(filename=filename, expected="library"))
		if int(config['version']) != self.FORMAT_VERSION:
			raise ValueError('"{filename}": Value of "version" need to be "{expected}"!'.format(filename=filename, expected=self.FORMAT_VERSION))
		
		# Locate binary
		defpath = os.path.dirname(filename)
		defname = os.path.splitext(os.path.basename(filename))[0]
		if binary is None:
			binary = config.get('binary', '*.*')
		binary = binary.replace('*', defname, 1)
		binary = self.locate(binary, path = [defpath] + self.path, extensions=self.extensions)
		if binary is None:
			raise ValueError('"{filename}": Not found!'.format(filename=filename))
		
		try:
			binary = self.binary_cache[binary]
		except KeyError:
			binary = self.binary_cache[binary] = ctypes.cdll.LoadLibrary(binary)
		
		# Create library
		config = config['library']
		library = Library(loader=self, binary=binary)
		library.version = config['version']
		library._version = library.version
		library.description = config['description']
		library._description = library.description
		self.load_defines(library, config['define'])
		self.load_exports(library, config['export'], delayed=delayed)
		
		# Save and return library
		if not private:
			self.cache[filename] = library
		return library
	
	def locate(self, filename, path=None, extensions=None):
		'''
		Locate the binary based on its name.
		
		When locating a binary for library, the directory of the library descriptor file is searched before any other
		locations in the path. To simulate this, you must manually add this directory to the path when invoking this
		function, otherwise binaries next to the descriptor file may not be found.
		'''
	
		# Set up path and extensions
		if path is None:
			path = self.path
		if extensions is None:
			extensions = self.extensions
		
		# Check directory and extension. Both are optional.
		hasdir = bool(os.path.dirname(filename))
		hasext = bool(os.path.splitext(filename)[1])
		
		# Special suffix for files with '.' in the name to indicate the lack of an extension
		if filename.endswith('.*'):
			hasext = False
			filename = filename[:-2]
		
		if hasdir:
			# Look up in directory
			if hasext:
				file = os.path.abspath(filename)
				if os.path.isfile(file):
					return file
			else:
				for e in extensions:
					file = os.path.abspath(filename) + '.' + e
					if os.path.isfile(file):
						return file
		else:
			# Look up in path
			for root in path:
				root = os.path.abspath(root)
				if hasext:
					file = os.path.join(root, filename)
					if os.path.isfile(file):
						return file
				else:
					for e in extensions:
						file = os.path.join(root, filename) + '.' + e
						if os.path.isfile(file):
							return file
		
		# Look up failed
		return None
		
	def load_defines(self, library, defines):
		# Define constants
		for id, kind, value in defines.get('const', []):
			self.check_unique(library, id)
			self.define_const(library, id, kind, value)
		
		# Define types - First pass
		for id, kind, value in defines.get('type', []):
			self.check_unique(library, id)
			if kind in ('struct', 'union'):
				self.declare_type(library, id, kind)
			else:
				self.define_type(library, id, kind, value)
		
		# Define types - Second pass
		for id, kind, value in defines.get('type', []):
			if kind in ('struct', 'union') and value is not None:
				self.define_type(library, id, kind, value)
	
	def load_exports(self, library, exports, delayed=False):
		# Export functions
		for id, name, type in exports.get('function', []):
			self.check_unique(library, id, delayed=delayed)
			if name is None:
				name = id
			if delayed:
				library._delayed[id] = ('F', id, name, type)
			else:
				self.export_function(library, id, name, type)
		
		# Export variables
		for id, name, type in exports.get('variable', []):
			self.check_unique(library, id, delayed=delayed)
			if name is None:
				name = id
			if delayed:
				library._delayed[id] = ('V', id, name, type)
			else:
				self.export_variable(library, id, name, type)
	
	def load_delayed(self, library, delayed):
		kind, id, name, type = delayed
		if kind == 'F':
			return self.export_function(library, id, name, type)
		elif kind == 'V':
			return self.export_variable(library, id, name, type)
		else:
			raise ValueError('"{id}": Value of "kind" must be in {expected}!'.format(id=id, expected=('F', 'V')))
	
	def check_unique(self, library, id, delayed=False):
		if not self.isident(id):
			raise ValueError('"{id}": Not a valid identifier!'.format(id=id))
		try:
			if delayed:
				_ = library._delayed[id]
			else:
				_ = library[id]
			raise ValueError('"{id}": Duplicate identifier!'.format(id=id))
		except KeyError:
			pass
	
	def define_const(self, library, id, kind, value):
		if kind in ('I', 'int'):
			library[id] = Utils.integer(value)
		elif kind in ('F', 'float'):
			library[id] = float(value)
		elif kind in ('S', 'string'):
			library[id] = Utils.bytes(value)
		elif kind in ('W', 'wstring'):
			library[id] = Utils.string(value)
		else:
			raise ValueError('"{id}": Value of "kind" must be in {expected}'.format(id=id, expected=("I", "int", "F", "float", "S", "string", "W", "wstring")))
	
	def define_type(self, library, id, kind, value):
		if kind in ('=', 'alias'):
			try:
				library[id] = self.types.build(self.types.parsetype(value), namespace=library)
			except ValueError as ex:
				raise ValueError('{id}: {error}'.format(id=id, error=str(ex)))
		
		elif kind in ('E', 'enum'):
			self.define_enum(library, id, value)
		elif kind in ('S', 'struct'):
			self.define_struct(library, id, value)
		elif kind in ('U', 'union'):
			self.define_union(library, id, value)
		else:
			raise ValueError('"{id}": Value of "kind" must be in {expected}'.format(id=id, expected=("=", "alias", "E", "enum", "S", "struct", "U", "union")))
	
	def define_enum(self, library, id, entries):
		# Check name
		self.check_unique(library, id)
		# Process entries
		values = []
		hi, lo, next = 0, 0, 0
		for entry in Utils.typecheck(entries, list):
			# Process entry
			name, value = Utils.ljust([x.strip() for x in entry.split('=', 1)], 2)
			# Auto increment unspecified enum values
			if value is not None:
				next = Utils.integer(value)
			value = next
			# Collect results
			values.append((name, value))
			hi, lo, next = max(hi, value), min(lo, value), next + 1

		# Enum types are fuzzy. This is what GCC does, so we roll with it
		if lo < 0:
			# Signed enum
			hi = max(hi, (- min - 1))
			if hi < 0x80000000:
				enumtype = ctypes.c_int32
			else:
				enumtype = ctypes.c_int64
		else:
			# Unsigned enum
			if hi < 0x100000000:
				enumtype = ctypes.c_uint32
			else:
				enumtype = ctypes.c_uint64
			
		# Define enum type
		library[id] = enumtype
		# Define enum values
		for name, value in values:
			self.check_unique(library, name)
			library[name] = value

	def define_struct(self, library, id, entries):
		# Check declaration
		try:
			cls = library[id]
			if not issubclass(cls, ctypes.Structure) or hasattr(cls, '_fields_'):
				raise ValueError('"{id}": Type is already defined'.format(id=id))
		except KeyError:
			cls = library[id] = type(istr(id), (ctypes.Structure,), {})

		# Define fields
		cls._fields_ = fields = []
		for entry in Utils.typecheck(entries, list):
			name, fieldtype = [x.strip() for x in entry.split(':', 1)]
			try:
				fields.append((name, self.types.build(self.types.parsetype(fieldtype), namespace=library)))
			except ValueError as ex:
				raise ValueError('{id}.{name}: {error}'.format(id=id, name=name, error=str(ex)))

	def define_union(self, library, id, entries):
		# Check declaration
		try:
			cls = library[id]
			if not issubclass(cls, ctypes.Union) or hasattr(cls, '_fields_'):
				raise ValueError('"{id}": Type is already defined'.format(id=id))
		except KeyError:
			cls = library[id] = type(istr(id), (ctypes.Union,), {})
		
		# Define fields
		cls._fields_ = fields = []
		for entry in Utils.typecheck(entries, list):
			name, fieldtype = [x.strip() for x in entry.split(':', 1)]
			try:
				fields.append((name, self.types.build(self.types.parsetype(fieldtype), namespace=library)))
			except ValueError as ex:
				raise ValueError('{id}.{name}: {error}'.format(id=id, name=name, error=str(ex)))

	def declare_type(self, library, id, kind):
		if kind in ('S', 'struct'):
			library[id] = type(istr(id), (ctypes.Structure,), {})
		elif kindin ('U', 'union'):
			library[id] = type(istr(id), (ctypes.Union,), {})
		else:
			raise ValueError('"{id}": Value of "kind" must be in {expected}'.format(id=id, expected=("S", "struct", "U", "union")))

	def export_function(self, library, id, name, type):
		try:
			type = self.types.build(self.types.parsetype(type), namespace=library)
		except ValueError as ex:
			raise ValueError('{id}: {error}'.format(id=id, error=str(ex)))
		result = ctypes.cast(getattr(library._binary, name), type)
		library[id] = result
		return result

	def export_variable(self, library, id, name, type):
		try:
			type = self.types.build(self.types.parsetype(type), namespace=library)
		except ValueError as ex:
			raise ValueError('{id}: {error}'.format(id=id, error=str(ex)))
		result = type.in_dll(library._binary, name)
		library[id] = result
		return result
	
	@staticmethod
	def isident(name):
		return Types.isident(name)

# Default loader used by the `load` function 
default_loader = Loader()

def load(filename, binary=None, private=False):
	'''Load a dynamic library definition file, using the default loader.'''
	return default_loader.load(filename, binary=None, private=False)

def generate(filename, language='python', template=None):
	raise NotImplementedError
	
class Utils(object):

	@staticmethod
	def dontchain(e):
		'''Disable automatic exception chaining in python 3 (Same as "raise ... from None", but this compiles in python 2)'''
		e.__cause__ = None
		return e
	
	@staticmethod
	def typecheck(value, types):
		'''Check the type of an expression and return it'''
		if not isinstance(value, types):
			raise TypeError('Expected value to have type: %r' % types)
		return value
	
	@staticmethod
	def bytes(val):
		'''Convert to byte string'''
		if isinstance(val, str):
			return val.encode('utf-8', errors='replace')
		return Utils.typecheck(val, bytes)
	
	@staticmethod
	def string(val):
		'''Convert to char string'''
		if isinstance(val, bytes):
			return val.decode('utf-8', errors='replace')
		return Utils.typecheck(val, str)
	
	@staticmethod
	def integer(val):
		'''Convert to integer'''
		# Convert from string
		if isinstance(val, str):
			# Get prefix
			if val[:1] in (u'+', u'-'):
				prefix = val[1:3]
			else:
				prefix = val[0:2]
			# Check prefix
			if prefix == u'0b':
				return int(val, 2)
			elif prefix == u'0o':
				return int(val, 8)
			elif prefix == u'0x':
				return int(val, 16)
		
		# Convert from bytes
		elif isinstance(val, bytes):
			# Get prefix
			if val[:1] in (b'+', b'-'):
				prefix = val[1:3]
			else:
				prefix = val[0:2]
			# Check prefix
			if prefix == b'0b':
				return int(val, 2)
			elif prefix == b'0o':
				return int(val, 8)
			elif prefix == b'0x':
				return int(val, 16)
		
		# Fallback
		return int(val)
		
	@staticmethod
	def ljust(list, width, fillitem=None):
		'''Padd a list to a mininum size, while keeping existing elements on the left.'''
		return list + [fillitem] * (width - len(list))
		
	@staticmethod
	def rjust(list, width, fillitem=None):
		'''Padd a list to a mininum size, while keeping existing elements on the right.'''
		return [fillitem] * (width - len(list)) + list

	@staticmethod
	def trace(f):
		'''Trace a function call'''
		level = Utils.trace.level = [0]
		def inner(*args, **kwargs):
			indent = '| ' * level[0]
			p = ", ".join([repr(x) for x in args] + ["%s=%r" % x for x in kwargs.items()])
			print('{indent}ENTER: {func} ({params})'.format(func=f.__name__, params=p, indent=indent))
			level[0] += 1
			
			r = f(*args, **kwargs)
			
			level[0] -= 1
			print('{indent}LEAVE: {func} -> {result}'.format(func=f.__name__, result=r, indent=indent))
			return r
		return inner
