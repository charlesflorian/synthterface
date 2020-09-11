import curses
import argparse
import os
import sys
import shutil

ROOT_SYNTH_DIR = "synths"

DIR_COLOR = 1
FILE_COLOR = 2

DISP_WIDTH = 16
DISP_HEIGHT = 5


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


def load_patches(curdir="synths"):
    directory = {}
    dirs = os.listdir(curdir)

    for d in dirs:
        path = f"{curdir}/{d}"
        if os.path.isdir(path):
            directory[d] = list(filter(lambda x: x.endswith(".vcv"), os.listdir(path)))

    return list(directory.keys()), directory


def show_synths(scr, patches, cur_synth):
    scr.clear()
    if cur_synth and cur_synth in patches.keys():
        for ix, synthname in enumerate(patches[cur_synth]):
            attr = curses.color_pair(FILE_COLOR)
            write_text(scr, ix, 1, synthname, attr)
    else:
        for ix, dirname in enumerate(patches.keys()):
            attr = curses.color_pair(DIR_COLOR)
            write_text(scr, ix, 1, dirname, attr)


def init_colors():
    curses.init_pair(DIR_COLOR, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(FILE_COLOR, curses.COLOR_WHITE, curses.COLOR_BLACK)


def launch_vcv(vcvpath, filename):
    autosave_path = f"{vcvpath}/autosave-v1.vcv"
    if os.path.isfile(autosave_path):
        shutil.move(autosave_path, autosave_path + ".old")

    shutil.copy(filename, autosave_path)

    os.system(f"open {vcvpath}/Rack.app")


def draw_disp(stdscr):
    stdscr.clear()

    dbox = stdscr.derwin(DISP_HEIGHT + 2, DISP_WIDTH + 2, 1, 0)
    dbox.border()

    display = dbox.derwin(DISP_HEIGHT, DISP_WIDTH, 1, 1)

    return display


def main(stdscr, vcvpath):
    stdscr.clear()
    init_colors()

    display = draw_disp(stdscr)

    write_text(stdscr, 0, 0, "Press 'q' to quit")

    synths, patches = load_patches(ROOT_SYNTH_DIR)
    row = 0

    cur_synth = None

    keep_going = True
    while keep_going:
        show_synths(display, patches, cur_synth)
        stdscr.refresh()
        display.move(row, 0)

        if cur_synth:
            max_rows = len(patches[cur_synth])
        else:
            max_rows = len(patches.keys())

        c = display.getch()
        if c == ord("q"):
            keep_going = False
        elif c == ord("w"):
            row = row - 1 if row > 0 else 0
        elif c == ord("s"):
            row = row + 1 if row < max_rows - 1 else max_rows - 1
        elif c == ord("d"):
            cur_synth = synths[row]
            row = 0
        elif c == ord("a"):
            row = synths.index(cur_synth)
            cur_synth = None


parser = argparse.ArgumentParser()
parser.add_argument("vcvlocation")

args = parser.parse_args(sys.argv[1:])

if not os.path.isdir(f"{args.vcvlocation}/Rack.app"):
    print("This is not the correct location for VCV rack!")
    sys.exit(1)

curses.wrapper(main, args.vcvlocation)
