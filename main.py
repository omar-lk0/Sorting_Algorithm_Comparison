
import random
import time
import copy
import csv
import math
import os
from typing import List, Any, Callable

def bubble_sort(arr: List[Any]) -> List[Any]:
    
    a = arr[:]                          # work on a copy so the original is safe
    n = len(a)
    for i in range(n):
        swapped = False
        # After pass i the last i elements are already in place
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        # Early exit: if no swap occurred the list is sorted
        if not swapped:
            break
    return a

def selection_sort(arr: List[Any]) -> List[Any]:
    
    a = arr[:]
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        # Swap the found minimum with the first unsorted element
        a[i], a[min_idx] = a[min_idx], a[i]
    return a

def insertion_sort(arr: List[Any]) -> List[Any]:
 
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        # Shift elements of the sorted prefix that are greater than 'key'
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a

def merge_sort(arr: List[Any]) -> List[Any]:
 
    if len(arr) <= 1:
        return arr[:]

    mid = len(arr) // 2
    left  = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)

def _merge(left: List[Any], right: List[Any]) -> List[Any]:
    
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]);  i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def quick_sort(arr: List[Any]) -> List[Any]:
   
    a = arr[:]
    if len(a) <= 1:
        return a

    # Explicit stack stores (low, high) pairs still needing sorting
    stack = [(0, len(a) - 1)]
    while stack:
        low, high = stack.pop()
        if low < high:
            pivot_idx = _partition(a, low, high)
            # Push both sub-ranges; smaller one first so we handle the
            # larger sub-range last (tail-call optimisation equivalent)
            stack.append((low, pivot_idx - 1))
            stack.append((pivot_idx + 1, high))
    return a

def _partition(a: List[Any], low: int, high: int) -> int:
 
    rand_idx = random.randint(low, high)
    a[rand_idx], a[high] = a[high], a[rand_idx]   # move pivot to end
    pivot = a[high]
    i = low - 1                                    # boundary of the 'less-than' region
    for j in range(low, high):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[high] = a[high], a[i + 1]         # place pivot in final position
    return i + 1

