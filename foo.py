from cse251 import *
import threading

# t1 = threading.Thread(target=func, args=(x,))
# t2 = threading.Thread(target=func, args=(y,))
# t3 = threading.Thread(target=func, args=(z,))

# t1.start()
# t2.start()
# t3.start()

# t1.join()
# t2.join()
# t3.join()

# def display_hello():
#     print ("Hello, World!")

# print('Before the thread')
# thread = threading.Timer(3.0, display_hello)
# thread.start()
# print('After the thread - End of program')

# threads = []

# for _ in range(10):
#     t = threading.Thread(target=func, args=(v,))
#     threads.append(t)

import logging
import threading
import time

def thread_function(name, sleep_time):
    """This is the function the thread will run"""
    print(f'Thread "{name}": starting')
    time.sleep(sleep_time)
    print(f'Thread "{name}": finishing')

if __name__ == '__main__':
    print('Main : before creating thread')

    # Create a thread. This doesn't start it, just it's creation
    # The args argument allow the main code to pass arguments to the
    # thread.
    # we DON'T want any global variables in this case.
    # Note: if you are wondering about the ',' after 'Sleep Function',
    # please review tuples in Python.
    t = threading.Thread(target=thread_function, args=('Sleep Function', 2))

    print('Main : before running thread')
    # The code here in main will start the thread and then keep
    # executing. It will not wait for the thread to return. 
    t.start()

    print('Main : wait for the thread to finish')
    # Joining a thead back to the main thread is waiting for the
    # created thread to finish.
    t.join()

    print('Main : all done')