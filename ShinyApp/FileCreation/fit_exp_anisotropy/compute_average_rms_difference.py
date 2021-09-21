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


fit_files = ['kt05_constrained_exp_total_energy_unconstrained.dat',
                'kt20_constrained_exp_total_energy_unconstrained.dat',
                'kt50_constrained_exp_total_energy_unconstrained.dat',
                    ]
    #['longrange_abs_cutoff_isa_slater_coeffs_unconstrained.dat','line_average_isa_slater_coeffs_unconstrained.dat'],\

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

for i,file1 in enumerate(fit_files):
    for file2 in fit_files[i+1:]:
        rms_tot = 0.0
        arms_tot = 0.0
        for imon1, mon1 in enumerate(molecules):
            for mon2 in molecules[imon1:]:
                with open(mon1 + '_' + mon2 + '/' + file1,'r') as f:
                    lines = f.readlines()
                    energies1 = np.array([ float(line.split()[-1]) for line in lines[1:] ])
                    sapt_energies = np.array([ float(line.split()[-2]) for line in lines[1:] ])
                with open(mon1 + '_' + mon2 + '/' + file2,'r') as f:
                    energies2 = np.array([ float(line.split()[-1]) for line in f.readlines()[1:] ])

                #rms_diff = np.sqrt(np.sum((energies1 - energies2)**2))
                rms_diffs = (energies1 - energies2)**2
                rms_diff = np.sqrt(np.sum(rms_diffs))
                rms_diff /= np.sqrt(rms_diffs.size)

                rms_diffs[(sapt_energies > 0)] = 0
                arms_diff = np.sqrt(np.sum(rms_diffs))
                arms_diff /= np.sqrt(np.sum( sapt_energies < 0))
                
                ## print mon1, mon2
                ## print rms_diff

                rms_tot += rms_diff
                arms_tot += arms_diff

        print 'TOTAL RMS:'
        print file1, file2
        dat1 = rms_tot/(len(molecules)**2)*2625.5
        dat2 = arms_tot/(len(molecules)**2)*2625.5
        template = '{:8.3f} ({:8.3f})'
        print template.format(dat1,dat2)


    ##     rms_geomeans = []
    ##     rms_geostds = []
    ##     weighted_rms_geomeans = []
    ##     weighted_rms_geostds = []
    ##     print 
    ##     print 'RMS Errors for ',fit_file

    ##     rms_geomeans.append(np.exp(np.mean(np.log(rms_geomean))))
    ##     rms_geostds.append(np.exp(np.std(np.log(rms_geomean))))
    ##     weighted_rms_geomeans.append(np.exp(np.mean(np.log(weighted_rms_geomean))))
    ##     weighted_rms_geostds.append(np.exp(np.std(np.log(weighted_rms_geomean))))
    ##     #weighted_rms_geomeans.append(gmean(weighted_rms_geomean))
    ## #template = '{:10s}\t{:16.6e}\t{:16.6e}\n'
    ## template = '{:15s}'+'\t{:^16s}'*4
    ## print template.format('Component','RMSE ','','Attractive RMSE ','')
    ## #template = '{:15s}'+ '\t{:16.8e} *// {:<8.3g}'*2 
    ## template = '{:15s}'+ '\t{:16.8g}'*2 
    ## for line in zip(components,rms_geomeans,weighted_rms_geomeans):
    ## #for line in zip(components,rms_geomeans,rms_geostds,weighted_rms_geomeans,weighted_rms_geostds):
    ##     print template.format(*line)
    ## ## print 'RMS Error Geometric Ratio:', gmean(rms_geomean)
    ## ## print 'Weighted RMS Error Geometric Ratio:', gmean(weighted_rms_geomean)
    ## print

###########################################################################
###########################################################################
