

class Multiplicative_Congruential_Model(object):
    """
        Class for a single Linear Congruential model generator to be used in the 
        main random number generation process
    """
    def __init__(self, seed:int, multiplier:int, modulus:int) -> None:
        """
            Constructor for Multiplicative_Congruential_Model class
            Based on linear multiplicative congruential model with a zero incrementor
        """
        self.__current = seed if seed!=0 else 1
        self.__a = multiplier
        self.__m = modulus
    
    def get_next_x(self) -> int:
        """
            Returns the next pseudorandom integer
        """
        next = (self.__a * self.__current) % self.__m
        self.__current = next
        return next