"""
Course: CSE 251
Lesson Week: 06
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- Implement the process functions to copy a text file exactly using a pipe

- After you can copy a text file word by word exactly,
  Change the program (any way you want) to be faster 
  (Still using the processes)

"""

import multiprocessing as mp
from multiprocessing import Value, Process
import filecmp

# Include cse 251 common Python files
from cse251 import *

stop = "None"


def sender(parent, filename1):
    """function to send messages to other end of pipe"""
    """
    open the file
    send all contents of the file over a pipe to the other process
    Note: you must break each line in the file into words and
          send those words through the pipe
    """
    with open(filename1) as file:
        for line in file:
            # line = line.strip()
            words = line.split(" ")

            parent.send(words[0])

            for i in range(1, len(words)):
                parent.send(" ")

                parent.send(words[i])

    parent.send(stop)
    parent.close()


def receiver(child, count, filename2):
    """function to print the messages received from other end of pipe"""
    """ 
    open the file for writing
    receive all content through the shared pipe and write to the file
    Keep track of the number of items sent over the pipe
    """
    with open(filename2, "w") as file:
        while True:
            kid = child.recv()
            if kid == stop:
                break

            file.write(kid)
            count.value += 1


def are_files_same(filename1, filename2):
    """Return True if two files are the same"""
    # cow1 = open(filename1, "r")
    # print(cow1.read())
    # cow2 = open(filename2, "r")
    # print(cow2.read())
    return filecmp.cmp(filename1, filename2, shallow=False)


def copy_file(log, filename1, filename2):
    # TODO create a pipe

    parent, child = mp.Pipe()

    # TODO create variable to count items sent over the pipe

    count = mp.Value("i", 0)

    # TODO create processes

    process_1 = mp.Process(target=sender, args=(parent, filename1))
    process_2 = mp.Process(target=receiver, args=(child, count, filename2))

    log.start_timer()
    start_time = log.get_time()

    # TODO start processes

    process_1.start()
    process_2.start()

    # TODO wait for processes to finish

    process_1.join()
    process_2.join()

    stop_time = log.get_time()

    log.stop_timer(f"Total time to transfer content = {count.value} : ")
    log.write(f"items / second = {count.value / (stop_time - start_time)}")

    if are_files_same(filename1, filename2):
        log.write(f"{filename1} - Files are the same")
    else:
        log.write(f"{filename1} - Files are different")


if __name__ == "__main__":
    log = Log(show_terminal=True)

    copy_file(log, "gettysburg.txt", "gettysburg-copy.txt")

    # After you get the gettysburg.txt file working, uncomment this statement
    # copy_file(log, 'bom.txt', 'bom-copy.txt')
