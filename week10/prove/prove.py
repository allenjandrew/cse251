"""
Course: CSE 251
Lesson Week: 10
File: assignment.py
Author: <your name>

Purpose: assignment for week 10 - reader writer problem

Instructions:

- Review TODO comments

- writer: a process that will send numbers to the reader.  
  The values sent to the readers will be in consecutive order starting
  at value 1.  Each writer will use all of the sharedList buffer area
  (ie., BUFF_SIZE memory positions)

- reader: a process that receive numbers sent by the writer.  The reader will
  accept values until indicated by the writer that there are no more values to
  process.  

- Do not use try...except statements

- Display the numbers received by the reader printing them to the console.

- Create WRITERS writer processes

- Create READERS reader processes

- You can use sleep() statements for any process.

- You are able (should) to use lock(s) and semaphores(s).  When using locks, you can't
  use the arguments "block=False" or "timeout".  Your goal is to make your
  program as parallel as you can.  Over use of lock(s), or lock(s) in the wrong
  place will slow down your code.

- You must use ShareableList between the two processes.  This shareable list
  will contain different "sections".  There can only be one shareable list used
  between your processes.
  1) BUFF_SIZE number of positions for data transfer. This buffer area must
     act like a queue - First In First Out.
  2) current value used by writers for consecutive order of values to send
  3) Any indexes that the processes need to keep track of the data queue
  4) Any other values you need for the assignment

- Not allowed to use Queue(), Pipe(), List(), Barrier() or any other data structure.

- Not allowed to use Value() or Array() or any other shared data type from 
  the multiprocessing package.

- When each reader reads a value from the sharedList, use the following code to display
  the value:
  
                    print(<variable>, end=', ', flush=True)

Add any comments for me:

"""

import random
from multiprocessing.managers import SharedMemoryManager
import multiprocessing as mp

BUFF_SIZE = 10
READERS = 1
WRITERS = 1

MAX_NUM = -1
CURR_NUM = -2  # doubles as head index. head = CURR_NUM % BUFF_SIZE
TOT_READ = -3  # doubles as tail index. tail = TOT_READ % BUFF_SIZE
FLAGGER = -1


def read(shared_list, sema_4_reader, sema_4_writer, gand):
    stop = False
    while not stop:
        sema_4_reader.acquire()
        gand.acquire()
        num = shared_list[shared_list[TOT_READ] % BUFF_SIZE]
        if num == FLAGGER:
            stop = True
        else:
            print(num, end=", ", flush=True)
            shared_list[TOT_READ] += 1
        sema_4_writer.release()
        gand.release()


def write(shared_list, sema_4_reader, sema_4_writer, gand):
    stop = False
    while not stop:
        sema_4_writer.acquire()
        gand.acquire()
        num = shared_list[CURR_NUM] + 1
        if num > shared_list[MAX_NUM]:
            stop = True
            shared_list[
                shared_list[CURR_NUM] % BUFF_SIZE
            ] = FLAGGER  # Flag has to be an integer? Why? I first had it set to a string and it wasn't working
        else:
            shared_list[shared_list[CURR_NUM] % BUFF_SIZE] = num
            shared_list[CURR_NUM] += 1
        sema_4_reader.release()
        gand.release()


def main():
    # This is the number of values that the writer will send to the reader
    items_to_send = random.randint(1000, 10000)
    # print(items_to_send)

    smm = SharedMemoryManager()
    smm.start()

    # TODO - Create a ShareableList to be used between the processes
    #      - The buffer should be size 10 PLUS at least three other
    #        values (ie., [0] * (BUFF_SIZE + 3)).  The extra values
    #        are used for the WRITE and READ for the circular buffer.
    #        The another value is the current number that the writers
    #        need to send over the buffer.  This last value is shared
    #        between the writers.
    #        You can add another value to the sharedable list to keep
    #        track of the number of values received by the readers.
    #        (ie., [0] * (BUFF_SIZE + 4))
    shared_list = smm.ShareableList([0] * (BUFF_SIZE + 3))
    shared_list[MAX_NUM] = items_to_send

    # TODO - Create any lock(s) or semaphore(s) that you feel you need
    # I originally tried to put these inside shared_list, but the system
    # freaked out because of their type (they're not ints, I guess?)
    # Maybe this explains why FLAGGER also has to be an int
    sema_4_reader = mp.Semaphore(0)
    sema_4_writer = mp.Semaphore()
    gand = mp.Lock()

    # TODO - create reader and writer processes
    readers = [
        mp.Process(target=read, args=(shared_list, sema_4_reader, sema_4_writer, gand))
        for _ in range(READERS)
    ]

    writers = [
        mp.Process(target=write, args=(shared_list, sema_4_reader, sema_4_writer, gand))
        for _ in range(WRITERS)
    ]

    # TODO - Start the processes and wait for them to finish
    for reader in readers:
        reader.start()
    for writer in writers:
        writer.start()
    for reader in readers:
        reader.join()
    for writer in writers:
        writer.join()

    print("\b\b ")  # Just to get rid of the last comma
    print(f"{items_to_send} values sent")

    # TODO - Display the number of numbers/items received by the reader.
    #        Cannot use "items_to_send", must be a value collected
    #        by the reader processes.
    print(f"{shared_list[TOT_READ]} values received")

    smm.shutdown()


if __name__ == "__main__":
    main()
