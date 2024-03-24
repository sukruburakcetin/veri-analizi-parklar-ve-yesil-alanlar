# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 17:02:28 2020

------ What's this file? ------

This script is responsible for the analysis and visualization of different
types of parks and green areas that exist in Istanbul.

The code produces visualizations in both Turkish and English.

The visualization will be a bar chart that has parks and green areas
categories on the X axis and their counts on the Y axis.

--------------------------------
"""

# %% --- Import required packages ---
import numpy as np  # Required for pandas
import pandas as pd  # For general data processing tasks
import matplotlib.pyplot as plt  # For plotting
import matplotlib.cm as cm
import matplotlib.colors as col
import os

# from matplotlib import rc
# rc('text', usetex=True)
# rc('text.latex', preamble=r'\usepackage{color}')

# %% --- Dynamically create a directory named after the file for outputs ---

# Get the absolute filepath
dirname = os.path.dirname(__file__)

# Split by \ to make it into relative
dirname_intermediary = dirname.split("\\")

# Join in a way that would make it relative
separator = r"/"
dirname_final = separator.join(dirname_intermediary)

# Craft a filepath without the final folder to which the plot will be exported
incomplete_output_directory = dirname_final + "/Data Analysis_Istanbul Parks and Green Areas Map/Media/Plots/"

# Get the name of the script
filename = os.path.basename(__file__)

# Split by _
filename_split = filename.split("_")

# Get the last to get the last folder name
filename_final = filename_split[-1]

# Remove the .py suffix
filename_final_processed = filename_final.split(".")[0]

# Craft the complete output directory
complete_output_directory = incomplete_output_directory + filename_final_processed

# Create the directory using os.mkdir.
try:
    os.mkdir(complete_output_directory)
except:
    pass


# %% --- Helper functions and definitions ---

# Helper function: Add labels to the top of a bar chart.
def add_value_labels(ax, spacing=5):
    """Add labels to the end of each bar in a bar chart.

    Arguments:
        ax (matplotlib.axes.Axes): The matplotlib object containing the axes
            of the plot to annotate.
        spacing (int): The distance between the labels and the bars.
    """

    # For each bar: Place a label
    for rect in ax.patches:
        # Get X and Y placement of label from rect.
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2

        # Number of points between bar and label. Change to your liking.
        space = spacing
        # Vertical alignment for positive values
        va = 'bottom'

        # If value of bar is negative: Place label below bar
        if y_value < 0:
            # Invert space to place label below
            space *= -1
            # Vertically align label at top
            va = 'top'

        # Use Y value as label and format number with one decimal place
        label = "{:}".format(y_value)  # Remove .1f if you don't want one decimal place

        # Create annotation
        ax.annotate(
            label,  # Use `label` as label
            (x_value, y_value),  # Place label at end of the bar
            xytext=(0, space),  # Vertically shift label by `space`
            textcoords="offset points",  # Interpret `xytext` as offset in points
            ha='center',  # Horizontally center label
            va=va,  # Vertically align label differently for  positive and negative values.
            rotation=90,  # Rotate label
            fontsize=15)


# Helper definitions --- Set dictionaries for fonts

# Set font info
font_title = {'family': 'sans-serif',
              "fontname": "Arial",
              'color': 'black',
              'weight': 'bold',
              'size': 30}

# Gill Sans MT doesn't work for Turkish charset.
font_axislabels = {'family': 'sans-serif',
                   "fontname": "Arial",
                   'color': 'black',
                   'weight': 'bold',
                   'size': 20}

font_xticks = {'family': 'sans-serif',
               "fontname": "Arial",
               'color': 'black',
               'weight': 'bold',
               'size': 16}

font_yticks = {'family': 'sans-serif',
               "fontname": "Arial",
               'color': 'black',
               'weight': 'normal',
               'size': 16}


# Helper definitions --- Set color for graphs

# Color quantitative sequential

def sequential_color_mapper(value):
    sequential_cmap = cm.ScalarMappable(col.Normalize(0, max(value)), cm.YlGnBu)
    return sequential_cmap


# Color categorical

categorical_color = cm.Set2.colors[0]

# Color emphasis

emphasis_color = cm.Set2.colors[2]

# %% --- Read in the datasets ---

# Istanbul park and green areas services data
parks_fp = "../../../Data/Non-GIS Data/cleaned/park_location_cleaned.csv"
parks_and_green_areas = pd.read_csv(parks_fp)

# %% --- Data Preparation ---

inst_types_counts = parks_and_green_areas.loc[:, "care_type"].value_counts()

# %% --- Visualization - English ---

# --- Figure Preparation ---

fig = plt.figure(figsize=(25.60, 14.40))

ax = fig.add_subplot(1, 1, 1)

# --- Data Selection ---

# Get labels for x - axis ticks
labels = list(parks_and_green_areas.loc[:, "care_type"].value_counts().index)

# Generate bar positions
from numpy import arange

bar_positions = arange(len(labels)) + 1

# Get bar heights from data
bar_heights = inst_types_counts.values.astype(int)

# --- Color Information ---

# For parks and green areas data  when both graphs and maps are used.
sequential_cmap = sequential_color_mapper(bar_heights)

# --- Plot Figure ---

ax.bar(bar_positions, bar_heights,
       width=0.7,
       align="center",
       color=categorical_color)

# --- Set x and y axis ticks ---

# Setting where x-ticks should be at
ax.set_xticks(bar_positions)

# Setting x-tick labels and positions
ax.set_xticklabels(labels, rotation=90)

# Setting custom y-axis tick intervals
start, end = ax.get_ylim()
ax.yaxis.set_ticks(np.arange(start, end, 500))

# --- Spine and Grid ---

# Disable right and top spine
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# --- Text ---

ax.set_title(
    # "In Istanbul, there are " + r'\textcolor{red}{3522}' + " healthcare institutions distributed across " + r'\textcolor{red}{33}' + " categories.",
    "İstanbul'daki Park Dağılımı",
    fontdict=font_title,
    pad=20)

# Add x axis label
ax.set_xlabel("Tür",
              fontdict=font_axislabels,
              labelpad=18)

# Add y axis label
ax.set_ylabel("Park Sayısı",
              fontdict=font_axislabels,
              labelpad=18)

# Set xtick font info

ax.set_xticklabels(ax.get_xticklabels(),
                   font_xticks)

# Add labels to the top of the bars
add_value_labels(ax)

# --- Export Visualization ---

# As SVG
# export_path = complete_output_directory +  r"/" + (filename_final_processed + "_eng.svg")
# plt.savefig(export_path, format = "svg", dpi = 300, bbox_inches="tight")

# As png
#export_path = complete_output_directory + r"/" + (filename_final_processed + "_eng.png")
#plt.savefig(export_path, format="png", dpi=300, bbox_inches="tight")

# %% --- Visualization - Turkish ---

# --- Figure Preparation ---

fig = plt.figure(figsize=(25.60, 14.40))

# Normall 18,9

ax = fig.add_subplot(1, 1, 1)

# --- Data Selection ---

# Get labels for x - axis ticks
labels = list(parks_and_green_areas.loc[:, "care_type"].value_counts().index)

# Generate bar positions
from numpy import arange

bar_positions = arange(len(labels)) + 1

# Get bar heights from data
bar_heights = inst_types_counts.values.astype(int)

# --- Color Information ---

# For park and green areas data  when both graphs and maps are used.
sequential_cmap = sequential_color_mapper(bar_heights)

# --- Plot Figure ---

ax.bar(bar_positions, bar_heights,
       width=0.7,
       align="center",
       color=categorical_color)

# --- Set x and y axis ticks ---

# Setting where x-ticks should be at
ax.set_xticks(bar_positions)

# Setting x-tick labels and positions
ax.set_xticklabels(labels, rotation=90)

# Setting custom y-axis tick intervals
start, end = ax.get_ylim()
ax.yaxis.set_ticks(np.arange(start, end, 500))

# --- Spine and Grid ---

# Disable right and top spine
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# --- Text ---

ax.set_title("İstanbul'da 3 farklı kategoriye dağıtılmış 3616 tane park vardır.",
             fontdict=font_title,
             pad=20)

# Add x axis label
ax.set_xlabel(u"Park Türü",
              fontdict=font_axislabels,
              labelpad=18)

# Add y axis label
ax.set_ylabel(u"Türe Göre Park Sayısı",
              fontdict=font_axislabels,
              labelpad=18)

# Set xtick font info

ax.set_xticklabels(ax.get_xticklabels(),
                   font_xticks)

# Add labels to the top of the bars
add_value_labels(ax)

# --- Export Visualization ---

# As svg
# export_path = complete_output_directory +  r"/" + (filename_final_processed + "_tr.svg")
# plt.savefig(export_path, format = "svg", dpi = 1200, bbox_inches="tight")

# As png
export_path = complete_output_directory + r"/" + (filename_final_processed + "_sadece_parklar_tr.png")
plt.savefig(export_path, format="png", dpi=600, bbox_inches="tight")