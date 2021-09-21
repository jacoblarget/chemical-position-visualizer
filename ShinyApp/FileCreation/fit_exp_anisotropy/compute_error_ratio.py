#!/usr/bin/env python
"""

Last Updated:
"""

# Standard modules
import numpy as np
import sys
import subprocess
from scipy.stats import gmean, binom_test, normaltest

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
    ['anisotropic_fit_exp_coeffs_unconstrained.out','fullisotropic_fit_exp_coeffs_unconstrained.out'],
    ['anisotropic_fit_exp_coeffs_unconstrained.out','isotropic_fit_exp_coeffs_unconstrained.out'],
    ['anisotropic_fit_exp_coeffs_constrained.out','isotropic_fit_exp_coeffs_constrained.out'],
    ['isotropic_fit_exp_coeffs_constrained.out','isotropic_fit_exp_coeffs_unconstrained.out'],
    ['anisotropic_fit_exp_coeffs_constrained.out','anisotropic_fit_exp_coeffs_unconstrained.out'],
    ['fullisotropic_fit_exp_coeffs_unconstrained.out','isotropic_fit_exp_coeffs_unconstrained.out'],
    ['fullisotropic_fit_exp_coeffs_constrained.out','isotropic_fit_exp_coeffs_constrained.out'],
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
    sign_test_p = []
    weighted_sign_test_p = []
    all_nsuccesses = []
    all_weighted_nsuccesses = []
    print 'RMS Error Ratios between ',fit_file[0],' and ',fit_file[1]
    for component in components:
        print component
        rms_geomean = []
        weighted_rms_geomean = []
        errors1 = []
        errors2 = []
        for imon1,mon1 in enumerate(molecules):
            for mon2 in molecules[imon1:]:
                [mona,monb] = sorted([mon1,mon2])
                dir_name = mona.lower() + '_' + monb.lower() + '/'

                rms_errors1 = subprocess.check_output('grep "' + component + ' RMS Error" ' + dir_name + fit_file[0] + " | awk '{print $4}'", shell=True)
                weighted_rms_errors1 = subprocess.check_output('grep "' + component + ' Weighted RMS Error" ' + dir_name + fit_file[0] + " | awk '{print $5}'", shell=True)
                rms_errors2 = subprocess.check_output('grep "' + component + ' RMS Error" ' + dir_name + fit_file[1] + " | awk '{print $4}'", shell=True)
                weighted_rms_errors2 = subprocess.check_output('grep "' + component + ' Weighted RMS Error" ' + dir_name + fit_file[1] + " | awk '{print $5}'", shell=True)

                rms_errors1 = [float(i) for i in rms_errors1.split()]
                weighted_rms_errors1 = [float(i) for i in weighted_rms_errors1.split()]
                rms_errors2 = [float(i) for i in rms_errors2.split()]
                weighted_rms_errors2 = [float(i) for i in weighted_rms_errors2.split()]

                errors1.append(rms_errors1[-1])
                errors2.append(rms_errors2[-1])
                rms_geomean.append(rms_errors1[-1]/rms_errors2[-1])
                weighted_rms_geomean.append(weighted_rms_errors1[-1]/weighted_rms_errors2[-1])

                ## if mon1 == mon2:
                ##     print mon1, rms_geomean[-1], weighted_rms_geomean[-1]


        ## print component
        ## print normaltest(np.array(errors1))
        ## print normaltest(np.array(errors2))
        rms_geomean = np.array(rms_geomean)
        weighted_rms_geomean = np.array(weighted_rms_geomean)
        nsuccesses = np.sum(rms_geomean < 1)
        nfailures = np.sum(rms_geomean > 1)
        weighted_nsuccesses = np.sum(weighted_rms_geomean < 1)
        weighted_nfailures = np.sum(weighted_rms_geomean > 1)
        try:
            all_nsuccesses.append(float(nsuccesses)/(nsuccesses+nfailures))
        except ZeroDivisionError:
            all_nsuccesses.append(np.nan)
        try:
            all_weighted_nsuccesses.append(float(weighted_nsuccesses)/(weighted_nfailures+weighted_nsuccesses))
        except ZeroDivisionError:
            all_weighted_nsuccesses.append(np.nan)
        ntrials = len(rms_geomean)
        sign_test_p.append( binom_test([nsuccesses, nfailures], p=0.5) )
        weighted_sign_test_p.append( binom_test([weighted_nsuccesses, weighted_nfailures], p=0.5))

        ## rms_geomeans.append(np.mean(rms_geomean))
        ## rms_geostds.append(np.std(rms_geomean))
        ## weighted_rms_geomeans.append(np.mean(weighted_rms_geomean))
        ## weighted_rms_geostds.append(np.std(weighted_rms_geomean))
        rms_geomeans.append(np.exp(np.mean(np.log(rms_geomean))))
        rms_geostds.append(np.exp(np.std(np.log(rms_geomean))))
        weighted_rms_geomeans.append(np.exp(np.mean(np.log(weighted_rms_geomean))))
        weighted_rms_geostds.append(np.exp(np.std(np.log(weighted_rms_geomean))))
        #weighted_rms_geomeans.append(gmean(weighted_rms_geomean))
    #template = '{:10s}\t{:16.6e}\t{:16.6e}\n'
    template = '{:15s}'+'\t{:^16s}'*7
    print template.format('Component','RMSE Ratio','','Attractive RMSE Ratio',
            'Sign Test Probability','Attractive Sign Test Probability',
            'Nsuccesses Ratio','Weighted_nsucccesses Ratio')
    template = '{:15s}'+ '\t{:16.3f} +/- {:<8.3f}'*2 + '\t{:16.3g}'*4 
    for line in zip(components,rms_geomeans,rms_geostds,
                    weighted_rms_geomeans,weighted_rms_geostds,
                    sign_test_p, weighted_sign_test_p,
                    all_nsuccesses, all_weighted_nsuccesses):
        print template.format(*line)
    print
    print 

###########################################################################
###########################################################################
