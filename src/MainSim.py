import time
import numpy as np
import queue
from Inspectors import Inspector1, Inspector2
from Lecuyer_Generator import Lecuyer_Generator
from SimulationEnums import Component, Product, Event_Types
from SimulationLogger import SimulationLogger
from Buffers import Component_Buffer_Manager
from Workstation import Workstation

# Remove/Add "#" from "# or True" to feature flags for easier enable/disable
USER_CHOOSES_SEED = False   or True
ENABLE_INSPECTOR_LOGGING = False  # or True
ENABLE_WORKSTATION_LOGGING = False  # or True
CREATE_LOG_FILES = False  # or True

TOTAL_PRODUCT_CREATION_LIMIT = 1000



class Simulation(object):
    def __init__(self, simulation_logger: SimulationLogger, seed : int):
        self._clock = 0
        self._simulation_logger = simulation_logger

        #Using a list instead of a queue because the order that events occur may not be chronological
        self._future_event_list = []

        

        randogen = Lecuyer_Generator(seed)

        # [None, I1, I2] so inspector number matches index
        self._inspectors = [None, Inspector1(randogen), Inspector2(randogen)]

        # [None, W1, W2, W3] so workstation number match index
        self._workstations = [None, 
                              Workstation(Product.P1,randogen),
                              Workstation(Product.P2,randogen),
                              Workstation(Product.P3,randogen)] 

        self._buffer_manager = Component_Buffer_Manager()

        # [Total, P1, P2, P3] - index matches product
        self._product_counts = [0, 0, 0, 0]
        self._component_most_recent_block_time = [None, -1, -1, -1]
        self._component_total_block_time = [None, 0,0,0]
        self._workstation_most_recent_wait_for_component_time = [None, 0,0,0]
        self._workstation_total_wait_for_component_time = [None, 0,0,0]

    

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



    def start_inspection_schedule_add_to_buffer(self, inspector_number: int):
        """
            Initiates an inspector's inspection process and schedules 
            the attempt to add the component to the buffer
        """
        inspect_time, component = self._inspectors[inspector_number].generate_inspect_time()
        self._simulation_logger.log_inspector_component_selection(component, self._clock)

        #Schedule event for inspection completion
        completion_time = self._clock + inspect_time
        self._future_event_list.append((completion_time, Event_Types.Inspection_Complete, component))



    def process_inspection_completed_attempt_to_add_to_buffer(self, component: Component):
        """
            Processes attempting to add an inspected component to a buffer
        """
        # If successful, the buffers will be updated accordingly by calling this
        success, product = self._buffer_manager.attempt_to_add_to_buffer(component)

        if not success: 
            # Inspector is blocked and can't add to buffer right now
            # Set the current time as the most recent block time
            self._component_most_recent_block_time[component.value] = self._clock
            return

        # If successfully put component onto buffer, start to inspect again A$AP
        self._future_event_list.append((self._clock, Event_Types.Start_Next_Inspection, 1 if component==Component.C1 else 2))

        # Schedule event for adding to buffer A$AP
        self._simulation_logger.log_inspector_buffered_component(component, product, self._clock)
        self._future_event_list.append((self._clock, Event_Types.Add_to_Buffer, product))





    def process_workstation_attempt_unbuffer_and_start_build(self, product: Product):
        """
            Processes attempting to start assembling a product
        """
        # Check if the current workstation is busy
        if self._workstations[product.value].is_building():
            return

        success = self._buffer_manager.attempt_to_assemble_product(product)
        if not success:
            # Could not build the product. 1 or more missing items on workstation buffer
            # Will eventually be successful once buffers get occupied
            return
        # Successfully unbuffered

        # Check if inspector 2 is waiting for a buffer spot 
        if product!=Product.P1 and self._component_most_recent_block_time[product.value]!=-1:
            # Component 2 or 3 get's buffered, resume Inspector 2
            self._buffer_manager.attempt_to_add_to_buffer(Component.C2 if product==Product.P2 else Component.C3)

            # Track the blocked time
            blocked_time = self._clock - self._component_most_recent_block_time[product.value]
            self._component_total_block_time[product.value] += blocked_time
            # Reset the most recent block time to unblocked
            self._component_most_recent_block_time[product.value]!=-1
            # Start inspector 2 next inspection A$AP
            self._future_event_list.append((self._clock, Event_Types.Start_Next_Inspection, 2))
        
        # Check if inspector 1 is waiting for a buffer spot 
        if self._component_most_recent_block_time[1]!=-1:
            # All products use component 1. Add it to the buffer if inspector 1 is stuck. Resume inspector 1
            self._buffer_manager.attempt_to_add_to_buffer(Component.C1)
            # Track the blocked time
            blocked_time = self._clock - self._component_most_recent_block_time[1]
            self._component_total_block_time[1] += blocked_time
            # Reset the most recent block time to unblocked
            self._component_most_recent_block_time[1]!=-1
            # Start the next inspection A$AP
            self._future_event_list.append((self._clock, Event_Types.Start_Next_Inspection, 1 ))

        # Get the time that the workstation has waiting to start building
        waiting_time = self._clock - self._workstation_most_recent_wait_for_component_time[product.value]
        self._workstation_total_wait_for_component_time[product.value] += waiting_time
        
        workstation_assembly_time = self._workstations[product.value].get_product_build_time()
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

        self._workstations[product.value].complete_build()

        # Try to create another product and note time to for waiting for component
        self._future_event_list.append((self._clock, Event_Types.Unbuffer_Start_Assembly, product))
        self._workstation_most_recent_wait_for_component_time[product.value] = self._clock


    def print_sim_summary(self):
        """
            Prints out a summary of the simulation
        """
        print("Simulation Completed")
        for i in range(3):
            print("Component " + str(i+1) + " - Total blocked time : " + str(self._component_total_block_time[i+1]))
        print("Total Component Block Time : " + str(sum(self._component_total_block_time[1:])))
        for i in range(3):
            print("Workstation " + str(i+1) + " - Total wait time : " + str(self._workstation_total_wait_for_component_time[i+1]))
        print("Total Workstation Wait Time : " + str(sum(self._workstation_total_wait_for_component_time[1:])))
        for i in range(3):
            print("Product " + str(i+1) + " - Total created : " + str(self._product_counts[i+1]))
        print("Total products created : " + str(self._product_counts[0]))


