from collections.abc import MutableMapping
from typing import Any, Iterator


class HashTable(MutableMapping):
    """Hash table with chaining for collision resolution."""

    def __init__(self, capacity: int = 16) -> None:
        """
        Initialize hash table.
        Args:
            capacity: Initial number of buckets
        """
        self._capacity = capacity
        self._size = 0
        self._buckets: list[list[tuple[Any, Any]]] = [[] for _ in range(capacity)]

    def _hash(self, key: Any) -> int:
        """
        Calculate bucket index for key.
        Args:
            key: Key to hash

        Returns:
            Bucket index
        """
        return hash(key) % self._capacity

    def _resize(self) -> None:
        """Double capacity and rehash all items."""
        old_buckets = self._buckets
        self._capacity *= 2
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0

        for bucket in old_buckets:
            for key, value in bucket:
                self[key] = value

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Set item in hash table.
        Args:
            key: Key to set
            value: Value to associate with key
        """
        index = self._hash(key)
        bucket = self._buckets[index]

        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self._size += 1
        if self._size / self._capacity > 0.75:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        """
        Get item from hash table.
        Args:
            key: Key to retrieve
        Returns:
            Value associated with key
        Raises:
            KeyError: If key not found
        """
        index = self._hash(key)

        for k, v in self._buckets[index]:
            if k == key:
                return v

        raise KeyError(key)

    def __delitem__(self, key: Any) -> None:
        """
        Delete item from hash table.
        Args:
            key: Key to delete
        Raises:
            KeyError: If key not found
        """
        index = self._hash(key)
        bucket = self._buckets[index]

        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self._size -= 1
                return

        raise KeyError(key)

    def __contains__(self, key: Any) -> bool:
        """
        Check if key exists in hash table.
        Args:
            key: Key to check
        Returns:
            True if key exists, False otherwise
        """
        index = self._hash(key)
        return any(k == key for k, _ in self._buckets[index])

    def __len__(self) -> int:
        """
        Get number of items.

        Returns:
            Number of key-value pairs
        """
        return self._size

    def __iter__(self) -> Iterator[Any]:
        """
        Iterate over keys.

        Yields:
            Keys in hash table
        """
        for bucket in self._buckets:
            for key, _ in bucket:
                yield key

    def __repr__(self) -> str:
        """
        String representation.

        Returns:
            String with all key-value pairs
        """
        return repr(dict(self.items()))
