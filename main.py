from queue import PriorityQueue, SimpleQueue
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any
import time
import logging
import threading

logging.basicConfig(filename="log.txt",
                    filemode='a',
                    format='%(asctime)s,%(msecs)03d,%(levelname)s,%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger("py_priority_q")

THREADS = []

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)

def current_time_in_ms()->int:
    return time.time_ns() // 1_000_000

def time_from_now(minutes:int, seconds:int=0)->int:
    return current_time_in_ms() + (minutes * 60_000) + (seconds * 1_000) 

def insert_N_tasks_due_at_time(number:int, time_due:int, queue:PriorityQueue):
    for _ in range(number):
        queue.put(PrioritizedItem(time_due, {'time_due':time_due, 'insert_time':current_time_in_ms(), 'concurrent_tasks':number}))

def insert_N_tasks_over_Y_seconds(seconds:int, queue:PriorityQueue, max_due_at_same_time:int=10):
    # insert N tasks every second for Y seconds, max due at the same time to test how many can be scheduled at the same
    # time
    print(f"insert_n_tasks_over_{seconds}_starting starting - max at same time {max_due_at_same_time}")
    start = current_time_in_ms() // 1_000
    current = start
    end = start + seconds
    while current < end:
        now = current_time_in_ms() // 1_000
        if now-current == 1:
            time_due = time_from_now(0, 30)
            print(f"inserting batch of size {max_due_at_same_time} at time {time_due}")
            insert_N_tasks_due_at_time(max_due_at_same_time, time_due, queue)
            current+=1
        else:
            continue

def drain_queue(queue:PriorityQueue, logger:logging.Logger, output:list):
    print("drain_queue starting")
    time.sleep(5)
    while not queue.empty():
        current_time = current_time_in_ms()
        while not queue.empty() and queue.queue[0].priority <= current_time:
            item:PrioritizedItem = queue.get()
            # logger.debug(f'{current_time},{item.item['time_due']},{item.item['insert_time']},{item.item['concurrent_tasks']}') 
            output.append(f'{current_time},{item.item['time_due']},{item.item['insert_time']},{item.item['concurrent_tasks']}') 
            current_time = current_time_in_ms()
    print("drain_queue ending")
    return output

def run_simulation(logger:logging.Logger, queue:PriorityQueue, run_size:int, max_same_time:int, run_time_secs:int):
    # for a period of 2 mins, insert N tasks with task insert time and task due time
    # iterate through queue to pull the top entry and log the task insert time, task due time, and current time
    for n in range(run_size):
        # how many concurrent tasks due at this specific epoch millisecond can we support?
        insert_N_tasks_over_Y_seconds(run_time_secs, queue, max_same_time)

def main():
    print("Starting QUEUE")
    logger.info('current_time,time_due,insert_time,concurrent_tasks')
    queue:PriorityQueue = PriorityQueue()
    t = threading.Thread(target=run_simulation, args=(logger, queue, 1, 500, 3))
    data = []
    drainer = threading.Thread(target=drain_queue, args=(queue, logger, data))
    THREADS.append(t)
    THREADS.append(drainer)
    t.start()
    drainer.start()
    t.join()
    drainer.join()
    data.insert(0, 'current_time,time_due,insert_time,concurrent_tasks')
    ## reducing logging makes the queue work faster, can we do async logging instead?
    with Path('no_log_output.txt').open('w') as f:
        for each in data:
            f.write(f'{each}\n')


if __name__ == "__main__":
    main()
