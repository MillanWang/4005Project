from SimulationEnums import Component, Product

BUFFER_CAPACITY = 2

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
    def __init__(self):
        # Create and populate buffer dictionary
        self._buffer_dict = dict()
        self._buffer_dict[(Component.C1, Product.P1)] = Component_Buffer()
        self._buffer_dict[(Component.C1, Product.P2)] = Component_Buffer()
        self._buffer_dict[(Component.C2, Product.P2)] = Component_Buffer()
        self._buffer_dict[(Component.C1, Product.P3)] = Component_Buffer()
        self._buffer_dict[(Component.C3, Product.P3)] = Component_Buffer()

    def attempt_to_add_to_buffer(self, component: Component):
        """
            Attempts to add find a buffer to send the given component to
            returns (True, Product) if successfully added
            returns (False, None) if all buffers are full. 
        """
        if component == Component.C1:
            # Check capacities of all C1 buffers [P1,P2,P3] buffer capacity list
            buffer_capacities = []
            buffer_capacities.append(self._buffer_dict[(Component.C1, Product.P1)]._component_count)
            buffer_capacities.append(self._buffer_dict[(Component.C1, Product.P2)]._component_count)
            buffer_capacities.append(self._buffer_dict[(Component.C1, Product.P3)]._component_count)

            # Check if all buffers are full. Can't add if they are
            if sum(buffer_capacities) == BUFFER_CAPACITY * 3:
                return False, None

            # Get the index of the lowest capacity. First index if tied
            # P1 before P2 before P3 prioritization
            buffer_choice = buffer_capacities.index(min(buffer_capacities))

            if buffer_choice == 0:
                return self._buffer_dict[(Component.C1, Product.P1)].attempt_to_add_to_buffer(), Product.P1
            elif buffer_choice == 1:
                return self._buffer_dict[(Component.C1, Product.P1)].attempt_to_add_to_buffer(), Product.P2
            elif buffer_choice == 2:
                return self._buffer_dict[(Component.C1, Product.P1)].attempt_to_add_to_buffer(), Product.P3

            # Should never get here. Error if we do
            raise ValueError("Internal buffer manager error attempting to add component C1 to a buffer")

        elif component == Component.C2:
            # Only one possible buffer this component can be sent to
            add_success = self._buffer_dict[(Component.C2, Product.P2)].attempt_to_add_to_buffer()
            return add_success,  Product.P2 if add_success else None

        elif component == Component.C3:
            # Only one possible buffer this component can be sent to
            add_success = self._buffer_dict[(Component.C3, Product.P3)].attempt_to_add_to_buffer()
            return add_success,  Product.P3 if add_success else None
        # END Component_Buffer_Manager.attempt_to_add_to_buffer

    def attempt_to_assemble_product(self, product: Product):
        """
            Takes components off of the corresponding workstation 
            buffers to assemble product

            Returns True if the needed buffers were non empty and this was done successfully
            Returns False if there are missing components on the buffers
        """
        if product == Product.P1:
            if (self._buffer_dict[(Component.C1, Product.P1)]._component_count == 0):
                return False
            self._buffer_dict[(Component.C1, Product.P1)].remove_from_buffer()
        elif product == Product.P2:
            if (self._buffer_dict[(Component.C1, Product.P2)]._component_count == 0 or self._buffer_dict[(Component.C2, Product.P2)]._component_count == 0):
                return False
            self._buffer_dict[(Component.C1, Product.P2)].remove_from_buffer()
            self._buffer_dict[(Component.C2, Product.P2)].remove_from_buffer()
        elif product == Product.P3:
            if (self._buffer_dict[(Component.C1, Product.P3)]._component_count == 0 or self._buffer_dict[(Component.C3, Product.P3)]._component_count == 0):
                return False
            self._buffer_dict[(Component.C1, Product.P3)].remove_from_buffer()
            self._buffer_dict[(Component.C3, Product.P3)].remove_from_buffer()

        return True  # Removed needed components from buffer
