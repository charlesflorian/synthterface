import curses
import os

ROOT_SYNTH_DIR = "synths"

DIR_COLOR = 1


def write_text(stdscr, x, y, text, attr=None):
    if attr is not None:
        stdscr.addstr(x, y, text, attr)
    else:
        stdscr.addstr(x, y, text)


def get_synths(curdir="synths"):
    dirs = os.listdir(curdir)

    out = []
    for d in dirs:
        path = f"{curdir}/{d}"
        if os.path.isdir(path):
            out.append([(True, d, path)])
        else:
            out.append([(False, d, path)])

    return out


def init_colors():
    curses.init_pair(DIR_COLOR, curses.COLOR_BLUE, curses.COLOR_BLACK)


def main(stdscr):
    stdscr.clear()
    init_colors()

    row = 1

    write_text(stdscr, 0, 0, "Press 'q' to quit")

    for ix, dirname in enumerate(os.listdir(ROOT_SYNTH_DIR)):
        if os.path.isdir(f"{ROOT_SYNTH_DIR}/{dirname}"):
            write_text(stdscr, ix + 1, 2, dirname, curses.color_pair(DIR_COLOR))
        else:
            write_text(stdscr, ix + 1, 2, dirname)

    stdscr.move(row, 0)

    stdscr.refresh()

    keep_going = True
    while keep_going:
        c = stdscr.getch()
        if c == ord("q"):
            keep_going = False
        elif c == ord("w"):
            row = row - 1 if row > 1 else 1
        elif c == ord("s"):
            row = row + 1 if row < 4 else 4
        stdscr.move(row, 0)


curses.wrapper(main)
