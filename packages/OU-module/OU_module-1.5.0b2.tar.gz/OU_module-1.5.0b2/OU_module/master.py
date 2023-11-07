##########################################################################################
import numpy as np
import matplotlib.pyplot as plt
import qutip as qt
from OU_module.basic_functions import pauli

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
##### Genov's Hamiltonian ################################################################
##########################################################################################

def genov(timelst, sample, Omega_1 = 0, f = 1, phi = 0, g = 0, 
          omega_s = 0, xi = 0, delta = 0, epsilon = 0):
    '''           
    --------------------------------------------------------------------------------------
    INTRODUCTION
    --------------------------------------------------------------------------------------

    Computes the full form of Genov's Hamiltonian in the interaction picture and RWA 
    approximation:

        H = delta(t) * sz / 2 
            + Omega_1 * f(t) * (1 + epsilon(t)) * (cos(phi(t)) * sx + sin(phi(t)) * sy)
            + g * sz * cos(omega_s * t + xi) / 2

    for ONE SAMPLE. 
    
    Returns a list which we can directly pass as a [qutip.mesolve] Hamiltonian argument. 

    The default values return the Hamiltonian argument corresponding to
        H = 0
        
    For multiple samples call this function for each sample. This function does not 
    support multiple-sample calls since looping will be needed for [qutip.mesolve] calls
    anyway. 

    --------------------------------------------------------------------------------------
    PARAMETERS
    --------------------------------------------------------------------------------------

    timelst -> Time list for evaluation of Hamiltonian.

    delta   -> Random noise for the precession about the z-axis, the off-resonance error.
    
    epsilon -> Random noise for f, the pulse length/amplitude error.
        
        [delta] and [epsilon] are ARRAYS obtained from [OU_module.noise]. LEAVE EMPTY
        FOR NO NOISE HAMILTONIAN.

    f       -> Modulation to the peak rabi frequency.
    
    phi     -> Axis control phase of the pulse.
        
        For the sake of simplicity, [f], and [phi] can be FUNCTIONS, LISTS, or NUMBERS.
    
    Omega_1 -> Peak rabi frequency, the frequency of the precession about the pulse axis.
    
    g       -> Probing amplitude.
    
    omega_s -> Probing frequency.
    
    xi      -> Unknown phase of probing.

        These four are CONSTANTS.

    --------------------------------------------------------------------------------------

    '''
    
    '''There is really no reason to use different parameters between samples other than 
    the noises, so we do not take those into account.'''
    
    def ff(timelst):

        if callable(f):
            return f(timelst)
        
        elif isinstance(f, (list, np.ndarray)):
            return f
        
        else:
            arr_f = np.empty(shape = (len(timelst),))
            arr_f.fill(f)
            return arr_f
        
    def phii(timelst):

        if callable(phi):
            return phi(timelst)
        
        elif isinstance(phi, (list, np.ndarray)):
            return phi
        
        else:
            arr_phi = np.empty(shape = (len(timelst),))
            arr_phi.fill(phi)
            return arr_phi
    
    sx, sy, sz = pauli()
    
    if not(isinstance(delta, np.ndarray)):
        delta = np.zeros(shape = (sample, len(timelst)))

    if not(isinstance(epsilon, np.ndarray)):
        epsilon = np.zeros(shape = (sample, len(timelst)))
        
    out_lst = []
    for i in range(sample):
                    
        # Building the Hamiltonian entry for [qutip.mesolve]
        # First term, td = time dependence
        H1 = sz / 2
        H1_td = delta[i]

        # Second term
        H2x = Omega_1 / 2 * sx
        H2x_td = ff(timelst) * (1 + epsilon[i]) * np.cos(phii(timelst))

        H2y = Omega_1 / 2 * sy
        H2y_td = ff(timelst) * (1 + epsilon[i]) * np.sin(phii(timelst))

        # Third term
        H3 = g / 2 * sz
        H3_td = np.cos(omega_s * timelst.astype(float) + xi)

    out_lst.append([[H1, H1_td], [H2x, H2x_td], [H2y, H2y_td], [H3, H3_td]])
    
    return out_lst

##########################################################################################
##### GENOV + TIMELINE ###################################################################
##########################################################################################

