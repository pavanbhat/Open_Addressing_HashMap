# Open_Addressing_HashMap
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
