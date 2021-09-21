#!/usr/bin/env python
"""

Last Updated:
"""

# Standard modules
import numpy as np
import sys
import subprocess
from scipy.stats import gmean, binom_test, normaltest
import matplotlib as mpl
from matplotlib import colors
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.patheffects as PathEffects

# mvanvleet specific modules
#from chemistry import io
#from fit_slater_corrected_ff_parameters import FitFFParameters

###########################################################################
####################### Global Variables ##################################
error_message='''
---------------------------------------------------------------------------
Improperly formatted arguments. Proper usage is as follows:

$ python tabulate_results.py

(<...> indicates required argument, [...] indicates optional argument)
---------------------------------------------------------------------------
    '''


fit_files = [
    # ['fullisotropic_fit_exp_total_energy_unconstrained.dat','anisotropic_fit_exp_total_energy_unconstrained.dat'],
    ['anisotropic_fit_exp_total_energy_constrained.dat','fullisotropic_fit_exp_total_energy_constrained.dat'],
    ## ['anisotropic_fit_exp_total_energy_unconstrained.dat','isotropic_fit_exp_total_energy_unconstrained.dat'],
    ## ['anisotropic_fit_exp_total_energy_constrained.dat','isotropic_fit_exp_total_energy_constrained.dat'],
    ## ['isotropic_fit_exp_total_energy_constrained.dat','isotropic_fit_exp_total_energy_unconstrained.dat'],
    ## ['anisotropic_fit_exp_total_energy_constrained.dat','anisotropic_fit_exp_total_energy_unconstrained.dat'],
    ## ['fullisotropic_fit_exp_total_energy_unconstrained.dat','isotropic_fit_exp_total_energy_unconstrained.dat'],
    ## ['fullisotropic_fit_exp_total_energy_constrained.dat','isotropic_fit_exp_total_energy_constrained.dat'],
        ]
    #['longrange_abs_cutoff_isa_slater_total_energy_unconstrained.dat','line_average_isa_slater_total_energy_unconstrained.dat'],\

molecules = ['acetone','ar','chloromethane','co2','dimethyl_ether','ethane',\
        'ethanol','ethene','h2o','methane','methanol','methyl_amine','nh3']

names = ['Acetone','Ar','Chloromethane','CO$_2$',
            'Dimethyl Ether','Ethane',
            'Ethanol','Ethene','H$_2$O',
            'Methane','Methanol','Methyl Amine','NH$_3$']

#components = ['Exchange','Electrostatics','Induction','Dhf','Dispersion','Total_Energy']
components = ['total_energy']

## for imon1, mon1 in enumerate(molecules[11:]):
##     imon1 = molecules.index(mon1)

###########################################################################
######################## Command Line Arguments ###########################


###########################################################################
###########################################################################


###########################################################################
########################## Main Code ######################################

for fit_file in fit_files:
    all_rms_ratios = []
    all_weighted_rms_ratios = []
    homodimer_weighted_rms_ratios = {}

    print 'RMS Error Ratios between ',fit_file[0],' and ',fit_file[1]
    print '-'*155
    template = '{:15s}' + '{:10s}\t|\t'*len(components)
    print template.format('',*components)
    print '-'*155
    for imon1,mon1 in enumerate(molecules):
        for mon2 in molecules:
            rms_ratios = []
            weighted_rms_ratios = []
            errors1 = []
            errors2 = []

            [mona,monb] = sorted([mon1,mon2])
            dir_name = mona.lower() + '_' + monb.lower() + '/'
            for component in components:


                # Get total energy data
                with open(dir_name + fit_file[0],'r') as f:
                    total_energy_data = [ line.split() for line in f.readlines()[1:] ]
                    total_energy_data = np.array(total_energy_data,dtype=float)

                rmse_errors = []
                weighted_rmse_errors = []
                for ifile in fit_file:
                    ifile = ifile.replace('total_energy',component)

                    with open(dir_name + ifile,'r') as f:
                        data = [ line.split() for line in f.readlines()[1:] ]
                        data = np.array(data,dtype=float)

                    rmse_error = np.sqrt(np.mean((data[:,0] - data[:,1])**2))
                    weighted_data = data[np.where(total_energy_data[:,0] < 0)]
                    weighted_rmse_error = np.sqrt(np.mean((weighted_data[:,0] -
                         weighted_data[:,1])**2))

                    rmse_errors.append(rmse_error)
                    weighted_rmse_errors.append(weighted_rmse_error)

                rmse_error_ratio = rmse_errors[0]/rmse_errors[1]
                weighted_rmse_error_ratio = weighted_rmse_errors[0]/weighted_rmse_errors[1]

                rms_ratios.append(rmse_error_ratio)
                weighted_rms_ratios.append(weighted_rmse_error_ratio)

            all_rms_ratios.append(rms_ratios)
            all_weighted_rms_ratios.append(weighted_rms_ratios)
            if mon1 == mon2:
                homodimer_weighted_rms_ratios[mon1] = weighted_rms_ratios


    print
    print

    count = 0
    palette = sns.color_palette("husl", 13)
    ncols=4
    nrows=4
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, sharex=True,
            sharey=True, figsize=(16,16))
    cmap = colors.ListedColormap(palette)
    for imon1,mon1 in enumerate(molecules):
        avg_ratios = []
        ratios = []
        c1 = []
        c2 = []
        for imon2,mon2 in enumerate(molecules):
            ratio = all_weighted_rms_ratios[count][0]
            count += 1
            ratios1 = homodimer_weighted_rms_ratios[mon1][0]
            ratios2 = homodimer_weighted_rms_ratios[mon2][0]

            #avg_ratio = (ratios1 + ratios2)/2
            avg_ratio = np.sqrt(ratios1 * ratios2)


            avg_ratios.append(avg_ratio)
            ratios.append(ratio)
            c1.append(imon1)
            c2.append(imon1+imon2)
        ax = axes[ imon1 / nrows, imon1 % nrows]
        #ax.scatter(avg_ratios, ratios, marker=',', s=75, c=c1, lw=3.0, cmap=cmap)
        ax.scatter(avg_ratios, ratios, marker=',', s=75, c=palette[imon1],lw=2.0)
        lims = [0,1]
        ax.plot(lims, lims, 'k-')
        ax.set_xlim(lims)
        ax.set_ylim(lims)
        ax.set_title(mon1)

    #print mon1, mon2, ratio[0], ratios1[0], ratios2[0]
    ## print cmap(c1)
    ## ax.scatter(avg_ratios, ratios, marker='1', s=75, c=c1, lw=3.0, cmap=cmap)
    ## ax.scatter(avg_ratios, ratios, marker='2', s=75, c=c2, lw=3.0, cmap=cmap)
    ## ax.scatter(avg_ratios, ratios, marker=',', s=75, c=c1, lw=3.0, cmap=cmap)
    #ax.scatter(avg_ratios, ratios, s=75, c=c2, cmap=cmap)
    #ax.plot(avg_ratio, avg_ratio, 'k-')

                    
    fig.savefig('grid_error_ratios.pdf',bbox_inches='tight',dpi=100)
    plt.show()
    exit()



###########################################################################
###########################################################################
