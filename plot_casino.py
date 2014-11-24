from benchpy import benchmarked
from Gnuplot import Gnuplot, Data

import numpy
from casino import Queue

if  __name__ == '__main__':

    g = Gnuplot(persist=True)

    queue = Queue()

    for i in range(10000):
        queue.enqueue(i)

    for i in range(10000):
        queue.dequeue()

    print(benchmarked.results[None])

    enqueue_data = Data(range(10), benchmarked.results[None]['enqueue'].take(1, axis=1))
    dequeue_data = Data(reversed(range(10)), benchmarked.results[None]['dequeue'])
    remove_data = Data(reversed(range(10)), benchmarked.results[None]['remove'])

    g.plot(enqueue_data)
    g.plot(dequeue_data)

