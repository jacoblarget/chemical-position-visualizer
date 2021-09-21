#!/usr/bin/env python
"""

Last Updated:
"""

# Standard modules
import numpy as np
import sys
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import copy
import matplotlib.patches as patches
import itertools
## from matplotlib import gridspec
# mvanvleet specific modules
from chemistry import io

###########################################################################
####################### Global Variables ##################################
error_message='''
---------------------------------------------------------------------------
Improperly formatted arguments. Proper usage is as follows:

$ 

(<...> indicates required argument, [...] indicates optional argument)
---------------------------------------------------------------------------
    '''



###########################################################################
###########################################################################


###########################################################################
######################## Command Line Arguments ###########################
## try:
##     component_prefix = sys.argv[1]
##     component_suffix = sys.argv[2]
## except IndexError:
##     component_prefix = 'slater_'
##     component_suffix = '_unconstrained.dat'
try:
    ifile = sys.argv[1]
except IndexError:
    ifile = 'rmse_averages.dat'

## # Filenames to read in 
## exchange_file = component_prefix +  'exchange' + component_suffix
## electrostatics_file = component_prefix +  'electrostatics' + component_suffix
## induction_file = component_prefix +  'induction' + component_suffix
## dhf_file = component_prefix +  'dhf' + component_suffix
## dispersion_file = component_prefix +  'dispersion' + component_suffix
## total_energy_file = component_prefix +  'total_energy' + component_suffix
## 
## exchange_file = 'slater_exchange_unconstrained.dat'
## electrostatics_file = 'slater_electrostatics_unconstrained.dat'
## induction_file = 'slater_induction_unconstrained.dat'
## dhf_file = 'slater_dhf_unconstrained.dat'
## dispersion_file = 'slater_dispersion_unconstrained.dat'
## total_energy_file = 'slater_total_energy_unconstrained.dat'

###########################################################################
###########################################################################


###########################################################################
########################## Main Code ######################################

# Read data from each dataset
with open(ifile,'r') as f:
    data = [line.split() for line in f.readlines()]

datasets = []
tmp = {'rmse' : [], 
       'attractive_rmse' : [],
       #'stds' : [], 
       #'attractive_stds' : [] 
       } #blank lines separate datasets
blank_tmp = copy.deepcopy(tmp)
names = []
for line in data:
    if not line:
        if tmp != blank_tmp:
            datasets.append(tmp)
        tmp = copy.deepcopy(blank_tmp)
    elif line[0] == 'RMS':
        #tmp.append(line[-1]) # header row
        names.append(line[-1]) # header row
    elif line[0] == 'Component':
        continue
    else:
        tmp['rmse'].append(float(line[1]))
        #tmp['stds'].append(float(line[3]))
        tmp['attractive_rmse'].append(float(line[2]))
        #tmp['attractive_stds'].append(float(line[6]))
        ## tmp.append({ name : float(i) 
        ##     for name, i in zip(['rmse','attractive_rmse'],line[1:]})

dfs = []
for i,dset in enumerate(datasets):
    dfs.append( pd.DataFrame(dset,
            index=['Exchange','Electrostatics','Induction','$\delta$HF','Dispersion','Total Energy'])
            )
    df = dfs[i]
    ## df['rms_pyerr'] = (df['rmse']*df['stds'] - df['rmse'])
    ## df['rms_nyerr'] = ( - df['rmse']/df['stds'] + df['rmse'])
    ## df['attractive_rms_pyerr'] = (df['attractive_rmse']*df['attractive_stds']
    ##                                 - df['attractive_rmse'])
    ## df['attractive_rms_nyerr'] = ( - df['attractive_rmse']/df['attractive_stds']
    ##                                 + df['attractive_rmse'])
    ## df['rms_pyerr'] = df.map(df['rmse']*df['stds'])
    ## df['rms_nyerr'] = df.map(df['rmse']/df['stds'])
    ## df['attractive_rms_pyerr'] = df.map(df['attractive_rmse']*df['attractive_stds'])
    ## df['attractive_rms_nyerr'] = df.map(df['attractive_rmse']/df['attractive_stds'])
    #print df[i]

# Set some global color preferences for how the graph's colors should look
sns.set_context('talk',rc={'grid.linewidth':0.15})
#sns.set_context('talk')
#print sns.context()
sns.set_color_codes()
palette = itertools.cycle(sns.color_palette())
sns.set_style("ticks", 
#sns.set_style("ticks", 
                  {
                  'ytick.direction': 'in', 'xtick.direction': 'in',
                  #'ytick.major.size':0.1,
                  'font.sans-serif': ['CMU Sans Serif','Helectiva','Arial', 'Liberation Sans', 'Bitstream Vera Sans', 'sans-serif'],
                  'grid.color':'white',
                  'axes.grid':True,
                  'axes.axisbelow':False,
                  'grid.linestyle':':'
                  }
                    )
print sns.axes_style()

#fig = df[0].plot(kind='bar',figsize=(20,10))
#fig = df[1].plot(kind='bar',))
fig = plt.figure(figsize=(20,10))
ax = fig.add_subplot(111)

