import threading, queue
import random

q = queue.Queue()


def worker():
    while True:
        item = q.get()
        print(f"Working on {item}")
        for i in range(5):
            print(item)
        q.task_done()


# send thirty task requests to the worker
for item in range(100):
    arg = random.randint(0, 5)
    q.put(item)
    threading.Thread(target=worker, daemon=True).start()
print("All task requests sent\n", end="")

# block until all tasks are done
q.join()
print("All work completed")
