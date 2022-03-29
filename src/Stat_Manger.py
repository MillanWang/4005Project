import math
import numpy
import os
import random
from Grapher import Grapher
import numpy as np

def weibull_inverse_cdf(p, k, lamb):
    """
        Calculate the inverse cumulative distribution function of the Weibull distribution given 
        a p-value, k-value and lambda.
    """
    return lamb * ((-np.log(1-p))**(1/k))

def expo_inverse_cdf(p, lamb):
    """
        Calculate the inverse cumulative distribution function of the Exponential distribution given 
        a p-value lambda.
    """
    return (-np.log(1-p))/lamb

def calculateRSquared(xList, yList):
    """
        Calculate the coefficent of determination of a relation given the x and y values
    """
    num = 0
    dem1 = 0
    dem2 = 0
    yAvg = sum(yList)/len(yList)
    xAvg = sum(xList)/len(xList)
    
    for i in range(len(xList)):
        a = (xList[i] - xAvg)*(yList[i] - yAvg)
        num += a
        
        b = (xList[i] - xAvg)**2
        dem1 += b
        
        c = (yList[i] - yAvg)**2
        dem2 += c
    
    dem = math.sqrt(dem1*dem2)
    return (num/dem)**2

def createReport(k, lamb, rSquared, file):
    """
        Append coefficent of determination dervied using k and lambda into the given file. (For Weibull distribution)
    """
    f = open("../output/reports/" + file, 'a')
    f.write("k = " + str(k) + ", lambda = " + str(lamb) + ", R^2 = " + str(rSquared) + "\n")
    f.close()
    
def createReportExpo(lamb, rSquared, file):
    """
        Append coefficent of determination dervied using lambda into the given file. (For Exponential distribution)
    """
    f = open("../output/reports/" + file, 'a')
    f.write("lambda = " + str(lamb) + ", R^2 = " + str(rSquared) + "\n")
    f.close()    
    

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


    def exponential_chi_squared(self):
        """
            Conduct a chi squared test, checking for fit with an exponential distribution
        
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
            expected_frequencies.append((self.exponential_cdf(i+1,exponential_lambda)-self.exponential_cdf(i,exponential_lambda))*300)
            
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


    def weibull_chi_squared(self):
        """
        Conduct a chi squared test, checking for fit with weibull distribution
        """
        # (intlist,qq_list, mean, variance, count, sample_sum)
        # self.__dat_file_contents
        sorted_data = self.__dat_file_contents[1]
        print(sorted_data[-1])
        # Calculating number of bins and bin width
        q25, q75 = np.percentile(sorted_data, [25, 75])
        bin_width = 2 * (q75 - q25) * len(sorted_data) ** (-1/3)
        k_intervals = round((max(sorted_data) - min(sorted_data)) / bin_width)


        weibull_k = 1
        weibull_b = 1

        expected_frequencies = []
        for i in range(k_intervals+1):
            expected_frequencies.append((self.weibull_cdf(i+1,weibull_k,weibull_b)-self.weibull_cdf(i,weibull_k,weibull_b))*300)
            
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
    
    def weibull_quantile_calc(self, k, lamb, name):
        """
            Calculates the quantile of a weibull distribution
        """
        result = []
        listItem = self.__dat_file_contents[1]
        for i in range(len(listItem)):
            p = ((i+1)-0.5)/len(listItem)
            q = weibull_inverse_cdf(p, k, lamb)
            result.append(q)

        Grapher.build_qq_plot(listItem, result, name)
        return calculateRSquared(listItem, result)
        
    def expo_quantile_calc(self, lamb, name):
        """
            Calculattes the qualtile of an exponential distribution
        """
        result = []
        listItem = self.__dat_file_contents[1]
        for i in range(len(listItem)):
            p = ((i+1)-0.5)/len(listItem)
            q = expo_inverse_cdf(p, lamb)
            result.append(q)
        Grapher.build_qq_plot(listItem, result, name)
        return calculateRSquared(listItem, result)
        

    def weibull_cdf(x,k,b):
        """
            Calculates the cumulative frequency from a weibull distribution
        """
        return 1 - math.exp(-b*math.pow(x,k))



    def exponential_cdf(x,ld):
        """
            Calculates the cumulative frequency of an exponential distribution
        """
        return 1 - math.exp(-x*ld)
    

# Stat manager objects for each dataset 
stat_man_obj_serv1 = Stat_Manager(1)
stat_man_obj_serv22 = Stat_Manager(2)
stat_man_obj_serv23 = Stat_Manager(3)
stat_man_obj_ws1 = Stat_Manager(4)
stat_man_obj_ws2 = Stat_Manager(5)
stat_man_obj_ws3 = Stat_Manager(6)


# DO NOT DELETE: USED FOR PARAM ESTIMATION ITERATION

# for i in range(1, 50):
#     for j in range(9000, 16000, 500):
#         k = i/4
#         name1 = "Inspector 1 Weibull QQ Plot, (k, lambda) = " + str(k) + ", " + str(j)
#         name2 = "Inspector 2, Component 2 Weibull QQ Plot, (k, lambda) = " + str(k) + ", " + str(j)
#         r1 = stat_man_obj_serv1.weibull_quantile_calc(k, j, name1)
#         r2 = stat_man_obj_serv22.weibull_quantile_calc(k, j, name2)
#          createReport(k, j, r1, "servinsp1_report.txt")
#          createReport(k, j, r2, "servinsp22_report.txt")
        
# for i in range(1, 100):
#     k = i/4
#     name1 = "Inspector 2, Component 3 Exponential QQ Plot, k = " + str(k)
#     name2 = "Workstation 1 Exponential QQ Plot, k = " + str(k)
#     name3 = "Workstation 2 Exponential QQ Plot, k = " + str(k)
#     name4 = "Workstation 3 Exponential QQ Plot, k = " + str(k)
#     r1 = stat_man_obj_serv23.expo_quantile_calc(k, name1)
#     r2 = stat_man_obj_ws1.expo_quantile_calc(k, name2)
#     r3 = stat_man_obj_ws2.expo_quantile_calc(k, name3)
#     r4 = stat_man_obj_ws3.expo_quantile_calc(k, name3)
#     createReportExpo(k, r1, "servinsp23_report.txt")
#     createReportExpo(k, r2, "ws1_report.txt")
#     createReportExpo(k, r3, "ws2_report.txt")
#     createReportExpo(k, r4, "ws3_report.txt")
    

    