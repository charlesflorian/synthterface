import curses
import os

ROOT_SYNTH_DIR = "synths"

DIR_COLOR = 1
FILE_COLOR = 2


def write_text(stdscr, row, col, text, attr=None):
    if attr is not None:
        stdscr.addstr(row, col, text, attr)
    else:
        stdscr.addstr(row, col, text)


def get_synths(curdir="synths"):
    dirs = os.listdir(curdir)

    out = []
    for d in dirs:
        path = f"{curdir}/{d}"
        if os.path.isdir(path):
            out.append((True, d, path))
        else:
            out.append((False, d, path))

    return out


def show_synths(stdscr, dir_contents):
    for ix, (isdir, short_path, _) in enumerate(dir_contents):
        attr = curses.color_pair(DIR_COLOR) if isdir else curses.color_pair(FILE_COLOR)
        write_text(stdscr, ix + 1, 2, short_path, attr)


def init_colors():
    curses.init_pair(DIR_COLOR, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(FILE_COLOR, curses.COLOR_WHITE, curses.COLOR_BLACK)


def main(stdscr):
    stdscr.clear()
    init_colors()

    row = 1

    write_text(stdscr, 0, 0, "Press 'q' to quit")

    dirs = [ROOT_SYNTH_DIR]

    dir_contents = get_synths(dirs[-1])

    keep_going = True
    while keep_going:
        show_synths(stdscr, dir_contents)
        stdscr.move(row, 0)

        max_rows = len(dir_contents)

        c = stdscr.getch()
        if c == ord("q"):
            keep_going = False
        elif c == ord("w"):
            row = row - 1 if row > 1 else 1
        elif c == ord("s"):
            row = row + 1 if row < max_rows else max_rows
        elif c == ord("d"):
            isdir, _, path = dir_contents[row - 1]
            if isdir:
                dirs.append(path)
                dir_contents = get_synths(dirs[-1])
                row = 1
        elif c == ord("a"):
            if len(dirs) > 1:
                dirs.pop()
                dir_contents = get_synths(dirs[-1])
                row = 1
        stdscr.move(row, 0)


curses.wrapper(main)
