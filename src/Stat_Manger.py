import math
import numpy
import os
import random
from Grapher import Grapher
import numpy as np

class Stat_Manager(object):
    """
        Class for managing statistics given sample data .dat files
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
        sorted_list = sorted(intlist)

        return (intlist, sorted_list, mean, variance, count, sample_sum)

    def generate_histogram(self):
        """
        Send required Data to plot the Histogram to the Graph_Master class 
        """
        Grapher.build_histogram(self.__dat_file_contents[0], "Histogram")

    def qq_plot(self):
        """
        Send required Data to plot the qq-polot to the Graph_Master class 
        
        """
        Grapher.build_qq_plot(self.__dat_file_contents[1], "QQPlot")

    def exponential_chi_squared(self,bin_number, Lambda ):
        """
            Conduct a chi squared test, checking for fit with an exponential distribution
        
        """
        # (intlist,qq_list, mean, variance, count, sample_sum)
        sorted_data = self.__dat_file_contents[1]
        # Calculating number of bins and bin width
        k_intervals = bin_number
        bin_width = round((max(sorted_data) - min(sorted_data)) / k_intervals)
        exponential_lambda = Lambda

        expected_frequencies = []
        for i in range(k_intervals):
            expected_frequencies.append((self.exponential_cdf(i+1,exponential_lambda)-self.exponential_cdf(i,exponential_lambda))*300)
            
        observed_frequencies = []
        for i in range(k_intervals):
            observed_frequencies.append(0)
            for elem in sorted_data:
                if elem>(i)*bin_width and elem<=(i+1)*bin_width:
                    observed_frequencies[i]+=1


        #Last element in the list is sometimes wonky. It's sorted so add it to last bin
        if len(observed_frequencies)<len(sorted_data) : observed_frequencies[-1]+=1
        
        Stat_Manager.chi_squared_rebin(observed_frequencies, expected_frequencies, 5)

        chi_components = []
        for i in range(len(observed_frequencies)):
            chi_components.append( math.pow(observed_frequencies[i]-expected_frequencies[i],2) / expected_frequencies[i])
        

        # All dat files in this project have 300 datapoints. 
        chi_squared_table_value = 339.26047583
        if chi_squared_table_value >sum(chi_components):
            print("Null hypothesis NOT rejected - Can assume distributions match")
        else:
            print("Null hypothesis REJECTED - Distributions don't match")
        print("Chi Sum: ",sum(chi_components))

    def weibull_chi_squared(self, bin_number, k_value, b_value):
        """
        Conduct a chi squared test, checking for fit with weibull distribution
        """
        #(intlist,qq_list, mean, variance, count, sample_sum)
        sorted_data = self.__dat_file_contents[1]
        # Calculating number of bins and bin width

        k_intervals = bin_number
        bin_width = round((max(sorted_data) - min(sorted_data)) / k_intervals)
        weibull_k = k_value
        weibull_b = b_value

        expected_frequencies = []
        for i in range(k_intervals):
            expected_frequencies.append((self.weibull_cdf(i+1,weibull_k,weibull_b)-self.weibull_cdf(i,weibull_k,weibull_b))*300)
            
        observed_frequencies = []
        for i in range(k_intervals):
            observed_frequencies.append(0)
            for elem in sorted_data:
                if elem>(i)*bin_width and elem<=(i+1)*bin_width:
                    observed_frequencies[i]+=1

        #Last element in the list is sometimes wonky. It's sorted so add it to last bin
        if len(observed_frequencies)<len(sorted_data) : observed_frequencies[-1]+=1

        Stat_Manager.chi_squared_rebin(observed_frequencies, expected_frequencies, 5)

        chi_components = []
        for i in range(len(observed_frequencies)):
            chi_components.append( math.pow(observed_frequencies[i]-expected_frequencies[i],2) / expected_frequencies[i])
        
        # All dat files in this project have 300 datapoints. 
        chi_squared_table_value = 339.26047583
        if chi_squared_table_value >sum(chi_components):
            print("Null hypothesis NOT rejected - Can assume distributions match")
        else:
            print("Null hypothesis REJECTED - Distributions don't match")
        print("Chi Sum: ",sum(chi_components))      
    
    def weibull_quantile_calc(self, k, lamb, name):
        """
            Calculates the quantile of a weibull distribution
        """
        result = []
        listItem = self.__dat_file_contents[1]
        for i in range(len(listItem)):
            p = i/300
            q = lamb * (-numpy.log(1-p))**(1/k)
            print(q)
            result.append(q)
            
        Grapher.build_qq_plot(listItem, result, name)

    def expo_quantile_calc(self, lamb, name):
        """
            Calculattes the qualtile of an exponential distribution
        """
        result = []
        listItem = self.__dat_file_contents[1]
        for i in range(len(listItem)):
            p = i/300
            q = -(numpy.log(1-p))/lamb
            print(q)
            result.append(q)
        
        Grapher.build_qq_plot(listItem, result, name)
    
    def weibull_cdf(self,x,k,b):
        """
            Calculates the cumulative frequency from a weibull distribution
        """
        return 1 - math.exp(-1*math.pow(x/b,k))

    def exponential_cdf(self,x,ld):
        """
            Calculates the cumulative frequency of an exponential distribution
        """
        return 1 - math.exp(-x*ld)

    def chi_squared_rebin(observed:list, expected:list, threshold:float)->list:
        """
            Rebins the given lists to combine neighbours under the threshold
        """
        if (len(observed)!=len(expected)):
            raise ValueError("ERROR : chi_squared_rebin : SIZE OF OBSERVED LIST DOES NOT MATCH SIZE OF EXPECTED")

        # Front compression
        while(True):
            if expected[0] < threshold:
                expected[1] += expected[0]
                observed[1] += observed[0]
                del expected[0]
                del observed[0]
            else:
                break

        # Back compression
        while(True):
            if expected[-1] < threshold:
                expected[-2] += expected[-1]
                observed[-2] += observed[-1]
                del expected[-1]
                del observed[-1]
            else:
                break
            

        return [observed, expected]


#Test1 = Stat_Manager(1)
#Test1.weibull_chi_squared(59,1,10)          # don't reject; chi total 32.7700 after rebin from 59 to 40 bins
#Test2 = Stat_Manager(2)
#Test2.weibull_chi_squared(60,1,14.500)      # don't reject; chi total 84.8121 after rebin from 60 to 50 bins
#Test3 = Stat_Manager(3)
#Test3.exponential_chi_squared(60, 0.048)    # don't reject; chi total 79.7825 after rebin from 56 to 44 bins
#Test4 = Stat_Manager(4)
#Test4.exponential_chi_squared(30, 0.21)     # don't reject; chi total 9.7014 after rebin from 30 to 19 bins
#Test5 = Stat_Manager(5)
#Test5.exponential_chi_squared(56, 0.085)    # don't reject; chi total 41.3009 after rebin from 56 to 44 bins
#Test6 = Stat_Manager(6)
#Test6.exponential_chi_squared(53, 0.11)     # don't reject; chi total 29.4318 after rebin from 53 to 36 bins