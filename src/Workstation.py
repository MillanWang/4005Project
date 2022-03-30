from multiprocessing.sharedctypes import Value
import numpy
import os
from Lecuyer_Generator import Lecuyer_Generator
from SimulationEnums import Product
from Stat_Manger import expo_inverse_cdf

class Workstation(object):
    """
        Class for Workstations
    """

    def __init__(self, product:Product, randogen: Lecuyer_Generator):
        """
            Ininital delclairation for the workstation class
        """
        self.__randogen = randogen
        self.__product = product
        self.__currently_building = False

    
    def get_product_build_time(self) -> float:
        """
            Creates a build completion time for the current workstation along the specified distribution 
            returns the build time time
        """
        self.__currently_building = True
        # TODO Send these randogens through an inverse transform to get the randovar
        if (self.__product== Product.P1):
            return expo_inverse_cdf(self.__randogen.get_next_r(), 0.00021)
        elif (self.__product== Product.P2):
            return expo_inverse_cdf(self.__randogen.get_next_r(), 0.000085)
        elif (self.__product== Product.P3):
            return expo_inverse_cdf(self.__randogen.get_next_r(), 0.00011)
    
    def complete_build(self) -> None:
        self.__currently_building = False

    def is_building(self) -> bool:
        """
            Returns the self.__currently_building field
        """
        return self.__currently_building