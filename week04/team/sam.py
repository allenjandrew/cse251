import threading
import queue
import requests
import json

# Include cse 251 common Python files
from cse251 import *

# Instructions say to start with 1, don't forget to change it back to 4!!!
RETRIEVE_THREADS = 4  # Number of retrieve_threads
NO_MORE_VALUES = "No more"  # Special value to indicate no more items in the queue


def retrieve_thread(url_holder, sem, log):  # TODO add arguments
    """Process values from the data_queue"""

    while True:
        # TODO check to see if anything is in the queue

        # TODO process the value retrieved from the queue
        # sem.acquire()
        url = url_holder.get()

        if url == NO_MORE_VALUES:
            break

        # TODO make Internet call to get characters name and log it
        data = {}
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            log.write(data["name"])
        else:
            print("There was an error making the call.")


def file_reader(url_holder, sem, log):  # TODO add arguments
    """This thread reading the data file and places the values in the data_queue"""

    # TODO Open the data file "urls.txt" and place items into a queue
    urls = open("urls.txt", "r")
    for i in urls:
        url = i.strip()
        # Commenting out the print statement as I was able to confirm that my urls are being retrieved
        # print(url)
        url_holder.put(url)
        # sem.release()

    log.write("finished reading file")

    # TODO signal the retrieve threads one more time that there are "no more values"
    # Learned about this in class... you are adding the flag to tell the threads taht they are done...
    # Modeling it after the way that we started and joined the threads earlier
    for _ in range(RETRIEVE_THREADS):
        url_holder.put(NO_MORE_VALUES)
        # sem.release()


def main():
    """Main function"""

    log = Log(show_terminal=True, filename_log="url.log")

    # TODO create queue
    url_holder = queue.Queue()

    # TODO create semaphore (if needed)
    # Bro Keers said we needed a semaphore hint hint...
    sem = threading.Semaphore(RETRIEVE_THREADS)

    # TODO create the threads. 1 filereader() and RETRIEVE_THREADS retrieve_thread()s
    # Pass any arguments to these thread need to do their job
    # This is my 1 filereader thread
    filereader_thread = threading.Thread(
        target=file_reader, args=(url_holder, sem, log)
    )
    # Going to use a list comprehension (like is shown in our reading) to create the retrieve_threads
    retrieving_threads = [
        threading.Thread(target=retrieve_thread, args=(url_holder, sem, log))
        for _ in range(RETRIEVE_THREADS)
    ]

    log.start_timer()

    # TODO Get them going - start the retrieve_threads first, then file_reader
    # Once again modeled after our reading
    for thread in range(RETRIEVE_THREADS):
        retrieving_threads[thread].start()
    filereader_thread.start()

    # TODO Wait for them to finish - The order doesn't matter
    for thread in range(RETRIEVE_THREADS):
        retrieving_threads[thread].join()

    log.stop_timer("Time to process all URLS")


if __name__ == "__main__":
    main()
