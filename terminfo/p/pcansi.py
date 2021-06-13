# Imports
from terminfo import TerminalModule

# Terminal: ibm-pc terminal programs claiming to be ansi
TerminalModule(['pcansi'], use=[], backspaces_with_bs=True, auto_right_margin=True, move_insert_mode=True, move_standout_mode=True, columns=80, init_tabs=8, lines=24, bell=b'\x07', back_tab=b'\x1b[Z', clear_screen=b'\x1b[H\x1b[J', carriage_return=b'\r', cursor_left=b'\x1b[D', cursor_down=b'\x1b[B', cursor_right=b'\x1b[C', cursor_address=b'\x1b[%i%p1%d;%p2%dH', cursor_up=b'\x1b[A', delete_character=b'\x1b[P', delete_line=b'\x1b[M', clr_eos=b'\x1b[J', clr_eol=b'\x1b[K', cursor_home=b'\x1b[H', tab=b'\t', set_tab=b'\x1bH', insert_line=b'\x1b[L', scroll_forward=b'\n', key_backspace=b'\x08', key_left=b'\x1b[D', key_down=b'\x1b[B', key_right=b'\x1b[C', key_up=b'\x1b[A', key_home=b'\x1b[H', clear_all_tabs=b'\x1b[3g', enter_blink_mode=b'\x1b[5m', enter_bold_mode=b'\x1b[1m', enter_secure_mode=b'\x1b[8m', enter_reverse_mode=b'\x1b[7m', exit_standout_mode=b'\x1b[m', exit_underline_mode=b'\x1b[m', set_attributes=b'\x1b[0;10%?%p1%t;7%;%?%p2%t;4%;%?%p3%t;7%;%?%p4%t;5%;%?%p6%t;1%;%?%p7%t;8%;%?%p9%t;12%;m', exit_attribute_mode=b'\x1b[0;10m', enter_alt_charset_mode=b'\x1b[12m', enter_standout_mode=b'\x1b[7m', enter_underline_mode=b'\x1b[4m', acs_chars=b'+\x10,\x11-\x18.\x190\xdb`\x04a\xb1f\xf8g\xf1h\xb0j\xd9k\xbfl\xdam\xc0n\xc5o~p\xc4q\xc4r\xc4s_t\xc3u\xb4v\xc1w\xc2x\xb3y\xf3z\xf2{\xe3|\xd8}\x9c~\xfe', exit_alt_charset_mode=b'\x1b[10m', max_colors=8, no_color_video=3, max_pairs=64, orig_pair=b'\x1b[37;40m', set_a_background=b'\x1b[4%p1%dm', set_a_foreground=b'\x1b[3%p1%dm')
