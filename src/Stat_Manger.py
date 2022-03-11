import numpy
import os
import random
from Grapher import Grapher


class Stat_Manager(object):

    """
        Class for Stat_Manager

    """
    def __init__(self, fileSelect):
        """
            intilazation of the Stat_Manager class 
        """
        self.__datFile= self.compute_stats(fileSelect)
    def compute_stats(fileSelect):
        """
            Inputs dataFile and Calculates Stats for other functions
        """
        
        script_dir = os.path.dirname(__file__) #this is to access the data files in their folder 
        if (fileSelect == 1):
            rel_path = "servinsp1.dat" 
        elif (fileSelect == 2):
            rel_path = "servinsp22.dat" 
        elif (fileSelect == 3):
            rel_path = "servinsp23.dat" 
        elif (fileSelect == 4):
            rel_path = "ws1.dat"
        elif (fileSelect == 5):
            rel_path = "ws2.dat"
        elif (fileSelect == 6):
            rel_path = "ws3.dat"
        abs_file_path = os.path.join(script_dir, rel_path)
        datalist = open(abs_file_path).read().splitlines()
        
        datalist = [x.strip(' ') for x in datalist]
        datalist_Float = [float(i) for i in datalist]
        intlist = [i * 1000 for i in datalist_Float]
        intlist = [int(x) for x in intlist]
        sum = sum(intlist)
        count = len(intlist)
        mean = sum/count
        variance = numpy.var(intlist)
        qq_list = sorted(intlist)
        print("List Data type: " ,type(intlist[5]))
        print("Count: " , count)
        print("Sum: " , sum)
        print("Mean: " , mean)
        print("Variance: " , variance)
        print("Sorted list: ", qq_list)
        print(intlist)
    



          


        return     


    def __qq_plot(self):
        """
        Send required Data to plot the qq-polot to the Graph_Master class 
        
        """
        datFile = self.__datFile
        qq_list = sorted(datFile)
        
        Grapher.build_qq_plot(qq_list, "QQPlot")
        return

        
    def __hypothesis_testing(self):
        """
        Input User Hypothesis and output a comparison to the simulation results
        """
        
        return


    def __generate_histogram(self):
        """
        Send required Data to plot the Histogram to the Graph_Master class 
        """
        datFile = self.__datFile
        Grapher.build_histogram(datFile, "Histogram")
        return
    def __chi_squared(self,):
        """
        Calculate the Chi Squared Value
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