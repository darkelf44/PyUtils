# Imports
from terminfo import TerminalModule

# Terminal: generic color xterm
TerminalModule(['xterm_color'], use=['xterm_r6'], no_color_video=None, orig_pair=b'\x1b[m', max_colors=8, max_pairs=64, set_a_background=b'\x1b[4%p1%dm', set_a_foreground=b'\x1b[3%p1%dm')
