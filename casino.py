#Question TP    - utilisation de set pour détecter les doublons == legit?
#                   -
#To do :        - implanter table queue (hash de {table:queue}? une seul queue de tuples (player, table)?...)
#                  -

from benchpy import benchmarked

class Queue:
    """
    Cette file est composée d'éléments simplement chaînées.

    La plupart des opérations sont réduites à O(1).
    """
    class Element:
        """Élément de la file"""
        def __init__(self, name, next=None):
            self.value = name
            self.next = next

        def __len__(self):
            """Calcule récursivement la longueur de la liste chaînée"""
            if self.next is None:
                return 1
            return 1 + len(self.next)

    def __init__(self, iterable=[]):
        self.first = None
        self.last = None
        for item in iterable:
            self.enqueue(item)

    def __len__(self):
        """Calcule la longueur de la liste en O(n)"""
        if self.first is None:
            return 0
        return len(self.first)

    def __bool__(self):
        """Test si la liste est vide en O(1)"""
        return self.first is None

    @benchmarked()
    def enqueue(self, item):
        """Ajoute un élément à la fin en O(1)"""
        self.last = self._insert(item, self.last)

    @benchmarked()
    def dequeue(self):
        """Enlève un élément au début en O(1)"""
        if self.first:
            e, self.first = self.first, self.first.next
            return e.value
        raise IndexError # la file est vide

    def _insert(self, item, previous=None):
        """Insère à n'importe quel point en O(1)"""
        if previous is None:
            self.first = Queue.Element(item, self.first)
            return self.first
        else:
            previous.next = Queue.Element(item, previous.next)
            return previous.next

class CasinoQueue:
    """
    Représentation du casino.

    Ce casino est un ensemble de 3 files abstrait comme une seule file de
    priorité.

    Les opérations de base sont O(1).
    """
    def __init__(self, players=[]):
        """Initialise un casino avec des joueurs initiaux"""
        self.players = {player for player in players} # set de tout les players
        self.broken_queue = Queue()
        self.table_queue = Queue()
        self.normal_queue = Queue()
        for player in players:
            self.enqueue(player)

    def __contains__(self, player):
        """
        Test si un joueur est dans le casino en O(1).

        Le casino conserve un ensemble haché pour vérifier rapidement si un
        joueur s'y trouve.

        Ex.
        if 'martin' in casino:
            pass
        """
        return player in self.players

    def __len__(self):
        """Nombre de joueurs dans le casino"""
        return len(self.players)

    @benchmarked()
    def enqueue(self, name, table=None, priority=0):
        if priority:
            #Le joueur vient d'une table brisee
            self.broken_queue.enqueue(name)
        elif table:
            pass
            #sil y a une table, c'est que le joueur a fait une demande de changement de table
            #self.table_queue       (name, table)
        else:
            if name in self.players :
                raise AttributeError
            self.players.add(name)
            self.normal_queue.enqueue(name)

    @benchmarked()
    def dequeue(self):
        if self.broken_queue:
            return self.broken_queue.dequeue
#       elif not self.table_queue:
        elif self.normal_queue:
            return self.normal_queue.dequeue
        else:
            raise IndexError

class Table:
    #initialplayers et players est l'ensembles des joueurs (leur id est une string) qui sont assis a la table
    def __init__ (self, min_players, max_players, initialplayers=None):
        self.players = initialplayers
        self.min_players = min_players
        self.max_players = max_players

# un casino est un ensemble de tables avec une file d'attente
casino = {'tables': [Table(i,2*i) for i in range(2,5)], 'queue': CasinoQueue()}

import unittest

class QueueTest(unittest.TestCase):
    """Test les fonctionnalités de base de la Queue"""
    def setUp(self):
        self.queue = Queue()

    def test_length(self):
        self.assertEqual(0, len(self.queue))

        self.queue.enqueue(4)
        self.assertEqual(1, len(self.queue))

    def test_enqueue(self):
        """ajout d'un item au début de la file"""
        self.queue.enqueue(5)
        self.assertEqual(1, len(self.queue))
        self.assertEqual(5, self.queue.dequeue())

    def test_dequeue(self):
        """retrait d'un item à la fin de la file"""
        for i in range(5):
            self.queue.enqueue(i)

        self.assertEqual(5, len(self.queue))

        for i in range(5):
            self.assertEqual(i, self.queue.dequeue())

class CasinoQueueTest(unittest.TestCase):
    """Test le fonctionnement du Casino"""
    def setUp(self):
        self.casino = CasinoQueue()

if  __name__ == '__main__':
    unittest.main()

    # run benchmarks
    benchmarked.results = {}
