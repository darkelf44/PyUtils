# Imports
from terminfo import TerminalModule

# Terminal: GNU Mach
TerminalModule(['mach_gnu'], use=['mach'], acs_chars=b'+>,<-^.v0\xdb`+a\xb1f\xf8g\xf1h\xb0i#j\xd9k\xbfl\xdam\xc0n\xc5o~p\xc4q\xc4r\xc4s_t\xc3u\xb4v\xc1w\xc2x\xb3y\xf3z\xf2{\xe3|\xd8}\x9c~\xfe', parm_dch=b'\x1b[%p1%dP', delete_character=b'\x1b[P', enter_dim_mode=b'\x1b[2m', erase_chars=b'\x1b[%p1%dX', clr_bol=b'\x1b[1K', column_address=b'\x1b[%i%p1%dG', parm_ich=b'\x1b[%p1%d@', insert_character=b'\x1b[@', enter_secure_mode=b'\x1b[8m', newline=b'\x1bE', set_attributes=b'\x1b[0%?%p1%t;7%;%?%p2%t;4%;%?%p3%t;7%;%?%p4%t;5%;%?%p5%t;2%;%?%p6%t;1%;%?%p7%t;8%;m', parm_index=b'\x1b[%p1%dS', parm_rindex=b'\x1b[%p1%dT')
