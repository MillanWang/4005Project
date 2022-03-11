import math
import numpy
import os
import random
from Grapher import Grapher
import numpy as np

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
    

        return (intlist,qq_list, mean, variance, count, sample_sum)


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

    def exponential_chi_squared(self):
        """
        Calculate the Chi Squared Value
        For each time in the list call the random generator of that 
        distribution to get a second value. each set of values  
        
        """
        # (intlist,qq_list, mean, variance, count, sample_sum)
        # self.__dat_file_contents
        sorted_data = self.__dat_file_contents[1]
        print(sorted_data[-1])
        # Calculating number of bins and bin width
        q25, q75 = np.percentile(sorted_data, [25, 75])
        bin_width = 2 * (q75 - q25) * len(sorted_data) ** (-1/3)
        k_intervals = round((max(sorted_data) - min(sorted_data)) / bin_width)

        exponential_lambda = 2

        expected_frequencies = []
        for i in range(k_intervals+1):
            expected_frequencies.append((exponential_cdf(i+1,exponential_lambda)-exponential_cdf(i,exponential_lambda))*300)
            
        observed_frequencies = []
        for i in range(k_intervals-1):
            observed_frequencies.append(0)
            for elem in sorted_data:
                if elem>(i)*bin_width and elem<=(i+1)*bin_width:
                    observed_frequencies[i]+=1

        #Last element in the list is sometimes wonky. It's sorted so add it to last bin
        if len(observed_frequencies)<len(sorted_data) : observed_frequencies[-1]+=1
        chi_components = []
        for i in range(len(observed_frequencies)):
            chi_components.append( math.pow(observed_frequencies[i]-expected_frequencies[i],2) / expected_frequencies[i])
        

        # All dat files in this project have 300 datapoints. 
        chi_squared_table_value = 339.26047583
        if chi_squared_table_value >sum(chi_components):
            print("Null hypothesis NOT rejected - Can assume distributions match")
        else:
            print("Null hypothesis REJECTED - Distributions don't match")
        print(sum(chi_components))
        print(observed_frequencies)
        print(expected_frequencies)
        print(sum(observed_frequencies))
        print(sum(expected_frequencies))




def weibull_cdf(x,k,b):
    return 1 - math.exp(-b*math.pow(x,k))



def exponential_cdf(x,ld):
    return 1 - math.exp(-x*ld)
