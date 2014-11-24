"""Code Python pour le cours IFT2015
   Mise à jour par François Major le 23 mars 2014.
"""

from PriorityQueue import PriorityQueue

#ArrayHeapPriorityQueue
class ArrayHeapPriorityQueue( PriorityQueue ):

    def __init__( self ):
        self._Q = []

    def __len__( self ):
        return len( self._Q )

    def __getitem__( self, i ):
        return self._Q[i]

    def is_empty( self ):
        return len( self ) == 0

    def _parent( self, j ):
        return (j-1) // 2

    def _left( self, j ):
        return 2*j + 1

    def _right( self, j ):
        return 2*j + 2

    def _has_left( self, j ):
        return self._left( j ) < len( self )

    def _has_right( self, j ):
        return self._right( j ) < len( self )

    def min( self ):
        if self.is_empty():
            return False
        #min is in the root
        return self._Q[0]

    def _swap( self, i, j ):
        tmp = self._Q[i]
        self._Q[i] = self._Q[j]
        self._Q[j] = tmp

    def _swim( self, j ):
        parent = self._parent( j )
        if j > 0 and self._Q[j] < self._Q[parent]:
            self._swap( j, parent )
            self._swim( parent )

    def _sink( self, j ):
        if self._has_left( j ):
            left = self._left( j )
            small_child = left
            if self._has_right( j ):
                right = self._right( j )
                if self._Q[right] < self._Q[left]:
                    small_child = right
            if self._Q[small_child] < self._Q[j]:
                self._swap( j, small_child )
                self._sink( small_child )

    def add( self, k, x ):
        #in O(log n)
        item = self._Item( k, x )
        self._Q.append( item )
        #swim the new item in O(log n)
        self._swim( len(self)-1 )
        #return the new item
        return item

    def remove_min( self ):
        if self.is_empty():
            return False
        #min is at the root
        the_min = self._Q[0]
        #move the last item to the root
        self._Q[0] = self._Q[len(self)-1]
        #delete the last item
        del self._Q[len(self)-1]
        if self.is_empty():
            return the_min
        #sink the new root in O(log n)
        self._sink( 0 )
        #return the min
        return the_min

            
"""unit testing
"""
if __name__ == '__main__':

    print( "ArrayHeapPriorityQueue unit testing..." )

    testQ = ArrayHeapPriorityQueue()
    testQ.add( 5, 'A' )
    testQ.add( 9, 'C' )
    testQ.add( 3, 'B' )
    testQ.add( 7, 'D' )
    print( testQ )
    print( "min = ", testQ.min() )
    print( "len = ", len( testQ ) )
    print( "empty?", testQ.is_empty() )

    testQ.remove_min()
    testQ.remove_min()
    print( testQ )
    print( "min = ", testQ.min() )
    print( "len = ", len( testQ ) )
    print( "empty?", testQ.is_empty() )

    testQ.add( 2, 'AA' )
    print( testQ )
    print( "min = ", testQ.min() )
    print( "len = ", len( testQ ) )
    print( "empty?", testQ.is_empty() )

    testQ.remove_min()
    testQ.remove_min()
    print( testQ )
    print( "min = ", testQ.min() )
    print( "len = ", len( testQ ) )
    print( "empty?", testQ.is_empty() )

    print( testQ.remove_min() )

    print( "End of testing." )
