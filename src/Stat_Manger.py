import numpy
import os
import random
from SimulationEnums import Component


class Stat_Manager(object):

    """
        Class for Stat_Manager

    """
    def __init__(self, datFile):
        """
            intilazation of the Stat_Manager class 
        """
    def compute_stats(fileSelect):
        """
            Inputs dataFile and Calculates Stats for other functions
        """
        
        script_dir = os.path.dirname(__file__) #this is to access the data files in their folder 
        rel_path = "servinsp1.dat" # this needs to change
        abs_file_path = os.path.join(script_dir, rel_path)
        datalist = open(abs_file_path).read().splitlines()
        
        datalist = [x.strip(' ') for x in datalist]
        #datalist_Filterd = filter(None, datalist)
        datalist_Float = [float(i) for i in datalist]

        sum = sum(map(float,datalist))
        count = len(datalist)
        mean = sum/count
        variance = numpy.var(datalist_Float)
        qq_list = sorted(datalist_Float)
        print("List Data type: " ,type(datalist_Float[5]))
        print("Count: " , count)
        print("Sum: " , sum)
        print("Mean: " , mean)
        print("Variance: " , variance)
        print("Sorted list: ", qq_list)
    



          


        return     


    def __qq_plot():
        """
        Send required Data to plot the qq-polot to the Graph_Master class 
        
        """

        return

        
    def __hypothesis_testing(self, Hypoth):
        """
        Input User Hypothesis and output a comparison to the simulation results
        """
        
        return


    def __generate_histogram(self,):
        """
        Send required Data to plot the Histogram to the Graph_Master class 
        """
        return
    def __chi_squared(self,):
        """
        Calculate teh Chi Squared Value
        For each time in the list call the random generator of that 
        distribution to get a second value. each set of values  
        
        """
        observed = [19,10,3,6,1,1,4,6]
        estimated = [6.25,6.25,6.25,6.25,6.25,6.25,6.25,6.25]
        chiSQpart = []
        for i in range(0,7):
            chiSQpart.append((((observed[i]-estimated[i])**2)/estimated[i]))
        chiSQtotal= sum(chiSQpart)
        print(chiSQpart)
        print(chiSQtotal)

        return

    def parameter_estimation():
        return

    def __get_random_number_generator(self,):
        """
        Call the random number generator to input random values 
        """
        return

    def __test_random_generator(self,):
        """
        Call the random number generator to test its output 
        """
        return