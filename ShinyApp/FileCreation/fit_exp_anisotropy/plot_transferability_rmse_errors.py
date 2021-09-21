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
from matplotlib.patches import Rectangle
import matplotlib.markers as mks
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
try:
    ifile = sys.argv[1]
except IndexError:
    ifile = 'transferability_rmse_averages.dat'
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
        tmp['attractive_rmse'].append(float(line[2]))

dfs = []
for i,dset in enumerate(datasets):
    dfs.append( pd.DataFrame(dset,
            index=['Exchange','Electrostatics','Induction','$\delta$HF','Dispersion','Total Energy'])
            )
    df = dfs[i]

# Set some global color preferences for how the graph's colors should look
sns.set_context('talk',rc={'grid.linewidth':0.15})
sns.set_context('talk',font_scale=1.5,rc={'grid.linewidth':0.15})
sns.set_color_codes()
palette = itertools.cycle(sns.color_palette())
sns.set_style("ticks", 
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
fig = plt.figure(figsize=(20,10))
ax = fig.add_subplot(111)

# Parameters determinging shapes of bars in the graph
N = len(dfs)
width=0.85/N
shift_all = (1.0 - width*N)/2
offset = 0.00
front_scale = 0.8
back_scale = 0.9

label_names = itertools.cycle(["Slater-ISA FF","MASTIFF"])
label_colors = [1,0]

rmse_colors = sns.color_palette('Set2',desat=0.75)
attractive_rmse_colors = sns.color_palette('Set2')
constrained_rmse_colors = sns.color_palette('Set2',desat=0.75)
constrained_attractive_rmse_colors = sns.color_palette('Set2',desat=1.00)
hatch_colors = sns.color_palette('Set2',desat=0.75)
attractive_hatch_colors = sns.color_palette('Set2',desat=1.00)
line_colors = sns.color_palette('Set2',desat=0.15)

## rmse_colors = sns.color_palette('Paired',desat=0.75)
## attractive_rmse_colors = sns.color_palette('Paired')
icolor=0
for i,dset in enumerate(dfs):
    # Determine if fit is constrained or unconstrained
    print names[i]
    if '_constrained.dat' in names[i]:
        constrained_fit = True
        print 'CONSTRAINED!'
    else:
        constrained_fit = False

    # Get colors for the different fit types
    # line_color = line_colors[label_colors[icolor]]
    line_color = '0.1'
    if constrained_fit:
    # Assumption here is that we just plotted an unconstrained fit, and so
    # don't have to update the color
        #hatch=''
        # ecolor=hatch_colors[label_colors[icolor]]
        # attractive_ecolor=hatch_colors[label_colors[icolor]]
        color=constrained_rmse_colors[label_colors[icolor]]
        attractive_color=constrained_attractive_rmse_colors[label_colors[icolor]]
        ecolor=hatch_colors[2]
        attractive_ecolor=attractive_hatch_colors[2]
        hatch=3*'x'
        #attractive_ecolor='grey'
        icolor +=1
    else:
        color=rmse_colors[label_colors[icolor]]
        attractive_color=attractive_rmse_colors[label_colors[icolor]]
        ecolor=color
        attractive_ecolor=attractive_color
        hatch=''

    # Determine colors and labels for fit
    ind = np.arange(len(dset))
    shift = ind +i*width + shift_all + width*(1-back_scale)/2
    ax.bar(shift,dset['rmse'],width*back_scale,
            color=color,
            edgecolor=ecolor,
            alpha=0.6,
            hatch=hatch,
            error_kw=dict(ecolor='gray', lw=1, capsize=3, capthick=1))
    shift = ind +i*width + shift_all + width*(1-front_scale)/2 + offset
    ax.bar(shift,dset['attractive_rmse'],width*front_scale,
            color=attractive_color,
            edgecolor=attractive_ecolor,
            label=label_names.next(),
            hatch=hatch,
            error_kw=dict(ecolor='gray', lw=1, capsize=3, capthick=1))
    print attractive_color
    # Last bar graphs just sets border color for attractive bars
    ## shift = ind +i*width + shift_all + width*(1-back_scale)/2
    ## ax.bar(shift,dset['rmse'],width*back_scale,
    ##         color='none',
    ##         lw=1.8,
    ##         edgecolor='grey',
    ##         error_kw=dict(ecolor='gray', lw=1, capsize=3, capthick=1))
    shift = ind +i*width + shift_all + width*(1-front_scale)/2 + offset
    ax.bar(shift,dset['attractive_rmse'],width*front_scale,
            color='none',
            # edgecolor=attractive_color,
            # edgecolor='black',
            edgecolor=line_color,
            label=label_names.next(),
            lw=2,
            zorder=10,
            # alpha=0.9,
            )

# Plot Legends
handles, label = ax.get_legend_handles_labels()
m1, = ax.plot([], [], c=attractive_rmse_colors[1] , marker='s', markersize=24,
                      fillstyle='left', linestyle='none',lw=2)
## h=24
## m1 = Rectangle((0.5,0.5), color='black', width=h, height=h)
## m3 = Rectangle((0.25,0.5), color='green', width=h, height=h)
# lc=attractive_rmse_colors[1],
m2, = ax.plot([], [], c=attractive_rmse_colors[0] , marker='s', markersize=24,
                      fillstyle='left', linestyle='none',lw=2)
mymkstyle = mks.MarkerStyle(marker=u's', fillstyle=u'right')
mymkstyle = 's'
m3 = ax.scatter([],[], s=500, marker=mymkstyle, c=attractive_rmse_colors[1],
        edgecolors=attractive_rmse_colors[2],hatch=3*'x',lw=2)
## m4, = ax.plot([], [], c=attractive_rmse_colors[2] , marker='s', markersize=24,
##                       linestyle='none',lw=2)
m4 = ax.scatter([],[], s=500, marker=mymkstyle, c=attractive_rmse_colors[0],
        edgecolors=attractive_rmse_colors[2],hatch=3*'x',lw=2)
m5 = ax.scatter([],[], s=500, marker=mymkstyle, c='none',
        edgecolors=attractive_rmse_colors[1],lw=4)
m6 = ax.scatter([],[], s=500, marker=mymkstyle, c='none',
        edgecolors=attractive_rmse_colors[0],lw=4)
m8 = ax.scatter([],[], s=650, marker=mymkstyle, c='none',
        edgecolors='0.1',lw=2)
m7 = ax.scatter([],[], s=650, marker=mymkstyle, c='none',
        edgecolors='0.1',lw=2)

## patterns = ('-','+')
## for pattern in patterns:
##     ax.scatter([],[], s=1000, marker='s', facecolor='white', hatch=3*pattern, label=pattern)

# plt.legend(scatterpoints=1, loc='best')

l1 = ax.legend([(m3,m1,m5,m7),(m4,m2,m6,m8)], label, 
# l1 = ax.legend([m1,m2,m3,m4,m5,m6], label, 
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

## with sns.axes_style('dark'):
##     #leg = fig.add_axes()
##     leg = fig.add_axes([0.5, 0.50, 0.05, 0.05])
##     #leg.axis([0, 1, 0, 1])
##     leg.axis('off')
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
ax.set_ylabel(r'Characteristic RMS Errors (kJ mol$^{\mathbf{-1}}$)',fontsize=30,fontweight='bold')
ax.set_xlabel('Energy Component',fontsize=30,fontweight='bold')
ax.set_xticks(ind+shift_all+N/2*width)

sns.despine()


fig.savefig('transferability_rmse_errors.pdf',bbox_inches='tight',dpi=200)
plt.show()

###########################################################################
###########################################################################
