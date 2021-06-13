# Imports
from terminfo import TerminalModule

# Terminal: dec vt102
TerminalModule(['vt102'], use=['vt100'], delete_character=b'\x1b[P', delete_line=b'\x1b[M', insert_line=b'\x1b[L', exit_insert_mode=b'\x1b[4l', enter_insert_mode=b'\x1b[4h')
