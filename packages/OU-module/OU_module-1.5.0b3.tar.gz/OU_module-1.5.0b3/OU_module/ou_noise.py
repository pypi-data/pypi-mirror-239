import numpy as np
import matplotlib.pyplot as plt
import qutip as qt
from OU_module.plotting import plotter

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

class noise_params():
    
    """
    --------------------------------------------------------------------------------------
    REFERENCES
    --------------------------------------------------------------------------------------

        Genov, G. T. (2023). Optimal control design for population transfer in different
        OU noise spectra.
        
        Gillespie, D. T. (1996). Exact numerical simulation of the Ornstein-Uhlenbeck 
        process and its integral. Physical Review E, 54(2), 2084-2091. 
        https://doi.org/10.1103/PhysRevE.54.2084
        
        Lim, H. (2023). [2] Formulating the Control Problem (Personal note). 
        http://bit.ly/OU_module_personal_refs_v2_2 (Repository currently private).

    --------------------------------------------------------------------------------------
    INTRODUCTION
    --------------------------------------------------------------------------------------
    
    Constructs OU noise parameters for use in [noise] and [noise_tl].

    --------------------------------------------------------------------------------------
    PARAMETERS
    --------------------------------------------------------------------------------------
    
    name    ->  Name of the noise, is ['delta'] by default. Inputting the following
                ignores [tau] and [delta] input; they get assigned the corresponding
                values instead:
                
                "delta"     ->  tau = 25, sigma = np.sqrt(2)/3
                "epsilon"   ->  tau = 500, sigma = 0.05
    
    tau     ->  Relaxation time of the OU process, is [25] by default.
    
    sigma   ->  Steady-state standard deviation of the OU process, is [np.sqrt(2)/3] by 
                default.

    --------------------------------------------------------------------------------------

    """
    
    def __init__(self, name = "delta", tau = 25, sigma = np.sqrt(2) / 3):
        
        self.name = name
        self.tau = tau
        self.sigma = sigma
        
        if name == "delta":
            self.tau = 25
            self.sigma = np.sqrt(2) / 3
        
        if name == "epsilon":
            self.tau = 500
            self.sigma = 0.05
        
    def __str__(self):
        s = f"OU process parameter for [{self.name}]: \n"
        s += f"tau = {self.tau} us \n"
        s += f"sigma = {self.sigma}"
    
    def __repr__(self):
        return self.__str__()
    

##########################################################################################
  
