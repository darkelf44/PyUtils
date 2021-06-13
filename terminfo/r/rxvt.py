# Imports
from terminfo import TerminalModule

# Terminal: rxvt terminal emulator (X Window System)
TerminalModule(['rxvt'], use=['rxvt_basic'], no_color_video=None, column_address=b'\x1b[%i%p1%dG', key_f0=b'\x1b[21~', exit_attribute_mode=b'\x1b[m\x0f', row_address=b'\x1b[%i%p1%dd', AX=True, max_colors=8, max_pairs=64, orig_pair=b'\x1b[39;49m', set_a_background=b'\x1b[4%p1%dm', set_a_foreground=b'\x1b[3%p1%dm')
