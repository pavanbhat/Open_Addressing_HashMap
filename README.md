# Open_Addressing_HashMap


A chained hash table that
      
(1) Automatically expands and contracts (by a factor of 2), and
      
(2) Recalls the insertion order of its elements
    
Terminology:
      
	number_of_buckets: the number of buckets/entries/chains in the hash table. It determines the range of legal table indices in the
			   implementation. It changes during resizing.
			   
      	size: the number of elements the client has added, and not yet removed, from the table
      
	load_factor: ratio of size to number_of_buckets
      
	load_limit: specifies a range outside of which the table is too full or empty. When load_factor reaches load_limit, the
	            number_of_buckets is doubled. When it gets under (1-load_limit), the number_of_buckets is cut in half.
   

Notes:
     
No hash table with a number of buckets less than MIN_BUCKETS is ever created, regardless of other parts of thi specification.
This is a hash-based set, not map, so there are only keys, not values.

3.1 Design Constraints

The add, contains, and remove methods should all run in O (1) time (assuming not much clustering due to excessive collisions). This means no linear searches besides the small chains of entries at specific “bucket” locations in the hash table. (Of course the iterator method is linear.)
The design is not built with, or uses the Python library, additional data structures beyond the list needed for the basic hash table implementation. For example, no parallel arrays or separate linked lists.
The data structure design is to build a chained hash table with keys only, no values, and the entry nodes have two additional references: previous and link(next) node links. This means that the ordering is done using the technique of a doubly linked list that overlays on top of the existing nodes needed for the bucket chains.

3.2  Testing

There are 3 additional non-trivial test cases and add them to the provided tests.py file. 
Each test must be distinct from the others in terms of what it demonstrates.
There is the beginning of a test program file available for you to use for adding test functions.
