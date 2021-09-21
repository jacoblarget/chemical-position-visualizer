#!/usr/bin/env python
"""

Last Updated:
"""

# Standard modules
import numpy as np
import sys
import subprocess
from scipy.stats import gmean

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
                'fullisotropic_fit_exp_total_energy_unconstrained.dat',
                'fullisotropic_fit_exp_total_energy_constrained.dat',
                'isotropic_fit_exp_total_energy_unconstrained.dat',
                'isotropic_fit_exp_total_energy_constrained.dat',
                'anisotropic_fit_exp_total_energy_unconstrained.dat',
                'anisotropic_fit_exp_total_energy_constrained.dat',
                ## 'ohnanisotropic_fit_exp_total_energy_unconstrained.dat',
                ## 'ohnanisotropic_fit_exp_total_energy_constrained.dat',
                    ]

molecules = ['acetone','ar','chloromethane','co2','dimethyl_ether','ethane',\
        'ethanol','ethene','h2o','methane','methanol','methyl_amine','nh3']

components = ['exchange','electrostatics','induction','dhf','dispersion','total_energy']

## for imon1, mon1 in enumerate(molecules[11:]):
##     imon1 = molecules.index(mon1)

###########################################################################
######################## Command Line Arguments ###########################


###########################################################################
###########################################################################


###########################################################################
########################## Main Code ######################################

for fit_file in fit_files:
    mae_geomeans = []
    mae_geostds = []
    weighted_mae_geomeans = []
    weighted_mae_geostds = []
    print 
    print 'MAE Errors for ',fit_file

    for component in components:
        mae_geomean = []
        weighted_mae_geomean = []
        for imon1,mon1 in enumerate(molecules):
            for mon2 in molecules[imon1:]:
                [mona,monb] = sorted([mon1,mon2])
                dir_name = mona.lower() + '_' + monb.lower() + '/'

                # Get total energy data
                with open(dir_name + fit_file,'r') as f:
                    total_energy_data = [ line.split() for line in f.readlines()[1:] ]
                    total_energy_data = np.array(total_energy_data,dtype=float)

                ifile = fit_file.replace('total_energy',component)

                with open(dir_name + ifile,'r') as f:
                    data = [ line.split() for line in f.readlines()[1:] ]
                    data = np.array(data,dtype=float)

                mae_error = np.mean(data[:,0] - data[:,1])
                weighted_data = data[np.where(total_energy_data[:,0] < 0)]
                weighted_mae_error = np.mean((weighted_data[:,0] - weighted_data[:,1]))
                ## weighted_mae_error = np.mean(np.where(total_energy_data[:,0] < 0,
                ##                                        data[:,0] - data[:,1],
                ##                                        0 ))
                mae_error *= 2625.5
                weighted_mae_error *= 2625.5

                mae_geomean.append(mae_error)
                weighted_mae_geomean.append(weighted_mae_error)

        mae_geomean = np.exp(np.mean(np.log(np.abs(mae_geomean))))
        weighted_mae_geomean = np.exp(np.mean(np.log(np.abs(weighted_mae_geomean))))

        template = '{:15s}'+'\t{:16.8f}'*2
        print template.format(component,mae_geomean,weighted_mae_geomean)

    ## print mae_geomean
    ## sys.exit()

    ## mae_geomean.append(np.exp(np.mean(np.log(mae_geomean))))
    ## mae_geostds.append(np.exp(np.std(np.log(mae_geomean))))
    ## weighted_mae_geomeans.append(np.mean(np.abs(weighted_mae_geomean)))

    #weighted_mae_geostds.append(np.exp(np.std(np.log(weighted_mae_geomean))))
    #weighted_mae_geomeans.append(gmean(weighted_mae_geomean))
    #template = '{:10s}\t{:16.6e}\t{:16.6e}\n'
    #print template.format('Component','AAMAE ','','Attractive AAMAE','')
    #template = '{:15s} & {:8.3f} ({:8.3f})'
    #for line in zip(components,weighted_mae_geomeans):
    #for line in zip(components,mae_geomeans,mae_geostds,weighted_mae_geomeans,weighted_mae_geostds):
    ## print 'RMS Error Geometric Ratio:', gmean(mae_geomean)
    ## print 'Weighted RMS Error Geometric Ratio:', gmean(weighted_mae_geomean)
    print

###########################################################################
###########################################################################
