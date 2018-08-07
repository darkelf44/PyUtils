import ctypes

class Types:

	def __init__(self, stdc=True, stddef=False, stdint=False, extint=False):
		# Init
		self._list = {}
		
		# Load standard types
		stdc and self.load_stdc()
		stddef and self.load_stddef()
		stdint and self.load_stdint()
		extint and self.load_extint()
	
	def load_stdc(self):
		self._list.update({
			'char' : ('char', ctypes.c_char),
			'wchar' : ('wchar_t', ctypes.c_wchar),
			'byte' : ('signed byte', ctypes.c_byte),
			'ubyte' : ('unsigned byte', ctypes.c_ubyte),
			'short' : ('signed short', ctypes.c_short),
			'ushort' : ('unsigned short', ctypes.c_ushort),
			'int' : ('signed int', ctypes.c_int),
			'uint' : ('unsigned int', ctypes.c_uint),
			'long' : ('signed long', ctypes.c_long),
			'ulong' : ('unsigned long', ctypes.c_ulong),
			'longlong' : ('signed long long', ctypes.c_longlong),
			'ulonglong' : ('unsigned long long', ctypes.c_ulonglong),
			'float' : ('float', ctypes.c_float),
			'double' : ('double', ctypes.c_double),
		})
	
	def load_stddef(self):
		bits = ctypes.sizeof(ctypes.c_void_p)	# Pointer size
		self._list.update({
			'size_t' : ('size_t', ctypes.c_size_t),
			'ptrdiff_t' : ('ptrdiff_t', ctypes.c_int32_t if bits == 4 else ctypes.c_int64_t),
		})

	def load_stdint(self):
		bits = ctypes.sizeof(ctypes.c_void_p)	# Pointer size
		self._list.update({
			'int8_t' : ('int8_t', ctypes.c_int8_t),
			'int16_t' : ('int16_t', ctypes.c_int16_t),
			'int32_t' : ('int32_t', ctypes.c_int32_t),
			'int64_t' : ('int64_t', ctypes.c_int64_t),
			'uint8_t' : ('uint8_t', ctypes.c_uint8_t),
			'uint16_t' : ('uint16_t', ctypes.c_uint16_t),
			'uint32_t' : ('uint32_t', ctypes.c_uint32_t),
			'uint64_t' : ('uint64_t', ctypes.c_uint64_t),
			'intptr_t' : ('intptr_t', ctypes.c_int32_t if bits == 4 else ctypes.c_int64_t),
			'uintptr_t' : ('uintptr_t', ctypes.c_uint32_t if bits == 4 else ctypes.c_uint64_t),
		})

	def load_stdext(self):
		self._list.update({
			's8' : ('int8_t', ctypes.c_int8_t),
			's16' : ('int16_t', ctypes.c_int16_t),
			's32' : ('int32_t', ctypes.c_int32_t),
			's64' : ('int64_t', ctypes.c_int64_t),
			'u8' : ('uint8_t', ctypes.c_uint8_t),
			'u16' : ('uint16_t', ctypes.c_uint16_t),
			'u32' : ('uint32_t', ctypes.c_uint32_t),
			'u64' : ('uint64_t', ctypes.c_uint64_t),
			'f32' : ('float', ctypes.c_float),
			'f64' : ('double', ctypes.c_double),
			'float32' : ('float', ctypes.c_float),
			'float64' : ('double', ctypes.c_double),
		})
		
	def __getitem__(self, index):
		return self._list[index][2]
		
	def get(self, type):
		pass
		
	def set(self, name, object):
		pass
		
	def set_alias(self, name, type):
		pass

	def get_typeinfo(self, name):
		pass
	
	def set_typeinfo(self, name, typeinfo):
		pass
		
	@classmethod
	def tokenize(cls, text):
		# List of symbols
		symbols = {'->', ',', '*', '[', ']', '(', ')'}
		
		# Tokenize input the fast way
		for s in symbols:
			text = text.replace(s, ' %s ' % s)
		return text.split()
		
	@classmethod
	def parsetype(cls, text):
		
		# Functions for errors reporting
		def error_unexpected(i):
			raise ValueError('Unexpected token: "%s" following: "%s"' % (expr[i], ' '.join(expr[:i])))
		def error_unfinished():
			raise ValueError('Unfinished expression: "%s"' % ' '.join(expr[:i]))
		
		# Tokenize the input
		expr = cls.tokenize(text)
		
		# The state machine for grammar:
		#	Start: (0)	End: (0) (3) (7)
		#	(0), (2) ---[id]--> (3) ---'*'---> (3) ---'['--> (4) ---[num]--> (5) ---']'--> (3) ---','--> (2)
		#	(6) ---[id]--> (7) ---'*'---> (7) ---'['--> (8) ---[num]--> (9) ---']'--> (7)
		#	(0), (3) ---'->'--> (6)
		#	(0)  ---'('--> (0) + push
		#	(2)  ---'('--> (0) + push 
		#	(6)  ---'('--> (0) + push 
		#	(3), (7) ---')'--> pop (?) /
		#	(1)  ---'->'--> (6)
		
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
					result = [('->', tuple(result[0]), result[1])]
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
			result = [('->', tuple(result[0]), result[1])]
			
		# Final check and result
		(state in (0, 3, 7)) and (len(result) == 1) or error_unfinished()
		return result[0]
