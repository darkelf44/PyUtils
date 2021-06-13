# Imports
from terminfo import TerminalModule

# Terminal: NetBSD wscons in 25 line DEC VT220 mode with Meta
TerminalModule(['wsvt25m'], use=['wsvt25'], has_meta_key=True)
