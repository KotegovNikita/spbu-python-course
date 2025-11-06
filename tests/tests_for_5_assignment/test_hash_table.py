import pytest
from project.Assignment_5.hash_table import HashTable


def test_basic_operations():
    """Test basic set and get operations."""
    ht = HashTable()
    ht["x"] = 1
    ht["y"] = 2
    assert ht["x"] == 1
    assert len(ht) == 2


def test_update_existing_key():
    """Test updating existing key."""
    ht = HashTable()
    ht["x"] = 1
    ht["x"] = 10
    assert ht["x"] == 10
    assert len(ht) == 1


def test_membership():
    """Test 'in' operator."""
    ht = HashTable()
    ht["x"] = 1
    assert "x" in ht
    assert "z" not in ht


def test_deletion():
    """Test deleting items."""
    ht = HashTable()
    ht["x"] = 1
    ht["y"] = 2
    del ht["x"]
    assert "x" not in ht
    assert len(ht) == 1


def test_key_error():
    """Test KeyError on missing key."""
    ht = HashTable()
    with pytest.raises(KeyError):
        _ = ht["nonexistent"]


def test_iteration():
    """Test iterating over keys."""
    ht = HashTable()
    ht["a"] = 1
    ht["b"] = 2
    ht["c"] = 3
    keys = set(ht.keys())
    assert keys == {"a", "b", "c"}


def test_collision_and_resize():
    """Test collision handling and automatic resize."""
    ht = HashTable(capacity=4)
    for i in range(20):
        ht[f"key{i}"] = i

    assert len(ht) == 20
    for i in range(20):
        assert ht[f"key{i}"] == i


def test_different_key_types():
    """Test different key types."""
    ht = HashTable()
    ht[42] = "int key"
    ht["str"] = "string key"
    ht[(1, 2)] = "tuple key"

    assert ht[42] == "int key"
    assert ht["str"] == "string key"
    assert ht[(1, 2)] == "tuple key"
