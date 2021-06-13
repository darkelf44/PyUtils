# Imports
from terminfo import TerminalModule

# Terminal: AppKit Terminal.app
TerminalModule(['nsterm', 'nsterm_256color'], use=[], exit_standout_mode=b'\x1b[27m', exit_underline_mode=b'\x1b[24m', XT=True, key_mouse=b'\x1b[<', key_end=b'\x1bOF', key_home=b'\x1bOH', key_sdc=b'\x1b[3;2~', key_sleft=b'\x1b[1;2D', key_sright=b'\x1b[1;2C', key_btab=b'\x1b[Z', key_f18=b'\x1b[32~', key_sdc5=b'\x1b[3;5~', key_sleft3=b'\x1bb', key_sleft5=b'\x1b[1;5D', key_sright3=b'\x1bf', key_sright5=b'\x1b[1;5C', back_color_erase=True, auto_left_margin=None, move_insert_mode=True, no_pad_char=True, parm_dch=b'\x1b[%p1%dP', delete_character=b'\x1b[P', flash_screen=b'\x1b[?5h$<200/>\x1b[?5l', column_address=b'\x1b[%i%p1%dG', parm_ich=b'\x1b[%p1%d@', insert_character=b'\x1b[@', key_dc=b'\x1b[3~', key_f10=b'\x1b[21~', key_f11=b'\x1b[23~', key_f12=b'\x1b[24~', key_f13=b'\x1b[25~', key_f14=b'\x1b[26~', key_f15=b'\x1b[28~', key_f16=b'\x1b[29~', key_f17=b'\x1b[31~', key_f19=b'\x1b[33~', key_f20=b'\x1b[34~', key_f5=b'\x1b[15~', key_f6=b'\x1b[17~', key_f7=b'\x1b[18~', key_f8=b'\x1b[19~', key_f9=b'\x1b[20~', key_npage=b'\x1b[6~', key_ppage=b'\x1b[5~', exit_ca_mode=b'\x1b[2J\x1b[?47l\x1b8', exit_insert_mode=b'\x1b[4l', enter_ca_mode=b'\x1b7\x1b[?47h', enter_insert_mode=b'\x1b[4h', row_address=b'\x1b[%i%p1%dd', cursor_invisible=b'\x1b[?25l', cursor_normal=b'\x1b[?25h', acs_chars=b'``aaffggjjkkllmmnnooppqqrrssttuuvvwwxxyyzz{{||}}~~', ena_acs=b'\x1b(B\x1b)0', exit_alt_charset_mode=b'\x0f', set_attributes=b'\x1b[0%?%p6%t;1%;%?%p2%t;4%;%?%p1%p3%|%t;7%;%?%p4%t;5%;%?%p5%t;2%;%?%p7%t;8%;m%?%p9%t\x0e%e\x0f%;', exit_attribute_mode=b'\x1b[m\x0f', enter_alt_charset_mode=b'\x0e', auto_right_margin=True, move_standout_mode=True, eat_newline_glitch=True, xon_xoff=True, columns=80, init_tabs=8, lines=24, bell=b'\x07', enter_blink_mode=b'\x1b[5m', enter_bold_mode=b'\x1b[1m', clear_screen=b'\x1b[H\x1b[J', carriage_return=b'\r', change_scroll_region=b'\x1b[%i%p1%d;%p2%dr', parm_left_cursor=b'\x1b[%p1%dD', cursor_left=b'\x08', parm_down_cursor=b'\x1b[%p1%dB', cursor_down=b'\n', parm_right_cursor=b'\x1b[%p1%dC', cursor_right=b'\x1b[C', cursor_address=b'\x1b[%i%p1%d;%p2%dH', parm_up_cursor=b'\x1b[%p1%dA', cursor_up=b'\x1b[A', enter_dim_mode=b'\x1b[2m', parm_delete_line=b'\x1b[%p1%dM', delete_line=b'\x1b[M', clr_eos=b'\x1b[J', clr_eol=b'\x1b[K', clr_bol=b'\x1b[1K', cursor_home=b'\x1b[H', tab=b'\t', set_tab=b'\x1bH', parm_insert_line=b'\x1b[%p1%dL', insert_line=b'\x1b[L', scroll_forward=b'\n', enter_secure_mode=b'\x1b[8m', key_backspace=b'', key_left=b'\x1bOD', key_down=b'\x1bOB', key_right=b'\x1bOC', key_up=b'\x1bOA', key_enter=b'\x1bOM', restore_cursor=b'\x1b8', enter_reverse_mode=b'\x1b[7m', scroll_reverse=b'\x1bM', exit_am_mode=b'\x1b[?7l', keypad_local=b'\x1b[?1l\x1b>', reset_2string=b'\x1b>\x1b[?3l\x1b[?4l\x1b[?5l\x1b[?7h\x1b[?8h', save_cursor=b'\x1b7', enter_am_mode=b'\x1b[?7h', keypad_xmit=b'\x1b[?1h\x1b=', enter_standout_mode=b'\x1b[7m', enter_underline_mode=b'\x1b[4m', clear_all_tabs=b'\x1b[3g', key_f1=b'\x1bOP', key_f2=b'\x1bOQ', key_f3=b'\x1bOR', key_f4=b'\x1bOS', key_a1=b'\x1bOq', key_a3=b'\x1bOs', key_b2=b'\x1bOr', key_c1=b'\x1bOp', key_c3=b'\x1bOn', user8=b'\x1b[?1;2c', user6=b'\x1b[%i%d;%dR', user7=b'\x1b[6n', user9=b'\x1b[c', orig_pair=b'\x1b[39;49m', max_colors=256, max_pairs=65536, set_a_background=b'\x1b[%?%p1%{8}%<%t4%p1%d%e%p1%{16}%<%t10%p1%{8}%-%d%e48;5;%p1%d%;m', set_a_foreground=b'\x1b[%?%p1%{8}%<%t3%p1%d%e%p1%{16}%<%t9%p1%{8}%-%d%e38;5;%p1%d%;m', set_background=None, set_foreground=None, width_status_line=50, has_status_line=True, dis_status_line=b'\x1b]2;\x07', from_status_line=b'\x07', to_status_line=b'\x1b]2;', TS=b'\x1b]2;', can_change=None, initialize_color=None, exit_italics_mode=b'\x1b[23m', enter_italics_mode=b'\x1b[3m', XM=b'\x1b[?1006;1000%?%p1%{1}%=%th%el%;', xm=b'\x1b[<%i%p3%d;%p1%d;%p2%d;%?%p4%tM%em%;')
