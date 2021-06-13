# Imports
from terminfo import TerminalModule

# Terminal: VT 100/ANSI X3.64 virtual terminal with bce
TerminalModule(['screen_256color_bce'], use=['screen_256color'], back_color_erase=True, erase_chars=None)
