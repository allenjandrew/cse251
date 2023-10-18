"""
Course: CSE 251 
Lesson: L06 Team Activity
File:   team.py
Author: <Add name here>

Purpose: Team Activity

Instructions:

- Implement the process functions to copy a text file exactly using a pipe
- After you can copy a text file word by word exactly, change the program (any way you want) to be
  faster (still using the processes).
"""

import multiprocessing as mp
from multiprocessing import Value, Process
import filecmp

# Include cse 251 common Python files
from cse251 import *

END_MESSAGE = "This is the end; there is no more."


def sender(mario, filename):  # Parent
    """function to send messages to other end of pipe"""
    """
    open the file
    send all contents of the file over a pipe to the other process
    Note: you must break each line in the file into words and
          send those words through the pipe
    """

    with open(filename) as f:
        for line in f:
            words = line.split(" ")

            mario.send(words[0])
            for i in range(1, len(words)):
                mario.send(" ")
                mario.send(words[i])

    mario.send(END_MESSAGE)
    mario.close()


def receiver(luigi, pipe_counter, filename):  # Child
    """function to print the messages received from other end of pipe"""
    """ 
    open the file for writing
    receive all content through the shared pipe and write to the file
    Keep track of the number of items sent over the pipe
    """

    with open(filename, "w") as f:
        while True:
            word = luigi.recv()

            if word == END_MESSAGE:
                break

            f.write(word)
            pipe_counter.value += 1


def are_files_same(filename1, filename2):
    """Return True if two files are the same"""
    return filecmp.cmp(filename1, filename2, shallow=False)


def copy_file(log, filename1, filename2):
    # TODO create a pipe
    mario, luigi = mp.Pipe()

    # TODO create variable to count items sent over the pipe
    pipe_counter = mp.Value("i", 0)

    # TODO create processes
    sender_p = mp.Process(target=sender, args=(mario, filename1))
    receiver_p = mp.Process(target=receiver, args=(luigi, pipe_counter, filename2))

    log.start_timer()
    start_time = log.get_time()

    # TODO start processes
    sender_p.start()
    receiver_p.start()

    # TODO wait for processes to finish
    sender_p.join()
    receiver_p.join()

    stop_time = log.get_time()

    log.stop_timer(f"Total time to transfer content = {pipe_counter.value}: ")
    log.write(f"items / second = {pipe_counter.value / (stop_time - start_time)}")

    if are_files_same(filename1, filename2):
        log.write(f"{filename1} - Files are the same")
    else:
        log.write(f"{filename1} - Files are different")


if __name__ == "__main__":
    log = Log(show_terminal=True)

    copy_file(log, "gettysburg.txt", "gettysburg-copy.txt")

    # After you get the gettysburg.txt file working, uncomment this statement
    copy_file(log, "bom.txt", "bom-copy.txt")
