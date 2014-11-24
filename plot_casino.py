from benchpy import benchmarked

import sys
import numpy
from casino import Queue, OrderedList, HeapCentile

if  __name__ == '__main__':
    queue = Queue()
    for i in range(500):
        queue.enqueue(i)

    for i in range(500):
        queue.dequeue()

    for i in range(200):
        queue = Queue(range(200))
        queue.remove(i)

    o = OrderedList()
    for i in range(1000):
        o.append(i)

    h = HeapCentile(30)
    for i in range(1000):
        # :h.append(i)
        pass

    for function in {'enqueue', 'dequeue', 'remove', 'orderedlist-append'}:
        with open('results/{}.plt'.format(function), 'w') as f:
            for col, row in enumerate(benchmarked.results(function)):
                f.write('{}\t{}\n'.format(col, row[0]))
