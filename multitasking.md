# Multithreading vs Multiprocessing Deep Dive

**Date**: May 3, 2025  
**Topic**: Understanding multithreading, multiprocessing, and pipeline parallelism

---

## 🔥 Key Concepts

### 🧠 Multitasking
- OS-level switching between different programs (Excel, Chrome, VS Code).
- Time slicing or core-based parallelism.

### 🧠 Multithreading
- Splitting a single process into multiple threads.
- **Threads share memory**.
- **In Python (CPython)**: Limited by the **Global Interpreter Lock (GIL)** → only one thread can execute Python bytecode at a time → poor for CPU-bound tasks.
- **In C++/Java**: No GIL → threads can run truly in parallel across cores.

### 🧠 Multiprocessing
- Splitting a program into multiple processes.
- **Each process has separate memory** → no shared data.
- Avoids the GIL limitation in Python.
- Best for CPU-bound tasks and safety (crash isolation).

---

## ✅ Key Clarifications

| | Multithreading | Multiprocessing |
|---|---|---|
| Memory | Shared | Separate |
| CPU Usage | Limited by GIL (Python) or true parallel (C++/Java) | Full parallelism |
| RAM Usage | Lower | Higher |
| Best for | I/O-bound tasks | CPU-bound tasks |

---

## 📝 Your Questions & Clarifications

### ❓ *Isn't multithreading the same as multiprocessing?*
- **No** → Memory sharing vs. isolation.
- CPU parallelism in multithreading depends on language/runtime (GIL in Python prevents it).

### ❓ *In C++/Java, would multithreading behave like multiprocessing?*
- **Yes** for CPU usage.
- **No** for memory (threads share, processes don’t).

### ❓ *What happens if two processes change the same global variable?*
- **Each process works on its own memory copy**.
- Changes in one process are invisible to others unless using shared memory or IPC.

### ❓ *What if two threads change the same global variable?*
- **Both see and affect the same variable** → race conditions possible without locks.

---

## 🧪 Code Demonstrations

### 🔹 Multithreading shares memory
```python
import threading
import time

# Shared global variable
X = 1

def thread_task():
    global X
    print(f"[{threading.current_thread().name}] Before change: X = {X}")
    X = 2
    print(f"[{threading.current_thread().name}] After change: X = {X}")

# Create two threads
thread1 = threading.Thread(target=thread_task, name="Thread-A")
thread2 = threading.Thread(target=thread_task, name="Thread-B")

thread1.start()
time.sleep(0.5)  # Just to make output clearer
thread2.start()

thread1.join()
thread2.join()

print(f"[Main Thread] Final X = {X}")
```
This results:
```txt
[Thread-A] Before change: X = 1
[Thread-A] After change: X = 2
[Thread-B] Before change: X = 2
[Thread-B] After change: X = 2
[Main Thread] Final X = 2
```

### 🔹 Multiprocessing isolates memory
```python
import multiprocessing
import time

# Global variable
X = 1

def process_task():
    global X
    print(f"[{multiprocessing.current_process().name}] Before change: X = {X}")
    X = 2
    print(f"[{multiprocessing.current_process().name}] After change: X = {X}")

if __name__ == "__main__":
    # Create two processes
    process1 = multiprocessing.Process(target=process_task, name="Process-A")
    process2 = multiprocessing.Process(target=process_task, name="Process-B")

    process1.start()
    time.sleep(0.5)  # Just to make output clearer
    process2.start()

    process1.join()
    process2.join()

    print(f"[Main Process] Final X = {X}")
```
**Expected output:**
```txt
[Process-A] Before change: X = 1
[Process-A] After change: X = 2
[Process-B] Before change: X = 1
[Process-B] After change: X = 2
[Main Process] Final X = 1
```

## Real-world Use Case: Image Tile Processing
**Scenario:** Split a large image (10,000 x 10,000) into 100 x 100 tiles.

Decision: Use Multiprocessing
- Tasks are CPU-bound.
- Tiles are independent → memory isolation is fine.
- Avoids GIL, true parallelism achieved.

**PesudoCode Sketch**
```python
import multiprocessing

# Step 1: Function to process each tile
def process_tile(tile_coordinates):
    x, y = tile_coordinates
    # 1. Extract the tile from the image
    # tile = image[y:y+100, x:x+100]
    # 2. Preprocess the tile (e.g., adjust colors)
    # tile = preprocess(tile)
    # 3. Classify the tile using your ML model
    # label = classify(tile)
    # For simplicity, let's return a fake label
    label = (x // 100 + y // 100) % 5  # fake class 0-4
    return (x, y, label)

if __name__ == "__main__":

    # Step 2: Define tile coordinates
    tile_coordinates = []
    for y in range(0, 10000, 100):
        for x in range(0, 10000, 100):
            tile_coordinates.append((x, y))  # Top-left corner of each tile

    # Step 3: Create a multiprocessing pool
    pool = multiprocessing.Pool(processes=8)

    # Step 4: Process tiles in parallel
    results = pool.map(process_tile, tile_coordinates)

    pool.close()
    pool.join()

    # Step 5: Reconstruct heatmap
    heatmap = [[0 for _ in range(100)] for _ in range(100)]  # 100x100 tiles
    for x, y, label in results:
        heatmap[y // 100][x // 100] = label

    # Step 6: Display or save heatmap
    # visualize_heatmap(heatmap)
```

## Advanced Concept: Pipeline Parallellism
**Your Idea:** While CPU processes Image 10 (Stage A), GPU processes Image 9 (Stage B), another CPU process handles Image 8 (Stage C).

**Architecture:**
- Process A → function_A (CPU) → Queue 1
- Process B → function_B (GPU) → Queue 2
- Process C → function_C (CPU) → Final Output

**Pesudocode:**
```python
from multiprocessing import Process, Queue

def function_A_worker(images, queue1):
    for image in images:
        result_a = function_A(image)
        queue1.put((image, result_a))
    queue1.put("DONE")

def function_B_worker(queue1, queue2):
    while True:
        item = queue1.get()
        if item == "DONE":
            queue2.put("DONE")
            break
        image, result_a = item
        result_b = function_B(result_a)
        queue2.put((image, result_b))

def function_C_worker(queue2):
    while True:
        item = queue2.get()
        if item == "DONE":
            break
        image, result_b = item
        result_c = function_C(result_b)
        save_result(image, result_c)

if __name__ == "__main__":
    queue1 = Queue()
    queue2 = Queue()

    # Divide images among processes
    images = load_images()

    p1 = Process(target=function_A_worker, args=(images, queue1))
    p2 = Process(target=function_B_worker, args=(queue1, queue2))
    p3 = Process(target=function_C_worker, args=(queue2,))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()
```

**Summary workflow:**
| Step | Process A            | Queue 1 | Process B            | Queue 2 | Process C            |
| ---- | -------------------- | ------- | -------------------- | ------- | -------------------- |
| 1    | Image 1 → result\_a1 | (1)     | idle                 | empty   | idle                 |
| 2    | Image 2 → result\_a2 | (2)     | Image 1 → result\_b1 | (1)     | idle                 |
| 3    | Image 3 → result\_a3 | (3)     | Image 2 → result\_b2 | (2)     | Image 1 → result\_c1 |
| 4    | Done                 | DONE    | Image 3 → result\_b3 | (3)     | Image 2 → result\_c2 |
| 5    | Done                 | empty   | DONE                 | DONE    | Image 3 → result\_c3 |
| 6    | Done                 | empty   | Done                 | empty   | Done                 |
