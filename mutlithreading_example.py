import threading
import time

def heavy_task(n):
    print(f"Processing {n}")
    result = 0
    for i in range(10_000_000):
        result += i * i


if __name__ == "__main__":
    start_time = time.time()

    num_threads = threading.active_count()  # Just to print initial count
    print(f"Active threads before: {num_threads}")

    threads = []
    for i in range(8):
        t = threading.Thread(target=heavy_task, args=(i,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    end_time = time.time()
    num_threads = threading.active_count()
    
    print(f"Active threads after: {num_threads}")
    print(f"Multithreading took {end_time - start_time:.2f} seconds")

