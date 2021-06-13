# Imports
from terminfo import TerminalModule

# Terminal: xterm with 16 colors like aixterm
TerminalModule(['xterm_16color'], use=['xterm'], can_change=True, initialize_color=b'\x1b]4;%p1%d;rgb:%p2%{255}%*%{1000}%/%2.2X/%p3%{255}%*%{1000}%/%2.2X/%p4%{255}%*%{1000}%/%2.2X\x1b\\', orig_colors=b'\x1b]104\x07', reset_1string=b'\x1bc\x1b]104\x07', max_colors=16, max_pairs=256, set_a_background=b'\x1b[%?%p1%{8}%<%t%p1%{40}%+%e%p1%{92}%+%;%dm', set_a_foreground=b'\x1b[%?%p1%{8}%<%t%p1%{30}%+%e%p1%{82}%+%;%dm', set_background=b'%p1%{8}%/%{6}%*%{4}%+\x1b[%d%p1%{8}%m%Pa%?%ga%{1}%=%t4%e%ga%{3}%=%t6%e%ga%{4}%=%t1%e%ga%{6}%=%t3%e%ga%d%;m', set_foreground=b'%p1%{8}%/%{6}%*%{3}%+\x1b[%d%p1%{8}%m%Pa%?%ga%{1}%=%t4%e%ga%{3}%=%t6%e%ga%{4}%=%t1%e%ga%{6}%=%t3%e%ga%d%;m')
