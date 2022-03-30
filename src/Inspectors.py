import numpy
import os
import random
from Lecuyer_Generator import Lecuyer_Generator
from SimulationEnums import Component


class Inspector1(object):
    """
        Class for Inspector1
    """
    def __init__(self, randogen: Lecuyer_Generator):
        """
            intilazation of the Inspector1 class 
        """
        self.__randogen = randogen
    
    def generate_inspect_time(self) -> float:
        """
            Creates a inspection time delay from the distribution returns delay time and component 
        """
        # TODO : Swap the randogen to use the inverse transform methodology
        time =  self.__randogen.get_next_r()
        return time, Component.C1




class Inspector2(object):
    """
        Class for Inspector2
    """
    
    def __init__(self,  randogen: Lecuyer_Generator):
        """
            intilazation of the Inspector1 class 
        """
        self.__randogen = randogen
    
    def __generate_comp2or3(self) -> Component:
        """
            Randomly picks between component 2 and 3 returns the component
        """
        if self.__randogen.get_next_r() >= 0.5:
            return Component.C2
        else:
            return Component.C3
    
    def generate_inspect_time(self) -> float:
        """
            Creates a inspection time delay from the distribution 
            returns the delay time and the component 
        """
        # TODO : Swap the randogen to use the inverse transform methodology
        component =  self.__generate_comp2or3()
        if component == Component.C2:
            time = self.__randogen.get_next_r()
        else: 
            time = self.__randogen.get_next_r()
        
        return time, component

   





