import numpy
import os
import random
from Grapher import Grapher


class Stat_Manager(object):

    """
        Class for Stat_Manager

    """
    def __init__(self, dat_file):
        """
            intilazation of the Stat_Manager class 
        """
        self.__dat_file_contents = self.compute_stats(dat_file) 
    def compute_stats(self, dat_file):
        """
            Inputs dataFile and Calculates Stats for other functions
        """
        
        script_dir = os.path.dirname(__file__) #this is to access the data files in their folder 
        if ( dat_file == 1):
            rel_path = "servinsp1.dat" 
        elif ( dat_file == 2):
            rel_path = "servinsp22.dat" 
        elif (dat_file == 3):
            rel_path = "servinsp23.dat" 
        elif (dat_file == 4):
            rel_path = "ws1.dat"
        elif (dat_file == 5):
            rel_path = "ws2.dat"
        elif (dat_file == 6):
            rel_path = "ws3.dat"
        abs_file_path = os.path.join(script_dir, "dat_files\\"+rel_path)
        datalist = open(abs_file_path).read().splitlines()
        
        datalist = [x.strip(' ') for x in datalist]
        datalist_Float = [float(i) for i in datalist]
        intlist = [i * 1000 for i in datalist_Float]
        intlist = [int(x) for x in intlist]
        sample_sum = sum(intlist)
        count = len(intlist)
        mean = sample_sum/count
        variance = numpy.var(intlist)
        qq_list = sorted(intlist)
        #print("List Data type: " ,type(intlist[5]))
        #print("Count: " , count)
        #print("Sum: " , sum)
        #print("Mean: " , mean)
        #print("Variance: " , variance)
        #print("Sorted list: ", qq_list)
        #print(intlist)
    

        return (intlist,qq_list, mean, variance, count, sum)


    def qq_plot(self):
        """
        Send required Data to plot the qq-polot to the Graph_Master class 
        
        """
        
        Grapher.build_qq_plot(self.__dat_file_contents[1], "QQPlot")
        return


    def generate_histogram(self):
        """
        Send required Data to plot the Histogram to the Graph_Master class 
        """
        Grapher.build_histogram(self.__dat_file_contents[0], "Histogram")
    def chi_squared(self):
        """
        Calculate the Chi Squared Value
        For each time in the list call the random generator of that 
        distribution to get a second value. each set of values  
        
        """
        observed = self.__dat_file_contents[0]

        estimated = [6.25,6.25,6.25,6.25,6.25,6.25,6.25,6.25]
        chiSQpart = []
        for i in self.__dat_file_contents[0]:
            chiSQpart.append((((observed[i]-estimated[i])**2)/estimated[i]))
        chiSQtotal= sum(chiSQpart)
        print(chiSQpart)
        print(chiSQtotal)

        return

    def parameter_estimation():
        return
    
    
    def weibull_quantile_calc(list, k, lamb, name):
        result = []
        for i in range(len(list)):
            q = lamb * (-numpy.log(1-list[i]))**(1/k)
            print(q)
            result.append(q)
            
        Grapher.build_qq_plot(list, result, name)
        
    def expo_quantile_calc(list, lamb, name):
        result = []
        for i in range(len(list)):
            q = -(numpy.log(1-list[i]))/lamb
            print(q)
            result.append(q)
        
        Grapher.build_qq_plot(list, result, name)
