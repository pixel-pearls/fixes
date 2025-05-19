import time
import dill
import psutil
import multiprocessing

CPU_LIMIT_SECONDS = 150000  # 2500 minutes
CHECKPOINT_FILE = "checkpoint.dill"
DONE_FLAG = "done.flag"

def save_state(state):
    with open(CHECKPOINT_FILE, "wb") as f:
        dill.dump(state, f)

def load_state():
    try:
        with open(CHECKPOINT_FILE, "rb") as f:
            return dill.load(f)
    except FileNotFoundError:
        return None

def get_main_cpu_time():
    proc = psutil.Process()
    t = proc.cpu_times()
    return t.user + t.system

def worker(x, y):
    # Your real work here
    return x + y

# Load or initialize
state = load_state() or {"index": 0, "results": []}

# Make input list
all_tasks = [(i, i+1) for i in range(state["index"], 1_000_000)]

CHUNK_SIZE = 1000

while state["index"] < len(all_tasks):
    # Check main process CPU time
    if get_main_cpu_time() >= CPU_LIMIT_SECONDS:
        print("Main process CPU limit hit. Saving and exiting.")
        save_state(state)
        exit()

    # Run a chunk
    batch = all_tasks[state["index"]:state["index"]+CHUNK_SIZE]

    with multiprocessing.Pool(processes=8) as pool:
        results = pool.starmap(worker, batch)

    state["results"].extend(results)
    state["index"] += CHUNK_SIZE
    save_state(state)

# Done
save_state(state)
with open(DONE_FLAG, "w") as f:
    f.write("done")
