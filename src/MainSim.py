import numpy as np
import queue
from Inspectors import Inspector1, Inspector2
from SimulationEnums import Component, Product, Event_Types
from SimulationLogger import SimulationLogger
from Buffers import Component_Buffer_Manager

# Remove/Add "#" from "# or True" to feature flags for easier enable/disable
USER_CHOOSES_SEED = False  # or True
ENABLE_INSPECTOR_LOGGING = False  # or True
ENABLE_WORKSTATION_LOGGING = False  # or True
CREATE_LOG_FILES = False  # or True

TOTAL_PRODUCT_CREATION_LIMIT = 100
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
        """
            Initiates an inspector's inspection process and schedules 
            the attempt to add the component to the buffer
        """
        # inspect_time, component = self._inspectors[inspector_number].get_inspect_time()
        inspect_time, component = 123, inspector_number
        completion_time = self._clock + inspect_time
        self._future_event_list.put((completion_time, Event_Types.Inspection_Complete, component))

    def process_add_to_buffer(self, component: Component):
        """
            Processes attempting to add an inspected component to a buffer
        """
        success, product = self._buffer_manager.attempt_to_add_to_buffer(component)

        if not success:
            # Inspector is blocked and can't add to buffer right now
            return
        return 0

    def process_workstation_unbuffer(self, product: Product):
        """
            Processes attempting to start assembling a product
        """
        success = self._buffer_manager.attempt_to_assemble_product(product)
        if not success:
            # Could not build the product. Missing items on buffer
            return

        workstation_assembly_time = 123
        # workstation_assembly_time = self._workstations[product.value].get_assembly_time()
        return 0

    def process_product_made(self, product: Product):
        """
            Processes the completeing the a specified product's assembly
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

    sim_logger = SimulationLogger(
        ENABLE_INSPECTOR_LOGGING,
        ENABLE_WORKSTATION_LOGGING,
        CREATE_LOG_FILES)

    # Create simulation object
    sim = Simulation(sim_logger)

    # Schedule first inspection completion for both inspectors I1 & I2
    sim.schedule_add_to_buffer(1)
    sim.schedule_add_to_buffer(2)

    while sim._product_counts[0] <= TOTAL_PRODUCT_CREATION_LIMIT:
        # Get next event
        # Events (time, event_type, )
        evt = sim._future_event_list.get()

        # update clock
        sim._clock = evt[0]

        #Update event type discernation
        if evt[1] == Event_Types.Inspection_Complete:
            sim.process_add_to_buffer()
        elif evt[1] == Event_Types.Unbuffer_Start_Assembly:
            sim.process_workstation_unbuffer()
        elif evt[1] == Event_Types.Assembly_Complete:
            sim.process_product_made()
        

        break  # TEMPORARY
