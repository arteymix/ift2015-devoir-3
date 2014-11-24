"""Code Python pour le cours IFT2015
   Mise à jour par François Major le 23 mars 2014.
"""

#ADT PriorityQueue
class PriorityQueue:

    #Abstract and basic class for PriorityQueue
    #From Goodrich, Tamassia & Goldwasser

    #Nested class for the items
    class _Item:
        #efficient composite to store items
        __slots__ = '_key', '_value'

        def __init__( self, k, v ):
            self._key = k
            self._value = v

        def __lt__( self, other ):
            return self._key < other._key

        def __gt__( self, other ):
            return self._key > other._key

        def __str__( self ):
            return "(" + str( self._key ) + "," + str( self._value ) + ")"

    #ADT and basic methods

    def __init__( self ):
        pass

    def __len__( self ):
        pass

    def __str__( self ):
        if self.is_empty():
            return "[]"
        pp = "["
        for item in self:
            pp += str( item )
        pp += "]"
        return pp

    def is_empty( self ):
        return len( self ) == 0

    def min( self ):
        pass

    def add( self, k, x ):
        pass

    def remove_min( self ):
        pass
            
"""unit testing
"""
if __name__ == '__main__':

    print( "PriorityQueue unit testing..." )



    print( "End of testing." )
