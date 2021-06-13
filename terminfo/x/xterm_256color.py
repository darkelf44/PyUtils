# Imports
from terminfo import TerminalModule

# Terminal: xterm with 256 colors
TerminalModule(['xterm_256color'], use=['xterm'], orig_colors=b'\x1b]104\x07', reset_1string=b'\x1bc\x1b]104\x07', can_change=True, max_colors=256, max_pairs=65536, initialize_color=b'\x1b]4;%p1%d;rgb:%p2%{255}%*%{1000}%/%2.2X/%p3%{255}%*%{1000}%/%2.2X/%p4%{255}%*%{1000}%/%2.2X\x1b\\', set_a_background=b'\x1b[%?%p1%{8}%<%t4%p1%d%e%p1%{16}%<%t10%p1%{8}%-%d%e48;5;%p1%d%;m', set_a_foreground=b'\x1b[%?%p1%{8}%<%t3%p1%d%e%p1%{16}%<%t9%p1%{8}%-%d%e38;5;%p1%d%;m', set_background=None, set_foreground=None)
