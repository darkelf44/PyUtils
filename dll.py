import sys, os, io
import re
import json
import ctypes

# Library version
version = (1, 0, 0)
versionstring = '%d.%d.%d' % version

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
		
		The Universal Type System (TM):
		
		TODO:
	'''
	
	CALLTYPES = {
		'@cdecl' : 'cdecl',
		'@stdcall' : 'stdcall',
	}

	def __init__(self, stdc=False, stddef=False, stdint=False, dlltype=False):
		# Init
		self._list = {}
		self._cache = {}
		
		# Load standard types
		stdc and self.load_stdc()
		stddef and self.load_stddef()
		stdint and self.load_stdint()
		dlltype and self.load_dlltype()
	
	def load_stdc(self):
		'''Load standard types from C'''
		self._list.update({
			'void'   : ('void', 'void', None),
			'char'   : ('char', 'char', ctypes.c_char),
			'wchar'  : ('wchar', 'wchar_t', ctypes.c_wchar),
			'byte'   : ('byte', 'signed byte', ctypes.c_byte),
			'ubyte'  : ('ubyte', 'unsigned byte', ctypes.c_ubyte),
			'short'  : ('short', 'signed short', ctypes.c_short),
			'ushort' : ('ushort', 'unsigned short', ctypes.c_ushort),
			'int'    : ('int', 'signed int', ctypes.c_int),
			'uint'   : ('uint', 'unsigned int', ctypes.c_uint),
			'long'   : ('long', 'signed long', ctypes.c_long),
			'ulong'  : ('ulong', 'unsigned long', ctypes.c_ulong),
			'longlong'  : ('longlong', 'signed long long', ctypes.c_longlong),
			'ulonglong' : ('ulonglong', 'unsigned long long', ctypes.c_ulonglong),
			'float'  : ('float', 'float', ctypes.c_float),
			'double' : ('double', 'double', ctypes.c_double),
		})
	
	def load_stddef(self):
		'''Load standard types from <stddef.h>'''
		bits = ctypes.sizeof(ctypes.c_void_p)	# Pointer size
		self._list.update({
			'size_t'    : ('size_t', 'size_t', ctypes.c_size_t),
			'ptrdiff_t' : ('ptrdiff_t', 'ptrdiff_t', ctypes.c_int32 if bits == 4 else ctypes.c_int64),
		})

	def load_stdint(self):
		'''Load standard types from <stdint.h>'''
		bits = ctypes.sizeof(ctypes.c_void_p)	# Pointer size
		self._list.update({
			'int8_t'    : ('int8_t', 'int8_t', ctypes.c_int8),
			'int16_t'   : ('int16_t', 'int16_t', ctypes.c_int16),
			'int32_t'   : ('int32_t', 'int32_t', ctypes.c_int32),
			'int64_t'   : ('int64_t', 'int64_t', ctypes.c_int64),
			'uint8_t'   : ('uint8_t', 'uint8_t', ctypes.c_uint8),
			'uint16_t'  : ('uint16_t', 'uint16_t', ctypes.c_uint16),
			'uint32_t'  : ('uint32_t', 'uint32_t', ctypes.c_uint32),
			'uint64_t'  : ('uint64_t', 'uint64_t', ctypes.c_uint64),
			'intptr_t'  : ('intptr_t', 'intptr_t', ctypes.c_int32 if bits == 4 else ctypes.c_int64),
			'uintptr_t' : ('uintptr_t', 'uintptr_t', ctypes.c_uint32 if bits == 4 else ctypes.c_uint64),
		})

	def load_dlltype(self):
		'''Load types from the Universal Type System, used by te DLL classes'''
		bits = ctypes.sizeof(ctypes.c_void_p)	# Pointer size
		self._list.update({
			'N'   :	('N', 'nothing', None),
			'P'   : ('P', 'pointer', ctypes.c_void_p),
			'C'   : ('C', 'character', ctypes.c_char),
			'W'   : ('W', 'wide character', ctypes.c_wchar),
			'SI'  : ('SI', 'signed integer (platform)', ctypes.c_int32 if bits == 4 else ctypes.c_int64),
			'S8'  : ('S8', 'signed integer (8)', ctypes.c_int8),
			'S16' : ('S16', 'signed integer (16)', ctypes.c_int16),
			'S32' : ('S32', 'signed integer (32)', ctypes.c_int32),
			'S64' : ('S64', 'signed integer (64)', ctypes.c_int64),
			'UI'  : ('UI', 'unsigned integer (platform)', ctypes.c_uint32 if bits == 4 else ctypes.c_uint64),
			'U8'  : ('U8', 'unsigned integer (8)', ctypes.c_uint8),
			'U16' : ('U16', 'unsigned integer (16)', ctypes.c_uint16),
			'U32' : ('U32', 'unsigned integer (32)', ctypes.c_uint32),
			'U64' : ('U64', 'unsigned integer (64)', ctypes.c_uint64),
			'F32' : ('F32', 'IEEE float (32)', ctypes.c_float),
			'F64' : ('F64', 'IEEE float (64)', ctypes.c_double),
		})
		
	def has(self, type):
		info = self.get_typeinfo(type.strip())
		return info is not None
		
	def get(self, type, calltype='cdecl'):
		# Remove some whitespace
		type = type.strip()
		
		# Lookup in type info or type cache
		if type.isalnum():
			info = self.get_typeinfo(type.strip())
			if info is not None:
				return info[2]
		elif self._cache is not None:
			info = self._cache.get(type)
			if info:
				return info[1]
			
		# Build type
		info = (type, self.build(self.parsetype(type)))
		self._cache[type] = info
		return info[1]
		
	def set(self, name, fullname, object):
		self.set_typeinfo(name, (name, fullname, object))
		
	def set_alias(self, name, typename):
		self.set_typeinfo(name, (self.parsetype(typename), 'Alias: %s' % typename, self.get(typename)))

	def get_typeinfo(self, name):
		return self._list.get(name)
	
	def set_typeinfo(self, name, typeinfo):
		self._list[name] = typeinfo
		
	# Operators
	__getitem__ = get
	__setitem__ = set
	
	def build(self, type):
		if type == '()':
			return None
		elif type == '...':
			return '...'
		else:
			op, nodes = type[0], type[1:]
			if op == '*':
				return self._pointer(self.build(nodes[0]))
			elif op == '[]':
				return self._array(self.build(nodes[0]), nodes[1])
			elif op == '->':
				return self._function(tuple(self.build(x) for x in nodes[0]), self.build(nodes[1]), nodes[2])
			elif op == 'id':
				info = self.get_typeinfo(nodes[0])
				if info is not None:
					return info[2]
				else:
					print(self._list)
					raise ValueError('type: Undefined type: %s' % type)
			else:
				raise ValueError('type: Invalid operator: %s' % op)
	
	def _pointer(self, type):
		'''Create type value for pointer'''
		return ctypes.POINTER(type)
	
	def _array(self, type, length):
		'''Create type value for array'''
		return type * (length or 0)
	
	def _function(self, params, result, calltype):
		'''Create type value for functions'''
		if '...' in params:
			# Vararg function
			result = self._function([], result, calltype)
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
		symbols = {'->', ',', '*', ':', '...', '[', ']', '(', ')'}
		
		# Tokenize input the fast way
		for s in symbols:
			text = text.replace(s, ' %s ' % s)
		return text.split()
		
	@classmethod
	def parsetype(cls, text):
	
		# Functions for errors reporting
		def error_unexpected(i):
			raise ValueError('text: Unexpected token: "%s" following: "%s"' % (expr[i], ' '.join(expr[:i])))
		def error_unfinished():
			raise ValueError('text: Unfinished expression: "%s"' % ' '.join(expr[:i]))
		
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
		
		level = [0]
		def trace(f):
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
		try:
			type, end = parse_type(0)
			if end != expr_len:
				raise ValueError('syntax error: Expression is not a valid type!')
			return type
		except TypeError:
			raise ValueError('syntax error: Expression is not a valid type!') 
				
class DLL(object):

	# Path to load
	path = ['.'] + list(sys.path)
	# Default extensions
	exts = ['dlib']
	if os.name == 'nt':
		exts += ['dll']
	else:
		exts += ['so']
	# Public dll cache
	cache = {}
	
	def __init__(self, library, libconf, libdesc):
		self._types = Types(dlltype=True)
		self._namespace = {}
		self._description = libdesc
		
		# Load library
		self._binary = ctypes.cdll.LoadLibrary(os.path.abspath(library))
		self._process_config(libconf)
		
	@classmethod
	def load(cls, jsonfile, dllfile=None, private=False):
	
		# Load from dll cache
		if not private:
			result = cls.cache.get(jsonfile)
			if result is not None:
				return result
	
		# Load json with comments
		with io.open(jsonfile, 'r', encoding='utf-8') as file:
			config = json.loads(re.sub(r'^[ \t]*#.*$', '', file.read(), flags=re.MULTILINE))
			
		def error_invalid(x):
			raise ValueError('jsonfile: Invalid value for %s' % x)
		def error_notfound(x):
			raise IOError('dllfile: File not found: %s' % x)
		
		# Validate file format
		(config['type'] == 'library') or error_invalid('type')
		(int(config['version']) == 1) or error_invalid('version')
		
		# Process filename
		jsonpath = os.path.abspath(os.path.dirname(jsonfile))
		jsonname = os.path.splitext(os.path.basename(jsonfile))[0]
		
		# Default values
		if dllfile is None:
			dllfile = config.get('binary', '*')
		dllfile = dllfile.replace('*', jsonname)
			
		# Locate dllfile
		dllfile = cls.locate(dllfile, [jsonpath] + cls.path, cls.exts) or error_notfound(dllfile)
		
		# Create object
		result = cls(library=dllfile, libconf=config['library'], libdesc=config.get('description'))
		
		# Save to dll cache
		if not private:
			cls.cache[jsonfile] = result
			
		# Return result
		return result
		
	@classmethod
	def locate(cls, filename, path=None, exts=None):
	
		# Default path and exts
		if path is None:
			path = cls.path
		if exts is None:
			exts = cls.exts
	
		# Separate path
		dlldir = os.path.dirname(filename)
		dllext = os.path.splitext(filename)[1]
		
		# Find dll file
		if dlldir:
			# Static lookup
			file = os.path.abspath(filename)
			if os.path.isfile(file):
				return file
				
			# With extensions
			if not dllext:
				for extension in exts:
					if os.path.isfile(file + '.' + extension):
						return file + '.' + extension
			
		else:
			for root in path:
				# Path lookup
				file = os.path.join(root, filename)
				if os.path.isfile(file):
					return file
				
				# With extensions
				if not dllext:
					for extension in exts:
						if os.path.isfile(file + '.' + extension):
							return file + '.' + extension
				
		# Not found
		return None
		
	def __getattr__(self, attr):
		return self._namespace[attr]
	
	def __getitem__(self, name):
		return self._namespace[name]
		
	def __iter__(self):
		return self._namespace.__iter__()
		
	def keys(self):
		return self._namespace.keys()
		
	def values(self):
		return self._namespace.values()
		
	def items(self):
		return self._namespace.items()
		
	def _process_config(self, config):
	
		# Library version
		self.version = config.get('version')
		
		# Process defines
		defines = config.get('define')
		if defines:
		
			# Define constants
			group = defines.get("const")
			if group:
				for item in group:
					k, t, v = item
					if t in ('I', 'int'):
						self._define_const_int(k, v)
					elif t in ('F', 'float'):
						self._define_const_float(k, v)
					elif t in ('S', 'string'):
						self._define_const_string(k, v)
					elif t in ('W', 'wstring'):
						self._define_const_wstring(k, v)
						
			# Define types
			group = defines.get("type")
			if group:
				for item in group:
					k, t, v = item
					if t in ('=', 'alias'):
						self._define_type_alias(k, v)
					elif t == 'enum':
						self._define_type_enum(k, v)
					elif t == 'union':
						self._define_type_union(k, v)
					elif t == 'struct':
						self._define_type_struct(k, v)
					
		# Process exports
		exports = config.get('export')
		if exports:
		
			# Export variables
			group = exports.get('variable')
			if group:
				for item in group:
					k, n, v = item
					self._export_variable(k, n, v)
					
			# Export functions
			group = exports.get('function')
			if group:
				for item in group:
					k, n, v = item
					self._export_function(k, n, v)
		
	def _define_const_int(self, name, value):
	
		# Check duplicates
		if name in self._namespace:
			raise ValueError('name: "%s" is already defined' % name)

		# Decode value
		if isstring(value) and value.startswith('0x'):
			value = int(value, 16)
		else:
			value = int(value)
		# Define constant
		self._namespace[name] = value
		
	def _define_const_float(self, name, value):
	
		# Check duplicates
		if name in self._namespace:
			raise ValueError('name: "%s" is already defined' % name)

		# Decode value
		value = float(value)
		# Define constant
		self._namespace[name] = value
		
	def _define_const_string(self, name, value):
	
		# Check duplicates
		if name in self._namespace:
			raise ValueError('name: "%s" is already defined' % name)

		# Define constant
		self._namespace[name] = value.encode('utf-8')
		
	def _define_const_wstring(self, name, value):
	
		# Check duplicates
		if name in self._namespace:
			raise ValueError('name: "%s" is already defined' % name)

		# Define constant
		self._namespace[name] = value
		
	def _define_type_alias(self, name, value):
	
		# Check duplicates
		if name in self._namespace:
			raise ValueError('name: "%s" is already defined' % name)
		
		# Define type alias
		self._types.set_alias(name, value)
		self._namespace[name] = self._types.get(name)
		
	def _define_type_enum(self, name, data):
	
		# Check duplicates
		if name in self._namespace:
			raise ValueError('name: "%s" is already defined' % name)
	
		# Define enum values
		if data:
			lo, hi, next = 0, 0, 0
			for v in data:
				# Get name and optional value
				v = [x.strip() for x in v.split('=', 1)]
				n = v[0]
				next = next if len(v) == 1 else int(v[1])
				
				# Check duplicates
				if name in self._namespace:
					raise ValueError('data: "%s" is already defined' % n)
				
				# Set enum value
				self._namespace[n] = next
				
				# Update
				lo = min(lo, next)
				hi = max(hi, next)
				next += 1
				
		# Define enum type
		if lo < 0:
			hi = max(hi, -lo)
			type = ctypes.c_int64
			limits = [(1 << 7, ctypes.c_int8), (1 << 15, ctypes.c_int16), (1 << 31, ctypes.c_int32)]
		else:
			type = ctypes.c_uint64
			limits = [(1 << 8, ctypes.c_uint8), (1 << 16, ctypes.c_uint16), (1 << 32, ctypes.c_uint32)]
		
		for l, t in limits:
			if hi < l:
				type = t
		
		self._types.set(name, 'Enum %s' % name, type)
		self._namespace[name] = type
		
		
	def _define_type_union(self, name, data):
	
		# Errors
		def error_duplicate():
			raise ValueError('name: "%s" is already defined' % name)
		
		# Declare union
		if name in self._namespace:
			union = self._namespace.get(name)
			# Check union type
			issubclass(union, ctypes.Union) or error_duplicate()
			# Check incomplete union
			(not hasattr(union, '_fields_')) or (union._fields_ is None) or error_duplicate()
		else:
			union = type(str(name), (ctypes.Union, ), {})
			self._types.set(name, 'Union %s'  % name, union)
			self._namespace[name] = union
		
		# Define union
		if data is not None:
			fields = []
			for v in data:
				# Get name and type
				field, type = [x.strip() for x in v.split(':', 1)]
				# Resolve field type
				fields.append((field, self._types.get(type)))
				
			# Define fields
			union._fields_ = fields
		
	def _define_type_struct(self, name, data):
	
		# Errors
		def error_duplicate():
			raise ValueError('name: "%s" is already defined' % name)
		
		# Declare struct
		if name in self._namespace:
			struct = self._namespace.get(name)
			# Check struct type
			issubclass(struct, ctypes.Structure) or error_duplicate()
			# Check incomplete struct
			(not hasattr(struct, '_fields_')) or (struct._fields_ is None) or error_duplicate()
		else:
			struct = type(str(name), (ctypes.Structure, ), {})
			self._types.set(name, 'Struct %s'  % name, struct)
			self._namespace[name] = struct
		
		# Define struct
		if data is not None:
			fields = []
			for v in data:
				# Get name and type
				fn, ft = [x.strip() for x in v.split(':', 1)]
				# Resolve field type
				fields.append((fn, self._types.get(ft)))
			
			# Define fields
			struct._fields_ = fields
		
	def _export_variable(self, name, dllname, type):
	
		# Check duplicates
		if name in self._namespace:
			raise ValueError('name: "%s" is already defined' % name)
		
		# Decode data
		if (dllname) is None:
			dllname = name
			
		# Get variable
		type = self._types.get(type)
		self._namespace[name] = type.in_dll(self._binary, "name")
		
	def _export_function(self, name, dllname, type):
	
		# Check duplicates
		if name in self._namespace:
			raise ValueError('name: "%s" is already defined' % name)
		
		# Decode data
		if (dllname) is None:
			dllname = name
		
		# Get function
		type = self._types.get(type)
		self._namespace[name] = ctypes.cast(getattr(self._binary, dllname), type)
		
def isstring(obj):
	'''Detects if the object is any of the two string types'''
	return type(obj) in (type(b''), type(u''))


# Exports
__all__ = ('Types', 'DLL')
	
