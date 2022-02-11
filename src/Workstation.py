from multiprocessing.sharedctypes import Value
import numpy
import os
import random
from SimulationEnums import Component 
from SimulationEnums import Product

class Workstation(object):
    """
    Class for Workstations
    """

    def __init__(self, product:Product):
        """
        Ininital delclairation for the workstation class
        """
        self.__mean = self.__build_distrubution_from_dat(product)
        self.__product = product

    def __build_distrubution_from_dat(self, product):
        """
        Calculaltes the distrubution for each products time to assemble returns the mean of the data set
        """
        if product == Product.P1:
            rel_path = "dat_files/ws1.dat"
        elif product == Product.P2 :
            rel_path = "dat_files/ws2.dat"
        elif product == Product.P3 :
            rel_path = "dat_files/ws3.dat"
        else:
            raise ValueError ("Illegel prduct")

        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        abs_file_path = os.path.join(script_dir, rel_path)
        datalist = open(abs_file_path).read().splitlines()
        datatotal = 0
        for x in datalist:    
            datatotal += int("".join(x.split(".")))
        mean = datatotal / len(datalist)
        return mean
    
    def get_unbuffer_time(self):
        """
        Creates a inspection time delay from the distribution 
        returns the delay time
        """
        time = numpy.random.exponential(self.__mean, 1)
        return time
    
   


