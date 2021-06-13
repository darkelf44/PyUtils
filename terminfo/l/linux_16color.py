# Imports
from terminfo import TerminalModule

# Terminal: linux console with 16 colors
TerminalModule(['linux_16color'], use=['linux'], max_colors=16, no_color_video=42, max_pairs=256, set_a_background=b'\x1b[4%p1%{8}%m%d%?%p1%{7}%>%t;5%e;25%;m', set_a_foreground=b'\x1b[3%p1%{8}%m%d%?%p1%{7}%>%t;1%e;22%;m')
