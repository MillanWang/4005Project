import numpy
import os
import random
from Lecuyer_Generator import Lecuyer_Generator
from SimulationEnums import Component
from Stat_Manger import expo_inverse_cdf, weibull_inverse_cdf

class Inspector1(object):
    """
        Class for Inspector1
    """
    def __init__(self, randogen: Lecuyer_Generator):
        """
            intilazation of the Inspector1 class 
        """
        self.__randogen = randogen
    
    def generate_inspect_time(self, component:Component) -> float:
        """
            Creates a inspection time delay from the distribution returns delay time and component 
        """
        time = weibull_inverse_cdf(self.__randogen.get_next_r(), 1, 10000)
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
    
    def generate_inspect_time(self, component:Component) -> float:
        """
            Creates a inspection time delay from the distribution 
            returns the delay time and the component 
        """
        
        # Standard operating policy, randomly select next component to inspect
        # Alt operating policy, the buffers will determine next component to select and pass it in as a param
        if component == None:
            component =  self.__generate_comp2or3()

        if component == Component.C2:
            time = weibull_inverse_cdf(self.__randogen.get_next_r(), 1, 145000)
        else: 
            time = expo_inverse_cdf(self.__randogen.get_next_r(), 0.000048)
        
        return time, component





