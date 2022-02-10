from SimulationEnums import Component, Product, Event_Types
from MainSim import BUFFER_CAPACITY


class Component_Buffer(object):
    def __init__(self):
        self._component_count = 0

    def attempt_to_add_to_buffer(self):
        """
            Attempts to add to the current buffer
            returns True if successful, False if buffer is full
        """
        if (self._component_count >= BUFFER_CAPACITY):
            # Buffer is full. Cannot add to it
            return False
        else:
            # Buffer has space. Add to it
            self._component_count += 1
            return True

    def remove_from_buffer(self):
        """
            Removes component from buffer. 
            Throws error if buffer is empty
        """
        if (self._component_count <= 0):
            raise ValueError("Attempted to remove component from empty buffer")
        self._component_count -= 1


class Component_Buffer_Manager(object):
    def __init__(self, simulation_logger):
        self._simulation_logger = simulation_logger  # NEEDS TO DO LOGGING
        self._clock = 0
        # Create and populate buffer dictionary
        self._buffer_dict = dict()
        self._buffer_dict[(Component.C1, Product.P1)] = Component_Buffer()
        self._buffer_dict[(Component.C1, Product.P2)] = Component_Buffer()
        self._buffer_dict[(Component.C2, Product.P2)] = Component_Buffer()
        self._buffer_dict[(Component.C1, Product.P3)] = Component_Buffer()
        self._buffer_dict[(Component.C3, Product.P3)] = Component_Buffer()

    def attempt_to_add_to_buffer(self, component):
        """
            Attempts to add find a buffer to send the given component to
            returns (True, Product) if successfully added
            returns (False, None) if all buffers are full. 



            WORK IN PROGRESS 
        """
        return None

    def assemble_product(self, product):
        """
            Takes components off of the corresponding workstation 
            buffers to assemble product

            NEEDS LOGGING
        """
        if product == Product.P1:
            self._buffer_dict[(Component.C1, Product.P1)].remove_from_buffer()
        elif product == Product.P2:
            self._buffer_dict[(Component.C1, Product.P2)].remove_from_buffer()
            self._buffer_dict[(Component.C2, Product.P2)].remove_from_buffer()
        elif product == Product.P3:
            self._buffer_dict[(Component.C1, Product.P3)].remove_from_buffer()
            self._buffer_dict[(Component.C3, Product.P3)].remove_from_buffer()
