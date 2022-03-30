import time
import math
from Multiplicative_Congruential_Model import Multiplicative_Congruential_Model

class Lecuyer_Generator(object):
    """
        Class for uniform pseudorandom number generation  
    """

    def __init__(self, seed:int) -> None:
        """
            Constructor for Lecuyer_Generator
        """
        clean_seed = seed if seed!=0 and seed<=2147483398 else 1
        self.__x2 = Multiplicative_Congruential_Model(clean_seed, 40692, 2147483399)
        clean_seed = self.__x2.get_next_x() + 1 #Guaranteed in range [1, 2147483562]
        self.__x1 = Multiplicative_Congruential_Model(clean_seed, 40014, 2147483563)
    
    def __get_next_x(self) -> int:
        """
            Returns the next pseudorandom integer using Lecuyer's algorithm
        """
        return (self.__x1.get_next_x() - self.__x2.get_next_x()) % 2147483562

    def get_next_r(self) -> float:
        """
            Returns the next pseudorandom number from a uniform distribution between 0 and 1
        """
        generated_x = self.__get_next_x()
        if generated_x==0:
            return 2147483562 / 2147483563
        else:
            return generated_x / 2147483563

def run_kolmogorov_smirnov_test():
    """
        Conducts a Kolmogorov-Smirnov test on a Lecuyer_Generator
    """
    print("Starting Kolmogorov-Smirnov test...")
    D_table = 1.36/math.sqrt(100)

    # Generate a list of 100 random numbers and the list of expected uniform cdf's
    generator = Lecuyer_Generator(round(time.time()))
    list_of_randoms = []
    expected_cdf = []
    for i in range(100):
        expected_cdf.append((i+1)/100)
        list_of_randoms.append(generator.get_next_r()) 

    # Sort the list
    list_of_randoms.sort()

    #Instantiate the D lists with first elements (D_minus first element unique procedure)
    D_plus = [expected_cdf[0]-list_of_randoms[0]]
    D_minus = [list_of_randoms[0]]

    for i in range(1,100):
        D_plus.append(expected_cdf[i]-list_of_randoms[i])
        D_minus.append(list_of_randoms[i]-expected_cdf[i-1])
    print("Max D_plus value: " + str(max(D_plus)))
    print("Max D_minus value: " + str(max(D_minus)))
    print("D_table value to beat: " + str(D_table))
    
    if max(max(D_plus),max(D_plus)) < D_table:
        print("Null Hypothesis is NOT rejected")
        print("Kolmogorov-Smirnov test passed\n\n")
        return True
    else:
        print("Null Hypothesis is REJECTED")
        print("Kolmogorov-Smirnov test FAILED\n\n")
        return False

def run_autocorrelation_test():
    """
        Conducts an autocorrelation test on a Lecuyer_Generator instance
    """
    
    print("Starting Autocorrelation test...")

    #Setup constants and variables
    clean_n = 1000
    clean_i = 1
    lag_m = 1 # from brightspace
    z_table_value = 1.96 # corresponds to alpha=0.05 halved
    big_M = (clean_n-clean_i)//lag_m - 1

    generator = Lecuyer_Generator(round(time.time()))

    print("Big M has a value of "+ str(big_M))

    #Create an n sized list of randomly generated numbers
    r_list = []
    for j in range(clean_n):
        r_list.append(generator.get_next_r())
    
    #Autocorrelation procedure
    sum_of_subsequent_products = 0
    previous_r = r_list[clean_i]
    for j in range(clean_i+lag_m, big_M+1):
        sum_of_subsequent_products += r_list[j] * previous_r
        previous_r = r_list[j]

    p_im = (1/(big_M+1))*sum_of_subsequent_products - 0.25
    sigma_im = math.sqrt(13*big_M+7) / (12*(big_M+1))
    generated_z = (p_im/sigma_im)
    if generated_z < z_table_value :
        print("Null Hypothesis is NOT rejected")
        print("Autocorrelation test passed with M="+str(big_M)+" and Z="+str(generated_z)+"\n\n")
        return True
    else:
        print("Null Hypothesis is REJECTED")
        print("Autocorrelation test failed with M="+str(big_M)+" and Z="+str(generated_z)+"\n\n")
        return False 



# run_kolmogorov_smirnov_test()
# run_autocorrelation_test()
