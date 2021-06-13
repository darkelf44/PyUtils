# Imports
from terminfo import TerminalModule

# Terminal: Mach Console with bold instead of underline
TerminalModule(['mach_bold'], use=['mach'], exit_underline_mode=b'\x1b[0m', enter_underline_mode=b'\x1b[1m')