# Main script
if __name__ == "__main__":

    # set seed for random number generator
    seed = 0
    if USER_CHOOSES_SEED:
        seed = int(input('Enter simulation seed:'))
    else:
        seed = int(round(time.time() * 1000))

    sim_logger = SimulationLogger(
        ENABLE_INSPECTOR_LOGGING,
        ENABLE_WORKSTATION_LOGGING,
        CREATE_LOG_FILES)

    # Create simulation object
    sim = Simulation(sim_logger, seed)

    # Schedule first inspection completion for both inspectors I1 & I2
    sim.start_inspection_schedule_add_to_buffer(1)
    sim.start_inspection_schedule_add_to_buffer(2)

    while sim._product_counts[0] <= TOTAL_PRODUCT_CREATION_LIMIT:
        # Get next event
        # Event Tuple Structure ( time, event_type, Product||Component||InspectorNumber )
        evt = sim.get_next_chronological_event()
        print(evt)
        # update clock
        sim._clock = evt[0]

        #Update event type discernation
        if evt[1] == Event_Types.Inspection_Complete:
            sim.process_inspection_completed_attempt_to_add_to_buffer(evt[2])
        elif evt[1] == Event_Types.Add_to_Buffer or evt[1] == Event_Types.Unbuffer_Start_Assembly:
            sim.process_workstation_attempt_unbuffer_and_start_build(evt[2])
        elif evt[1] == Event_Types.Assembly_Complete:
            sim.process_product_made(evt[2])
        elif evt[1] == Event_Types.Start_Next_Inspection:
            sim.start_inspection_schedule_add_to_buffer(evt[2])

sim.print_sim_summary()