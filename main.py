import curses # console library
import curses.ascii # ascii classification
from interface import Screen
from curses import wrapper
from editor import get_text
from tree import TreeList

from interface import iswide_char, nchars_to_chars

def main(stdscr):
    screen = Screen() # object representing console/windows
    tl = TreeList() # object representing lists of parsed statements

    while True:
        c = stdscr.getkey()
        if c == '\t': # TAB = switch window focus (and associated pad)
            screen.switch_window()
            tl.switch_list()
        elif c == 'q': # q = quit
            break
        elif c == 'e': # e = edit
            line = tl.focus.line
            data = '' if line == tl.focus.len() else repr(tl.focus.data[line])
            tree = get_text(screen, data) # parse text from user
            tl.focus[line] = tree # insert tree in treelist
            screen.focus[line] = str(tree) # insert unicode string into pad
            screen.focus.refresh()
        elif c == 'KEY_RIGHT':
            pad = screen.focus
            line = pad.scroll_line + pad.cursor_line
            string = pad.pad[line]
            i = pad.scroll_char + nchars_to_chars(string, \
                pad.scroll_char, pad.cursor_char) # current pos. within string
            if i < len(string): # check we are not at end of string
                screen.focus.cursor_right(iswide_char(string[i]))
                screen.focus.refresh()
        elif c == 'KEY_LEFT':
            pad = screen.focus
            line = pad.scroll_line + pad.cursor_line
            string = pad.pad[line]
            i = pad.scroll_char + nchars_to_chars(string, \
                pad.scroll_char, pad.cursor_char) # current pos. within string
            if i > 0: # check we are not at end of string
                string = pad.pad[line]
                screen.focus.cursor_left(iswide_char(string[i - 1]))
                screen.focus.refresh()
        elif c == 'KEY_DOWN':
            pad = screen.focus
            if pad != screen.pad0 and tl.focus.line != tl.focus.len():
                pad.cursor_down()
                pad.refresh()
                tl.focus.line += 1
        elif c == 'KEY_UP':
            pad = screen.focus
            if pad != screen.pad0 and tl.focus.line != 0:
                pad.cursor_up()
                pad.refresh()
                tl.focus.line -= 1

    screen.exit()

wrapper(main) # curses wrapper handles exceptions
