#!/usr/bin/env python
"""Given a set of parameters to fit and a list of molecules with associated
camCASP calculations, produces a set of converged dispersion parameters and
prints out the ratio of rms errors between the constrained and unconstrained
dispersion parameters.

Last Updated: October 3, 2014 by mvanvleet
"""

# Standard modules
import numpy as np
import sys
import os
import commands
import subprocess
from copy import copy

# mvanvleet specific modules
from chemistry import io
from force_fields.fit_ff_parameters import FitFFParameters

###########################################################################
####################### Global Variables ##################################

# List of molecules to fit
Molecule_List = ['acetone','ar','chloromethane','co2','dimethyl_ether','ethane',\
        'ethanol','ethene','h2o','methane','methanol','methyl_amine','nh3']
#Molecule_List = ['ar','chloromethane']

Templates_Dir = './input_templates/'

###########################################################################
###########################################################################


###########################################################################
########################## Main Code ######################################

###########################################################################
def main():
    ''' Runs the main dispersion parameter fitting procedure. For a
    description of the general algorithm employed here, refer to
    dx.doi.org/10.1021/jp3108182
    '''


    # Obtain initial parameters from the set of homo-atomic systems.
    slater_params = {}
    noslater_params = {}
    homedir = os.getcwd()

    print 'Finished all constrained Slater calculations'
    # Plot results for all systems.
    for imon1, mon1 in enumerate(Molecule_List):
        for mon2 in Molecule_List[imon1:]:
            dimer_dir = mon1 + '_' + mon2 + '/'
            print dimer_dir
            #for plot_file in ['plot_dispersion.plt','plot_exchange.plt','plot_all_sapt_components.plt']:
            for plot_file in ['plot_all_component_errors.plt','plot_all_comparisons.plt']:
                subprocess.call(['cp',Templates_Dir + plot_file, dimer_dir])
                subprocess.call(['sed','-i','s/mon1/'+mon1+'/',dimer_dir + plot_file])
                subprocess.call(['sed','-i','s/mon2/'+mon2+'/',dimer_dir + plot_file])

                os.chdir(dimer_dir)
                #subprocess.call('echo \'load "'+ plot_file + '"\' | gnuplot', shell=True)
                subprocess.call(['gnuplot',plot_file])
                os.chdir(homedir)

###########################################################################





###########################################################################
###########################################################################


###########################################################################
################### Run Code ##############################################
if __name__ == '__main__':
    main()
###########################################################################
###########################################################################
