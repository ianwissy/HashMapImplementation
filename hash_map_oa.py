# Name: Ian Wyse
# OSU Email: wysei@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: March 11, 2022
# Description: Contains classes for implementation of an open addressing hash table object. Contains methods to
# add elements to a hash table, remove them by key, return them by key, determine if a specific key is in the table,
# clear the table, resize the table, and return the load factor and the number of empty buckets in the table.


from a6_include import *


class HashEntry:

    def __init__(self, key: str, value: object):
        """
        Initializes an entry for use in a hash map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.key = key
        self.value = value
        self.is_tombstone = False

    def __str__(self):
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return f"K: {self.key} V: {self.value} TS: {self.is_tombstone}"


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses Quadratic Probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()

        for _ in range(capacity):
            self.buckets.append(None)

        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            out += str(i) + ': ' + str(self.buckets[i]) + '\n'
        return out

    def clear(self) -> None:
        """
        Clears the hash table, emptying all buckets.
        """
        for inx in range(self.capacity):
            self.buckets[inx] = None
        self.size = 0

    def get(self, key: str) -> object:
        """
        Returns the object from the table with key 'key'. If no such object exists, returns None.
        """
        # Get initial hash
        inx_initial = self.hash_function(key)
        for count in range(10 * self.capacity):
            # calculate the index based on the count and the initial hash
            inx = (inx_initial + count ** 2) % self.capacity
            # Return if search results in an empty bucket
            if self.buckets[inx] is None:
                return
            # Return the value if the search results in the correct bucket
            elif self.buckets[inx].key == key and self.buckets[inx].is_tombstone is False:
                return self.buckets[inx].value

    def put(self, key: str, value: object) -> None:
        """
        Adds object with key 'key' and value 'value' to the hash table. If an object with given key already exists,
        updates the table instead. If the load factor of the table is >=.5, doubles the capacity of the table.
        """
        if self.table_load() >= .5:
            self.resize_table(self.capacity * 2)
        inx_initial = self.hash_function(key)
        for count in range(10 * self.capacity):
            inx = (inx_initial + count ** 2) % self.capacity
            # If the bucket is empty or is a tombstone, add the new value
            if self.buckets[inx] is None or self.buckets[inx].is_tombstone is True:
                self.buckets[inx] = HashEntry(key, value)
                self.size += 1
                return
            # If the bucket contains the key, update to the new value
            elif self.buckets[inx].key == key:
                self.buckets[inx].value = value
                return

    def remove(self, key: str) -> None:
        """
        Removes the object with the given key from the table if such an object exists.
        """
        inx_initial = self.hash_function(key)
        for count in range(10 * self.capacity):
            inx = (inx_initial + count ** 2) % self.capacity
            if self.buckets[inx] is None:
                return
            elif self.buckets[inx].key == key and self.buckets[inx].is_tombstone is False:
                self.buckets[inx].is_tombstone = True
                self.size -= 1

    def contains_key(self, key: str) -> bool:
        """
        Returns true if an object with the given key exists in the table, otherwise returns false.
        """
        inx_initial = self.hash_function(key)
        for count in range(10 * self.capacity):
            inx = (inx_initial + count ** 2) % self.capacity
            if self.buckets[inx] is None:
                return False
            elif self.buckets[inx].key == key and self.buckets[inx].is_tombstone is False:
                return True

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the table.
        """
        return self.capacity - self.size

    def table_load(self) -> float:
        """
        Returns the current load factor of the table.
        """
        return self.size / self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the table to a given capacity, rehashing all current elements of the table.
        Will not resize a table to be smaller than its current size.
        """
        # Return immediately if new capacity is impossible
        if new_capacity < 1 or new_capacity < self.size:
            return
        # Copy current table to a temporary location
        temp_table = self.buckets
        temp_capacity = self.capacity
        # Replace current table with an empty table of the correct capacity
        self.capacity = new_capacity
        self.buckets = DynamicArray()
        self.size = 0
        for inx in range(self.capacity):
            self.buckets.append(None)
        # Rehash elements from the temporary table into the new table.
        for inx in range(temp_capacity):
            if temp_table[inx] is not None and temp_table[inx].is_tombstone is not True:
                self.put(temp_table[inx].key, temp_table[inx].value)

    def get_keys(self) -> DynamicArray:
        """
        Returns a dynamic array containing the keys of all objects stored in the hash table.
        """
        key_array = DynamicArray()
        for inx in range(self.capacity):
            if self.buckets[inx] is not None and self.buckets[inx].is_tombstone is False:
                key_array.append(self.buckets[inx].key)
        return key_array


if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    # this test assumes that put() has already been correctly implemented
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
