import random
import time
import string
import csv
import sys
import multiprocessing as mp
import os

# ── Reproducibility ───────────────────────────────────────────────────────────
SEED = 42
random.seed(SEED)

# ── Increase recursion limit for large recursive sorts ─────────────────────────
sys.setrecursionlimit(300_000)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — SORTING ALGORITHMS (9 Required Algorithms)
# ═══════════════════════════════════════════════════════════════════════════════

def bubble_sort(arr):
    a = list(arr)
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a

def selection_sort(arr):
    a = list(arr)
    n = len(a)
    for i in range(n):
        m = i
        for j in range(i + 1, n):
            if a[j] < a[m]:
                m = j
        a[i], a[m] = a[m], a[i]
    return a

def insertion_sort(arr):
    a = list(arr)
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a

def merge_sort(arr):
    if len(arr) <= 1:
        return list(arr)
    mid = len(arr) // 2
    return _merge(merge_sort(arr[:mid]), merge_sort(arr[mid:]))

def _merge(left, right):
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out

def quick_sort(arr):
    if len(arr) <= 1:
        return list(arr)
    a, b, c = arr[0], arr[len(arr) // 2], arr[-1]
    pivot   = sorted([a, b, c])[1]          
    left    = [x for x in arr if x < pivot]
    middle  = [x for x in arr if x == pivot]
    right   = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def heap_sort(arr):
    a = list(arr)
    n = len(a)
    for i in range(n // 2 - 1, -1, -1):
        _sift_down(a, n, i)
    for i in range(n - 1, 0, -1):
        a[0], a[i] = a[i], a[0]
        _sift_down(a, i, 0)
    return a

def _sift_down(a, n, i):
    while True:
        largest, l, r = i, 2 * i + 1, 2 * i + 2
        if l < n and a[l] > a[largest]: largest = l
        if r < n and a[r] > a[largest]: largest = r
        if largest == i: break
        a[i], a[largest] = a[largest], a[i]
        i = largest

def counting_sort(arr):
    """Note: Will throw TypeError intentionally if applied to floats/strings."""
    if not arr:
        return []
    mn, mx = min(arr), max(arr)
    spread = mx - mn
    if spread > 2_000_000:
        return sorted(arr)
    count = [0] * (spread + 1)
    for x in arr:
        count[x - mn] += 1
    out = []
    for i, c in enumerate(count):
        if c:
            out.extend([mn + i] * c)
    return out

class _Node:
    __slots__ = ("val", "nxt")
    def __init__(self, val):
        self.val = val
        self.nxt = None

def _array_to_ll(arr):
    if not arr: return None
    head = cur = _Node(arr[0])
    for x in arr[1:]:
        cur.nxt = _Node(x); cur = cur.nxt
    return head

def _ll_to_array(head):
    out = []
    while head:
        out.append(head.val); head = head.nxt
    return out

def _ll_merge_sort(head):
    if not head or not head.nxt:
        return head
    slow, fast = head, head.nxt
    while fast and fast.nxt:
        slow = slow.nxt; fast = fast.nxt.nxt
    mid = slow.nxt
    slow.nxt = None
    return _ll_merge_nodes(_ll_merge_sort(head), _ll_merge_sort(mid))

def _ll_merge_nodes(a, b):
    dummy = cur = _Node(0)
    while a and b:
        if a.val <= b.val:
            cur.nxt = a; a = a.nxt
        else:
            cur.nxt = b; b = b.nxt
        cur = cur.nxt
    cur.nxt = a or b
    return dummy.nxt

def linked_list_sort(arr):
    head = _array_to_ll(list(arr))
    sorted_head = _ll_merge_sort(head)
    return _ll_to_array(sorted_head)

def tim_sort(arr):
    return sorted(arr)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — DATA GENERATORS
# ═══════════════════════════════════════════════════════════════════════════════

def gen_random_int(n):        return [random.randint(0, 100_000) for _ in range(n)]
def gen_sorted_int(n):        return list(range(n))
def gen_reverse_int(n):       return list(range(n, 0, -1))
def gen_almost_sorted(n):
    a = list(range(n))
    for _ in range(max(1, n // 50)):
        i, j = random.randrange(n), random.randrange(n)
        a[i], a[j] = a[j], a[i]
    return a
def gen_flat(n):              return [random.randint(0, 5) for _ in range(n)]
def gen_random_float(n):      return [random.random() * 100_000 for _ in range(n)]
def gen_random_string(n):     return ["".join(random.choices(string.ascii_lowercase, k=6)) for _ in range(n)]

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — BENCHMARK ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

def _worker_process(func, gen, n, runs, return_dict):
    """Executes the benchmark inside a separate process to allow strict termination."""
    try:
        import time
        total_time = 0.0
        for _ in range(runs):
            arr = gen(n)
            start = time.perf_counter()
            func(list(arr)) 
            total_time += (time.perf_counter() - start)
        return_dict['result'] = total_time / runs
    except TypeError:
        return_dict['result'] = "UNSUPPORTED"
    except Exception as e:
        return_dict['result'] = f"ERR"



def benchmark_with_timeout(func, gen, n, runs, timeout=10):
    """Runs the sorting workload with an absolute 10-second kill switch."""
    manager = mp.Manager()
    return_dict = manager.dict()
    
    p = mp.Process(target=_worker_process, args=(func, gen, n, runs, return_dict))
    p.start()
    p.join(timeout)
    
    if p.is_alive():
        p.terminate()  # Hard kill the process
        p.join()
        return "TIMEOUT"
        
    return return_dict.get('result', "ERR")

def fmt_time(t):
    if isinstance(t, str):
        return t  
    if t < 1e-6:   return f"{t * 1e9:.2f} ns"
    if t < 1e-3:   return f"{t * 1e6:.2f} μs"
    if t < 1.0:    return f"{t * 1e3:.2f} ms"
    return             f"{t:.3f} s "

def runs_for_size(n):
    if n == 50:           return 20_000
    if n == 100:          return 10_000
    if n == 1_000:        return 100
    if n == 10_000:       return 10
    return 1

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — EXPERIMENT CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

ALGORITHMS = {
    "Bubble":          bubble_sort,
    "Selection":       selection_sort,
    "Insertion":       insertion_sort,
    "Merge":           merge_sort,
    "Quick":           quick_sort,
    "Heap":            heap_sort,
    "Counting":        counting_sort,
    "LinkedListMerge": linked_list_sort,
    "TimSort":         tim_sort,
}

DATA_PROFILES = {
    "Random":          (gen_random_int,    "int"),
    "Sorted":          (gen_sorted_int,    "int"),
    "Reverse_Sorted":  (gen_reverse_int,   "int"),
    "Almost_Sorted":   (gen_almost_sorted, "int"),
    "Flat":            (gen_flat,          "int"),
    "Random_Float":    (gen_random_float,  "float"),
    "Random_String":   (gen_random_string, "str"),
}

SIZES = [50, 100, 1_000, 10_000, 100_000, 1_000_000, 10_000_000]
CSV_FILE = "sorting_results.csv"

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — MAIN EXPERIMENT RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

def run_experiment():
    rows = []
    W = 85 
    print()
    print("═" * W)
    print("  SORTING ALGORITHM BENCHMARK ")
    print("═" * W)

    for profile_name, (gen, etype) in DATA_PROFILES.items():
        print()
        print("━" * W)
        print(f"  DATA PROFILE : {profile_name} [{etype.upper()}]")
        print("━" * W)

        algo_col = 18
        time_col = 10
        print(f"  {'Algorithm':<{algo_col}}", end="")
        for n in SIZES:
            if n >= 1_000_000:   label = f"{n // 1_000_000}M"
            elif n >= 1_000:     label = f"{n // 1_000}k"
            else:                label = str(n)
            print(f"{label:>{time_col}}", end="")
        print()
        print(f"  {'-' * (algo_col + time_col * len(SIZES))}")

        for aname, func in ALGORITHMS.items():
            print(f"  {aname:<{algo_col}}", end="", flush=True)

            for n in SIZES:
                runs = runs_for_size(n)
                t = benchmark_with_timeout(func, gen, n, runs, timeout=10)
                
                cell = fmt_time(t)
                raw_time = t if isinstance(t, str) else f"{t:.9f}"

                print(f"{cell:>{time_col}}", end="", flush=True)

                rows.append({
                    "profile":   profile_name,
                    "elem_type": etype,
                    "algo":      aname,
                    "size":      n,
                    "runs":      runs,
                    "time_s":    raw_time,
                    "display":   cell.strip(),
                })

            print()

    # ── CSV export ────────────────────────────────────────────────────────────
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["profile", "elem_type", "algo", "size", "runs", "time_s", "display"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print()
    print("═" * W)
    print(f"  ✓  {len(rows)} data points collected")
    print(f"  ✓  Results saved to: {os.path.abspath(CSV_FILE)}")
    print("═" * W)
    print()

if __name__ == "__main__":
    mp.freeze_support() # Required for safe multiprocessing on Windows
    run_experiment()