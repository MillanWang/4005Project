import numpy
import os
import random
from SimulationEnums import Component


class Inspector1(object):
    """
        Class for Inspector1
    """
    def __init__(self):
        """
            intilazation of the Inspector1 class 
        """
        self.__mean= self.__build_distribution_from_dat()

    def __build_distribution_from_dat(self):
        """
            Calculaltes the Mean for component 1 from the data set. returns the mean
        """
        script_dir = os.path.dirname(__file__) #this is to access the data files in their folder 
        rel_path = "dat_files/servinsp1.dat"
        abs_file_path = os.path.join(script_dir, rel_path)
        self.datalist = open(abs_file_path).read().splitlines()
        datatotal = 0
        for x in range(0, 300):
            datatotal += float(self.datalist[x]) # Reads all of the data points and sums them up
        mean = datatotal / 300
        return mean
    
    def generate_inspect_time(self):
        """
            Creates a inspection time delay from the distribution returns delay time and component 
        """
        time = numpy.random.exponential(self.__mean, 1) #Generate the random time delay from the mean
        time = int("".join(time.split("."))) # change to seconds
        return time, Component.C1




class Inspector2(object):
    """
        Class for Inspector2
    """
    
    def __init__(self):
        """
            intilazation of the Inspector1 class 
        """
        self.__C2_mean = self.__build_distribution_from_dat(Component.C2)
        self.__C3_mean = self.__build_distribution_from_dat(Component.C3)
    
    def __generate_comp2or3(self):
        """
            Randomly picks between component 2 and 3 returns the component
        """
        if random.getrandbits(1) == 1:
            return Component.C2
        else:
            return Component.C3
    
    def __build_distribution_from_dat(self, component):
        """
            Calculaltes the Mean for component 1 from the distribution  returns the mean  of the data set
        """
        if component == Component.C2:
            rel_path = "dat_files/servinsp22.dat"
        else:
            rel_path = "dat_files/servinsp23.dat"
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        abs_file_path = os.path.join(script_dir, rel_path)
        self.datalist = open(abs_file_path).read().splitlines()
        datatotal = 0
        for x in range(0, 300):
            datatotal += float(self.datalist[x])
        mean = datatotal / 300
        return mean
    
    def generate_inspect_time(self):
        """
            Creates a inspection time delay from the distribution 
            returns the delay time and the component 
        """
        component =  self.__generate_comp2or3()
        if component == Component.C2:

            time = numpy.random.exponential(self.__C2_mean, 1)
        else: 
            time = numpy.random.exponential(self.__C3_mean, 1)
        
        time = int("".join(time.split(".")))
        return time, component

   





