# Imports
from terminfo import TerminalModule

# Terminal: GNU Screen with 256 colors
TerminalModule(['screen_256color'], use=['screen'], can_change=None, max_colors=256, max_pairs=65536, initialize_color=None, orig_pair=b'\x1b[39;49m', set_a_background=b'\x1b[%?%p1%{8}%<%t4%p1%d%e%p1%{16}%<%t10%p1%{8}%-%d%e48;5;%p1%d%;m', set_a_foreground=b'\x1b[%?%p1%{8}%<%t3%p1%d%e%p1%{16}%<%t9%p1%{8}%-%d%e38;5;%p1%d%;m', set_background=None, set_foreground=None)
