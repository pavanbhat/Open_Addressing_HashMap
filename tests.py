""" 
file: tests.py
description: Verify the LinkedHashTable class implementation
"""

__author__ = [ "Pavan Prabhakar Bhat" ]

from linkedhashtable import LinkedHashTable

def print_set( a_set ):
    for word in a_set: # uses the iter method
        print( word, end=" " )
    print()

# A simple test case for which 2 elements have been removed from the array and also several words have been added
def test0():
    table = LinkedHashTable( 100 )
    table.add( "to" )
    table.add( "do" )
    table.add( "is" )
    table.add( "to" )
    table.add( "be" )

    print_set( table )

    print( "'to' in table?", table.contains( "to" ) )
    table.remove( "to" )
    print( "'to' in table?", table.contains( "to" ) )
    print_set( table )

    print( "'is' in table?", table.contains( "is" ) )
    table.remove( "is" )
    # print(table.length())
    print( "'is' in table?", table.contains( "is" ) )
    print_set( table )

# Removes the first element in the array and also tries removing an element which is not in the list
# due to which the program throws an error.
def test1():
    table = LinkedHashTable( 100 )
    table.add('batman')
    table.add('has')
    table.add('lots')
    table.add('of')
    table.add('gizmos')
    table.add('in')
    table.add('his')
    table.add('belt')

    print_set(table)
    print( "'batman' in table?", table.contains( "batman" ) )
    table.remove( "batman" )
    print(table.length())
    print( "'batman' in table?", table.contains( "batman" ) )
    print_set(table)

    print( "'hello' in table?", table.contains( "hello" ) )
    table.remove( "hello" )
    print_set(table)


# This test case removes the last element in the sentence and prints the updated last element
def test2():
    table = LinkedHashTable( 100 )
    table.add( "I" )
    table.add( "am" )
    table.add( "a" )
    table.add( "Hero" )
    table.add( "from" )
    table.add( "this")
    table.add( "generation")

    print_set( table )

    print( table.back.key + " in table?", table.contains( table.back.key ) )
    last_element = table.back.key
    table.remove( last_element )
    print( last_element + " in table?", table.contains( last_element ) )
    print_set( table )
    print( table.back.key + " is the new last element in the table " )



if __name__ == '__main__':
    # test0()
    # test1()
    test2()

