from benchpy import benchmarked

import random
import sys
import numpy
from casino import Queue, OrderedList, HeapCentile

if  __name__ == '__main__':
    queue = Queue()
    for i in range(1000):
        queue.enqueue(i)

    for i in range(1000):
        queue.dequeue()

    for i in range(1000):
        queue = Queue(range(1000))
        queue.remove(i)

    o = OrderedList()
    for d in range(1000):
        o.append(d)

    h = HeapCentile(30)
    for i in range(1000):
        h.append(i)

    for function in {'enqueue', 'dequeue', 'remove', 'orderedlist-append', 'heapcentile-append'}:
        with open('results/{}.plt'.format(function), 'w') as f:
            for col, row in enumerate(benchmarked.results(function)):
                f.write('{}\t{}\n'.format(col, row[0]))
