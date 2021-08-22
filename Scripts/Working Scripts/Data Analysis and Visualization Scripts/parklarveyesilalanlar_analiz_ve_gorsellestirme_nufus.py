# -*- coding: utf-8 -*-
"""
------ What's this file? ------

This script contains some helper functions and definitions that i can
use across my actual analysis and visualization scripts.

--------------------------------
"""

# %% --- ENVIRONMENT CHECK ---
# The module dependencies of this script are located within my conda environment
# "mappingenv"

# %% --- Import required packages ---

import numpy as np  # Required for pandas
import pandas as pd  # For general data processing tasks
import matplotlib.pyplot as plt  # For plotting
import matplotlib.cm as cm
import matplotlib.colors as col
import os
from scipy import stats as st
import geopandas as gpd  # A module built on top of pandas for geospatial analysis
from pyproj import CRS  # For CRS (Coordinate Reference System) functions
from shapely.geometry import Point, MultiPoint  # Required for point/polygon geometry
from shapely.ops import nearest_points  # Required for nearest neighbor analysis
import contextily as ctx  # Used in conjuction with matplotlib/geopandas to set a basemap
from geopy import distance  # For geodesic distance calculation (radians to meters)

# %% --- Dynamically create a directory named after the file for outputs ---

# Get the absolute filepath
dirname = os.path.dirname(__file__)

# Split by \ to make it into relative
dirname_intermediary = dirname.split("\\")

# Join in a way that would make it relative
separator = r"/"
dirname_final = separator.join(dirname_intermediary[0:5])

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
            rotation=90,
            fontsize=14)  # Rotate label


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
               'size': 12}

font_yticks = {'family': 'sans-serif',
               "fontname": "Arial",
               'color': 'black',
               'weight': 'normal',
               'size': 16}

font_figtitle = {'family': 'sans-serif',
                 "fontname": "Arial",
                 'color': 'black',
                 'weight': 'bold',
                 'size': 90}


# Helper definitions --- Set color for graphs

# Color quantitative sequential

def sequential_color_mapper(value):
    sequential_cmap = cm.ScalarMappable(col.Normalize(0, max(value)), cm.YlOrBr)
    return sequential_cmap


# Color categorical

categorical_color = cm.Set2.colors[0]
categorical_color_2 = cm.Set2.colors[3]

# Color emphasis

emphasis_color = cm.Set2.colors[2]

# %% --- Read in the datasets ---
# istanbul_park_location_cleaned
# Istanbul parks and green areas services data
parks_fp = "../../../Data/Non-GIS Data/cleaned/park_location_cleaned.csv"
parks_and_green_areas = pd.read_csv(parks_fp)

# Istanbul geospatial districts data
istanbul_districts_fp = "../../../Data/GIS data/Processed/istanbul_districts.shp"
istanbul_districts = gpd.read_file(istanbul_districts_fp)

# Istanbul districts extra data
districts_extra_fp = "../../../Data/Non-GIS Data/external/district_income.xlsx"
districts_extra = pd.read_excel(districts_extra_fp)

# %% --- Data Preparation ---

# Create a mask to select low level parks only
low_level_mask = parks_and_green_areas.loc[:, "institution_type_tr"] == "Park"

# Use the boolean mask to select
parks_low_level = parks_and_green_areas.loc[low_level_mask, :]

# How many first-step parks and green areas are region child vs. region sport?
# private_vs_public = health_low_level.loc[:,"private_or_public"].value_counts()

# Distribution across districts
district_inst_count = parks_low_level.loc[:, "district_tr"].value_counts().rename_axis("district_tr").reset_index(
    name="count")

# Does this correlate with population ?
#district_inst_count.to_csv(r'counts.csv')

district_inst_count.reset_index(drop=True)
# Merge into an intermediary dataframe
districts_with_inst_count = pd.merge(districts_extra,
                                     district_inst_count,
                                     how="left",
                                     on="district_tr")
