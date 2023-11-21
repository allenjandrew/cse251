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
  (ie., BUFFER_SIZE memory positions)

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
  1) BUFFER_SIZE number of positions for data transfer. This buffer area must
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

BUFFER_SIZE = 10
READERS = 2
WRITERS = 2

NEXT_VAL_INDEX = BUFFER_SIZE
WRITE_POS_INDEX = BUFFER_SIZE + 1
READ_POS_INDEX = BUFFER_SIZE + 2
RESULT_INDEX = BUFFER_SIZE + 3
STOP_VAL = -1


def read(gand, sema_4_read, sema_4_write, shared_list):
    stop = False
    while not stop:
        sema_4_read.acquire()
        gand.acquire()
        next_ind = shared_list[READ_POS_INDEX]
        next_val = shared_list[next_ind]
        if next_val == STOP_VAL:
            stop = True
        else:
            shared_list[RESULT_INDEX] = next_val
            print(next_val, end=", ", flush=True)
            shared_list[READ_POS_INDEX] = (
                shared_list[READ_POS_INDEX] + 1
            ) % BUFFER_SIZE
        gand.release()
        sema_4_write.release()


def write(end_value, gand, sema_4_read, sema_4_write, shared_list):
    stop = False
    while not stop:
        sema_4_write.acquire()
        gand.acquire()
        if shared_list[NEXT_VAL_INDEX] > end_value:
            next_val = STOP_VAL
        else:
            next_val = shared_list[NEXT_VAL_INDEX]
        next_ind = shared_list[WRITE_POS_INDEX]
        shared_list[next_ind] = next_val
        if next_val == STOP_VAL:
            stop = True
        else:
            shared_list[NEXT_VAL_INDEX] += 1
            shared_list[WRITE_POS_INDEX] = (
                shared_list[WRITE_POS_INDEX] + 1
            ) % BUFFER_SIZE
        gand.release()
        sema_4_read.release()


def main():
    # This is the number of values that the writer will send to the reader
    items_to_send = random.randint(1000, 10000)

    smm = SharedMemoryManager()
    smm.start()

    # TODO - Create a ShareableList to be used between the processes
    #      - The buffer should be size 10 PLUS at least three other
    #        values (ie., [0] * (BUFFER_SIZE + 3)).  The extra values
    #        are used for the head and tail for the circular buffer.
    #        The another value is the current number that the writers
    #        need to send over the buffer.  This last value is shared
    #        between the writers.
    #        You can add another value to the sharedable list to keep
    #        track of the number of values received by the readers.
    #        (ie., [0] * (BUFFER_SIZE + 4))
    shared_list = smm.ShareableList([0] * (BUFFER_SIZE + 4))

    # TODO - Create any lock(s) or semaphore(s) that you feel you need
    gand = mp.Lock()
    sema_4_read = mp.Semaphore(0)
    sema_4_write = mp.Semaphore()

    # TODO - create reader and writer processes
    readers = []
    for _ in range(READERS):
        readers.append(
            mp.Process(target=read, args=(gand, sema_4_read, sema_4_write, shared_list))
        )

    writers = []
    for _ in range(WRITERS):
        writers.append(
            mp.Process(
                target=write,
                args=(items_to_send, gand, sema_4_read, sema_4_write, shared_list),
            )
        )

    # TODO - Start the processes and wait for them to finish
    for reader in readers:
        reader.start()
    for writer in writers:
        writer.start()
    for reader in readers:
        reader.join()
    for writer in writers:
        writer.join()

    print(f"\n{items_to_send} values sent")

    # TODO - Display the number of numbers/items received by the reader.
    #        Can not use "items_to_send", must be a value collected
    #        by the reader processes.
    print(f"{shared_list[RESULT_INDEX]} values received")

    smm.shutdown()


if __name__ == "__main__":
    main()
