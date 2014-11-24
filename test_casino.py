import unittest

from casino import Queue, CasinoQueue, Table, random_players

class QueueTest(unittest.TestCase):
    """Test les fonctionnalités de base de la Queue"""
    def test_length(self):
        queue = Queue()
        self.assertEqual(0, len(queue))
        self.assertIs(queue.first, queue.last)

        queue.enqueue(4)
        self.assertIs(queue.first, queue.last)
        self.assertEqual(1, len(queue))

    def test_enqueue(self):
        """ajout d'un item au début de la file"""
        queue = Queue()
        self.assertEqual(0, len(queue))

        queue.enqueue(5)
        self.assertIs(queue.first, queue.last)
        self.assertEqual(1, len(queue))

        queue.enqueue(7)
        self.assertEqual(2, len(queue))
        self.assertIsNot(queue.first, queue.last)
        self.assertIs(queue.first.next(), queue.last)

        # il reste 1 élément
        self.assertEqual(5, queue.dequeue())
        self.assertIs(queue.first, queue.last)

        # il reste aucun élément
        self.assertEqual(7, queue.dequeue())
        self.assertIsNone(queue.first)
        self.assertIsNone(queue.last)

    def test_dequeue(self):
        """retrait d'un item à la fin de la file"""
        queue = Queue()
        for i in range(5):
            queue.enqueue(i)

        self.assertEqual(5, len(queue))

        for i in range(5):
            self.assertEqual(i, queue.dequeue())

    def test_remove(self):
        queue = Queue()

        queue.enqueue(1)
        self.assertEqual(1, len(queue))

        queue.remove(1)
        self.assertEqual(0, len(queue))
        self.assertIsNone(queue.first)
        self.assertIsNone(queue.last)

class CasinoQueueTest(unittest.TestCase):
    """Test le fonctionnement du Casino"""
    def setUp(self):
        self.casino = CasinoQueue()

    def test_centile(self):
        self.casino.enqueue('John')

        self.casino.dequeue()

        print(self.casino.centile.centile(20))

if __name__ == '__main__':
    unittest.main()