# districts_with_inst_count.to_csv(r'extracted.csv', index = False)
r1 = st.pearsonr(districts_with_inst_count["population"],
                 districts_with_inst_count["total_active_green_space"])[0]

# Does this correlate with income ?

r2 = st.pearsonr(districts_with_inst_count["green_space_per_person"],
                 districts_with_inst_count["total_active_green_space"])[0]

# Distribution across district normalized by population
districts_with_inst_count.loc[:, "normalized_count"] = districts_with_inst_count.loc[:,
                                                       "count"] / districts_with_inst_count.loc[:, "population"]

# Merge with districts

districts_with_inst_count.rename(columns={"district_eng": "district_e"},
                                 inplace=True)

istanbul_districts_merged = pd.merge(left=istanbul_districts,
                                     right=districts_with_inst_count,
                                     how="left",
                                     on="district_e")
# %%  --- Visualization - English ---

# --- Figure Preparation ---

# Create a figure
fig = plt.figure(figsize=(19.20, 19.20),
                 constrained_layout=True)  # Constrained layout to use with gridspec

# Define a gridspect of 2 rows and 4 columns
gs = fig.add_gridspec(4, 4)

# The first ax will occupy all space of columns 1,2 in row 1,2
ax_1 = fig.add_subplot(gs[:2, :])

# The second ax will occupy the half of columns 3,4
ax_2 = fig.add_subplot(gs[2:4, :2])

ax_3 = fig.add_subplot(gs[2, 2:])

ax_4 = fig.add_subplot(gs[3, 2:])

# --- Plotting ---

#       --- Ax_1 : Map ---
istanbul_districts_merged.plot(ax=ax_1,
                               column="count",
                               edgecolor="black",
                               alpha=1,
                               cmap=cm.YlOrBr)

ctx.add_basemap(ax_1, zoom=11,  # 16
                crs='epsg:4326',
                source=ctx.providers.Esri.WorldGrayCanvas)

# --- Spine and Grid ---

ax_1.set_axis_off()  # Turn off axis

# --- Map Labels ---

# Select districts that you want labels for
districts_to_label_list = ["Silivri", "Catalca", "Buyukcekmece", "Arnavutkoy", "Eyupsultan", "Sariyer",
                           "Beykoz", "Sile", "Cekmekoy", "Tuzla", "Pendik", "Maltepe",
                           "Basaksehir", "Bahcelievler", "Beyoglu", "Bakirkoy"]

# Create a boolean indexing mask checking for those districts
labels_mask = istanbul_districts.loc[:, "district_e"].isin(districts_to_label_list)

# Pass in the boolean mask to create a dataframe
districts_to_label = istanbul_districts.loc[labels_mask, ["district_e", "geometry"]]

# Create a representative point within each district polygon to place the label
districts_to_label["representative_point"] = districts_to_label.geometry.representative_point().geometry.values

# Pass over each row label the repsentative point according to that row's name
for idx, row in districts_to_label.iterrows():
    ax_1.annotate(s=row["district_e"], xy=(row["representative_point"].x, row["representative_point"].y),
                  horizontalalignment='center')

#   --- Ax_2 : Bar plot ---

# Get labels for x - axis ticks
labels = list(districts_with_inst_count.sort_values(by="count", ascending=False).loc[:, "district_e"])

# Generate bar positions
from numpy import arange

bar_positions = arange(len(labels)) + 1

# Get bar heights from data
bar_heights = districts_with_inst_count.loc[:, "count"].sort_values(ascending=False).astype(int)

# --- Color Information ---

# For parks and green areas data  when both graphs and maps are used.
sequential_cmap = cm.ScalarMappable(col.Normalize(0, max(bar_heights)), cm.YlOrBr)

# --- Plot Figure ---

ax_2.bar(bar_positions, bar_heights,
         width=0.5,
         align="center",
         color=sequential_cmap.to_rgba(bar_heights))

