# Imports
from terminfo import TerminalModule

# Terminal: xterm terminal emulator (X Window System)
TerminalModule(['xterm'], use=[], no_pad_char=True, key_btab=b'\x1b[Z', key_enter=b'\x1bOM', newline=b'\x1bE', backspaces_with_bs=True, auto_right_margin=True, back_color_erase=True, move_insert_mode=True, move_standout_mode=True, eat_newline_glitch=True, AX=True, XT=True, max_colors=8, columns=80, init_tabs=8, lines=24, max_pairs=64, acs_chars=b'``aaffggiijjkkllmmnnooppqqrrssttuuvvwwxxyyzz{{||}}~~', bell=b'\x07', enter_blink_mode=b'\x1b[5m', enter_bold_mode=b'\x1b[1m', back_tab=b'\x1b[Z', clear_screen=b'\x1b[H\x1b[2J', carriage_return=b'\r', change_scroll_region=b'\x1b[%i%p1%d;%p2%dr', parm_left_cursor=b'\x1b[%p1%dD', cursor_left=b'\x08', parm_down_cursor=b'\x1b[%p1%dB', cursor_down=b'\n', parm_right_cursor=b'\x1b[%p1%dC', cursor_right=b'\x1b[C', cursor_address=b'\x1b[%i%p1%d;%p2%dH', parm_up_cursor=b'\x1b[%p1%dA', cursor_up=b'\x1b[A', parm_dch=b'\x1b[%p1%dP', delete_character=b'\x1b[P', enter_dim_mode=b'\x1b[2m', parm_delete_line=b'\x1b[%p1%dM', delete_line=b'\x1b[M', erase_chars=b'\x1b[%p1%dX', clr_eos=b'\x1b[J', clr_eol=b'\x1b[K', clr_bol=b'\x1b[1K', flash_screen=b'\x1b[?5h$<100/>\x1b[?5l', cursor_home=b'\x1b[H', column_address=b'\x1b[%i%p1%dG', tab=b'\t', set_tab=b'\x1bH', parm_ich=b'\x1b[%p1%d@', parm_insert_line=b'\x1b[%p1%dL', insert_line=b'\x1b[L', scroll_forward=b'\n', enter_secure_mode=b'\x1b[8m', init_2string=b'\x1b[!p\x1b[?3;4l\x1b[4l\x1b>', key_mouse=b'\x1b[<', memory_lock=b'\x1bl', memory_unlock=b'\x1bm', orig_pair=b'\x1b[39;49m', restore_cursor=b'\x1b8', enter_reverse_mode=b'\x1b[7m', scroll_reverse=b'\x1bM', exit_alt_charset_mode=b'\x1b(B', exit_am_mode=b'\x1b[?7l', exit_insert_mode=b'\x1b[4l', keypad_local=b'\x1b[?1l\x1b>', exit_standout_mode=b'\x1b[27m', exit_underline_mode=b'\x1b[24m', reset_1string=b'\x1bc', reset_2string=b'\x1b[!p\x1b[?3;4l\x1b[4l\x1b>', save_cursor=b'\x1b7', set_a_background=b'\x1b[4%p1%dm', set_a_foreground=b'\x1b[3%p1%dm', set_background=b'\x1b[4%?%p1%{1}%=%t4%e%p1%{3}%=%t6%e%p1%{4}%=%t1%e%p1%{6}%=%t3%e%p1%d%;m', set_foreground=b'\x1b[3%?%p1%{1}%=%t4%e%p1%{3}%=%t6%e%p1%{4}%=%t1%e%p1%{6}%=%t3%e%p1%d%;m', set_attributes=b'%?%p9%t\x1b(0%e\x1b(B%;\x1b[0%?%p6%t;1%;%?%p5%t;2%;%?%p2%t;4%;%?%p1%p3%|%t;7%;%?%p4%t;5%;%?%p7%t;8%;m', exit_attribute_mode=b'\x1b(B\x1b[m', enter_alt_charset_mode=b'\x1b(0', enter_am_mode=b'\x1b[?7h', enter_insert_mode=b'\x1b[4h', keypad_xmit=b'\x1b[?1h\x1b=', enter_standout_mode=b'\x1b[7m', enter_underline_mode=b'\x1b[4m', clear_all_tabs=b'\x1b[3g', row_address=b'\x1b[%i%p1%dd', erase_saved_lines=b'\x1b[3J', has_meta_key=True, meta_off=b'\x1b[?1034l', meta_on=b'\x1b[?1034h', cursor_invisible=b'\x1b[?25l', cursor_normal=b'\x1b[?12l\x1b[?25h', cursor_visible=b'\x1b[?12;25h', user6=b'\x1b[%i%d;%dR', user7=b'\x1b[6n', user8=b'\x1b[?%[;0123456789]c', user9=b'\x1b[c', exit_ca_mode=b'\x1b[?1049l\x1b[23;0;0t', enter_ca_mode=b'\x1b[?1049h\x1b[22;0;0t', key_backspace=b'\x08', prtr_silent=True, print_screen=b'\x1b[i', prtr_off=b'\x1b[4i', prtr_on=b'\x1b[5i', kp5=b'\x1bOE', key_padd=b'\x1bOk', key_pcma=b'\x1bOl', key_pdiv=b'\x1bOo', key_pdot=b'\x1bOn', key_pmul=b'\x1bOj', key_psub=b'\x1bOm', key_pzero=b'\x1bOp', key_a1=b'\x1bOw', key_a3=b'\x1bOy', key_b2=b'\x1bOu', key_c1=b'\x1bOq', key_c3=b'\x1bOs', key_f1=b'\x1bOP', key_f2=b'\x1bOQ', key_f3=b'\x1bOR', key_f4=b'\x1bOS', key_a2=b'\x1bOx', key_b1=b'\x1bOt', key_b3=b'\x1bOv', key_c2=b'\x1bOr', exit_italics_mode=b'\x1b[23m', enter_italics_mode=b'\x1b[3m', Cr=b'\x1b]112\x07', Cs=b'\x1b]12;%p1%s\x07', Ms=b'\x1b]52;%p1%s;%p2%s\x07', Se=b'\x1b[2 q', Ss=b'\x1b[%p1%d q', XM=b'\x1b[?1006;1000%?%p1%{1}%=%th%el%;', xm=b'\x1b[<%i%p3%d;%p1%d;%p2%d;%?%p4%tM%em%;', clear_margins=b'\x1b[?69l', set_lr_margin=b'\x1b[?69h\x1b[%i%p1%d;%p2%ds', exit_strikeout_mode=b'\x1b[29m', enter_strikeout_mode=b'\x1b[9m', repeat_char=b'%p1%c\x1b[%p2%{1}%-%db', parm_index=b'\x1b[%p1%dS', parm_rindex=b'\x1b[%p1%dT', key_sdc=b'\x1b[3;2~', key_send=b'\x1b[1;2F', key_shome=b'\x1b[1;2H', key_sic=b'\x1b[2;2~', key_snext=b'\x1b[6;2~', key_sprevious=b'\x1b[5;2~', key_ic=b'\x1b[2~', key_npage=b'\x1b[6~', key_ppage=b'\x1b[5~', key_sdc3=b'\x1b[3;3~', key_sdc4=b'\x1b[3;4~', key_sdc5=b'\x1b[3;5~', key_sdc6=b'\x1b[3;6~', key_sdc7=b'\x1b[3;7~', key_send3=b'\x1b[1;3F', key_send4=b'\x1b[1;4F', key_send5=b'\x1b[1;5F', key_send6=b'\x1b[1;6F', key_send7=b'\x1b[1;7F', key_shome3=b'\x1b[1;3H', key_shome4=b'\x1b[1;4H', key_shome5=b'\x1b[1;5H', key_shome6=b'\x1b[1;6H', key_shome7=b'\x1b[1;7H', key_sic3=b'\x1b[2;3~', key_sic4=b'\x1b[2;4~', key_sic5=b'\x1b[2;5~', key_sic6=b'\x1b[2;6~', key_sic7=b'\x1b[2;7~', key_snext3=b'\x1b[6;3~', key_snext4=b'\x1b[6;4~', key_snext5=b'\x1b[6;5~', key_snext6=b'\x1b[6;6~', key_snext7=b'\x1b[6;7~', key_sprevious3=b'\x1b[5;3~', key_sprevious4=b'\x1b[5;4~', key_sprevious5=b'\x1b[5;5~', key_sprevious6=b'\x1b[5;6~', key_sprevious7=b'\x1b[5;7~', key_dc=b'\x1b[3~', key_end=b'\x1bOF', key_home=b'\x1bOH', key_sleft=b'\x1b[1;2D', key_sright=b'\x1b[1;2C', key_sf=b'\x1b[1;2B', key_sr=b'\x1b[1;2A', key_sdown=b'\x1b[1;2B', key_sdown3=b'\x1b[1;3B', key_sdown4=b'\x1b[1;4B', key_sdown5=b'\x1b[1;5B', key_sdown6=b'\x1b[1;6B', key_sdown7=b'\x1b[1;7B', key_sleft3=b'\x1b[1;3D', key_sleft4=b'\x1b[1;4D', key_sleft5=b'\x1b[1;5D', key_sleft6=b'\x1b[1;6D', key_sleft7=b'\x1b[1;7D', key_sright3=b'\x1b[1;3C', key_sright4=b'\x1b[1;4C', key_sright5=b'\x1b[1;5C', key_sright6=b'\x1b[1;6C', key_sright7=b'\x1b[1;7C', key_sup=b'\x1b[1;2A', key_sup3=b'\x1b[1;3A', key_sup4=b'\x1b[1;4A', key_sup5=b'\x1b[1;5A', key_sup6=b'\x1b[1;6A', key_sup7=b'\x1b[1;7A', key_f10=b'\x1b[21~', key_f11=b'\x1b[23~', key_f12=b'\x1b[24~', key_f13=b'\x1b[1;2P', key_f14=b'\x1b[1;2Q', key_f15=b'\x1b[1;2R', key_f16=b'\x1b[1;2S', key_f17=b'\x1b[15;2~', key_f18=b'\x1b[17;2~', key_f19=b'\x1b[18;2~', key_f20=b'\x1b[19;2~', key_f21=b'\x1b[20;2~', key_f22=b'\x1b[21;2~', key_f23=b'\x1b[23;2~', key_f24=b'\x1b[24;2~', key_f25=b'\x1b[1;5P', key_f26=b'\x1b[1;5Q', key_f27=b'\x1b[1;5R', key_f28=b'\x1b[1;5S', key_f29=b'\x1b[15;5~', key_f30=b'\x1b[17;5~', key_f31=b'\x1b[18;5~', key_f32=b'\x1b[19;5~', key_f33=b'\x1b[20;5~', key_f34=b'\x1b[21;5~', key_f35=b'\x1b[23;5~', key_f36=b'\x1b[24;5~', key_f37=b'\x1b[1;6P', key_f38=b'\x1b[1;6Q', key_f39=b'\x1b[1;6R', key_f40=b'\x1b[1;6S', key_f41=b'\x1b[15;6~', key_f42=b'\x1b[17;6~', key_f43=b'\x1b[18;6~', key_f44=b'\x1b[19;6~', key_f45=b'\x1b[20;6~', key_f46=b'\x1b[21;6~', key_f47=b'\x1b[23;6~', key_f48=b'\x1b[24;6~', key_f49=b'\x1b[1;3P', key_f5=b'\x1b[15~', key_f50=b'\x1b[1;3Q', key_f51=b'\x1b[1;3R', key_f52=b'\x1b[1;3S', key_f53=b'\x1b[15;3~', key_f54=b'\x1b[17;3~', key_f55=b'\x1b[18;3~', key_f56=b'\x1b[19;3~', key_f57=b'\x1b[20;3~', key_f58=b'\x1b[21;3~', key_f59=b'\x1b[23;3~', key_f6=b'\x1b[17~', key_f60=b'\x1b[24;3~', key_f61=b'\x1b[1;4P', key_f62=b'\x1b[1;4Q', key_f63=b'\x1b[1;4R', key_f7=b'\x1b[18~', key_f8=b'\x1b[19~', key_f9=b'\x1b[20~', key_left=b'\x1bOD', key_down=b'\x1bOB', key_right=b'\x1bOC', key_up=b'\x1bOA')