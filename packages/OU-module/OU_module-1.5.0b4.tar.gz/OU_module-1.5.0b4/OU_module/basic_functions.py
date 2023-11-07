##########################################################################################
import numpy as np
import matplotlib.pyplot as plt
import qutip as qt
import itertools
import operator

##### INTRODUCTION #######################################################################

'''

This file is a compilation of resuable functions in the research, made for ease of use
in future written programs.

ERROR HANDLING IS A PAIN, and I am too lazy to do it. When you use this function,
better make sure the inputs are correct. 

SIMULATIONS RAN PRIOR TO 2023/09/18 WILL HAVE DIFFERENT RESULTS DUE TO THE DIFFERENCE
IN THE RANDOM NUMBERS GENERATED. OLDER SIMULATIONS USING TIMELINE WILL NOT WORK. MAKE 
SURE TO EDIT ACCORDINGLY.

Written by: 
  Hendry. Department of Physics, University of Indonesia. 

'''

##########################################################################################
##### BLOCH SPHERE STATE VECTOR ##########################################################
##########################################################################################

def T2star():
    '''
    --------------------------------------------------------------------------------------
    INTRODUCTION
    --------------------------------------------------------------------------------------
        
    Returns the time constant for T2-relaxation/dephasing/decoherence in microseconds.

    --------------------------------------------------------------------------------------
    PARAMETERS
    --------------------------------------------------------------------------------------
    
    (none)
    
    '''
    
    return 3.0

##########################################################################################
##### BLOCH SPHERE STATE VECTOR ##########################################################
##########################################################################################

def bloch_psi(theta, phi):
    '''
    --------------------------------------------------------------------------------------
    INTRODUCTION
    --------------------------------------------------------------------------------------
        
    Make a qubit state parameterized by its coordinate in the Bloch sphere.

    --------------------------------------------------------------------------------------
    PARAMETERS
    --------------------------------------------------------------------------------------
    
    theta   ->  polar angle.
    
    phi     ->  azimuthal angle.

    '''
    
    return (np.cos(theta / 2) * qt.basis(2, 0) 
            + np.exp(1j * phi) * np.sin(theta / 2) * qt.basis(2, 1))


##########################################################################################
##### MAKE TIMELINE ######################################################################
##########################################################################################

def timeline(input_array : list):
    '''
    --------------------------------------------------------------------------------------
    INTRODUCTION
    --------------------------------------------------------------------------------------
        
    Makes a nested numpy array containing arrays of time values of multiple intervals, 
    all starting from zero. The reason for the starting point is that the final state of
    a process is interpreted as the initial state for the next process.
    
    The function also makes timestamps, which counts the time starting from zero of the 
    first entry. The zero of the second entry is taken to coincide with the end of the 
    first entry, so the end of the second entry is the sum of the ends of both entries. 
    This goes on for the subsequent entries.

    Lastly, the function cascades the timeline with the appropriate
    timestamps added to give the full time list.

    --------------------------------------------------------------------------------------
    PARAMETERS
    --------------------------------------------------------------------------------------
    
    input_array ->  Lists of time intervals. It is taken as a nested list with the follo-
                    wing format:

                        [[end_1, timepoints_1], [end_2, timepoints_2], ...]
                    
                    where 'end' specifies the endpoint of the interval, and 'timepoints' 
                    specifies the number of evenly-spaced points in that interval. 

                    If timepoints are all the same, an alternative input is

                        [end_1, end_2, ..., end_last, timepoints]


    '''

    if is_lst := isinstance(input_array[0], list):
        end_points, num_points = np.swapaxes(input_array, 0, 1)
    else:
        end_points = input_array[ : -1]

    '''
    List comprehension utilizing the assignment operator is also possible:

    x = 0
    stamp_lst = [0, *[x := x + endpoint for endpoint in end_points]]
    '''
    
    time_line = [np.linspace(0, end_points[i], num_points[i]) if is_lst \
               else np.linspace(0, end_points[i], input_array[-1]) \
                for i in range(len(end_points))]
    
    stamp_lst = list(itertools.accumulate([0, *end_points[ : -1]], operator.add))
    
    cascaded_timelst = np.concatenate((time_line[0], 
                        *[time_line[i] + stamp_lst[i] 
                            for i in range(1,len(end_points))]))

    return time_line, stamp_lst, cascaded_timelst

##########################################################################################
##### The Pauli Spin Matrices ############################################################
##########################################################################################

def pauli():
    '''
    --------------------------------------------------------------------------------------
    INTRODUCTION
    --------------------------------------------------------------------------------------

    Returns a list containing sigma_x, sigma_y, and sigma_z.

    '''

    return [qt.sigmax(), qt.sigmay(), qt.sigmaz()]


