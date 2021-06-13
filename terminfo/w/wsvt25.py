# Imports
from terminfo import TerminalModule

# Terminal: NetBSD wscons in 25 line DEC VT220 mode
TerminalModule(['wsvt25'], use=['vt220'], back_color_erase=True, move_standout_mode=True, max_colors=8, columns=80, init_tabs=8, lines=25, no_color_video=2, max_pairs=64, init_2string=b'\x1b[r\x1b[25;1H', key_dc=b'\x1b[3~', key_end=b'\x1b[8~', key_f1=b'\x1b[11~', key_f10=b'\x1b[21~', key_f11=b'\x1b[23~', key_f12=b'\x1b[24~', key_f2=b'\x1b[12~', key_f3=b'\x1b[13~', key_f4=b'\x1b[14~', key_f5=b'\x1b[15~', key_f6=b'\x1b[17~', key_f7=b'\x1b[18~', key_f8=b'\x1b[19~', key_f9=b'\x1b[20~', key_home=b'\x1b[7~', orig_pair=b'\x1b[m', reset_1string=b'\x1bc', set_a_background=b'\x1b[4%p1%dm', set_a_foreground=b'\x1b[3%p1%dm')
