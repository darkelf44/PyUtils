# Imports
from terminfo import TerminalModule

# Terminal: 80-column dumb tty
TerminalModule(['dumb'], use=[], auto_right_margin=True, columns=80, bell=b'\x07', carriage_return=b'\r', cursor_down=b'\n', scroll_forward=b'\n')
