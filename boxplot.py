# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 01:46:14 2025

@author: Lalie

Boxplot to show transient lengths for each violoncello bow

  - save your data by activating savefile = 'ON'

LOAD:
    filename:
        'your_csvfile_with_transients_detected_by_hand.csv'

    datatype:
        [('Transient number', int, 1),
        ('Bow part', np.unicode_, 512),
        ('Dynamics', np.unicode_, 512),
        ('Direction', np.unicode_, 512),
        ('Musician', np.unicode_, 512),
        ('Bow', np.unicode_, 512),
        ('Transient start', int, 1),
        ('Transient end', int, 1)]

OUTPUT: save your data by activating savefile = 'ON'
    filename:
        'your_boxplot_of_transient_lengths.svg'
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# activate latex
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "Times New Roman"
})

main_path = "C:/Users/Lalie/Documents/transitoires/attaquesAstring"

os.chdir(main_path)
string = 'A'

# bow_part = 'pointe'
bow_part = 'talon'
dynamics = 'piano_and_forte'
# dynamics = 'piano'
# dynamics = 'forte'

# Save file parameters
savefile = 'ON'
svgfilename = "boxplot_attack_transient_lengths_" + bow_part + '.pdf'

transients = pd.read_csv("Transient_durations_Astring_musicians1and2_EditForBoxplot.csv")

bows = ['BowA', 'BowB', 'Bowmusician']
sr = 51200

title_index = ["A", "B", "musician"]

musicians = ['musician1','musician2']

# for scatter with boxplot
transient_color_dynamics = {'forte': 'm' ,'piano': 'g'}
transient_marker_direction = {'pousse': 'o', 'tire': 'x'}


fig, axs = plt.subplots(1,3,figsize=(8,4), sharey=True)
fig.subplots_adjust(wspace=0, bottom=0.15, left=0.15)

for bow_index, bow in enumerate(transients['Bow'].unique()):
    # Init dictionaries for boxplotting
    transients_dict = {musicians[0]: [],
                       musicians[1]: []}

    transients_dict_stroketype = {musicians[0]: [], 
                                  musicians[1]: []}
    
    all_durations = np.array([])
    # assign transient durations to a bow for the boxplot
    for musician in musicians:
        transient_durations = np.array([])
        for i in range(len(transients)):
    
            # BOXPLOT SELECTED DATA ----------
            if transients['Bow_part'][i] != bow_part:
                continue
            if transients['Bow'][i] != bow:
                continue
            if dynamics == 'piano_and_forte':
                pass
            elif transients['Dynamics'][i] != dynamics:
                continue
            # BOXPLOT SELECTED DATA ----------
            if transients['Musician'][i] == musician:
                # print(transients.iloc[i])
                transient_duration = np.abs(transients['Transient_end'][i] - transients['Transient_start'][i])
                all_durations = np.append(all_durations, transient_duration)
                # print(str(transient_duration))
                transients_dict[musician].append(1000*transient_duration/sr)
                transients_dict_stroketype[musician].append([
                    1000*transient_duration/sr,
                    transient_color_dynamics[transients['Dynamics'][i]],
                    transient_marker_direction[transients['Direction'][i]]])
    
    # calculate median of all durations in order to plot it as a horizontal line
    median = 1000*np.median(all_durations)/sr
    
    # Boxplot
    axs[bow_index].boxplot(transients_dict.values(), showfliers=False,
                                widths=0.7)
    
    for i, musician in enumerate(musicians):
        y = np.array(transients_dict_stroketype[musician])[:, 0].astype(float)
        y_colors = np.array(transients_dict_stroketype[musician])[:, 1] #.astype(str)
        y_markers = np.array(transients_dict_stroketype[musician])[:, 2]
        x = np.random.normal(i+1, 0.1, size=len(y))  # Add random "jitter" to x-ax
        for j in range(len(y)):  # Didn't came up with a better solution...
            axs[bow_index].scatter(x[j], y[j], c=y_colors[j],
                       marker=y_markers.tolist()[j], alpha=0.4, edgecolors='none')
    n_musician1 = len(transients_dict_stroketype['musician1'])
    n_musician2 = len(transients_dict_stroketype['musician2'])
    axs[bow_index].set_xticklabels([r'Musician 1''\n''$N='+str(n_musician1)+'$',
                                         r'Musician 2''\n''$N='+str(n_musician2)+'$'], fontsize=12)
    axs[bow_index].tick_params(axis='y', which='major', labelsize=12)
    axs[bow_index].hlines(median, 0, 3, color='blue', linestyle='--',
              alpha=0.5, label='Median = ' + str(round(median, 1)) + ' ms')
    axs[bow_index].set_xlim([0.5, 2.5])
    axs[bow_index].grid(axis='y')
    axs[bow_index].set_ylim([0, 200])
    axs[bow_index].set_title('Bow ' + title_index[bow_index], fontsize=12)
    if bow_index == 0:
        axs[bow_index].set_ylabel('Transient duration (ms)', fontsize=12)
    else:
        axs[bow_index].tick_params(axis='y', which='both', length=0)
    if bow_part == 'talon':
        if bow_index == 0:
            axs[bow_index].legend(loc='upper right',frameon=False, fontsize=12)
        else:
            axs[bow_index].legend(frameon=False, fontsize=12)
    else:
        axs[bow_index].legend(frameon=False, fontsize=12)

if savefile == 'ON':
    plt.savefig(main_path + '//' + svgfilename)
