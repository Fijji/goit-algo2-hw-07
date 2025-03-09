import timeit
import matplotlib.pyplot as plt
from functools import lru_cache
import pandas as pd
import logging

class FibonacciPerformanceTest:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
    logger = logging.getLogger(__name__)

    class SplayTreeNode:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.left = None
            self.right = None

    class SplayTree:
        def __init__(self):
            self.root = None

        def _splay(self, root, key):
            if root is None or root.key == key:
                return root

            if key < root.key:
                if root.left is None:
                    return root
                if key < root.left.key:
                    root.left.left = self._splay(root.left.left, key)
                    root = self._rotate_right(root)
                elif key > root.left.key:
                    root.left.right = self._splay(root.left.right, key)
                    if root.left.right:
                        root.left = self._rotate_left(root.left)
                return self._rotate_right(root) if root.left else root

            else:
                if root.right is None:
                    return root
                if key > root.right.key:
                    root.right.right = self._splay(root.right.right, key)
                    root = self._rotate_left(root)
                elif key < root.right.key:
                    root.right.left = self._splay(root.right.left, key)
                    if root.right.left:
                        root.right = self._rotate_right(root.right)
                return self._rotate_left(root) if root.right else root

        def _rotate_right(self, root):
            new_root = root.left
            root.left = new_root.right
            new_root.right = root
            return new_root

        def _rotate_left(self, root):
            new_root = root.right
            root.right = new_root.left
            new_root.left = root
            return new_root

        def search(self, key):
            self.root = self._splay(self.root, key)
            return self.root.value if self.root and self.root.key == key else None

        def insert(self, key, value):
            if self.root is None:
                self.root = FibonacciPerformanceTest.SplayTreeNode(key, value)
                return

            self.root = self._splay(self.root, key)
            if self.root.key == key:
                return

            new_node = FibonacciPerformanceTest.SplayTreeNode(key, value)
            if key < self.root.key:
                new_node.right = self.root
                new_node.left = self.root.left
                self.root.left = None
            else:
                new_node.left = self.root
                new_node.right = self.root.right
                self.root.right = None
            self.root = new_node

    @lru_cache(maxsize=128)
    def fibonacci_lru(n):
        if n < 2:
            return n
        return FibonacciPerformanceTest.fibonacci_lru(n - 1) + FibonacciPerformanceTest.fibonacci_lru(n - 2)

    def fibonacci_splay(n, tree):
        if n < 2:
            return n
        cached_value = tree.search(n)
        if cached_value is not None:
            return cached_value
        result = FibonacciPerformanceTest.fibonacci_splay(n - 1, tree) + FibonacciPerformanceTest.fibonacci_splay(n - 2, tree)
        tree.insert(n, result)
        return result

    def measure_time(method, n, tree=None):
        if method == "lru":
            return timeit.timeit(lambda: FibonacciPerformanceTest.fibonacci_lru(n), number=1)
        elif method == "splay":
            return timeit.timeit(lambda: FibonacciPerformanceTest.fibonacci_splay(n, tree), number=1)

    def main():
        FibonacciPerformanceTest.logger.info("Test LRU Cache vs Splay Tree.")
        test_values = list(range(0, 951, 50))
        lru_times = []
        splay_times = []

        for n in test_values:
            tree = FibonacciPerformanceTest.SplayTree()
            lru_time = FibonacciPerformanceTest.measure_time("lru", n)
            splay_time = FibonacciPerformanceTest.measure_time("splay", n, tree)
            lru_times.append(lru_time)
            splay_times.append(splay_time)
            FibonacciPerformanceTest.logger.info(f"Fibonacci({n}): LRU Cache = {lru_time:.6f}s, Splay Tree = {splay_time:.6f}s")

        plt.figure(figsize=(10, 5))
        plt.plot(test_values, lru_times, label="LRU Cache", marker="o")
        plt.plot(test_values, splay_times, label="Splay Tree", marker="s")
        plt.xlabel("n (номер числа Fibonacci)")
        plt.ylabel("Час виконання (секунди)")
        plt.title("LRU Cache vs Splay Tree")
        plt.legend()
        plt.grid()
        plt.show()

        df = pd.DataFrame({"n": test_values, "LRU Cache Time (s)": lru_times, "Splay Tree Time (s)": splay_times})
        print(df.to_string(index=False))
        FibonacciPerformanceTest.logger.info("The end.")

    class TestFibonacciPerformance:
        def test_lru_cache(self):
            FibonacciPerformanceTest.logger.info("Test LRU Cache")
            assert FibonacciPerformanceTest.fibonacci_lru(10) == 55, "Error in fibonacci_lru(10)"
            assert FibonacciPerformanceTest.fibonacci_lru(20) == 6765, "Error in fibonacci_lru(20)"
            FibonacciPerformanceTest.logger.info("Test LRU Cache completed.")

        def test_splay_tree(self):
            FibonacciPerformanceTest.logger.info("Test Splay Tree")
            tree = FibonacciPerformanceTest.SplayTree()
            assert FibonacciPerformanceTest.fibonacci_splay(10, tree) == 55, "Error in fibonacci_splay(10)"
            assert FibonacciPerformanceTest.fibonacci_splay(20, tree) == 6765, "Error in fibonacci_splay(20)"
            FibonacciPerformanceTest.logger.info("Test Splay Tree completed.")

if __name__ == "__main__":
    FibonacciPerformanceTest.main()

    tester = FibonacciPerformanceTest.TestFibonacciPerformance()
    tester.test_lru_cache()
    tester.test_splay_tree()