N = len(dfs)
width=0.85/N
shift_all = (1.0 - width*N)/2
offset = 0.00
#rmse_colors = itertools.cycle(sns.color_palette('Paired',desat=0.75))
## rmse_colors = itertools.cycle(sns.color_palette('Set2',desat=0.75))
## #attractive_rmse_colors = itertools.cycle(sns.hls_palette(l=.3, s=.8))
## #attractive_rmse_colors = itertools.cycle(sns.color_palette('Paired'))
## attractive_rmse_colors = itertools.cycle(sns.color_palette('Set2'))
#names = itertools.cycle(names)
names = itertools.cycle(["Isotropic","Anisotropic ON Atoms","Anisotropic ONH Atoms (select H)","Full Anisotropy"])
front_scale = 0.8
back_scale = 0.9
rmse_colors = sns.color_palette('Set2',desat=0.75)
attractive_rmse_colors = sns.color_palette('Set2')
for i,dset in enumerate(dfs):
    ind = np.arange(len(dset))
    shift = ind +i*width + shift_all + width*(1-back_scale)/2
    #shift = ind +i*width + width*(back_scale/2)
    #ax.bar(shift,dset['rmse'],width*back_scale,color=rmse_colors.next(),alpha=0.6,yerr=dset['stds'])
    ax.bar(shift,dset['rmse'],width*back_scale,
            color=rmse_colors[1-i],
            edgecolor=rmse_colors[1-i],
            #color=rmse_colors.next(),
            alpha=0.6,
            #yerr=[dset['rms_nyerr'],dset['rms_pyerr']],
            error_kw=dict(ecolor='gray', lw=1, capsize=3, capthick=1))
    shift = ind +i*width + shift_all + width*(1-front_scale)/2 + offset
    ax.bar(shift,dset['attractive_rmse'],width*front_scale,
            color=attractive_rmse_colors[1-i],
            edgecolor=attractive_rmse_colors[1-i],
            label=names.next(),
            #yerr=[dset['attractive_rms_nyerr'],dset['attractive_rms_pyerr']],
            error_kw=dict(ecolor='gray', lw=1, capsize=3, capthick=1))

# Plot Legends
handles, label = ax.get_legend_handles_labels()
m1, = ax.plot([], [], c=attractive_rmse_colors[1] , marker='s', markersize=24,
                      fillstyle='full', linestyle='none')
m2, = ax.plot([], [], c=attractive_rmse_colors[0] , marker='s', markersize=24,
                      fillstyle='full', linestyle='none')
m3, = ax.plot([], [], c=attractive_rmse_colors[-1] , marker='s', markersize=24,
                      fillstyle='full', linestyle='none')
m4, = ax.plot([], [], c=attractive_rmse_colors[-2] , marker='s', markersize=24,
                      fillstyle='full', linestyle='none')
l1 = ax.legend([m1,m2,m3,m4], label, 
        fontsize=22,
        labelspacing=1.2,
        loc='center',
        fancybox=True,
        bbox_to_anchor=(0.50,0.70),
        bbox_transform=ax.figure.transFigure,
        )
ax.get_legend().get_title().set_fontsize('16')
ax.get_legend().get_title().set_fontweight('bold')
plt.gca().add_artist(l1)

with sns.axes_style('dark'):
    #leg = fig.add_axes()
    leg = fig.add_axes([0.5, 0.50, 0.05, 0.05])
    #leg.axis([0, 1, 0, 1])
    leg.axis('off')
## m1, = leg.plot([], [], c=rmse_colors[0] , marker='s', markersize=15,
##                       fillstyle='left', linestyle='none',alpha=0.6)
## m2, = leg.plot([], [], c=rmse_colors[1] , marker='s', markersize=15,
##                       fillstyle='right', linestyle='none',alpha=0.6)
## m3, = leg.plot([], [], c=attractive_rmse_colors[0] , marker='s', markersize=15,
##                       fillstyle='left', linestyle='none')
## m4, = leg.plot([], [], c=attractive_rmse_colors[1] , marker='s', markersize=15,
##                       fillstyle='right', linestyle='none')
## leg.legend([(m2,m1),(m3,m4)],
##         ['All Points','Attractive (E$_{tot} < 0$)\npoints only'],
##         numpoints=1,
##         #labelspacing=0.81,
##         #loc='center',
##         fontsize=13,
##         title='RMS Errors',
##         ##frameon=True,
##         ##fancybox=True,
##         bbox_to_anchor=(0.87,0.87),
##         bbox_transform=ax.figure.transFigure)
## leg.get_legend().get_title().set_fontsize('11')
## leg.get_legend().get_title().set_fontweight('bold')
#leg.get_legend().get_frame().set_facecolor('white')
#ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

ax.set_xticklabels( dset.index, ha='center', fontsize=20 )
ax.set_ylabel('Average RMS Errors (kJ/mol)',fontsize=24,fontweight='bold')
ax.set_xlabel('Energy Component',fontsize=24,fontweight='bold')
ax.set_xticks(ind+shift_all+N/2*width)

sns.despine()


fig.savefig('rmse_errors.pdf',bbox_inches='tight',dpi=1200)
plt.show()

###########################################################################
###########################################################################
