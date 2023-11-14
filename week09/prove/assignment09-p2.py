"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p2.py 
Author: <Add name here>

Purpose: Part 2 of assignment 09, finding the end position in the maze

Instructions:
- Do not create classes for this assignment, just functions.
- Do not use any other Python modules other than the ones included.
- Each thread requires a different color by calling get_color().


This code is not interested in finding a path to the end position,
However, once you have completed this program, describe how you could 
change the program to display the found path to the exit position.

What would be your strategy?  

I feel the best strategy would be to use a data structure that can keep track of each thread's route.
For example, a tree that branches for each time a thread is created, or a stack that each thread carries on
its own (the problem with this one would be that we are creating so many threads, it would not be optimal
to create so many stacks). I think a tree with nodes for each position would be best. At each intersection
of the map, a new node would be added for each possible move. When the end of the maze is found, we can easily
access the branch/route from the root to the end.

Why would it work?

A tree not only keeps track of all routes, it keeps them organized by parent thread &c. It also makes sure no
extra nodes get put in between two positions of a single thread, because positions of other threads are stored
in nodes in other areas of the tree.

"""
import math
import threading
from screen import Screen
from maze import Maze
import sys
import cv2

# Include cse 251 files
from cse251 import *

SCREEN_SIZE = 700
COLOR = (0, 0, 255)
COLORS = (
    (0, 0, 255),
    (0, 255, 0),
    (255, 0, 0),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255),
    (128, 0, 0),
    (128, 128, 0),
    (0, 128, 0),
    (128, 0, 128),
    (0, 128, 128),
    (0, 0, 128),
    (72, 61, 139),
    (143, 143, 188),
    (226, 138, 43),
    (128, 114, 250),
)
SLOW_SPEED = 100
FAST_SPEED = 0

# Globals
current_color_index = 0
thread_count = 1
stop = False
speed = SLOW_SPEED


def get_color():
    """Returns a different color when called"""
    global current_color_index
    if current_color_index >= len(COLORS):
        current_color_index = 0
    color = COLORS[current_color_index]
    current_color_index += 1
    return color


def solve_find_end(maze, visited=None, pos=None, color=None):
    """finds the end position using threads.  Nothing is returned"""
    # When one of the threads finds the end position, stop all of them
    global stop
    global thread_count

    if not visited:
        pos = maze.get_start_pos()
        visited = []
        stop = False
        color = get_color()

    if pos in visited:
        return

    row, col = pos

    maze.move(row, col, color)
    visited.append(pos)

    if maze.at_end(row, col):
        stop = True

    if stop:
        return

    poss_moves = maze.get_possible_moves(row, col)
    threads = []

    if len(poss_moves) == 0:
        return

    for i in range(1, len(poss_moves)):
        if poss_moves[i] in visited:
            continue
        threads.append(
            threading.Thread(
                target=solve_find_end, args=(maze, visited, poss_moves[i], get_color())
            )
        )
        thread_count += 1

    for t in threads:
        t.start()

    solve_find_end(maze, visited, poss_moves[0], color)

    # for t in threads:
    #     t.join()


def find_end(log, filename, delay):
    """Do not change this function"""

    global thread_count
    global speed

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)

    solve_find_end(maze)

    log.write(f"Number of drawing commands = {screen.get_command_count()}")
    log.write(f"Number of threads created  = {thread_count}")

    done = False
    while not done:
        if screen.play_commands(speed):
            key = cv2.waitKey(0)
            if key == ord("1"):
                speed = SLOW_SPEED
            elif key == ord("2"):
                speed = FAST_SPEED
            elif key == ord("q"):
                exit()
            elif key != ord("p"):
                done = True
        else:
            done = True


def find_ends(log):
    """Do not change this function"""

    files = (
        ("verysmall.bmp", True),
        ("verysmall-loops.bmp", True),
        ("small.bmp", True),
        ("small-loops.bmp", True),
        ("small-odd.bmp", True),
        ("small-open.bmp", False),
        ("large.bmp", False),
        ("large-loops.bmp", False),
    )

    log.write("*" * 40)
    log.write("Part 2")
    for filename, delay in files:
        log.write()
        log.write(f"File: {filename}")
        find_end(log, filename, delay)
    log.write("*" * 40)


def main():
    """Do not change this function"""
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_ends(log)


if __name__ == "__main__":
    main()
