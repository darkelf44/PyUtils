# Imports
from terminfo import TerminalModule

# Terminal: Mach Console with ANSI color
TerminalModule(['mach_color'], use=['mach'], max_colors=8, max_pairs=64, enter_dim_mode=b'\x1b[2m', enter_secure_mode=b'\x1b[8m', orig_pair=b'\x1b[37;40m', exit_standout_mode=b'\x1b[27m', set_a_background=b'\x1b[4%p1%dm', set_a_foreground=b'\x1b[3%p1%dm')