# --- Add color legend ---

# Import required toolkit
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# Create an inset_axes instance with different parameters
axins1 = inset_axes(ax_2,
                    width="50%",  # width = 50% of parent_bbox width
                    height="5%",  # height : 5%
                    loc="upper right")

# Create a colormap
cbar = plt.colorbar(sequential_cmap,
                    cax=axins1,
                    # ticks = [] Cna also set ticks like this
                    orientation="horizontal",
                    shrink=0.25,
                    anchor=(30, 10))

cbar.set_label('Number of first step healthcare institutions',
               size=8,
               weight="bold")

# --- Set x and y axis ticks ---

# Setting where x-ticks should be at
ax_2.set_xticks(bar_positions)

# Setting x-tick labels and positions
ax_2.set_xticklabels(labels, rotation=90)

start, end = ax_2.get_ylim()
ax_2.yaxis.set_ticks(np.arange(start, end, 5))

# --- Spine and Grid ---

# Disable right and top spine
ax_2.spines['right'].set_visible(False)
ax_2.spines['top'].set_visible(False)

# --- Text ---

# Add x axis label
ax_2.set_xlabel("District",
                fontdict=font_axislabels,
                labelpad=18)

# Add y axis label
ax_2.set_ylabel("Number of first step healthcare institutions",
                fontdict=font_axislabels,
                labelpad=18)

# Add labels to the top of the bars
add_value_labels(ax_2)

# Set xtick font info

ax_2.set_xticklabels(ax_2.get_xticklabels(),
                     font_xticks)

#   --- Ax_3 : Scatterplot 1 ---

ax_3.scatter(x=districts_with_inst_count.loc[:, "population"],
             y=districts_with_inst_count.loc[:, "count"],
             s=150,  # To specify face width
             c=categorical_color)

# --- Set x and y axis ticks ---


# --- Spine and Grid ---

# Disable right and top spine
ax_3.spines['right'].set_visible(False)
ax_3.spines['top'].set_visible(False)

# --- Text ---

# Add x axis label
ax_3.set_xlabel("Population",
                fontdict=font_axislabels,
                labelpad=18)

ax_3.set_title("Correlation of the number of first step healthcare institutions with:",
               color="black",
               weight="bold",
               fontsize=14,
               pad=15)

# Annotate pearson's r

ax_3.annotate(s="r = {:.2f}".format(r1),
              xy=(.9, .9),
              xycoords=ax_3.transAxes,
              color="black",
              weight="bold",
              fontsize=15)

#   --- Ax_4 : Scatterplot 2 ---

ax_4.scatter(x=districts_with_inst_count.loc[:, "yearly_average_household_income"],
             y=districts_with_inst_count.loc[:, "count"],
             s=150,  # To specify face width
             c=categorical_color)

# --- Set x and y axis ticks ---


# --- Spine and Grid ---

# Disable right and top spine
ax_4.spines['right'].set_visible(False)
ax_4.spines['top'].set_visible(False)

# --- Text ---

# Add x axis label

ax_4.set_xlabel("Yearly average household income",
                fontdict=font_axislabels,
                labelpad=2)

# Annotate pearson's r

ax_4.annotate(s="r = {:.2f}".format(r2),
              xy=(.9, .9),
              xycoords=ax_4.transAxes,
              color="black",
              weight="bold",
              fontsize=15)

# # --- Misc ---

# Set figure title
fig.suptitle("In Istanbul, first step healthcare institutions \n are distributed in accordance with population.",
             family='sans-serif',
             fontname="Arial",
             color='black',
             weight='bold',
             size=30,
             x=0.60,
             y=0.90)  # Doesn't use fontdict for some reason

# #Make layout tighter
plt.tight_layout()

# --- Export Visualization ---

# As SVG
# export_path = complete_output_directory +  r"/" + (filename_final_processed + "_eng.svg")
# plt.savefig(export_path, format = "svg", dpi = 1200, bbox_inches="tight")

