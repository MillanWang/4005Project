import numpy as np
import queue
from Inspectors import Inspector1, Inspector2
from SimulationEnums import Component, Product, Event_Types
from SimulationLogger import SimulationLogger
from Buffers import Component_Buffer_Manager
from Workstation import Workstation

# Remove/Add "#" from "# or True" to feature flags for easier enable/disable
USER_CHOOSES_SEED = False  # or True
ENABLE_INSPECTOR_LOGGING = False  # or True
ENABLE_WORKSTATION_LOGGING = False  # or True
CREATE_LOG_FILES = False  # or True

TOTAL_PRODUCT_CREATION_LIMIT = 100



class Simulation(object):
    def __init__(self, simulation_logger: SimulationLogger):
        self._clock = 0
        self._simulation_logger = simulation_logger

        #Using a list instead of a queue because the order that events occur may not be chronological
        self._future_event_list = []

        # [Total, P1, P2, P3] - index matches product
        self._product_counts = [0, 0, 0, 0]

        # [None, I1, I2] so inspector number matches index
        self._inspectors = [None, Inspector1(), Inspector2()]

        # [None, W1, W2, W3] so workstation number match index
        self._workstations = [None, 
                              Workstation(Product.P1),
                              Workstation(Product.P2),
                              Workstation(Product.P3)] 

        self._buffer_manager = Component_Buffer_Manager()


    def get_next_chronological_event(self):
        """
            Removes and returns the next nearest chronological event from the future event list 
        """
        if len(self._future_event_list) == 0:
            raise ValueError("Error trying to get next chronological event before any have been scheduled")
        
        # Identify the index of the earliest chronological event from the future event list
        current_min = self._future_event_list[0][0]
        current_min_index = 0

        for i in range(len(self._future_event_list)):
            if self._future_event_list[i][0] < current_min:
                current_min = self._future_event_list[i][0]
                current_min_index = i
        # Remove and return the event at that index
        return self._future_event_list.pop(current_min_index)



    def schedule_add_to_buffer(self, inspector_number: int):
        """
            Initiates an inspector's inspection process and schedules 
            the attempt to add the component to the buffer
        """
        inspect_time, component = self._inspectors[inspector_number].generate_inspect_time()
        self._simulation_logger.log_inspector_component_selection(component, self._clock)

        #Schedule event for inspection completion
        completion_time = self._clock + inspect_time
        self._future_event_list.append((completion_time, Event_Types.Inspection_Complete, component))



    def process_add_to_buffer(self, component: Component):
        """
            Processes attempting to add an inspected component to a buffer
        """
        # If successful, the buffers will be updated accordingly by calling this
        success, product = self._buffer_manager.attempt_to_add_to_buffer(component)

        if not success:
            # Inspector is blocked and can't add to buffer right now
            # TODO: Add some behavior that tracks the inspector stuck time
            return

        # Schedule event for adding to buffer A$AP
        self._simulation_logger.log_inspector_buffered_component(component, product, self._clock)
        self._future_event_list.append((self._clock, Event_Types.Add_to_Buffer, product))



    def process_workstation_unbuffer(self, product: Product):
        """
            Processes attempting to start assembling a product
        """
        success = self._buffer_manager.attempt_to_assemble_product(product)
        if not success:
            # Could not build the product. 1 or more missing items on workstation buffer
            # Will eventually be successful once buffers get occupied
            return
        # SUCCESSFUL HERE : TODO: Add behavior to track inspector possibly getting unstuck
        
        workstation_assembly_time = self._workstations[product.value].get_assembly_time()
        self._simulation_logger.log_workstation_unbuffer(product, self._clock)
        
        # Schedule event for completing assembly
        build_completion_time = self._clock + workstation_assembly_time
        self._future_event_list.append((build_completion_time, Event_Types.Assembly_Complete, product))



    def process_product_made(self, product: Product):
        """
            Processes the completeing the a specified product's assembly
        """
        self._product_counts[0] += 1  # Total product counter
        self._product_counts[product.value] += 1  # Product specific counter
        self._simulation_logger.log_product_created(product, self._clock)

        # Try to create another product
        self._future_event_list.append((self._clock, Event_Types.Unbuffer_Start_Assembly, product))


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
        # Event Tuple Structure ( time, event_type, Product||Component )
        evt = sim.get_next_chronological_event()

        # update clock
        sim._clock = evt[0]

        #Update event type discernation
        if evt[1] == Event_Types.Inspection_Complete:
            sim.process_add_to_buffer(evt[2])
        elif evt[1] == Event_Types.Add_to_Buffer or evt[1] == Event_Types.Unbuffer_Start_Assembly:
            sim.process_workstation_unbuffer(evt[2])
        elif evt[1] == Event_Types.Assembly_Complete:
            sim.process_product_made(evt[2])

