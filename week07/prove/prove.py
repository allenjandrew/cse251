"""
Course: CSE 251 
Lesson: L07 Prove
File:   prove.py
Author: <Add name here>

Purpose: Process Task Files.

Instructions:

See Canvas for the full instructions for this assignment. You will need to complete the TODO comment
below before submitting this file:

TODO: My fastest time was 9.246 seconds, achieved with the following pool sizes (I have 8 cores):
    primer = mp.Pool(3)
    worder = mp.Pool(4)
    upper = mp.Pool(1)
    summer = mp.Pool(5)
    namer = mp.Pool(2)
To find these pool sizes, I initially set them up at 2 cores each. Then, in my callback functions, I printed the
corresponding task name to the terminal and ran the program. I watched the terminal fly through every task and
noticed which task name was the last to print out. I then incremented that task's pool size by 1 and continued. 

Add your comments here on the pool sizes that you used for your assignment and why they were the best choices.
"""

from datetime import datetime, timedelta
import requests
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
import glob
import math

# Include cse 251 common Python files - Dont change
from cse251 import *

TYPE_PRIME = "prime"
TYPE_WORD = "word"
TYPE_UPPER = "upper"
TYPE_SUM = "sum"
TYPE_NAME = "name"

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []


def is_prime(n: int):
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


def task_prime(value):
    """
    Use the is_prime() above
    Add the following to the global list:
        {value} is prime
            - or -
        {value} is not prime
    """
    return f"{value} is prime" if is_prime(value) else f"{value} is not prime"


def call_prime(result):
    result_primes.append(result)
    # print("prime")


def task_word(word):
    """
    search in file 'words.txt'
    Add the following to the global list:
        {word} Found
            - or -
        {word} not found *****
    """
    with open("words.txt") as f:
        for line in f:
            if line.strip() == word:
                return f"{word} found"

    return f"{word} not found *****"


def call_word(result):
    result_words.append(result)
    # print("word")


def task_upper(text):
    """
    Add the following to the global list:
        {text} ==>  uppercase version of {text}
    """
    return f"{text} ==> {text.upper()}"


def call_upper(result):
    result_upper.append(result)
    # print("upper")


def task_sum(start_value, end_value):
    """
    Add the following to the global list:
        sum of {start_value:,} to {end_value:,} = {total:,}
    """
    total = 0
    for i in range(start_value, end_value + 1):
        total += i
    return f"sum of {start_value:,} to {end_value:,} = {total:,}"


def call_sum(result):
    result_sums.append(result)
    # print("sum")


def task_name(url):
    """
    use requests module
    Add the following to the global list:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """
    response = requests.get(url)
    return (
        f"{url} has name {response.json()['name']}"
        if response.status_code == 200
        else f"{url} had an error receiving the information"
    )


def call_name(result):
    result_names.append(result)
    # print("name")


def main():
    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create process pools
    cpu_count = mp.cpu_count()

    primer = mp.Pool(3)
    worder = mp.Pool(4)
    upper = mp.Pool(1)
    summer = mp.Pool(5)
    namer = mp.Pool(2)

    # TODO you can change the following
    # TODO start and wait pools
    # primer.start()
    # worder.start()
    # upper.start()
    # summer.start()
    # namer.start()

    count = 0
    task_files = glob.glob("tasks/*.task")
    for filename in task_files:
        # print()
        # print(filename)
        task = load_json_file(filename)
        print(task)
        count += 1
        task_type = task["task"]
        if task_type == TYPE_PRIME:
            primer.apply_async(task_prime, args=(task["value"],), callback=call_prime)
        elif task_type == TYPE_WORD:
            worder.apply_async(task_word, args=(task["word"],), callback=call_word)
        elif task_type == TYPE_UPPER:
            upper.apply_async(task_upper, args=(task["text"],), callback=call_upper)
        elif task_type == TYPE_SUM:
            summer.apply_async(
                task_sum, args=(task["start"], task["end"]), callback=call_sum
            )
        elif task_type == TYPE_NAME:
            namer.apply_async(task_name, (task["url"],), callback=call_name)
        else:
            log.write(f"Error: unknown task type {task_type}")

    primer.close()
    worder.close()
    upper.close()
    summer.close()
    namer.close()

    primer.join()
    worder.join()
    upper.join()
    summer.join()
    namer.join()

    # DO NOT change any code below this line!
    # ---------------------------------------------------------------------------
    def log_list(lst, log):
        for item in lst:
            log.write(item)
        log.write(" ")

    log.write("-" * 80)
    log.write(f"Primes: {len(result_primes)}")
    log_list(result_primes, log)

    log.write("-" * 80)
    log.write(f"Words: {len(result_words)}")
    log_list(result_words, log)

    log.write("-" * 80)
    log.write(f"Uppercase: {len(result_upper)}")
    log_list(result_upper, log)

    log.write("-" * 80)
    log.write(f"Sums: {len(result_sums)}")
    log_list(result_sums, log)

    log.write("-" * 80)
    log.write(f"Names: {len(result_names)}")
    log_list(result_names, log)

    log.write(f"Number of Primes tasks: {len(result_primes)}")
    log.write(f"Number of Words tasks: {len(result_words)}")
    log.write(f"Number of Uppercase tasks: {len(result_upper)}")
    log.write(f"Number of Sums tasks: {len(result_sums)}")
    log.write(f"Number of Names tasks: {len(result_names)}")
    log.stop_timer(f"Total time to process {count} tasks")
    # print(cpu_count)


if __name__ == "__main__":
    main()
