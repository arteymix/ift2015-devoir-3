# -*- coding: utf-8 -*-

import time
import unittest

from casino import CasinoQueue, Table, random_players

class CasinoQueueTest(unittest.TestCase):
    """Test le fonctionnement du Casino"""
    def test_centile(self):
        casino = CasinoQueue()
        tables = [Table(['Alfred', 'Jean', 'Harry', 'Diego']) for _ in range(10)]

        for player in random_players(50):
            casino.enqueue(player)

        self.assertEqual(50, len(casino))
        for _ in range(50):
            time.sleep(0.1)
            casino.dequeue()

        self.assertNotEqual(casino.centile(10), casino.centile(50))

    def test_centile_with_centileheapqueue(self):
        casino = CasinoQueue()
        tables = [Table(['Alfred', 'Jean', 'Harry', 'Diego']) for _ in range(10)]

        for player in random_players(50):
            casino.enqueue(player)

        self.assertEqual(50, len(casino))
        for _ in range(50):
            time.sleep(0.1)
            casino.dequeue()

        self.assertNotEqual(casino.centile(10), casino.centile(50))

if __name__ == '__main__':
    unittest.main()
