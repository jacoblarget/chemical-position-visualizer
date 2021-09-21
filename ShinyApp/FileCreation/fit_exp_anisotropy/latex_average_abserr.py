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


fit_files = ['isa_constrained_exp_coeffs_unconstrained.out',
                'saptff_constrained_exp_coeffs_unconstrained.out',
                'isa_constrained_exp_coeffs_constrained.out',
                'saptff_constrained_exp_coeffs_constrained.out',
                'old_isa_constrained_exp_coeffs_unconstrained.out',
                'old_saptff_constrained_exp_coeffs_unconstrained.out',
                ]
    #['longrange_abs_cutoff_isa_slater_coeffs_unconstrained.out','line_average_isa_slater_coeffs_unconstrained.out'],\

molecules = ['acetone','ar','chloromethane','co2','dimethyl_ether','ethane',\
        'ethanol','ethene','h2o','methane','methanol','methyl_amine','nh3']

components = ['Exchange','Electrostatics','Induction','Dhf','Dispersion','Total_Energy']

## for imon1, mon1 in enumerate(molecules[11:]):
##     imon1 = molecules.index(mon1)

###########################################################################
######################## Command Line Arguments ###########################


###########################################################################
###########################################################################


###########################################################################
########################## Main Code ######################################

for fit_file in fit_files:
    rms_geomeans = []
    rms_geostds = []
    weighted_rms_geomeans = []
    weighted_rms_geostds = []
    print 
    print 'RMS Errors for ',fit_file
    for component in components:
        rms_geomean = []
        weighted_rms_geomean = []
        for imon1,mon1 in enumerate(molecules):
            for mon2 in molecules[imon1:]:
                [mona,monb] = sorted([mon1,mon2])
                dir_name = mona.lower() + '_' + monb.lower() + '/'

                rms_errors = subprocess.check_output('grep "' + component + ' RMS Error" ' + dir_name + fit_file + " | awk '{print $4}'", shell=True)
                weighted_rms_errors = subprocess.check_output('grep "' +
                        component + ' Weighted Absolute Error" ' + dir_name + fit_file + " | awk '{print $5}'", shell=True)
                #absolute_errors1 = subprocess.check_output('grep "' + component + ' Weighted Absolute Error" ' + dir_name + fit_file[0] + " | awk '{print $5}'", shell=True)
                #weighted_rms_errors1 = subprocess.check_output('grep "Weighted Least" ' + dir_name + fit_file[0] + " | awk '{print $4}'", shell=True)
                ## rms_errors2 = subprocess.check_output('grep "RMS Error" ' + dir_name + fit_file[1] + " | awk '{print $3}'", shell=True)
                ## weighted_rms_errors2 = subprocess.check_output('grep "Weighted Least" ' + dir_name + fit_file[1] + " | awk '{print $4}'", shell=True)

                rms_errors = [2625.5*float(i) for i in rms_errors.split()]
                weighted_rms_errors = [2625.5*abs(float(i)) for i in weighted_rms_errors.split()]

                rms_geomean.append(rms_errors[-1])
                weighted_rms_geomean.append(weighted_rms_errors[-1])

        rms_geomeans.append(np.exp(np.mean(np.log(rms_geomean))))
        rms_geostds.append(np.exp(np.std(np.log(rms_geomean))))
        weighted_rms_geomeans.append(np.exp(np.mean(np.log(weighted_rms_geomean))))
        weighted_rms_geostds.append(np.exp(np.std(np.log(weighted_rms_geomean))))
        #weighted_rms_geomeans.append(gmean(weighted_rms_geomean))
    #template = '{:10s}\t{:16.6e}\t{:16.6e}\n'
    template = '{:15s}'+'\t{:^16s}'*4
    print template.format('Component','RMSE ','','Attractive RMSE ','')
    #template = '{:15s}'+ '\t{:16.8e} *// {:<8.3g}'*2 
    template = '{:15s} & & {:8.3f} ({:8.3f})'
    for line in zip(components,rms_geomeans,weighted_rms_geomeans):
    #for line in zip(components,rms_geomeans,rms_geostds,weighted_rms_geomeans,weighted_rms_geostds):
        print template.format(*line)
    ## print 'RMS Error Geometric Ratio:', gmean(rms_geomean)
    ## print 'Weighted RMS Error Geometric Ratio:', gmean(weighted_rms_geomean)
    print

###########################################################################
###########################################################################
