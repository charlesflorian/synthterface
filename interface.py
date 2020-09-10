import curses
import argparse
import os
import sys
import shutil

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
        write_text(stdscr, ix, 2, short_path, attr)


def init_colors():
    curses.init_pair(DIR_COLOR, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(FILE_COLOR, curses.COLOR_WHITE, curses.COLOR_BLACK)


def launch_vcv(vcvpath, filename):
    autosave_path = f"{vcvpath}/autosave-v1.vcv"
    if os.path.isfile(autosave_path):
        shutil.move(autosave_path, autosave_path + ".old")

    shutil.copy(filename, autosave_path)

    os.system(f"open {vcvpath}/Rack.app")


def main(stdscr, vcvpath):
    stdscr.clear()
    init_colors()

    dbox = stdscr.derwin(10, 60, 1, 0)
    dbox.border()

    display = dbox.derwin(8, 58, 1, 1)

    row = 0

    write_text(stdscr, 0, 0, "Press 'q' to quit")

    dirs = [ROOT_SYNTH_DIR]

    dir_contents = get_synths(dirs[-1])

    keep_going = True
    while keep_going:
        show_synths(display, dir_contents)
        stdscr.refresh()
        display.move(row, 0)

        max_rows = len(dir_contents)

        c = display.getch()
        if c == ord("q"):
            keep_going = False
        elif c == ord("w"):
            row = row - 1 if row > 0 else 0
        elif c == ord("s"):
            row = row + 1 if row < max_rows - 1 else max_rows - 1
        elif c == ord("d"):
            isdir, _, path = dir_contents[row]
            if isdir:
                display.clear()
                dirs.append(path)
                dir_contents = get_synths(dirs[-1])
                row = 0
            elif path.endswith(".vcv"):
                launch_vcv(vcvpath, path)
        elif c == ord("a"):
            if len(dirs) > 1:
                display.clear()
                dirs.pop()
                dir_contents = get_synths(dirs[-1])
                row = 0


parser = argparse.ArgumentParser()
parser.add_argument("vcvlocation")

args = parser.parse_args(sys.argv[1:])

if not args.vcvlocation.endswith(".App"):
    pass

curses.wrapper(main, args.vcvlocation)
