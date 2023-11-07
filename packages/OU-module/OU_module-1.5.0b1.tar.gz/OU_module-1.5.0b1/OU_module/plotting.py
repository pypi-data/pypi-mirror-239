##########################################################################################
import numpy as np
import matplotlib.pyplot as plt
import qutip as qt

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
##### Plotting ###########################################################################
##########################################################################################

def plotter(timelst, sample, plotdata):
    '''
    --------------------------------------------------------------------------------------
    INTRODUCTION
    --------------------------------------------------------------------------------------

    Returns one figure containing plots of all the specified quantities vs time. 
    
    Able to do multiple samples in one plot.

    The plots are stacked vertically. 
    
    This is useful for our purposes since we usually want to compare some quantities at 
    a given time. 

    I try to keep to codes simple. Extra features are to be added when needed. 

    Note that this plotting function will not be used all that much. Considering the 
    diversity of graphs we make in the research, directly using matplotlib would be a 
    better idea.

    --------------------------------------------------------------------------------------
    PARAMETERS
    --------------------------------------------------------------------------------------

    timelst     -> Time list.

    sample      -> Number of samples. Only to be shown at the top of the figure.
    
    plotdata    -> The data to plot, written like so:
                    [
                        [plot_1_name, [
                                        [plot1_sample1], [plot1_sample2],...
                                                                            ]
                                                                             ],
                        [plot_2_name, [
                                        [plot2_sample1], [plot2_sample2],...
                                                                            ]
                                                                             ],
                        ...
                                                                                    ]
                    For example,
                    [['delta', [[delta_sample1], [delta_sample2]]], 
                     ['epsilon', [[epsilon_sample1], [epsilon_sample2]]]

                    It's a list of what to plot in each plot,
                     
                    containing a 2-entry list of the name of the vertical axis and
                    the data to plot,
                     
                    the data to plot being a list
                     
                    of lists corresponding to each sample.

                    In other words, it is a FOUR DIMENSIONAL list. 
                    
                    One might find it convoluted at first, but a little work 
                    with it should make one used to it.

                    plot_x_name can be chosen from the dictionary in the program.

    --------------------------------------------------------------------------------------
    '''

    # Making the subplotss
    fig, ax = plt.subplots(len(plotdata), num = 'Plotted with [OU_module.plotter]')

    # Make a dummy array to avoid indexing error for the case of 1 plot
    if not(isinstance(ax, np.ndarray)):
        ax = [ax, ax] 

    # Set things up for the plot
    ax[0].set_title(f'Number of samples: {sample}')
    ax[-1].set_xlabel('$time$')

    # A dictionary for naming the vertical axis
    ydict = {
        'delta'         :   "$\delta$",
        'epsilon'       :   '$\epsilon$',
        'expsigmax'     :   '$<\sigma_x>$',
        'expsigmay'     :   '$<\sigma_y>$',
        'expsigmaz'     :   '$<\sigma_z>$',
        'meanexpsigmax' :   '$\overline{<\sigma_x>}$',
        'meanexpsigmay' :   '$\overline{<\sigma_y>}$',
        'meanexpsigmaz' :   '$\overline{<\sigma_z>}$',
        ''              :   ''
    }

    # Plotting
    for i in range(len(plotdata)):
        # Get the y-label name from the input
        name = plotdata[i][0]   

        # Set the y-label
        ax[i].set_ylabel(ydict[name])
                
        for j in range(len(plotdata[i][1])):
                        # range(sample) is not used here so that
                        # plots such as 'meanexpsigmaz' with only
                        # one value for one time can be plotted 
                        # together with those whose values vary
                        # with the sample. 
            ax[i].plot(timelst, plotdata[i][1][j])
    
    plt.show()


def blochplotter(quantity, plotdata):
    '''
    --------------------------------------------------------------------------------------
    INTRODUCTION
    --------------------------------------------------------------------------------------
    This function plots the result of [qutip.mesolve] onto the bloch sphere, for multiple
    samples. Each samples is plotted in one separate plot. 

    --------------------------------------------------------------------------------------
    PARAMETERS
    --------------------------------------------------------------------------------------
    quantity    -> Object to print:
                    >> states   ->  obtained from qutip.mesolve().states
                    >> sigma    ->  obtained from qutip.mesolve().expect
                                    with e_ops = [sigmax(), sigmay(), sigmaz()]

    plotdata    -> The data to plot, written like so:
                    [[point_set_1], [point_set_2], ...]
                   
                   states   -> point_set_x = mesolve().states.

                   sigma    -> point_set_x = mesolve().expect[0], .expect[1], .expect[2]
                                                       (sigmax)    (sigmay)    (sigmaz)  

    --------------------------------------------------------------------------------------
    '''

    # List to store Bloch sphere figures
    b = []

    # Get the number of samples
    sample = len(plotdata)

    # Making one Bloch sphere for each sample, with the object plotted
    # depending on the input.
    for i in range(sample):
        b.append(qt.Bloch())

        if quantity == 'states':
            b[i].add_states(plotdata[i][0])

        if quantity == 'sigma':
            # Plot with point and line
            b[i].add_points(plotdata[i])
            b[i].add_points(plotdata[i], meth = 'l')
            # Also plot the initial and final vectors.
            b[i].add_vectors([plotdata[i][0][0], plotdata[i][1][0], plotdata[i][2][0]])
            b[i].add_vectors([plotdata[i][0][-1], plotdata[i][1][-1], plotdata[i][2][-1]])
        
        b[i].show()
    
    plt.show()