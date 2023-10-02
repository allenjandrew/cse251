"""
Course: CSE 251 
Lesson: L04 Team Activity
File:   team.py
Author: <Add name here>

Purpose: Practice concepts of Queues, Locks, and Semaphores.

Instructions:

- Review instructions in Canvas.

Question:

- Is the Python Queue thread safe? (https://en.wikipedia.org/wiki/Thread_safety)
"""

import threading
import queue
import requests
import json

# Include cse 251 common Python files
from cse251 import *

RETRIEVE_THREADS = 4        # Number of retrieve_threads
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue

def retrieve_thread(shopper, log):  # TODO add arguments
    """ Process values from the data_queue """

    while True:
        # TODO check to see if anything is in the queue
        # if shopper.empty():
        #     print('awkward')
        #     continue

        # TODO process the value retrieved from the queue
        url = shopper.get()
        if url == 'finished':
            break

        # TODO make Internet call to get characters name and log it
        response = requests.get(url)
        if response.status_code == 200: # if this is a valid response:
            data = response.json()
            log.write(data["name"])


def file_reader(shopper, log): # TODO add arguments
    """ This thread reading the data file and places the values in the data_queue """

    # TODO Open the data file "urls.txt" and place items into a queue
    with open('urls.txt') as file:
        for line in file:
            shopper.put(line.strip())

    log.write('finished reading file')

    # TODO signal the retrieve threads one more time that there are "no more values"
    for _ in range(RETRIEVE_THREADS):
        shopper.put('finished')


def main():
    """ Main function """

    log = Log(show_terminal=True)

    # TODO create queue
    shopper = queue.Queue()

    # TODO create semaphore (if needed)

    # TODO create the threads. 1 filereader() and RETRIEVE_THREADS retrieve_thread()s
    # Pass any arguments to these thread need to do their job
    threads = []

    for _ in range(RETRIEVE_THREADS):
        threads.append(threading.Thread(target=retrieve_thread, args=(shopper,log,)))
    threads.append(threading.Thread(target=file_reader, args=(shopper,log,)))

    log.start_timer()

    # TODO Get them going - start the retrieve_threads first, then file_reader
    for t in threads: t.start()

    # TODO Wait for them to finish - The order doesn't matter
    for t in threads: t.join()

    log.stop_timer('Time to process all URLS')


if __name__ == '__main__':
    main()