def heap_sort(arr: List[Any]) -> List[Any]:
 
    a = arr[:]
    n = len(a)

    # 1. Build a max-heap by heapifying from the last non-leaf node downward
    for i in range(n // 2 - 1, -1, -1):
        _heapify(a, n, i)

    # 2. Extract elements one by one: swap root (max) with last element,
    #    shrink heap, restore heap property
    for i in range(n - 1, 0, -1):
        a[0], a[i] = a[i], a[0]
        _heapify(a, i, 0)
    return a

def _heapify(a: List[Any], heap_size: int, root: int) -> None:
 
    largest = root
    left    = 2 * root + 1
    right   = 2 * root + 2

    if left  < heap_size and a[left]  > a[largest]: largest = left
    if right < heap_size and a[right] > a[largest]: largest = right

    if largest != root:
        a[root], a[largest] = a[largest], a[root]
        _heapify(a, heap_size, largest)

def generate_random(n: int, lo: int = 0, hi: int = 10_000) -> List[int]:
    return [random.randint(lo, hi) for _ in range(n)]

def generate_sorted(n: int, lo: int = 0, hi: int = 10_000) -> List[int]:
    return sorted(generate_random(n, lo, hi))

def generate_reverse(n: int, lo: int = 0, hi: int = 10_000) -> List[int]:
    return sorted(generate_random(n, lo, hi), reverse=True)

def generate_nearly_sorted(n: int, swap_fraction: float = 0.02,
                            lo: int = 0, hi: int = 10_000) -> List[int]:
    
    a = generate_sorted(n, lo, hi)
    num_swaps = max(1, int(n * swap_fraction))
    for _ in range(num_swaps):
        i, j = random.sample(range(n), 2)
        a[i], a[j] = a[j], a[i]
    return a

def generate_flat(n: int, num_unique: int = 4,
                  lo: int = 0, hi: int = 100) -> List[int]:
    
    unique_vals = random.sample(range(lo, hi + 1),
                                min(num_unique, hi - lo + 1))
    return [random.choice(unique_vals) for _ in range(n)]

DATA_GENERATORS: dict[str, Callable[[int], List[Any]]] = {
    "Random"       : generate_random,
    "Sorted"       : generate_sorted,
    "Reverse"      : generate_reverse,
    "NearlySorted" : generate_nearly_sorted,
    "Flat"         : generate_flat,
}
SMALL_N_THRESHOLD  = 100      # lists smaller than this are timed with repetition
SMALL_N_REPETITIONS = 1_000   # number of repetitions for small lists

def benchmark(sort_fn: Callable, data: List[Any]) -> float:
    
    n = len(data)

    if n < SMALL_N_THRESHOLD:
        total_time = 0.0
        for _ in range(SMALL_N_REPETITIONS):
            data_copy = data[:]                   # fresh copy every repetition
            t_start   = time.perf_counter()
            sort_fn(data_copy)
            t_end     = time.perf_counter()
            total_time += t_end - t_start
        return total_time / SMALL_N_REPETITIONS   # average time per sort

    else:
        data_copy = data[:]
        t_start   = time.perf_counter()
        sort_fn(data_copy)
        t_end     = time.perf_counter()
        return t_end - t_start

ALGORITHMS: dict[str, Callable] = {
    "BubbleSort"   : bubble_sort,
    "SelectionSort": selection_sort,
    "InsertionSort": insertion_sort,
    "MergeSort"    : merge_sort,
    "QuickSort"    : quick_sort,
    "HeapSort"     : heap_sort,
}
SIZES = [50, 500, 5_000, 50_000]

O2_SKIP_ABOVE = 10_000
O2_ALGORITHMS = {"BubbleSort", "SelectionSort", "InsertionSort"}

CSV_FILENAME = "sorting_results.csv"

def format_time(seconds: float) -> str:

    if seconds < 1e-3:
        return f"{seconds * 1e6:>9.2f} µs"
    elif seconds < 1.0:
        return f"{seconds * 1e3:>9.2f} ms"
    else:
        return f"{seconds:>9.4f}  s"

def run_benchmarks() -> List[dict]:

    results = []
    random.seed(42)   # reproducibility – remove this line for fresh data each run

    total_runs = sum(
        1
        for size in SIZES
        for dist_name in DATA_GENERATORS
        for algo_name in ALGORITHMS
        if not (algo_name in O2_ALGORITHMS and size > O2_SKIP_ABOVE)
    )
    completed = 0

    print(f"\n{'─' * 72}")
    print(f"  Sorting Algorithm Benchmark   ({total_runs} experiments)")
    print(f"{'─' * 72}\n")

    for size in SIZES:
        print(f"  ▶  n = {size:,}")

        # Column header for this size block
        col_w = 14
        header = f"  {'Distribution':<15}" + "".join(
            f"{name:>{col_w}}" for name in ALGORITHMS
            if not (name in O2_ALGORITHMS and size > O2_SKIP_ABOVE)
        )
        print(header)
        print("  " + "─" * (len(header) - 2))

        for dist_name, gen_fn in DATA_GENERATORS.items():
            data = gen_fn(size)
            row_str = f"  {dist_name:<15}"

            for algo_name, sort_fn in ALGORITHMS.items():
                if algo_name in O2_ALGORITHMS and size > O2_SKIP_ABOVE:
                    # Skip O(n²) algorithms for large n
                    continue

                elapsed = benchmark(sort_fn, data)
                row_str += f"{format_time(elapsed):>{col_w}}"

                results.append({
                    "Size"        : size,
                    "Distribution": dist_name,
                    "Algorithm"   : algo_name,
                    "Time_s"      : round(elapsed, 9),
                })

                completed += 1
                # Simple progress indicator
                print(f"\r  Progress: {completed}/{total_runs}", end="", flush=True)

            print(f"\r{row_str}          ")   # overwrite progress line with full row

        note = ""
        if size > O2_SKIP_ABOVE:
            note = f"  (O(n²) algorithms skipped for n={size:,} – would take minutes)"
        print(f"\n{note}\n")

    return results

def save_csv(results: List[dict], filename: str = CSV_FILENAME) -> None:

    fieldnames = ["Size", "Distribution", "Algorithm", "Time_s"]
    with open(filename, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    print(f"  ✔  Results saved to '{filename}'  ({len(results)} rows)\n")

def demo_multi_type() -> None:

    samples = {
        "integers" : [5, 2, 8, 1, 9, 3],
        "floats"   : [3.14, 1.41, 2.72, 0.57, 1.62],
        "strings"  : ["banana", "apple", "cherry", "date", "elderberry"],
    }

    print("  ── Multi-type verification ──────────────────────────────────────")
    for type_name, data in samples.items():
        sorted_data = quick_sort(data)    # use one algorithm as a spot-check
        print(f"  {type_name:<10}: {data}  →  {sorted_data}")
    print()

if __name__ == "__main__":
    demo_multi_type()
    results = run_benchmarks()
    output_path = os.path.join(os.path.dirname(__file__), CSV_FILENAME)
    save_csv(results, output_path)
    print("  Done.  Open 'sorting_results.csv' to import data into your report.\n")