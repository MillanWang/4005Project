
# from sys import ps1
from msilib.schema import Error
import numpy as np
# from scipy.stats import expon
# from scipy.stats import norm
# import matplotlib.pyplot as plt # For data visualization
# import simpy #Might be useful for simulation tools
import queue
# from dataclasses import dataclass, field
# from typing import Any
from SimulationEnums import Component, Product, Event_Types
from SimulationLogger import SimulationLogger
from Buffers import Component_Buffer, Component_Buffer_Manager

# Remove/Add #or True to feature flags for easier enable/disable
USER_CHOOSES_SEED = False  # or True

PRODUCT_CREATION_LIMIT = 100
BUFFER_CAPACITY = 2


class Simulation(object):
    def __init__(self, simulation_logger):
        self._clock = 0
        self._simulation_logger = simulation_logger

        self._future_event_list = queue.PriorityQueue()

        # [Total, P1, P2, P3] - index matches product
        self._product_counts = [0, 0, 0, 0]
        self._buffer_manager = Component_Buffer_Manager(simulation_logger)

    def schedule_add_to_buffer(self, inspector):
        return inspector

    def process_add_to_buffer(self):
        return 0

    def process_workstation_unbuffer(self):
        return 0


# Main script
if __name__ == "__main__":

    # set seed for random number generator
    seed = 0
    if USER_CHOOSES_SEED:
        seed = input('Enter simulation seed:')
    np.random.seed((int(seed)))

    sim_logger = SimulationLogger(True, True, False)

    # Create simulation object
    sim = Simulation(sim_logger)

    while sim._product_counts[0] <= PRODUCT_CREATION_LIMIT:
        # Events (time, event_type, )
        evt = sim._future_event_list.get()
        sim._clock = evt[0]

        break  # TEMPORARY
