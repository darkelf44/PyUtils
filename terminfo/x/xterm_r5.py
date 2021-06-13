# Imports
from terminfo import TerminalModule

# Terminal: xterm R5 version
TerminalModule(['xterm_r5'], use=[], backspaces_with_bs=True, auto_right_margin=True, has_meta_key=True, move_standout_mode=True, eat_newline_glitch=True, columns=80, init_tabs=8, lines=24, bell=b'\x07', enter_bold_mode=b'\x1b[1m', clear_screen=b'\x1b[H\x1b[2J', carriage_return=b'\r', change_scroll_region=b'\x1b[%i%p1%d;%p2%dr', parm_left_cursor=b'\x1b[%p1%dD', cursor_left=b'\x08', parm_down_cursor=b'\x1b[%p1%dB', cursor_down=b'\n', parm_right_cursor=b'\x1b[%p1%dC', cursor_right=b'\x1b[C', cursor_address=b'\x1b[%i%p1%d;%p2%dH', parm_up_cursor=b'\x1b[%p1%dA', cursor_up=b'\x1b[A', parm_dch=b'\x1b[%p1%dP', delete_character=b'\x1b[P', parm_delete_line=b'\x1b[%p1%dM', delete_line=b'\x1b[M', clr_eos=b'\x1b[J', clr_eol=b'\x1b[K', cursor_home=b'\x1b[H', tab=b'\t', set_tab=b'\x1bH', parm_ich=b'\x1b[%p1%d@', insert_character=b'\x1b[@', parm_insert_line=b'\x1b[%p1%dL', insert_line=b'\x1b[L', scroll_forward=b'\n', key_left=b'\x1bOD', key_down=b'\x1bOB', key_right=b'\x1bOC', key_up=b'\x1bOA', key_dl=b'\x1b[31~', key_eol=b'\x1b[8~', key_f0=b'\x1bOq', key_f1=b'\x1b[11~', key_f10=b'\x1b[21~', key_f11=b'\x1b[23~', key_f12=b'\x1b[24~', key_f2=b'\x1b[12~', key_f3=b'\x1b[13~', key_f4=b'\x1b[14~', key_f5=b'\x1b[15~', key_f6=b'\x1b[17~', key_f7=b'\x1b[18~', key_f8=b'\x1b[19~', key_f9=b'\x1b[20~', key_home=b'\x1b[1~', key_il=b'\x1b[30~', key_mouse=b'\x1b[M', restore_cursor=b'\x1b8', enter_reverse_mode=b'\x1b[7m', scroll_reverse=b'\x1bM', exit_insert_mode=b'\x1b[4l', keypad_local=b'\x1b[?1l\x1b>', exit_standout_mode=b'\x1b[m', exit_underline_mode=b'\x1b[m', reset_2string=b'\x1b>\x1b[?1;3;4;5;6l\x1b[4l\x1b[?7h\x1b[m\x1b[r\x1b[2J\x1b[H', save_cursor=b'\x1b7', set_attributes=b'\x1b[%?%p1%t;7%;%?%p2%t;4%;%?%p3%t;7%;%?%p4%t;5%;%?%p6%t;1%;m', exit_attribute_mode=b'\x1b[m', enter_insert_mode=b'\x1b[4h', keypad_xmit=b'\x1b[?1h\x1b=', enter_standout_mode=b'\x1b[7m', enter_underline_mode=b'\x1b[4m', clear_all_tabs=b'\x1b[3g', key_backspace=b'\x08', user8=b'\x1b[?1;2c', user6=b'\x1b[%i%d;%dR', user7=b'\x1b[6n', user9=b'\x1b[c', key_dc=b'\x1b[3~', key_end=b'\x1b[4~', key_ic=b'\x1b[2~', key_npage=b'\x1b[6~', key_ppage=b'\x1b[5~')
