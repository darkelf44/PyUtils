import sys, os, io
import re
import json
import ctypes

class Types:

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

	def __init__(self, stdc=True, stddef=False, stdint=False, dlltype=False):
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
		if isinstance(type, tuple):
			op, nodes = type[0], type[1:]
			if op == '*':
				return self._pointer(self.build(nodes[0]))
			elif op == '[]':
				return self._array(self.build(nodes[0]), nodes[1])
			elif op == '->':
				return self._function(tuple(self.build(x) for x in nodes[0]), self.build(nodes[1]), nodes[2])
			else:
				raise ValueError('type: Invalid operator: %s' % op)
		elif isstring(type):
			info = self.get_typeinfo(type)
			if info is not None:
				return info[2]
			else:
				raise ValueError('type: Undefned type: %s' % type)
		else:
			raise ValueError('type: Invalid tree')
	
	def _pointer(self, type):
		'''Create type value for pointer'''
		return ctypes.POINTER(type)

	def _array(self, type, length):
		'''Create type value for array'''
		return type * length
		
	def _function(self, params, result, calltype):
		'''Create type value for functions'''
		if calltype == 'cdecl':
			return ctypes.CFUNCTYPE(result, *params)
		elif calltype == 'stdcall':
			return ctypes.WINFUNCTYPE(result, *params)
		else:
			raise ValueError('calltype: Invalid value')
		
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
		
		# Tokenize the input
		expr = cls.tokenize(text)
		
		# Calltype prefix "cdecl:" or "stdcall:"
		calltype = 'cdecl'
		if len(expr) > 1 and expr[1] == ':' and not expr[0][:1].isnumeric() and expr[0].replace('_', '').isalnum() :
			calltype, expr = expr[0], expr[2:]

		# The state machine for grammar:
		#	Start: (0)	End: (0) (3) (7)
		#	(0), (2) ---[id]--> (3) ---'*'---> (3) ---'['--> (4) ---[num]--> (5) ---']'--> (3) ---','--> (2)
		#	(6) ---[id]--> (7) ---'*'---> (7) ---'['--> (8) ---[num]--> (9) ---']'--> (7)
		#	(0), (3) ---'->'--> (6)
		#	(0)  ---'('--> (0) + push
		#	(2)  ---'('--> (0) + push 
		#	(6)  ---'('--> (0) + push 
		#	(3), (7) ---')'--> pop (?)
		#	(1)  ---'->'--> (6)
		
		# TODO: Additional grammar for '...'
		#	(2)  ---'...'--> (10) ---'->'--> (6)
		#	(10) ---')'--> pop (?)
		
		state = 0
		state_stack = []
		result = []
		result_stack = []
		
		# Process tokens
		for i, t in enumerate(expr):
			if t == '->':
				(state in (0, 1, 3)) or error_unexpected(i)
				state = 6
				result = [result]
			elif t == ',':
				(state == 3) or error_unexpected(i)
				state = 2
			elif t == '*':
				(state in (3, 7)) or error_unexpected(i)
				result[-1] = ('*', result[-1])
			elif t == '[':
				(state in (3, 7)) or error_unexpected(i)
				state += 1
			elif t == ']':
				(state in (5, 9)) or error_unexpected(i)
				state -= 2
			elif t == '(':
				(state in (0, 2, 6)) or error_unexpected(i)
				state_stack.append(state)
				state = 0
				result_stack.append(result)
				result = []
			elif t == ')':
				state_stack and result_stack or error_unexpected(i)
				# Create function result
				if state == 7:
					result = [('->', tuple(result[0]), result[1], calltype)]
				# Unify results
				if state == 0 or (state == 3 and len(result) > 1):	# Allows you to use "(A, B) -> C"
					(state_stack[-1] == 0) or error_unexpected(i)
					state = 1
				else:
					(state in (3, 7)) or error_unexpected(i)
					(state_stack[-1] in (0, 2, 6)) or error_unexpected(i)
					state = {0:3, 2:3, 6:7}[state_stack.pop()]
				result = result_stack.pop() + result
			elif t[:1].isdigit():
				(state in (4, 8)) and t.isdigit() or error_unexpected(i)
				result[-1] = ('[]', result[-1], int(t))
				state += 1
			elif t is not None:
				(state in (0, 2, 6)) and t.replace('_', '').isalnum() or error_unexpected(i)
				result.append(t)
				state = {0:3, 2:3, 6:7}[state]
		
		# Create function result
		if state == 7:
			result = [('->', tuple(result[0]), result[1], calltype)]
			
		# Final check and result
		(state in (0, 3, 7)) and (len(result) == 1) or error_unfinished()
		return result[0]
		
class DLL:

	# Path to load
	path = ['.'] + list(sys.path)
	# Extensions to use
	exts = ['dll', 'so', 'dlib']
	# Public dll cache
	cache = {}
	
	def __init__(self, library, libconf, libdesc):
		self._types = Types(False, False, False, True)
		self._namespace = {}
		self._description = libdesc
		
		# TODO: process config & load binary
		self._binary = ctypes.cdll.LoadLibrary(library)
		self.process(libconf)
	
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
		dllfile.replace('*', jsonname)
			
		# Locate dllfile
		dllfile = cls.locate(dllfile, [jsonpath] + cls.path, cls.exts) or error_notfound(dllfile)
		
		# Create object
		result = cls(library=config['library'], binary=dllfile)
		
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
		
	def process(self, config):
		
		# Process types
		pass
		
			
	def _define_const_int(self, name, value):
		# Decode value
		if isstring(value) and value.startswith('0x'):
			value = int(value, 16)
		else:
			value = int(value)
		# Define constant
		self._namespace[name] = value
		
	def _define_const_float(self, name, value):
		# Decode value
		value = float(value)
		# Define constant
		self._namespace[name] = value
		
	def _define_const_string(self, name, value):
		# Define constant
		self.namespace[name] = value
		
	def _define_type_alias(self, name, value):
		# Define type alias
		self._types.set_alias(name, value)
		self._namespace[name] = self._types.get(name)
		
	def _define_type_enum(self, name, data):
		pass
		
	def _define_type_union(self, name, data):
		pass
		
	def _define_type_struct(self, name, data):
		pass
		
	def _export_var(self, name, data):
		pass
		
	def _export_function(self, name, data):
		pass
		
def isstring(obj):
	'''Detects if the object is any of the two string types'''
	return type(obj) in (type(b''), type(u''))


# Exports
__all__ = ('Types', 'DLL')
	
