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

PHILOSOPHERS = 1000
MAX_MEALS_EATEN = PHILOSOPHERS * 20


class Philosopher(threading.Thread):
    def __init__(self, id, names, forks, meals_eaten, meal_checker):
        super().__init__()

        # Pass all the arguments to self
        self.id = id  # int
        self.meals_eaten = meals_eaten  # array
        self.meal_checker = meal_checker  # lock

        self.name = names[
            id % len(names)
        ]  # string - gets a single name out of the array, based on id number
        # We don't want duplicate philos. If this philo isn't the first with their name, add a modifier to it
        if id >= len(names):
            self.name += f" {int(id / len(names)) + 1}.0"

        # Grab this philo's corresponding forks (see line 50). If this is the last philo, give them the first fork
        if id >= len(forks) - 1:
            self.fork1, self.fork2 = (
                forks[id],
                forks[0],
            )  # Grabbing the locks from the forks array
        else:
            self.fork1, self.fork2 = (forks[id], forks[id + 1])

    def run(self):
        # First off, let's make sure we haven't eaten all the meals up yet. To do that, we acquire the meal_checker lock. The point of this lock is to make sure only one philo is viewing the meals_eaten array at a time
        self.meal_checker.acquire()

        while (
            sum(self.meals_eaten) < MAX_MEALS_EATEN
        ):  # This check always happens when we have the lock
            # Once we've verified that the sum of all meals eaten by philos is less than the max number of meals to eat, we update this philo's meal count so all other philos know. Then we release the lock
            # Optimized code might have this '+= 1' statement inside the eat() method. That would be nice. I have it here because I don't want some other philo trying to check the meals_eaten total without accounting for the fact that this philo is already about to eat
            self.meals_eaten[self.id] += 1
            self.meal_checker.release()

            # First, we think for a bit
            self.think()

            # Then, we eat for a bit
            self.eat()

            # We need to acquire the lock again so the while loop can check meals_eaten again!
            self.meal_checker.acquire()

        # Make sure to release the lock once you exit the while loop!!
        self.meal_checker.release()

        # We don't need to get the lock this time because we're just viewing meals_eaten, not updating it
        print(self.meals_eaten[self.id])

    def eat(self):
        # Grab both the forks. This code is imperfect because we must grab the first lock before we can look for the other. Optimized code might have us looking for both at the same time.
        self.fork1.acquire()
        self.fork2.acquire()

        # We have both locks - let's dig in!!
        print(f"{self.id} - {self.name} started eating")

        # Technically, the instructions don't say we have to sleep a random amount of time - just that it has to be between 1 and 3 seconds
        time.sleep(1)  # random.randint(1, 3))

        # We've finished eating. Yum!
        print(
            f"{self.id} - {self.name} finished their {ordinal(self.meals_eaten[self.id])} meal"
        )

        # Let go of both forks so our coleagues can eat
        self.fork1.release()
        self.fork2.release()

    def think(self):
        # Start thinking
        print(f"{self.id} - {self.name} started thinking")

        # Wait a second, unless this is the first time we're thinking. If so, half of our philos will go straight to eating instead. This allows us to start out alternating thinking and eating
        if self.meals_eaten[self.id] == 0:
            time.sleep(
                self.id % 2
            )  # For half of philos, this will be 0; for the other half it'll be 1
        else:
            time.sleep(1)  # random.randint(1, 3))

        # Great job. Let's go back to eating now!
        print(f"{self.id} - {self.name} thought up a new philosophy")


# This is a quick little lambda function I found online to get an ordinal string from any int
ordinal = lambda n: str(n) + {1: "st", 2: "nd", 3: "rd"}.get(
    10 <= n % 100 <= 20 and n or n % 10, "th"
)


def main():
    # TODO - create the forks - same number of forks as philos
    forks = [threading.Lock() for _ in range(PHILOSOPHERS)]

    # Create a lock for checking if we need to eat more meals
    meal_checker = threading.Lock()

    # Let's give these philos some names, just for fun
    names = [
        "DesCartes",
        "Socrates",
        "Locke",
        "Plato",
        "St. Thomas Aquinus",
        "Aristotle",
        "Demosthenes",
        "Hippocrates",
        "Freud",
        "Confucius",
        "Doofenshmirtz",
        "Eric Gee",
    ]

    # This is an array to keep track of each philo's eating habits
    meals_eaten = [0 for _ in range(PHILOSOPHERS)]

    # Create the philos, and pass in id=i, names array, forks array, meals_eaten array, and meal_checker lock
    philos = [
        Philosopher(i, names, forks, meals_eaten, meal_checker)
        for i in range(PHILOSOPHERS)
    ]

    # TODO - Start them eating and thinking
    for philo in philos:
        philo.start()
    for philo in philos:
        philo.join()

    # TODO - Display how many times each philosopher ate
    print()
    print(f"Philosophers and # of meals eaten:")
    for i in range(PHILOSOPHERS):
        print(
            f"{i})  " if i < 10 else f"{i}) " if i < 100 else f"{i})",
            f"{philos[i].name:<24} ----  {meals_eaten[i]} meals eaten",
        )
    # print(meals_eaten)  # This just prints the array itself
    # Print out the total number of meals eaten
    print(f"\nTotal: {sum(meals_eaten)} out of {MAX_MEALS_EATEN} meals eaten")
    print()


if __name__ == "__main__":
    main()
