import numpy
import random
from SimulationEnums import Component


def mean(self, component):
    if component == Component.C1:
        self.datalist = open("servinsp1.dat").read().splitlines()  
    elif component == Component.C2:
        self.datalist = open("servinsp22.dat").read().splitlines()  
    else:
        self.datalist = open("servinsp23.dat").read().splitlines()
    datatotal = 0
    for x in range(0, 300):
        datatotal += float(self.datalist[x])
    mean = datatotal / 300
    return mean

def generate_inspect_time(component, mean):
    time = numpy.random.exponential(mean, 1)[0]*60
    return time, component


class Inspector1(object):

    def __init__(self, data):
        self.data = data
    
    def __generate_comp1(self):
        return Component.C1

    # call generate_inspect1_time and generate_comp1
    component = __generate_comp1()
    mean = mean(component)
    inspect_time = generate_inspect_time(component, mean )

    # wait for delay
    # Find Buffer with the most space
    # place Component in the buffer with the most space
    # if there is no room signal that its blocked and wait until space opens


class Inspector2(object):

    def __init__(self, data):
        self.data = data

    def __generate_comp2or3(self):
        if random.getrandbits(1) == 1:
            return Component.C2
        else:
            return Component.C3

   

    # call generate comp2or3
    component = __generate_comp2or3()
    mean = mean(component)
    inspect_time = generate_inspect_time(component, mean)
    

    # wait for delay
    # Send Components to the correct buffer
    # if there is no room signal that its blocked and wait until space opens
