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
    all_rms_ratios = []
    all_weighted_rms_ratios = []

    print 'RMS Error Ratios between ',fit_file[0],' and ',fit_file[1]
    print '-'*155
    template = '{:15s}' + '{:10s}\t|\t'*6
    print template.format('',*components)
    print '-'*155
    for imon1,mon1 in enumerate(molecules):
        for mon2 in molecules[imon1:]:
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


    print
    print


    ratios = np.array(all_weighted_rms_ratios)
    print ratios.shape
    all_names = [ '{:20s}  {:20s}'.format(atom1,atom2) for i,atom1 in enumerate(names) for atom2 in names[i:] ]
    df = pd.DataFrame(ratios,
                index=all_names,
                columns=['Exchange','Electrostatics','Induction','$\delta$HF','Dispersion','Total Energy'],
                )

    print df
    #df = df.sort(['Total Energy'])
    vals = df.values
    normal = mpl.colors.Normalize(vals.min(), 1.0)
    # print normal


    hcell=0.4
    wcell=0.7
    nrows = len(df.index) + 1
    ncols = len(df.columns) + 1
    print nrows
    print ncols
    wpad = 0
    hpad = 0
    fig = plt.figure(figsize=(ncols*wcell+wpad, nrows*hcell+hpad))
    #fig = plt.figure(figsize=(nrows*hcell+hpad,ncols*wcell+wpad,))
    ax = fig.add_subplot(111, frameon=True, xticks=[], yticks=[])
    cmap = sns.cubehelix_palette(8, start=.5, rot=-.75,as_cmap=True, reverse=True)
    ## pcm = fig.pcolormesh(X, Y, Z1,
    ##             norm=colors.LogNorm(linthresh=0.03,
    ##             linscale=0.03,
    ##             vmin=0.0,
    ##             vmax=1.0),
    ##             cmap=cmap)

    rounded_vals = [['%.2f' % j for j in i] for i in vals]
    table=plt.table(cellText=rounded_vals, rowLabels=df.index,
            colLabels=df.columns, 
            cellLoc='center',
            #colWidths = [wcell]*vals.shape[1],
            #colWidths = [wcell/5]*vals.shape[1],
            loc='center', 
            fontsize=20,
            bbox=[0.1, 0.0, wcell, hcell],
            #cellColours=plt.cm.viridis(normal(vals)))
            cellColours=cmap(normal(vals)))

    table_props = table.properties()
    table_cells = table_props['child_artists']
    for cell in table_cells: 
        #print cell
        cell._text.set_fontsize(20)
        #cell._text.set_color('white')

    print cmap(0)

    for i in range(1,nrows):
        for j in range(0,ncols-1):
            table._cells[(i, j)]._text.set_fontsize(20)
            table._cells[(i, j)]._text.set_fontweight('bold')
            table._cells[(i, j)]._text.set_color('white')
            ## table._cells[(i, j)]._text.set_path_effects([PathEffects.withStroke(linewidth=1,
            ##     foreground=cmap(0))])
            # plt.draw()

    plt.axis('off')
    fig.savefig('all_error_ratios.pdf',bbox_inches='tight',dpi=100)
    plt.show()


    exit()




###########################################################################
###########################################################################
