import enum
# from sys import ps1
# import numpy as np
# from scipy.stats import expon
# from scipy.stats import norm
# import matplotlib.pyplot as plt
import queue
# from dataclasses import dataclass, field
# from typing import Any


# Remove/Add #or True for easier enable/disable
USER_CHOOSES_SEED = False  # or True


class Product(enum.Enum):
    P1 = 1
    P2 = 2
    P3 = 3


class Component(enum.Enum):
    C1 = 1
    C2 = 2
    C3 = 3


class Workstation(object):
    def __init__(self):
        self.name = 1
        self._departure = 2
        self._MeanServiceTime = 3.2
        self._SIGMA = 0.6

        self._QueueLength = 0
        self._QueueLengthTime = [[0, 0.0]]
        self._NumberInService = 0
        self._InService = []
        self._LastEventTime = 0.0
        self._TotalBusy = 0.0
        self._MaxQueueLength = 0
        self._SumResponseTime = 0.0


class Simulation(object):
    def __init__(self):
        self._clock = 0

        self._future_event_list = queue.PriorityQueue()

        self._QueueID = 0
        self._NumberOfQueues = 2
        self._QList = []

        # create a future event list
        self._FutureEventList = queue.Queue()


# Main script
if __name__ == "__main__":

    # set seed for random number generator
    seed = 0
    if USER_CHOOSES_SEED:
        seed = input('Enter simulation seed:')
    # np.random.seed((int(seed)))

    # Create simulation object
    sim = Simulation()
    print("Good")


"""
    Time for performace metrics. Eventual time optimizations
import time
start = time.time()
for i in rang(12000 * 100 * 100):
end = time.time()
print(end - start)
"""


"""

Inspectors getting stucc
    They inspect component, not knowing anything about the state of the buffers.
    Try to put the component on the first ordered buffer. If the buf is full, note down the buffer unstuck time. Try next
    If no buf is free, find who has the nearest unstuck time with min method on the list of tracked unbuff times 
                    get_unbuffer_time() : int 
                            return negative if buffer is free
                            return the complete time for the current product if buffer full


Step by step sim 
I1 starts at t=0 and determines the time that the inspect will complete. 
W1 knows that it's start time is at I1 complete time


Enum used to denote the state of the workstation's buffer
https://docs.python.org/3/library/enum.html



Insp putting c's onto the bufs
    Insp should have a ref to particular workstation refs. 


Time skippers. 
    Calculate the nearest time for an event. 



Somethings to test
What happens when the order of the workstations are changed
Different algorithms for distributing the components to bufs

"""