# As png
#export_path = complete_output_directory + r"/" + (filename_final_processed + "_eng.png")
#plt.savefig(export_path, format="png", dpi=300, bbox_inches="tight")

# %% --- Visualization - Turkish ---

# --- Figure Preparation ---

# Create a figure
fig = plt.figure(figsize=(19.20, 19.20),
                 constrained_layout=True)  # Constrained layout to use with gridspec

# Define a gridspect of 2 rows and 4 columns
gs = fig.add_gridspec(4, 4)

# The first ax will occupy all space of columns 1,2 in row 1,2
ax_1 = fig.add_subplot(gs[:2, :])

# The second ax will occupy the half of columns 3,4
ax_2 = fig.add_subplot(gs[2:4, :2])

ax_3 = fig.add_subplot(gs[2, 2:])

ax_4 = fig.add_subplot(gs[3, 2:])

# --- Plotting ---

#       --- Ax_1 : Map ---
istanbul_districts_merged.plot(ax=ax_1,
                               column="total_active_green_space",
                               edgecolor="black",
                               alpha=1,
                               cmap=cm.YlOrBr)

ctx.add_basemap(ax_1, zoom=11,  # 16
                crs='epsg:4326',
                source=ctx.providers.Esri.WorldGrayCanvas)

# --- Spine and Grid ---

ax_1.set_axis_off()  # Turn off axis

# --- Map Labels ---

# Select districts that you want labels for
districts_to_label_list = ["Silivri", "Catalca", "Buyukcekmece", "Arnavutkoy", "Eyupsultan", "Sariyer",
                           "Beykoz", "Sile", "Cekmekoy", "Tuzla", "Pendik",
                           "Maltepe", "Basaksehir", "Bahcelievler", "Beyoglu", "Bakirkoy"]

# Create a boolean indexing mask checking for those districts
labels_mask = istanbul_districts.loc[:, "district_e"].isin(districts_to_label_list)

# Pass in the boolean mask to create a dataframe
districts_to_label = istanbul_districts.loc[labels_mask, ["district_t", "geometry"]]

# Create a representative point within each district polygon to place the label
districts_to_label["representative_point"] = districts_to_label.geometry.representative_point().geometry.values

# Pass over each row label the repsentative point according to that row's name
for idx, row in districts_to_label.iterrows():
    ax_1.annotate(s=row["district_t"], xy=(row["representative_point"].x, row["representative_point"].y),
                  horizontalalignment='center')

#   --- Ax_2 : Bar plot ---

# Get labels for x - axis ticks
labels = list(districts_with_inst_count.sort_values(by="total_active_green_space", ascending=False).loc[:, "district_tr"])

# Generate bar positions
from numpy import arange

bar_positions = arange(len(labels)) + 1

# Get bar heights from data
bar_heights = districts_with_inst_count.loc[:, "total_active_green_space"].sort_values(ascending=False).astype(int)

# --- Color Information ---

# For parks and green areas data  when both graphs and maps are used.
sequential_cmap = cm.ScalarMappable(col.Normalize(0, max(bar_heights)), cm.YlOrBr)

# --- Plot Figure ---

ax_2.bar(bar_positions, bar_heights,
         width=0.5,
         align="center",
         color=sequential_cmap.to_rgba(bar_heights))

# --- Add color legend ---

# Import required toolkit
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# Create an inset_axes instance with different parameters
axins1 = inset_axes(ax_2,
                    width="50%",  # width = 50% of parent_bbox width
                    height="5%",  # height : 5%
                    loc="upper right")

# Create a colormap
cbar = plt.colorbar(sequential_cmap,
                    cax=axins1,
                    # ticks = [] Cna also set ticks like this
                    orientation="horizontal",
                    shrink=0.25,
                    anchor=(30, 10))

cbar.set_label('Toplam Aktif Yeşil Alan',
               size=8,
               weight="bold")

