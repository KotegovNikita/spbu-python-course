from collections.abc import MutableMapping
from typing import Any, Iterator, Optional
from multiprocessing import Manager
from multiprocessing.managers import SyncManager


class ThreadSafeHashTable(MutableMapping):
    """
    Thread-safe hash table implementation with chaining for collision resolution.

    Uses multiprocessing.Manager for shared state between processes.
    All operations are protected by locks to prevent race conditions.
    """

    _shared_manager: Optional[SyncManager] = None

    @classmethod
    def get_manager(cls) -> SyncManager:
        """
        Get or create shared Manager instance.

        Returns:
            SyncManager: Shared manager for multiprocessing
        """
        if cls._shared_manager is None:
            cls._shared_manager = Manager()
        return cls._shared_manager

    def __init__(
        self, capacity: int = 16, manager: Optional[SyncManager] = None
    ) -> None:
        """
        Initialize thread-safe hash table.

        Args:
            capacity: Initial number of buckets (default: 16)
            manager: Optional existing Manager instance for shared state
        """
        if manager is None:
            manager = self.get_manager()

        self._manager = manager
        self._capacity = manager.Value("i", capacity)
        self._size = manager.Value("i", 0)
        self._buckets = manager.list([manager.list() for _ in range(capacity)])
        self._lock = manager.Lock()

    def _hash(self, key: Any) -> int:
        """
        Calculate bucket index for given key.

        Args:
            key: Key to hash

        Returns:
            int: Bucket index in range [0, capacity)
        """
        return hash(key) % self._capacity.value

    def _resize(self) -> None:
        """
        Double the capacity and rehash all existing items.

        Called automatically when load factor exceeds 0.75.
        """
        old_buckets = list(self._buckets)
        old_capacity = self._capacity.value
        new_capacity = old_capacity * 2

        self._capacity.value = new_capacity
        self._buckets[:] = [self._manager.list() for _ in range(new_capacity)]
        self._size.value = 0

        for bucket in old_buckets:
            for key, value in list(bucket):
                self[key] = value

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Set item in hash table.

        Args:
            key: Key to set
            value: Value to associate with key
        """
        with self._lock:
            index = self._hash(key)
            bucket = self._buckets[index]

            for i, (k, _) in enumerate(list(bucket)):
                if k == key:
                    bucket[i] = (key, value)
                    return

            bucket.append((key, value))
            self._size.value += 1

            if self._size.value / self._capacity.value > 0.75:
                self._resize()

    def __getitem__(self, key: Any) -> Any:
        """
        Get item from hash table.

        Args:
            key: Key to retrieve

        Returns:
            Any: Value associated with key

        Raises:
            KeyError: If key not found in table
        """
        with self._lock:
            index = self._hash(key)
            for k, v in list(self._buckets[index]):
                if k == key:
                    return v
            raise KeyError(key)

    def __delitem__(self, key: Any) -> None:
        """
        Delete item from hash table.

        Args:
            key: Key to delete

        Raises:
            KeyError: If key not found in table
        """
        with self._lock:
            index = self._hash(key)
            bucket = self._buckets[index]

            for i, (k, _) in enumerate(list(bucket)):
                if k == key:
                    del bucket[i]
                    self._size.value -= 1
                    return

            raise KeyError(key)

    def __contains__(self, key: Any) -> bool:
        """
        Check if key exists in hash table.

        Args:
            key: Key to check

        Returns:
            bool: True if key exists, False otherwise
        """
        with self._lock:
            index = self._hash(key)
            return any(k == key for k, _ in list(self._buckets[index]))

    def __len__(self) -> int:
        """
        Get number of items in hash table.

        Returns:
            int: Number of key-value pairs
        """
        with self._lock:
            return self._size.value

    def __iter__(self) -> Iterator[Any]:
        """
        Iterate over keys in hash table.

        Yields:
            Any: Keys in hash table
        """
        with self._lock:
            for bucket in self._buckets:
                for key, _ in list(bucket):
                    yield key

    def __repr__(self) -> str:
        """
        Get string representation of hash table.

        Returns:
            str: String representation with all key-value pairs
        """
        with self._lock:
            return repr(dict(self.items()))
