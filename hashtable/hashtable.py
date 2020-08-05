class HashTableEntry:
    """
    Linked List hash table key/value pair
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8

class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys
    """
    def __init__(self, capacity=8):
        # capacity dafault
        if capacity < MIN_CAPACITY:
            capacity = MIN_CAPACITY
        self.capacity = capacity
        self.storage = [None] * self.capacity
        self.count = 0

    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)
        One of the tests relies on this.
        """
        return self.capacity

    def get_load_factor(self):
        """
        Return the load factor for this hash table.
        """
        # (# of items in hash table) / (total # of slots)
        return self.count / self.capacity

    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit
        """
        # constants 64 bit
        FNV_prime = 1099511628211
        offset_basis = 14695981039346656037
        
        # function
        hash = offset_basis 
        for character in key:
            hash = hash * FNV_prime
            hash = hash ^ ord(character)
        return hash

    def djb2(self, key):
        """
        DJB2 hash, 32-bit
        """
        # function
        hash = 5381
        for character in key:
            hash = (hash * 33) + ord(character)
        return hash

    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        #return self.fnv1(key) % self.capacity
        return self.djb2(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.
        Hash collisions should be handled with Linked List Chaining.
        """
        # hash key & get index
        index = self.hash_index(key)
        # create node instance
        new_node = HashTableEntry(key, value)
        # if list exist at index
        node_list = self.storage[index]
        if self.storage[index] != None:
            # if key exist, replace value
            self.storage[index] = new_node
            self.storage[index].next = node_list
        # else add node to head
        else:
            self.storage[index] = new_node
        # incease count
        self.count +=1
  
    def delete(self, key):
        """
        Remove the value stored with the given key.
        Print a warning if the key is not found.
        """
        # hash key & get index
        index = self.hash_index(key) 
        count = self.count
        # if only one entry in list
        if self.storage[index].key == key:
            self.storage[index] = self.storage[index].next 
            self.count -= 1 
        else:
            # go through entire list
            current = self.storage[index]
            prev = None
            while current != None:
                if current.key == key:
                    prev.next = current.next
                    self.count -= 1
                    return
                prev = current
                current = current.next

        if count == self.count:
            print(f"Key '{key}' is not in hashtable")

    def get(self, key):
        """
        Retrieve the value stored with the given key.
        Returns None if the key is not found.
        """
        # hash key & get index
        index = self.hash_index(key)
        current = self.storage[index]
        # search for key
        while current != None:
            if current.key == key:
                return current.value
            current = current.next
        return None


    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.
        """
        # temp store old data
        old_storage = self.storage.copy()
        # new blank storage/ update capacity/ reset count
        self.capacity = new_capacity
        self.storage = [None] * self.capacity
        self.count = 0

        # iterate through old array
        for index in range(len(old_storage)):
            # and iterate old linked lists
            current = old_storage[index]
            while current != None:
                # insert into new array / increse count
                self.put(current.key, current.value)
                current = current.next




if __name__ == "__main__":

    # table = HashTable()
    # table.put("avery","quinn")
    # table.put("aveyr","quinn")
    # table.delete("avery")
    # table.delete("avyer")
    # print(table.storage)
    # print(table.count)

    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))
    
    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")
