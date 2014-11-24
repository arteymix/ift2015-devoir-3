# -*- coding: utf-8 -*-
#
# Ensemble de collections
#
from benchpy import benchmarked

#ADT PriorityQueue
class PriorityQueue:
    """Code Python pour le cours IFT2015
       Mise à jour par François Major le 23 mars 2014.
    """
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

class OrderedList(list):
    """Liste ordonnée"""
    @benchmarked(name='orderedlist-append')
    def append(self, value):
        """Ajout ordonné en O(n)"""
        for i, v in enumerate(self):
            if value <= v:
                self.insert(i, value)
                return
        else:
            list.append(self, value)

    def centile(self, n):
        if n < 0 or n >= 100:
            raise AttributeError
        return self[n // 100 * (len(self) - 1)]

class HeapCentile:
    """
    Utilise deux monceaux pour déterminer le centile d'un ensemble de données
    """
    __slots__ = ['_centile', 'heap_smaller', 'heap_greater']

    def __init__(self, centile):
        # monceaux et liste ordonnée pour calculer les centiles
        self._centile = centile
        self.heap_smaller = ArrayHeapPriorityQueue()
        self.heap_greater = ArrayHeapPriorityQueue()

    def _normalize(self, c):
        """Normalise les deux monceaux autours du centile c"""
        total = len(self.heap_smaller) + len(self.heap_greater)

        a = c // 100 * total

        if len(self.heap_smaller) < a:
            for _ in range(a - len(self.heap_smaller)):
                k, v = self.heap_greater.remove_min()
                self.heap_smaller.add(-k, v)
        elif len(self.heap_smaller) > a:
            for _ in range(len(self.heap_smaller) - a):
                k, v = self.heap_smaller.remove_min()
                self.heap_greater.add(-k, v)

    def centile(self):
        if self.heap_smaller.is_empty() or self.heap_greater.is_empty():
            raise RuntimeError('Les monceaux sont vides.')

        return (self.heap_smaller.min() + self.heap_greater.min()) / 2

    @benchmarked(name='heapcentile-append')
    def append(self, temps):
        """Ajoute une donnée et renormalise autours du centile"""
        if self.heap_greater.is_empty() or temps > self.heap_greater.min():
            self.heap_greater.add(temps, temps)
        else:
            self.heap_smaller.add(-temps, temps)

        self._normalize(self._centile)

class Queue:
    """
    Cette file est composée d'éléments simplement chaînées.

    La plupart des opérations sont réduites à O(1).
    """
    class Element:
        """Élément de la file"""
        __slots__ = ['value', '_next']
        def __init__(self, value, n=None):
            self.value = value
            self._next = n

        def __next__(self):
            return self._next

        def next(self):
            return self._next

    __slots__ = ['first', 'last']

    def __init__(self, iterable=[]):
        self.first = None
        self.last = None
        for item in iterable:
            self.enqueue(item)

    def __iter__(self):
        """
        Les éléments de la file sont directement itérable par __next__, alors il
        suffit de retourner le premier

        Le parcours se fait en O(n).
        """
        element = self.first
        while element is not None:
            yield element.value
            element = element._next

    def __len__(self):
        """Compte la longueur de la file en O(n)"""
        return sum(1 for _ in self)

    def __bool__(self):
        """Test si la liste est vide en O(1)"""
        return self.first is not None

    @benchmarked()
    def enqueue(self, item):
        """Ajoute un élément à la fin en O(1)"""
        element = Queue.Element(item)

        if self.last is None:
            assert self.first is None
            self.first = element
            self.last = element
            assert self.first is self.last
        else:
            self.last._next = element
            self.last = element

    @benchmarked()
    def dequeue(self):
        """Enlève un élément au début en O(1)"""
        if self.first is None:
            assert self.first is self.last
            raise IndexError # la file est vide

        element, self.first = self.first, self.first._next

        if element is self.last:
            self.last = None

        return element.value

    @benchmarked()
    def remove(self, item):
        """Enlève la première occurence de item dans la file en O(n)"""
        before = None
        element = self.first
        while element:
            if item == element.value:
                # début ou fin
                if element is self.first:
                    self.first = element._next
                if element is self.last:
                    self.last = before

                #
                if before is not None:
                    before._next = element._next

                return element
            before = element
            element = next(element)
