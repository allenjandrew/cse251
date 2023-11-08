"""
Course: CSE 251
Lesson Week: 09
File: team1.py

Purpose: team activity - Dining philosophers problem

Problem statement

Five silent philosophers sit at a round table with bowls of spaghetti. Forks
are placed between each pair of adjacent philosophers.

Each philosopher must alternately think and eat. However, a philosopher can
only eat spaghetti when they have both left and right forks. Each fork can be
held by only one philosopher and so a philosopher can use the fork only if it
is not being used by another philosopher. After an individual philosopher
finishes eating, they need to put down both forks so that the forks become
available to others. A philosopher can only take the fork on their right or
the one on their left as they become available and they cannot start eating
before getting both forks.  When a philosopher is finished eating, they think 
for a little while.

Eating is not limited by the remaining amounts of spaghetti or stomach space;
an infinite supply and an infinite demand are assumed.

The problem is how to design a discipline of behavior (a concurrent algorithm)
such that no philosopher will starve

Instructions:

        **************************************************
        ** DO NOT search for a solution on the Internet **
        ** your goal is not to copy a solution, but to  **
        ** work out this problem.                       **
        **************************************************

- You have Locks and Semaphores that you can use.
- Remember that lock.acquire() has an argument called timeout.
- philosophers need to eat for 1 to 3 seconds when they get both forks.  
  When the number of philosophers has eaten MAX_MEALS times, stop the philosophers
  from trying to eat and any philosophers eating will put down their forks when finished.
- philosophers need to think for 1 to 3 seconds when they are finished eating.  
- You want as many philosophers to eat and think concurrently.
- Design your program to handle N philosophers and N forks after you get it working for 5.
- Use threads for this problem.
- When you get your program working, how to you prove that no philosopher will starve?
  (Just looking at output from print() statements is not enough)
- Are the philosophers each eating and thinking the same amount?
- Using lists for philosophers and forks will help you in this program.
  for example: philosophers[i] needs forks[i] and forks[i+1] to eat (the % operator helps)
"""

import time
import threading
import random

PHILOSOPHERS = 5
MAX_MEALS_EATEN = PHILOSOPHERS * 5
TOTAL_MEALS_EATEN = 0


class Philosopher(threading.Thread):
    def __init__(self, id, forks, sema_4):
        super.init(self)
        self.id = id
        self.forks = forks
        self.meals_eaten = 0
        self.sema_4 = sema_4

    def run(self):
        start = True
        while TOTAL_MEALS_EATEN < MAX_MEALS_EATEN:
            self.think(start)
            start = False
            self.eat()

    def eat(self):
        TOTAL_MEALS_EATEN += 1
        self.meals_eaten += 1

    def think(self, start=False):
        if start:
            time.sleep(self.id % 2)
        else:
            time.sleep(random.randint(1, 3))


# def philosophize(phil_num, fork_a, fork_b, shopper_a, shopper_b):
#     start = True
#     meals_eaten = 0
#     while True:
#         think(phil_num, start)
#         start = False

#         eat(fork_a, fork_b, shopper_a, shopper_b)
#         meals_eaten += 1

#     return meals_eaten


# def eat(fork_a, fork_b, shopper_a, shopper_b):
#     fork_a.acquire()
#     fork_b.acquire()
#     shopper_a.acquire()
#     time.sleep(random.randint(1, 3))
#     shopper_b.release()
#     fork_a.release()
#     fork_b.release()


# def think(phil_num, start=False):
#     if start:
#         time.sleep(phil_num % 2)
#         return
#     time.sleep(random.randint(1, 3))


def main():
    # TODO - create the forks
    forks = []
    for _ in range(PHILOSOPHERS):
        forks.append(threading.Lock())

    shopper_remaining = threading.Semaphore(MAX_MEALS_EATEN)
    shopper_eaten = threading.Semaphore(MAX_MEALS_EATEN)
    for _ in MAX_MEALS_EATEN:
        shopper_eaten.acquire()

    philos = []
    for i in range(PHILOSOPHERS):
        philos.append(Philosopher(i, forks))

    # TODO - create PHILOSOPHERS philosophers
    # philos = []
    # philos.append(
    #     threading.Thread(
    #         target=philosophize,
    #         args=(1, fork_1, fork_2, shopper_remaining, shopper_eaten),
    #     )
    # )
    # philos.append(
    #     threading.Thread(
    #         target=philosophize,
    #         args=(2, fork_2, fork_3, shopper_remaining, shopper_eaten),
    #     )
    # )
    # philos.append(
    #     threading.Thread(
    #         target=philosophize,
    #         args=(3, fork_3, fork_4, shopper_remaining, shopper_eaten),
    #     )
    # )
    # philos.append(
    #     threading.Thread(
    #         target=philosophize,
    #         args=(4, fork_4, fork_5, shopper_remaining, shopper_eaten),
    #     )
    # )
    # philos.append(
    #     threading.Thread(
    #         target=philosophize,
    #         args=(5, fork_5, fork_1, shopper_remaining, shopper_eaten),
    #     )
    # )

    # TODO - Start them eating and thinking
    for philo in philos:
        philo.start()

    for philo in philos:
        philo.join()

    # TODO - Display how many times each philosopher ate

    pass


if __name__ == "__main__":
    main()
