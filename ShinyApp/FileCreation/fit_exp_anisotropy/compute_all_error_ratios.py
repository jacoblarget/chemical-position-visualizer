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
    ['scaledispanisotropic_fit_exp_total_energy_unconstrained.dat','scaledispfullisotropic_fit_exp_total_energy_unconstrained.dat'],
    ## ['anisotropic_fit_exp_total_energy_unconstrained.dat','isotropic_fit_exp_total_energy_unconstrained.dat'],
    ## ['scaledispanisotropic_fit_exp_total_energy_unconstrained.dat','anisotropic_fit_exp_total_energy_unconstrained.dat'],
    ['anisotropic_fit_exp_total_energy_unconstrained.dat','fullisotropic_fit_exp_total_energy_unconstrained.dat'],
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

#components = ['Exchange','Electrostatics','Induction','Dhf','Dispersion','Total_Energy']
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
    rms_geomeans = []
    rms_geostds = []
    weighted_rms_geomeans = []
    weighted_rms_geostds = []
    sign_test_p = []
    weighted_sign_test_p = []
    all_nsuccesses = []
    all_weighted_nsuccesses = []
    print 'RMS Error Ratios between ',fit_file[0],' and ',fit_file[1]
    print '-'*155
    template = '{:15s}' + '{:10s}\t|\t'*6
    print template.format('',*components)
    print '-'*155
    for imon1,mon1 in enumerate(molecules):
        #for mon2 in molecules[imon1:]:
        mon2 = mon1
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
            rms_ratios.append(weighted_rmse_error_ratio)
            #weighted_rms_ratios.append(weighted_rmse_error_ratio)

                ## rmse_error *= 2625.5
                ## weighted_rmse_error *= 2625.5

                ## rms_errors1 = subprocess.check_output('grep "' + component + ' RMS Error" ' + dir_name + fit_file[0] + " | awk '{print $4}'", shell=True)
                ## weighted_rms_errors1 = subprocess.check_output('grep "' + component + ' Weighted RMS Error" ' + dir_name + fit_file[0] + " | awk '{print $5}'", shell=True)
                ## rms_errors2 = subprocess.check_output('grep "' + component + ' RMS Error" ' + dir_name + fit_file[1] + " | awk '{print $4}'", shell=True)
                ## weighted_rms_errors2 = subprocess.check_output('grep "' + component + ' Weighted RMS Error" ' + dir_name + fit_file[1] + " | awk '{print $5}'", shell=True)

                ## rms_errors1 = [float(i) for i in rms_errors1.split()]
                ## weighted_rms_errors1 = [float(i) for i in weighted_rms_errors1.split()]
                ## rms_errors2 = [float(i) for i in rms_errors2.split()]
                ## weighted_rms_errors2 = [float(i) for i in weighted_rms_errors2.split()]

                ## errors1.append(rms_errors1[-1])
                ## errors2.append(rms_errors2[-1])
                ## rms_geomean.append(rms_errors1[-1]/rms_errors2[-1])
                ## weighted_rms_geomean.append(weighted_rms_errors1[-1]/weighted_rms_errors2[-1])

                ## template = '{:15s}' + '{:8.3f}'*2
                ## ## if mon1 == mon2:
                ## ##     print template.format(mon1, rmse_error_ratio, weighted_rmse_error_ratio)

                ## rms_geomean.append(rmse_error_ratio)
                ## weighted_rms_geomean.append(weighted_rmse_error_ratio)

        template = '{:15s}' + '{:4.3f} ({:4.3f})\t|\t'*6
        print template.format(mon1, *rms_ratios)


    print
    print

exit()



for i in foo:
    for j in foo:
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
    ## for line in zip(components,rms_geomeans,rms_geostds,
    ##                 weighted_rms_geomeans,weighted_rms_geostds,
    ##                 sign_test_p, weighted_sign_test_p,
    ##                 all_nsuccesses, all_weighted_nsuccesses):
    ##     print template.format(*line)
    template = '{:15s}'+ '\t{:16.3f}'*2 
    for line in zip(components,rms_geomeans,
                    weighted_rms_geomeans,
                    ):
        print template.format(*line)
    print
    print 
    exit()

###########################################################################
###########################################################################
