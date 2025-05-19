import dill
import os
import time

STATE_FILE = "state.dill"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "rb") as f:
            print("Loaded existing state.")
            return dill.load(f)
    print("No saved state found — starting fresh.")
    return {
        "step1_done": False,
        "step2_done": False,
        "step3_done": False,
        "lookup_dict": {},
        "counts_dict": {},
    }

def save_state(state):
    with open(STATE_FILE, "wb") as f:
        dill.dump(state, f)
    print("State saved.")

def step1(state):
    print("Step 1: Building lookup_dict...")
    time.sleep(10)  # Simulate work
    state["lookup_dict"]["a"] = "apple"
    state["lookup_dict"]["b"] = "banana"
    state["step1_done"] = True
    save_state(state)

def step2(state):
    print("Step 2: Counting things...")
    time.sleep(10)  # Simulate work
    state["counts_dict"]["apple"] = 1
    state["counts_dict"]["banana"] = 2
    state["step2_done"] = True
    save_state(state)

def step3(state):
    print("Step 3: Final processing...")
    time.sleep(10)  # Simulate work
    # Example logic
    total = sum(state["counts_dict"].values())
    print(f"Total count: {total}")
    state["step3_done"] = True
    save_state(state)

def main():
    state = load_state()

    if not state["step1_done"]:
        step1(state)

    if not state["step2_done"]:
        step2(state)

    if not state["step3_done"]:
        step3(state)

    # Finished everything
    print("All steps complete.")
    with open("done.flag", "w") as f:
        f.write("done")

if __name__ == "__main__":
    main()
