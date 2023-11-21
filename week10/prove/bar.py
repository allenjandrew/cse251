from multiprocessing import shared_memory
import multiprocessing as mp


def do_work(shared_name, value, start, end):
    # Attach to an exist shared memory block
    shared = shared_memory.SharedMemory(shared_name)
    for i in range(start, end):
        shared.buf[i] = value
    # need to close this local shared memory block access
    shared.close()


def main():
    shared = shared_memory.SharedMemory(create=True, size=100)
    # Create a shared memory block of 100 items
    print(f"Shared memory name = {shared.name}")

    # Divide the work among two processes, storing partial results in "shared"
    p1 = mp.Process(target=do_work, args=(shared.name, 1, 0, 50))
    p2 = mp.Process(target=do_work, args=(shared.name, 2, 50, 100))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    # we must loop through the shared.buf array to display the values
    print("Buffer values:")
    for i in range(100):
        print(shared.buf[i], end=" ")
    print()

    # close and give the memory block back to the OS
    shared.close()
    shared.unlink()


if __name__ == "__main__":
    main()
