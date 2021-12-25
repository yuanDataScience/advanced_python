import concurrent.futures
import multiprocessing
import time

start = time.perf_counter()


def do_something():
    print(f'Sleeping 1 second...')
    time.sleep(1)
    return f'Done Sleeping...'

do_something()

finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} second(s)')

