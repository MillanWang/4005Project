import numpy as np
import queue
from Inspectors import Inspector1, Inspector2
from SimulationEnums import Component, Product, Event_Types
from SimulationLogger import SimulationLogger
from Buffers import Component_Buffer_Manager

# Remove/Add #or True to feature flags for easier enable/disable
USER_CHOOSES_SEED = False  # or True

PRODUCT_CREATION_LIMIT = 100
BUFFER_CAPACITY = 2


class Simulation(object):
    def __init__(self, simulation_logger: SimulationLogger):
        self._clock = 0
        self._simulation_logger = simulation_logger

        self._future_event_list = queue.PriorityQueue()

        # [Total, P1, P2, P3] - index matches product
        self._product_counts = [0, 0, 0, 0]

        # [None, I1, I2] so inspector number matches index
        self._inspectors = [None, Inspector1(), Inspector2()]

        # [None, W1, W2, W3] so workstation number match index
        self._workstations = [None]  # WORKSTATIONS NEEDED

        self._buffer_manager = Component_Buffer_Manager()

    def schedule_add_to_buffer(self, inspector_number: int):
        # inspect_time, component = self._inspectors[inspector_number].get_inspect_time()
        inspect_time, component = 123
        return 0

    def process_add_to_buffer(self, component: Component):
        success, product = self._buffer_manager.attempt_to_add_to_buffer(
            component)

        if not success:
            # Inspector is blocked and can't add to buffer right now
            return
        return 0

    def process_workstation_unbuffer(self, product: Product):
        success = self._buffer_manager.attempt_to_assemble_product(product)
        if not success:
            # Could not build the product. Missing items on buffer
            return

        workstation_assembly_time = 123
        # workstation_assembly_time = self._workstations[product.value].get_assembly_time()
        return 0

    def process_product_made(self, product: Product):
        """
            Processes the process of completeing the production of a product
        """
        self._product_counts[0] += 1  # Total product counter
        self._product_counts[product.value] += 1  # Product specific counter
        self._simulation_logger.log_product_created(product, self._clock)


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

    # Schedule first inspection completion for both inspectors

    while sim._product_counts[0] <= PRODUCT_CREATION_LIMIT:
        # Events (time, event_type, )
        evt = sim._future_event_list.get()
        sim._clock = evt[0]

        break  # TEMPORARY
