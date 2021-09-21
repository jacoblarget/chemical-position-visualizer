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
## import matplotlib.patches as patches
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
    ifile = 'rmse_ratios.dat'

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
       'stds' : [], 
       'attractive_stds' : [] } #blank lines separate datasets
blank_tmp = copy.deepcopy(tmp)
names = []
for line in data:
    if not line:
        if tmp != blank_tmp:
            datasets.append(tmp)
        tmp = copy.deepcopy(blank_tmp)
    elif line[0] == 'RMS':
        #tmp.append(line[-1]) # header row
        names.append(line[-3]+ ' vs. ' + line[-1]) # header row
    elif line[0] == 'Component':
        continue
    else:
        tmp['rmse'].append(float(line[1]))
        tmp['stds'].append(float(line[3]))
        tmp['attractive_rmse'].append(float(line[4]))
        tmp['attractive_stds'].append(float(line[6]))
        ## tmp.append({ name : float(i) 
        ##     for name, i in zip(['rmse','attractive_rmse'],line[1:]})

dfs = []
for i,dset in enumerate(datasets):
    dfs.append( pd.DataFrame(dset,
            index=['Exchange','Electrostatics','Induction','DHF','Dispersion','Total_Energy'])
            )
    df = dfs[i]
    df['rms_pyerr'] = (df['rmse']*df['stds'] - df['rmse'])
    df['rms_nyerr'] = (- df['rmse']/df['stds'] + df['rmse'])
    df['attractive_rms_pyerr'] = (df['attractive_rmse']*df['attractive_stds']
            - df['attractive_rmse'])
    df['attractive_rms_nyerr'] = ( -
            df['attractive_rmse']/df['attractive_stds'] + df['attractive_rmse'])

    ## df['rms_nyerr'] = df.map(df['rmse']/df['stds'])
    ## df['attractive_rms_pyerr'] = df.map(df['attractive_rmse']*df['attractive_stds'])
    ## df['attractive_rms_nyerr'] = df.map(df['attractive_rmse']/df['attractive_stds'])
    #print df[i]

# Set some global color preferences for how the graph's colors should look
sns.set_context('paper')
sns.set_style("darkgrid")
sns.set_color_codes()

#fig = df[0].plot(kind='bar',figsize=(20,10))
#fig = df[1].plot(kind='bar',))
fig = plt.figure(figsize=(20,10))
ax = fig.add_subplot(111)

N = len(dfs)
width=0.85/N
shift_all = (1.0 - width*N)/2
offset = 0.03
rmse_colors = itertools.cycle(sns.color_palette(desat=0.75))
#attractive_rmse_colors = itertools.cycle(sns.hls_palette(l=.3, s=.8))
attractive_rmse_colors = itertools.cycle(sns.color_palette())
names = itertools.cycle(names)
front_scale = 0.4
back_scale = 0.8
for i,dset in enumerate(dfs):
    ind = np.arange(len(dset))
    shift = ind +i*width + shift_all + width*(1-back_scale)/2 - offset
    #shift = ind +i*width + width*(back_scale/2)
    #ax.bar(shift,dset['rmse'],width*back_scale,color=rmse_colors.next(),alpha=0.6,yerr=dset['stds'])
    ax.bar(shift,dset['rmse'],width*back_scale,
            color=rmse_colors.next(),
            alpha=0.6,
            yerr=[dset['rms_nyerr'],dset['rms_pyerr']],
            error_kw=dict(ecolor='gray', lw=1, capsize=3, capthick=1))
    shift = ind +i*width + shift_all + width*(1-front_scale)/2 + offset
    ax.bar(shift,dset['attractive_rmse'],width*front_scale,
            color=attractive_rmse_colors.next(),
            label=names.next(),
            yerr=[dset['attractive_rms_nyerr'],dset['attractive_rms_pyerr']],
            error_kw=dict(ecolor='gray', lw=1, capsize=3, capthick=1))
handles, label = ax.get_legend_handles_labels()
ax.legend(handles, label)
#ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

ax.set_xticklabels( dset.index )
ax.set_ylabel('RMS Error Ratios')
ax.set_xticks(ind+N/2*width+shift_all+width*back_scale/2)
ax.axhline(1, color='k',linestyle='--',alpha=0.75)

## g = sns.factorplot(x="rmse", data=df[0], kind='count',
##                            palette="BuPu", size=6, aspect=1.5)