def noise(timelst, sample, rng, params, init_val = None, plot = False):
    
    """
    --------------------------------------------------------------------------------------
    REFERENCES
    --------------------------------------------------------------------------------------

        Genov, G. T. (2023). Optimal control design for population transfer in different
        OU noise spectra.
        
        Gillespie, D. T. (1996). Exact numerical simulation of the Ornstein-Uhlenbeck 
        process and its integral. Physical Review E, 54(2), 2084-2091. 
        https://doi.org/10.1103/PhysRevE.54.2084
        
        Lim, H. (2023). [2] Formulating the Control Problem (Personal note). 
        http://bit.ly/OU_module_personal_refs_v2_2 (Repository currently private).
    
    --------------------------------------------------------------------------------------
    INTRODUCTION
    --------------------------------------------------------------------------------------
        
    Computes the noise, which is a stochastic Ornstein-Uhlenbeck process. 
    
    Returns an array of size (number of samples) x (number of time points).

    --------------------------------------------------------------------------------------
    PARAMETERS
    --------------------------------------------------------------------------------------
    
    timelist    ->  List of time points.
   
    sample      ->  Number of samples.
    
    rng         ->  RNG for the noise, use [numpy.random.default_rng].
    
    params      ->  Noise parameters, use [OU_module.noise_params].
        
    init_val    ->  Set fixed initial value for each sample. 
                    Can be a [list] or [numpy array] of length [sample] 
                    or one number [int] or [float] for all samples. 
                    
                    Default is [None]. 
                    
                    If [None] or any other type is passed, the intiial values are randomly 
                    taken from a Gaussian random number with mean 0 and steady-state 
                    standard deviation [sigma], in accordance to the research.
    
    plot        ->  Plot the result. [False] by default.

    --------------------------------------------------------------------------------------
    
    """
    
    tau = params.tau
    sigma = params.sigma

    exp_term = np.exp(-(timelst[1]-timelst[0]) / tau)
    sqrt_term = np.sqrt(sigma ** 2 * (1 - exp_term ** 2))

    timepoints = len(timelst)
    
    '''
    
    Meanwhile, the random number appearing in the equation for the increments have a standard deviation of 1. 
    
    The output of this function will be different from the previous versions due to the
    different orders in which the random numbers are generated. 

    '''
    
    if isinstance(init_val, (list, np.ndarray)):
        init_val = init_val
    elif isinstance(init_val, (int, float)):
        init_val = [init_val for i in range(sample)]
    else:
        init_val = rng.normal(loc = 0, scale = sigma, size = sample)
    
    out_arr = []
    
    for i in range(sample):
        x = [init_val[i]]

        rand_unitary = rng.normal(loc = 0, scale = 1, size = timepoints - 1)
        # Writing it like this is allowed, since different [rng.normal] calls return
        # different numbers. 
        
        for j in range(timepoints - 1):
            x.append(x[j] * exp_term + rand_unitary[j] * sqrt_term)
        
        out_arr.append(x)
    
    '''
    I did some testing (unfortunately the code is messy and not saved).

    List comprehension seems useful, but the recursion present in the loop demands
    variable assignment, which seems to slow down things more. 

    And while it is stated above that the number of rng.normal calls is to be
    minimized due to the computation demands, by making rand_unitary an array
    of dimension sample * (timepoints - 1) we would need to put extra resources to
    compute the indices inside the loop, which outweights the burden of creating
    rand_unitary of dimension (timepoints-1) in each sample iteration. 

    I also tried the "MATLAB way" of creating an empty array then replacing the
    values, but it is expectedly way slower.

    A big improvement is obtained when I realized that the old version had been
    calculaing the constant sqrt_term over each loop. By fixing this the computational
    time goes down tremendously.

    In any case, this version is currently the fastest one I have come with. Not that
    it really matters, since the usual case of 2500 samples and 100 timepoints takes
    less than 10 seconds to run.
    '''
    
    # Plot if specified.
    if plot:
        plotter(timelst, sample, [[params.name, out_arr]])
        # Function defined below.

    return np.array(out_arr)

##########################################################################################
##### OU NOISE + TIMELINE ################################################################
##########################################################################################

def noise_tl(timeline, sample, rng, params, init_val = None):
    
    '''
    --------------------------------------------------------------------------------------
    INTRODUCTION
    --------------------------------------------------------------------------------------
        
    Compute the OU noise for every timelist contained within [timeline]. The output is
    a nested array. The first axis corresponds to the [samples], while the second axis
    corresponds to the [timeline]. This function is compatible with [genov_tl] and
    [execute]. 

    --------------------------------------------------------------------------------------
    PARAMETERS
    --------------------------------------------------------------------------------------
    
    timeline    ->  First entry in the output tuple of [timeline].
   
    sample      ->  Number of samples.
    
    rng         ->  RNG for the noise, use [numpy.random.default_rng].
    
    name        ->  Name of the noise, is [None] by default. This function calls the 
                    default values for [tau] and [sigma] when this is specified, IGNORING 
                    those input.
                    >> 'delta'      -> delta noise
                    >> 'epsilon'    -> epsilon noise
        
    tau         ->  Relaxation time. [None] by default.
   
    sigma       ->  Steady-state standard deviation. [None] by default.
        
    init_val    ->  Set fixed initial value for the first interval in [timeline] 
                    for each sample.
                    
                    Can be a [list] or [numpy array] of length [sample] 
                    or one number [int] or [float] for all samples. 
                    
                    Default is [None]. 
                    
                    If [None] or any other type is passed, the intiial values are randomly 
                    taken from a Gaussian random number with mean 0 and steady-state 
                    standard deviation [sigma], in accordance to the research.
    
    '''

    l = len(timeline)
    
    out_arr = [noise(timelst = timeline[0], sample = sample, rng = rng, 
                     params = params, init_val = init_val)]

    for i in range(l-1):
        # Take last value of previous noise instance for each sample
        init_val = [out_arr[i][j][-1] for j in range(sample)]
        
        out_arr.append(noise(timelst = timeline[i + 1], sample = sample, 
                            rng = rng, params = params, init_val = init_val))

    return out_arr