"""
file: linkedhashtable.py
description: The LinkedHashTable class implementation
"""

__author__ = [ "Pavan Prabhakar Bhat" ]

# All imports here
import collections.abc
from _operator import index
import set

class LinkedHashTable(set.SetType, collections.abc.Iterable):
    """
    A chained hash table that
      (1) Automatically expands and contracts (by a factor of 2), and
      (2) Recalls the insertion order of its elements
    Terminology:
      number_of_buckets: the number of buckets/entries/chains in the hash
                        table. It determines the range of legal table indices in the
                        implementation. It changes during resizing.
      size: the number of elements the client has added, and not yet
            removed, from the table
      load_factor: ratio of size to number_of_buckets
      load_limit: specifies a range outside of which the table is too
                  full or empty. When load_factor reaches load_limit, the
                  number_of_buckets is doubled. When it gets under (1-load_limit),
                  the number_of_buckets is cut in half.
    Notes:
      No hash table with a number of buckets less than MIN_BUCKETS
      is ever created, regardless of other parts of thi specification.
      This is a hash-based set, not map, so there are only keys, not values.
    """

    __slots__ = 'initial_num_buckets','table', 'number_of_buckets', 'size', 'load_limit', 'load_factor', 'front', 'back'

    def __init__(self, initial_num_buckets=10, load_limit=0.75):
        """
        Create a new empty hash table.
        :param initial_num_buckets: starting number_of_buckets
        :param load_limit: See class documentation above.
        :return:
        """
        self.initial_num_buckets = 10 if initial_num_buckets < 10 else initial_num_buckets
        self.table = self.initial_num_buckets * [ None ]
        self.number_of_buckets = self.initial_num_buckets
        self.load_limit = load_limit
        self.size = 0
        self.load_factor = self.size / self.number_of_buckets
        self.front = None
        self.back = None

    def add(self, obj):
        """
        Insert a new object into the hash table and remember when it was added
        relative to other calls to this method. However, if the object is
        added multiple times, the hash table is left unchanged, including the
        fact that this object's location in the insertion order does not change.
        Double the size of the table if its load_factor exceeds the load_limit.
        :param obj: the object to add
        :return: None
        """
        # found the index of the table using the hashing function
        index = hash_function(obj, self.number_of_buckets)
        # bucket is a node that is used for chaining
        bucket = self.ChainNode( obj )
        if not self.contains(obj):
            # Checks if the object needs to be added as the first element
            if self.front is None:
                self.front = bucket
                self.back = bucket
                self.table[index] = bucket
            else:
                # Checks if the object needs to be added on the table and as the first element of the linked list
                if self.table[index] is None:
                    bucket.prev = self.back
                    self.back.next = bucket
                    self.table[index] = bucket
                    self.back = self.table[index]
                else:
                    # Checks if the object needs to be added in the linked list but not at the first position
                    tempBucket = self.table[index]
                    while tempBucket is not None:
                        tempPrevious = tempBucket
                        tempBucket = tempBucket.chain
                    bucket.prev = self.back
                    self.back.next = bucket
                    tempPrevious.chain = bucket
                    self.back = tempPrevious.chain
            # Increments the size if the object is added
            self.size += 1
            # Checks if rehashing is required during addition of the object
            self.load_factor = self.size / self.number_of_buckets
            if self.load_factor >= self.load_limit:
                self._rehash(self.load_factor)
        else:
            # Raises an exception if the table doesnt contain the object
            raise Exception('The table doesnt contain the object')


    def contains(self, obj):
        """
        Is the given obj in the hash table?
        :param obj:
        :return: True iff obj or its equivalent has been added to this table
        """
        # found the index of the table using the hashing function
        index = hash_function(obj, self.number_of_buckets)
        # bucket is a node that is used for chaining
        bucket = self.table[index]
        while bucket is not None:
            if bucket.key == obj:
                return True
            bucket = bucket.chain
        return False

    def remove(self, obj):
        """
        Remove an object from the hash table (and from the insertion order).
        Resize the table if its size has dropped below
        (1-load_factor)*current_size.
        :param obj: the value to remove; assumes hashing and equality work
        :return:
        """
        # found the index of the table using the hashing function
        index = hash_function(obj, self.number_of_buckets)
        # bucket is a node that is used for chaining
        bucket = LinkedHashTable.ChainNode( obj )
        if self.front is not None:
            if bucket is None:
                raise Exception('Element entered is None')
            if (self.contains(obj)):
                # Checks for the object in the first location
                if self.front.key == bucket.key:
                    if self.front.next is not None:
                        self.front.next.prev = None
                        self.front = self.front.next
                # Checks for the object in the last location
                elif self.back.key == bucket.key:
                    if self.back is not None:
                        self.back.prev.next = None
                        self.back = self.back.prev
                        self.back.chain = None
                else:
                    # Checks if the object exist in the linked chains to the table
                    if self.table[index].key == bucket.key:
                        if self.table[index].next is not None and self.table[index] is not None:
                            self.table[index].prev.next = self.table[index].next
                            self.table[index].next.prev = self.table[index].prev
                            self.table[index] = self.table[index].next
                    else:
                        tempBucket = self.table[index]
                        while tempBucket.key is not bucket.key:
                            tempPrevious = tempBucket
                            tempBucket = tempBucket.chain
                        if tempBucket is not None:
                            tempBucket.prev.next = tempBucket.next
                            tempBucket.next.prev = tempBucket.prev
                            tempPrevious.chain = tempBucket.chain
                # Decrements the size if the object is removed
                self.size -= 1
            else:
                raise Exception('Element does not exist in the table')
        else:
            raise Exception('List is empty')
        # Checks if rehashing is required after removing the object
        self.load_factor = self.size / self.number_of_buckets
        if self.number_of_buckets > 10:
            if self.load_factor < (1-self.load_limit):
                self._rehash(self.load_factor)

    def __iter__( self ):
        """
        Build an iterator.
        :return: an iterator for the current elements in the set
        """
        # Starts iteration from the first element
        i = self.front
        j = 0
        while j < self.size:
            # returns the value if the object is iterated
            yield i.key
            i = i.next
            j += 1

    # Inner class used to create a chaining effect on the hashset using a linked list structure.
    class ChainNode:

        __slots__ = 'prev', 'next', 'chain', 'key'

        def __init__(self, key):
            self.prev = None
            self.next = None
            self.chain = None
            self.key = key

        def __str__( self ):
            """ Return a string representation of the contents of
                this node. The link is not included.
            """
            # required to print the value in the nodes
            return "(" + str( self.key ) + ")"

    def _rehash( self, load_factor ):
        """
        Rebuild the map in a larger table. The current map is not changed
        in any way that can be seen by its clients, but internally its table is
        grown.
        :return: None
        """
        # Checks if the rehashing needs to be done to increment or decrement the size of the table
        if load_factor >= self.load_limit:
            new_cap = 2 * self.number_of_buckets
            print( "Rehashing from", self.number_of_buckets, "to", new_cap )
        elif load_factor < self.load_limit:
            new_cap = self.number_of_buckets // 2
            print( "Rehashing from", self.number_of_buckets, "to", new_cap )
        # Reinitialized the table descriptors
        new_table = new_cap * [None]
        self.table = new_table
        front_new = self.front
        self.front =None
        self.back = None
        self.size = 0
        self.number_of_buckets = new_cap

        while front_new is not None:
            self.add(front_new.key)
            front_new = front_new.next

    def length(self):
        """
        Returns the size of the table or the capacity
        :return:
        """
        return self.number_of_buckets


def hash_function(obj, n):
    """
    The hash function which is used to generate hashcode for the Hash table.
    :param obj: The object of which the hashcode needs to be generated
    :param n: The total capacity of the linkedHashTable
    :return: hashcode
    """
    hashcode = hash( obj ) % n
    return hashcode