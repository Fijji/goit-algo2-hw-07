import random
import time
import logging
from collections import OrderedDict

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def range_sum_no_cache(array, L, R):
    return sum(array[L:R + 1])

def update_no_cache(array, index, value):
    array[index] = value

class LRUCache:
    def __init__(self, capacity=5000):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return None

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = value

    def invalidate(self, index):
        keys_to_remove = [key for key in self.cache if key[0] <= index <= key[1]]
        for key in keys_to_remove:
            self.cache.pop(key, None)

def range_sum_with_cache(array, L, R, cache):
    cached_result = cache.get((L, R))
    if cached_result is not None:
        return cached_result
    result = sum(array[L:R+1])
    cache.put((L, R), result)
    return result

def update_with_cache(array, index, value, cache):
    array[index] = value
    cache.invalidate(index)

def run_performance_test(N=100_000, Q=50_000):
    array = [random.randint(1, 100) for _ in range(N)]
    queries = []
    for _ in range(Q):
        if random.choice(['Range', 'Update']) == 'Range':
            L, R = sorted(random.sample(range(N), 2))
            queries.append(('Range', L, R))
        else:
            index = random.randint(0, N - 1)
            value = random.randint(1, 100)
            queries.append(('Update', index, value))

    start_no_cache = time.time()
    for query in queries:
        if query[0] == 'Range':
            range_sum_no_cache(array, query[1], query[2])
        else:
            update_no_cache(array, query[1], query[2])
    elapsed_no_cache = time.time() - start_no_cache
    logging.info(f"Час виконання без кешування: {elapsed_no_cache:.2f} секунд")

    cache = LRUCache(5000)
    start_with_cache = time.time()
    for query in queries:
        if query[0] == 'Range':
            range_sum_with_cache(array, query[1], query[2], cache)
        else:
            update_with_cache(array, query[1], query[2], cache)
    elapsed_with_cache = time.time() - start_with_cache
    logging.info(f"Час виконання з LRU-кешем: {elapsed_with_cache:.2f} секунд")

def main():
    run_performance_test()

if __name__ == "__main__":
    main()
