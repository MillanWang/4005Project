import numpy
import random

def time_list(datalist):
    datatotal = 0
    for x in range(0, 300):
        datatotal += float(datalist[x])
    mean = datatotal / 300
    #   Return number, adjust to seconds        The next line is from the example online I still need to figure out how it works 
    return numpy.random.exponential(mean, 1)[0]*60

class Inspector1(object):
    
    def __init__(self, data):
        self.data = data

    def generate_inspect1_time(self):
        self.datalist = open("servinsp1.dat").read().splitlines()
        return time_list(self.datalist)

    def generate_comp1(self):
        return "C1"

    #call generate_inspect1_time and generate_comp1
    Component = generate_comp1()
    inspect_time = generate_inspect1_time()

    #wait for delay
    #Find Buffer with the most space
    #place Component in the buffer with the most space
    #if there is no room signal that its blocked and wait until space opens 

class Inspector2(object):

    def __init__(self, data):
        self.data = data

    def generate_comp2or3(self):
        if random.getrandbits(1) == 1:
            return "C2"
        else:
            return "C3"
    def generate_inspect2_time(self, Component):
        if Component == "C2":
            self.datalist = open("servinsp22.dat").read().splitlines()
            return time_list(self.datalist)
        else:
            self.datalist = open("servinsp23.dat").read().splitlines()
            return time_list(self.datalist)
    
    #call generate comp2or3
    Component = generate_comp2or3()
    generate_inspect2_time(Component)
    #wait for delay
    #Send Components to the correct buffer
    #if there is no room signal that its blocked and wait until space opens 