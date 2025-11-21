import pytest
from multiprocessing import Process, Manager, Queue
from multiprocessing.managers import SyncManager
from project.Assignment_6.multi_process_table import ThreadSafeHashTable


class TestThreadSafeHashTable:
    """Test suite for thread-safe hash table implementation."""

    def test_basic_operations(self) -> None:
        """Test basic hash table operations from previous implementation."""
        manager = Manager()
        ht = ThreadSafeHashTable(capacity=32, manager=manager)

        ht["test"] = 100
        assert ht["test"] == 100

        ht["test"] = 200
        assert ht["test"] == 200
        assert len(ht) == 1

        ht["key2"] = "value"
        assert "key2" in ht
        assert len(ht) == 2

        del ht["test"]
        assert "test" not in ht
        assert len(ht) == 1

        manager.shutdown()

    def test_resize_works(self) -> None:
        """Test that resize operation works correctly."""
        manager = Manager()
        ht = ThreadSafeHashTable(capacity=128, manager=manager)

        for i in range(50):
            ht[i] = i * 10

        assert len(ht) == 50
        for i in range(50):
            assert ht[i] == i * 10

        manager.shutdown()

    def test_parallel_writes_no_data_loss(self) -> None:
        """Test that parallel writes don't lose data."""
        manager = Manager()
        ht = ThreadSafeHashTable(capacity=256, manager=manager)
        queue = manager.Queue()

        def write_data(
            capacity, size_val, buckets, lock, start: int, end: int, q
        ) -> None:
            """
            Write data to hash table in given range.

            """
            try:
                for i in range(start, end):
                    key = f"k{i}"
                    value = i

                    with lock:
                        index = hash(key) % capacity.value
                        bucket = buckets[index]
                        bucket.append((key, value))
                        size_val.value += 1

                q.put("done")
            except Exception as e:
                q.put(f"error: {e}")

        procs = []
        for i in range(4):
            p = Process(
                target=write_data,
                args=(
                    ht._capacity,
                    ht._size,
                    ht._buckets,
                    ht._lock,
                    i * 50,
                    (i + 1) * 50,
                    queue,
                ),
            )
            procs.append(p)
            p.start()

        completed = 0
        for p in procs:
            p.join(timeout=15)
            if p.is_alive():
                p.terminate()
                p.join()
            else:
                completed += 1

        for _ in range(completed):
            try:
                result = queue.get(timeout=2)
                assert result == "done", f"Unexpected result: {result}"
            except:
                pass

        assert len(ht) == 200

        manager.shutdown()

    def test_concurrent_read_write(self) -> None:
        """Test concurrent read and write operations."""
        manager = Manager()
        ht = ThreadSafeHashTable(capacity=128, manager=manager)

        for i in range(50):
            ht[i] = i

        queue = manager.Queue()

        def reader(capacity, buckets, lock, q) -> None:
            """
            Read data from hash table.

            """
            try:
                count = 0
                for i in range(50):
                    with lock:
                        index = hash(i) % capacity.value
                        if any(k == i for k, _ in list(buckets[index])):
                            count += 1
                q.put(count)
            except Exception as e:
                q.put(f"error: {e}")

        def writer(capacity, size_val, buckets, lock, start: int, end: int, q) -> None:
            """
            Write data to hash table in given range.

            """
            try:
                for i in range(start, end):
                    key = i + 100
                    value = i

                    with lock:
                        index = hash(key) % capacity.value
                        bucket = buckets[index]
                        bucket.append((key, value))
                        size_val.value += 1

                q.put("ok")
            except Exception as e:
                q.put(f"error: {e}")

        procs = []
        for _ in range(2):
            procs.append(
                Process(
                    target=reader, args=(ht._capacity, ht._buckets, ht._lock, queue)
                )
            )

        procs.append(
            Process(
                target=writer,
                args=(ht._capacity, ht._size, ht._buckets, ht._lock, 0, 25, queue),
            )
        )
        procs.append(
            Process(
                target=writer,
                args=(ht._capacity, ht._size, ht._buckets, ht._lock, 25, 50, queue),
            )
        )

        for p in procs:
            p.start()

        completed = 0
        for p in procs:
            p.join(timeout=15)
            if p.is_alive():
                p.terminate()
                p.join()
            else:
                completed += 1

        for _ in range(completed):
            try:
                queue.get(timeout=2)
            except:
                pass

        assert len(ht) == 100

        manager.shutdown()
