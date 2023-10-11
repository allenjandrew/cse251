"""
Course: CSE 251 
Lesson: L05 Team Activity
File:   team.py
Author: <Add your name here>

Purpose: Check for prime values

Instructions:

- You can't use thread pools or process pools.
- Follow the graph from the `../canvas/teams.md` instructions.
- Start with PRIME_PROCESS_COUNT = 1, then once it works, increase it.
"""

import time
import threading
import multiprocessing as mp
import random
from os.path import exists

# Include cse 251 common Python files
from cse251 import *

PRIME_PROCESS_COUNT = 5


def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i**2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


# TODO create read_thread function
def read_thread(filename, shopper):
    with open(filename, "r") as f:
        for line in f:
            stripped = line.strip()
            num = int(stripped)
            shopper.put(num)
    for _ in range(PRIME_PROCESS_COUNT):
        shopper.put("no more")


# TODO create prime_process function
def prime_process(shopper, primes):
    while True:
        num = shopper.get()
        if num == "no more":
            break
        if is_prime(num):
            primes.append(num)


def create_data_txt(filename):
    # only create if it doesn't exist
    if not exists(filename):
        with open(filename, "w") as f:
            for _ in range(1000):
                f.write(str(random.randint(10000000000, 100000000000000)) + "\n")
                # f.write(str(random.randint(1, 10000)) + "\n")


def main():
    """Main function"""

    # Create the data file for this demo if it does not already exist.
    filename = "data.txt"
    create_data_txt(filename)

    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create shared data structures
    shopper = mp.Queue()
    primes = mp.Manager().list([])
    processes = []

    # TODO create reading thread
    processes.append(
        mp.Process(
            target=read_thread,
            args=(
                filename,
                shopper,
            ),
        )
    )

    # TODO create prime processes
    for _ in range(PRIME_PROCESS_COUNT):
        processes.append(mp.Process(target=prime_process, args=(shopper, primes)))

    # TODO Start them all
    for p in processes:
        p.start()

    # TODO wait for them to complete
    for p in processes:
        p.join()

    log.stop_timer(f"All primes have been found using {PRIME_PROCESS_COUNT} processes")

    # display the list of primes
    print(f"There are {len(primes)} found:")
    for prime in primes:
        print(prime)


if __name__ == "__main__":
    main()
