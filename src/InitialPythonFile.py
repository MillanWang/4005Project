def first_function(i):
    return i*4*3*34*9023*3





"""
Time for performace metrics. Eventual time optimizations
"""

import time

start = time.time()
for i in range(12000*100*100):
    first_function(i)
end = time.time()
print(end - start)





"""

Inspectors getting stucc
    They inspect component, not knowing anything about the state of the buffers.
    Try to put the component on the first ordered buffer. If the buf is full, note down the buffer unstuck time. Try next
    If no buf is free, find who has the nearest unstuck time with min method on the list of tracked unbuff times 
                    get_unbuffer_time() : int 
                            return negative if buffer is free
                            return the complete time for the current product if buffer full


Step by step sim 
I1 starts at t=0 and determines the time that the inspect will complete. 
W1 knows that it's start time is at I1 complete time


Enum used to denote the state of the workstation's buffer
https://docs.python.org/3/library/enum.html



Insp putting c's onto the bufs
    Insp should have a ref to particular workstation refs. 


Time skippers. 
    Calculate the nearest time for an event. 



Somethings to test
What happens when the order of the workstations are changed
Different algorithms for distributing the components to bufs

"""