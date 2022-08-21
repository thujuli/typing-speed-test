import curses
from curses import wrapper
import time
import random
from essential_generators import DocumentGenerator


def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Wellcome to the Speed Typing Test!")
    stdscr.addstr(1, 0, "(1) Press any key to Start Game!")
    stdscr.addstr(2, 0, "(2) Press ESC to Start Game!")
    stdscr.addstr(3, 0, "")
    stdscr.refresh()
    key = stdscr.getkey()
    if ord(key) == 27:
        exit()


def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)


def load_text():
    return DocumentGenerator().sentence()


def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.erase()
        display_text(stdscr, target_text, current_text, wpm)

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(
            2,
            0,
            "You completed the text! Press ESC to Close and Press any key to continue...",
        )
        key = stdscr.getkey()

        if ord(key) == 27:
            break


wrapper(main)