# --- Set x and y axis ticks ---

# Setting where x-ticks should be at
ax_2.set_xticks(bar_positions)

# Setting x-tick labels and positions
ax_2.set_xticklabels(labels, rotation=90)

start, end = ax_2.get_ylim()
ax_2.yaxis.set_ticks(np.arange(start, end, 5))

# --- Spine and Grid ---

# Disable right and top spine
ax_2.spines['right'].set_visible(False)
ax_2.spines['top'].set_visible(False)

# --- Text ---

# Add x axis label
ax_2.set_xlabel("İlçe",
                fontdict=font_axislabels,
                labelpad=18)

# Add y axis label
ax_2.set_ylabel("Toplam Aktif Yeşil Alan",
                fontdict=font_axislabels,
                labelpad=18)

# Add labels to the top of the bars
add_value_labels(ax_2)

# Set xtick font info

ax_2.set_xticklabels(ax_2.get_xticklabels(),
                     font_xticks)

#   --- Ax_3 : Scatterplot 1 ---
ax_3.ticklabel_format(style='plain') #added for preventing "e" scientific notation // burak
ax_3.scatter(x=districts_with_inst_count.loc[:, "population"],
             y=districts_with_inst_count.loc[:, "total_active_green_space"],
             s=150,  # To specify face width
             c=categorical_color)

# --- Set x and y axis ticks ---

# --- Spine and Grid ---

# Disable right and top spine
ax_3.spines['right'].set_visible(False)
ax_3.spines['top'].set_visible(False)

# --- Text ---

# Add x axis label
ax_3.set_xlabel("Nüfus",
                fontdict=font_axislabels,
                labelpad=18)

ax_3.set_title("Aktif yeşil alanların farklı değişkenler ile korelasyonu:",
               color="black",
               weight="bold",
               fontsize=14,
               pad=15)

# Annotate pearson's r

ax_3.annotate(s="r = {:.2f}".format(r1),
              xy=(.9, .9),
              xycoords=ax_3.transAxes,
              color="black",
              weight="bold",
              fontsize=15)
#   --- Ax_4 : Scatterplot 2 ---

ax_4.scatter(x=districts_with_inst_count.loc[:, "green_space_per_person"],
             y=districts_with_inst_count.loc[:, "total_active_green_space"],
             s=150,  # To specify face width
             c=categorical_color)

# --- Set x and y axis ticks ---


# --- Spine and Grid ---

# Disable right and top spine
ax_4.spines['right'].set_visible(False)
ax_4.spines['top'].set_visible(False)

# --- Text ---

# Add x axis label

ax_4.set_xlabel("Kişi Başına Düşen Yeşil Alan Miktarı m2/kisi",
                fontdict=font_axislabels,
                labelpad=2)

# Annotate pearson's r

ax_4.annotate(s="r = {:.2f}".format(r2),
              xy=(.9, .9),
              xycoords=ax_4.transAxes,
              color="black",
              weight="bold",
              fontsize=15)

# # --- Misc ---

# Set figure title
fig.suptitle("İstanbul'da aktif yeşil alanların \n nüfus ile orantısı düşük seviyelidir. \n ayrıca TESEV verileri kendi için de örtüşmektedir. ",
             family='sans-serif',
             fontname="Arial",
             color='black',
             weight='bold',
             size=30,
             x=0.60,
             y=0.90)  # Doesn't use fontdict for some reason

# #Make layout tighter
plt.tight_layout()

# --- Export Visualization ---

# As SVG
export_path = complete_output_directory +  r"/" + (filename_final_processed + "_alt_population_tr.svg")
plt.savefig(export_path, format = "svg", dpi = 900, bbox_inches="tight")

# As png
export_path = complete_output_directory + r"/" + (filename_final_processed + "_alt_population_tr.png")
plt.savefig(export_path, format="png", dpi=300, bbox_inches="tight")