## # Overal graph layout and title
## ncols=4
## nrows=2
## #fig, axes = plt.subplots(nrows=nrows, ncols=ncols,figsize=(20,10))
## gs = gridspec.GridSpec(nrows, ncols, width_ratios=[1,1,0.5,2]) 
## fig.suptitle('FF Fitting Quality Benchmarks',y=0.95,fontweight='bold', fontsize=14)
## fig.text(0.30,0.075, 'Absolute Error in the Total Energy (mH, FF - SAPT)',ha='center', va='center')
## fig.text(0.095,0.5, 'Absolute Error (FF - SAPT) in Component Energy (mH)',ha='center', va='center',rotation='vertical')
## 
## # Scale error plot axes
## xy_max = 0
## for component in electrostatics,exchange,dispersion,induction,dhf,total_energy:
##     y_qm = component['qm'][order]
##     y_ff = component['ff'][order]
##     y = y_qm - y_ff
##     xy_max = max(np.amax(np.abs(y)),xy_max)
##     xy_min = -xy_max
## 
## # Plot each energy component
## count=0
## titles=['Electrostatics','Exchange','','Induction + $\delta$HF','Dispersion',
##         'Total Energy','Total Energy (attractive configurations)']
## for component in electrostatics,exchange,None,(induction+dhf),dispersion,None:
##     count += 1
##     if count > 3:
##         # Ignore last column for now
##         #ax = plt.subplot(nrows*100 + ncols*10 + count + 1)
##         ax = plt.subplot(gs[count])
##         #ax = plt.subplot(gs[count],sharey=ax,sharex=ax)
##     ## elif count > 1:
##     ##     #ax = plt.subplot(nrows*100 + ncols*10 + count)
##     ##     ax = plt.subplot(gs[count-1],sharey=ax,sharex=ax)
##     else:
##         ax = plt.subplot(gs[count-1])
##     if component is None:
##         # Plot colorbar instead of energy component
##         ax.axis('off')
##         continue
## 
##     x_qm = total_energy['qm'][order]
##     x_ff = total_energy['ff'][order]
##     y_qm = component['qm'][order]
##     y_ff = component['ff'][order]
## 
##     x = - x_qm + x_ff
##     y = - y_qm + y_ff
## 
##     # Scatterplot settings
##     sc = plt.scatter(x,y,
##             c=colors, vmin=vmin, vmax=vmax, cmap=cmap, s=25, lw =.75)
## 
##     # Axes scaling and title settings
##     scale = 0.02
##     ## xy_max = max(np.amax(np.abs(x)),np.amax(np.abs(y)))
##     ## xy_min = -xy_max
##     lims = [ xy_min - scale*abs(xy_max - xy_min), 
##              xy_max + scale*abs(xy_max - xy_min) ]
##     if titles[count-1] == titles[-1]:
##         # Only plot attractive energies in this last plot
##         lims[1] = 0
##     ax.set_aspect('equal')
##     ax.set_xlim(lims)
##     ax.set_ylim(lims)
##     ax.set_title(titles[count-1])
## 
##     # Plot y=x line
##     plt.plot(lims, lims, 'k-', alpha=0.75)
## 
##     # Plot grid lines
##     plt.axhline(0, color='k',linestyle='--',alpha=0.75)
##     plt.axvline(0, color='k',linestyle='--',alpha=0.75)
## 
## cbaxes = fig.add_axes([0.48, 0.34, 0.01, 0.35]) 
## cb = plt.colorbar(sc, cax = cbaxes, extend='max') 
## cb.set_label('SAPT Total Energy (mH)')
## 
## # Finally, plot graph summarizing all errors contributing to errors in the
## # total energy
## ax = plt.subplot(gs[ncols-1])
## x_qm = total_energy['qm'][order]
## x_ff = total_energy['ff'][order]
## count = 0
## (xmin, xmax) = [np.amin(x_qm),0]
## (ymin, ymax) = [0,0]
## marker = itertools.cycle(('v', '8', 'd', 'p', 's','o','+')) 
## labels=itertools.cycle(
##         ('Electrostatics','Exchange','Induction','$\delta$HF','Dispersion','Total Energy'))
## for component in electrostatics,exchange,induction,dhf,dispersion,total_energy:
##     y_qm = component['qm'][order]
##     y_ff = component['ff'][order]
##     x = x_qm
##     y = - y_qm + y_ff
##     ymin_i = np.amin(np.where(x < 0, y, 0))
##     ymax_i = np.amax(np.where(x < 0, y, 0))
##     (ymin,ymax) = (min(ymin,ymin_i),max(ymax,ymax_i))
##     label=labels.next()
##     if label == 'Total Energy':
##         sc = plt.scatter(x,y,
##                 facecolors='none', edgecolors='k', s=25, lw = 0.75,
##                 #c=colors, vmin=vmin, vmax=vmax, cmap=cmap, s=25, lw =.75,
##                 label=label,zorder=10)
##     else:
##         plt.plot(x,y,marker = marker.next(), markersize=5, linestyle='', label=label)
## ax.set_xlabel('SAPT Energy (mH)')
## ax.set_ylabel('Absolute Error (FF Energy - QM energy) (mH)')
## ax.set_title('Absolute Error in FF Fitting')
## plt.axhline(0, color='k',linestyle='--',alpha=0.75,zorder=20)
## handles, label = ax.get_legend_handles_labels()
## ax.legend(handles, label)
## plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
## 
## xlims = [ xmin - scale*abs(xmax - xmin), 
##          xmax ]
## ylims = [ ymin - scale*abs(ymax - ymin), 
##          ymax + scale*abs(ymax - ymin) ]
## ax.set_xlim(xlims)
## ax.set_ylim(ylims)
## 
## # Total Attractive energies (for reference)
## #ax = plt.subplot(nrows*100 + ncols*10 + ncols*nrows)
## ax = plt.subplot(gs[ncols*nrows -1])
## x = total_energy['qm'][order]
## y = total_energy['ff'][order]
## sc = plt.scatter(x,y,
##         c=colors, vmin=vmin, vmax=vmax, cmap=cmap, s=25, lw =.75)
## xy_min = min(np.amin(y),np.amin(x))
## xy_max = max(np.amax(y),np.amax(x))
## lims = [ xy_min - scale*abs(xy_max - xy_min), 
##          0 + scale*abs(xy_max - xy_min) ]
## ax.set_aspect('equal')
## ax.set_xlim(lims)
## ax.set_ylim(lims)
## ax.set_title('Overall Fit Quality')
## ax.set_xlabel('SAPT Total Energy (mH)')
## ax.set_ylabel('FF Total Energy (mH)')
## # Plot y=x line
## plt.plot(lims, lims, 'k-', alpha=0.75)
## # Shade in region to indicate +/- 10% error in ff
## rel = 0.1
## x1 = np.arange(lims[0],lims[1],0.01)
## plt.fill_between(x1,x1-x1*rel,x1+x1*rel,zorder=0,alpha=0.25)


#plt.show()
fig.savefig('rmse_ratios.png',bbox_inches='tight')

###########################################################################
###########################################################################
