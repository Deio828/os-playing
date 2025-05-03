import multiprocessing
import time
# import tqdm


def heavy_task(n):
    print(f"processing {n}")
    result = 0
    for i in range(10_000_000):
        result += i * i
    return result


if __name__ == "__main__":
    num_processes = multiprocessing.cpu_count()
    print(f"Using {num_processes} processes")

    numbers = [i for i in range(num_processes)]

    start_time = time.time()

    # Create a pool of processes
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(heavy_task, numbers)

    end_time = time.time()

    print(f"Multiprocessing took {end_time - start_time:.2f} seconds")
