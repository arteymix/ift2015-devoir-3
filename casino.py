#!/usr/local/env python
# -*- coding: utf-8 -*-
# Question TP    - utilisation de set pour détecter les doublons == legit?
#                   -
#To do :        - implanter table queue (hash de {table:queue}? une seul queue de tuples (player, table)?...)
#                  -

import string
import random
import heapq
from benchpy import benchmarked
from itertools import chain
import time

from ArrayHeapPriorityQueue import ArrayHeapPriorityQueue

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
        def __init__(self, value, n=None):
            self.value = value
            self._next = n

        def __next__(self):
            return self._next

        def next(self):
            return self._next

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

class CasinoQueue:
    """
    Représentation du casino.

    Ce casino est un ensemble de 3 files abstrait comme une seule file de
    priorité.

    Les opérations de base sont O(1).
    """
    def __init__(self, players=set(), centile=OrderedList()):
        """Initialise un casino avec des joueurs initiaux"""
        self.players = set() # set de tout les players

        self._centile = centile

        # files
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

    def __iter__(self):
        """
        Itère à travers toutes les files du casino en chaînant les itérateurs
        sur chaque files.

        Itérer chaque file est dans l'ordre O(n) et itérer sur 3 files chaînées
        par chain est dans l'ordre de O(j + k + l).
        """
        return chain(self.broken_queue, self.table_queue, self.normal_queue)

    @benchmarked()
    def enqueue(self, name, table=None, broken=False):
        if name in self.players:
            raise AttributeError("Quelqu'un dans la file porte déjà ton nom, tu vas attendre mec.")

        if broken:
            # Le joueur vient d'une table brisee
            self.broken_queue.enqueue((name, table, time.time()))
        elif table:
            self.table_queue.enqueue((name, table, time.time()))
        else: # le joueur se rajoute au casino
            self.normal_queue.enqueue((name, table, time.time()))

        # ajout du joueur à l'index des joueurs dans la file
        self.players.add(name)

    @benchmarked()
    def dequeue(self, table=None):
        """
        Dequeue un joueur de la file du casino lorsque qu'une table se libère.
        """
        if self.broken_queue: # file brisée
            joueur, table, temps = self.broken_queue.dequeue()

            # statistique
            self._centile.append(time.time() - temps)
            return joueur

        elif table: # file de table
            for joueur, t, temps in self.table_queue:
                if t is table:
                    # statistique
                    self.broken_queue.remove((joueur, t, temps))
                    self._centile.append(time.time() - temps)
                    return joueur

        joueur, table, temps = self.normal_queue.dequeue()

        # statistiques...
        self._centile.append(time.time() - temps)
        return joueur

    @benchmarked()
    def centile(self, c):
        return self._centile.centile(c)

class Table(set):
    """
    La table est un ensemble de joueurs avec des bornes minimales et maximales.

    players est un itérable qui popule le set initial.
    """
    #initialplayers et players est l'ensembles des joueurs (leur id est une string) qui sont assis a la table
    def __init__(self, players, min_players=4, max_players=8):
        if not min_players <= len(players) <= max_players:
            raise AttributeError('Le nombre de joueurs doit être entre {} et {} inclusivement.'.format(min_players, max_players))
        self.min_players = min_players
        self.max_players = max_players

        # ajout des joueurs dans l'ensemble
        set.__init__(self, players)

def random_players(count=10):
    """Génère un ensemble de joueurs aléatoires"""
    return {''.join(random.choice(string.ascii_letters) for _ in range(random.randint(3, 10))).capitalize() for _ in range(count)}

# un casino est un ensemble de tables avec une file d'attente
casino = {'tables': [Table(random_players(2 * i), i, 3 * i) for i in range(2, 5)], 'queue': CasinoQueue()}
