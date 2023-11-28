"""
Course: CSE 251
Lesson Week: 11
File: Assignment.py
"""

import time
import random
import multiprocessing as mp

# number of cleaning staff and hotel guests
CLEANING_STAFF = 2
HOTEL_GUESTS = 5

# Run program for this number of seconds
TIME = 60

STARTING_PARTY_MESSAGE = "Turning on the lights for the party vvvvvvvvvvvvvv"
STOPPING_PARTY_MESSAGE = "Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^"

STARTING_CLEANING_MESSAGE = "Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
STOPPING_CLEANING_MESSAGE = "Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"


def cleaner_waiting():
    time.sleep(random.uniform(0, 2))


def cleaner_cleaning(id):
    print(f"Cleaner: {id}")
    time.sleep(random.uniform(0, 2))


def guest_waiting():
    time.sleep(random.uniform(0, 2))


def guest_partying(id, count):
    print(f"Guest: {id}, count = {count}")
    time.sleep(random.uniform(0, 1))


def cleaner(id, start_time, view_lock, room_lock, cleaned_count, guest_count):
    """
    do the following for TIME seconds
        cleaner will wait to try to clean the room (cleaner_waiting())
        get access to the room
        display message STARTING_CLEANING_MESSAGE
        Take some time cleaning (cleaner_cleaning())
        display message STOPPING_CLEANING_MESSAGE
    """
    while time.time() < start_time + TIME:
        cleaner_waiting()

        view_lock.acquire()
        if guest_count.value != 0:
            view_lock.release()
            continue
        room_lock.acquire()

        print(STARTING_CLEANING_MESSAGE)
        cleaner_cleaning(id)
        print(STOPPING_CLEANING_MESSAGE)
        cleaned_count.value += 1

        room_lock.release()
        view_lock.release()


def guest(id, start_time, view_lock, room_lock, party_count, guest_count):
    """
    do the following for TIME seconds
        guest will wait to try to get access to the room (guest_waiting())
        get access to the room
        display message STARTING_PARTY_MESSAGE if this guest is the first one in the room
        Take some time partying (call guest_partying())
        display message STOPPING_PARTY_MESSAGE if the guest is the last one leaving in the room
    """
    while time.time() < start_time + TIME:
        guest_waiting()

        view_lock.acquire()
        if guest_count.value == 0:
            room_lock.acquire()
            print(STARTING_PARTY_MESSAGE)
            party_count.value += 1
        guest_count.value += 1
        current_guest_count = guest_count.value
        view_lock.release()

        guest_partying(id, current_guest_count)

        view_lock.acquire()
        if guest_count.value == 1:
            print(STOPPING_PARTY_MESSAGE)
            room_lock.release()
        guest_count.value -= 1
        view_lock.release()


def main():
    # Start time of the running of the program.
    start_time = time.time()

    # TODO - add any variables, data structures, processes you need
    # TODO - add any arguments to cleaner() and guest() that you need
    view_lock = mp.Lock()
    room_lock = mp.Lock()
    cleaned_count = mp.Value("i", 0)
    party_count = mp.Value("i", 0)
    guest_count = mp.Value("i", 0)

    processes = [
        mp.Process(
            target=cleaner,
            args=(i + 1, start_time, view_lock, room_lock, cleaned_count, guest_count),
        )
        for i in range(CLEANING_STAFF)
    ] + [
        mp.Process(
            target=guest,
            args=(j + 1, start_time, view_lock, room_lock, party_count, guest_count),
        )
        for j in range(HOTEL_GUESTS)
    ]

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    # Results
    print(
        f"Room was cleaned {cleaned_count.value} times, there were {party_count.value} parties"
    )


if __name__ == "__main__":
    main()