def genov_tl(timeline, sample, Omega_1_lst = 0, f_lst = 1, phi_lst = 0, g_lst = 0, 
             omega_s_lst = 0, xi_lst = 0, delta_lst = 0, epsilon_lst = 0):
    '''
    --------------------------------------------------------------------------------------
    INTRODUCTION
    --------------------------------------------------------------------------------------
        
    Compute the Genov Hamiltonian for every timelist contained within [timeline]. Every
    time interval has a different syntax for [genov] corresponding to the different 
    processes, so unlike in [noise_tl] the Hamiltonian parameters are taken in as LISTS.

    --------------------------------------------------------------------------------------
    PARAMETERS
    --------------------------------------------------------------------------------------

    (see [timeline] and [genov]). 
    
    "_lst" is added to explicitly say that the variables are taken as LISTS corresponding 
    to [timeline]. There is no need for variations between samples. 

    If a single number is passed in instead, this function will make a list with the same
    length as the timeline and put in that number for all entries. 

    For the OU noises, the function generates a nested array full of zeros as the default
    values. Passing in other numbers does not work and is useless for the physics, so I
    will not deal with it. 

    Note that the first index of the noise lists passed into the argument corresponds to 
    [timeline]. 

    '''
    
    l = len(timeline)
    
    # Change the input into a list if a single number is passed in.
    param_lst = [Omega_1_lst, f_lst, phi_lst, g_lst, omega_s_lst, xi_lst]

    for i in range(len(param_lst)):

        if not(isinstance(param_lst[i], list)) and not(isinstance(param_lst[i], np.ndarray)):

            param_lst[i] = np.full(shape = (l,), fill_value = param_lst[i])

    # For the OU noises, the form is a bit different:
    noise = [delta_lst, epsilon_lst]

    for i in range(len(noise)):

        if not(isinstance(noise[i], list)) and not(isinstance(noise[i], np.ndarray)):
                
            noise[i] = [np.zeros(shape = (len(timeline[j]),)) for j in range(l)]

    out_arr = []
    for i in range(l):
        Omega_1 = param_lst[0][i]
        f = param_lst[1][i]
        phi = param_lst[2][i]
        g = param_lst[3][i]
        omega_s = param_lst[4][i]
        xi = param_lst[5][i]
        delta = noise[0][i]
        epsilon = noise[1][i]
        out_arr.append(genov(timelst = timeline[i], sample = sample, 
                              Omega_1 = Omega_1, f = f, phi = phi,
                              g = g, omega_s = omega_s, xi = xi, delta = delta,
                              epsilon = epsilon)
                        for i in range(l))
    
    return out_arr

##########################################################################################
##### EXECUTE MESOLVE OVER A TIMELINE ####################################################
##########################################################################################

def execute(timeline, sample, rho0, Ham, flatten = False):
    '''
    --------------------------------------------------------------------------------------
    INTRODUCTION
    --------------------------------------------------------------------------------------
    
    This program executes multiple mesolve corresponding to different time intervals and 
    different Hamiltonians. The main purpose of this function is so that a whole 
    simulation of different operations (e.g. free precession, then 90-rotation, then free 
    precession again, then 90-rotation again) can be executed with the call of a function.
    
    To make this function as useful as possible, it needs to stay as general as possible.
    So, I made this function to output only the states of the system for the whole
    [timeline] for all [sample]. With QuTiP, we can do a lot of things with the states, 
    after all.

    This function returns a nested array, each array inside contains the result states 
    from a single mesolve. 
    
    The states passed as arguments into mesolve can be chosen to stay constant. Each 
    array are independent of each other, allowing multiple independent mesolve calls. 
    
    The end state of one mesolve is taken as the initial state for the next mesolve. 

    --------------------------------------------------------------------------------------
    PARAMETERS
    --------------------------------------------------------------------------------------

    timeline    ->  see [timeline].

    rho0        ->  initial state.

    Ham         ->  List of Hamiltonian, use [genov_tl].

    flatten     ->  flatten the list of mesolve solutions with respect to [timeline].
    '''
    
    l = len(timeline)
    
    out_arr = []

    for i in range(sample):
        
        per_sample = []

        for j in range(l):
            rho = qt.mesolve(Ham[j][i], rho0, timeline[j]).states

            per_sample.append(rho)
                
            rho0 = rho[-1]
            
        if flatten:
            per_sample = sum(per_sample, [])
        
        out_arr.append(per_sample)
    
    return out_arr
