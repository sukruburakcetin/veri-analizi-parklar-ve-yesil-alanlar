# import the necessary packages
import os

import cv2
import numpy as np
import pandas as pd  # For general data processing tasks
from matplotlib import pyplot as plt
import geopandas as gpd  # A module built on top of pandas for geospatial analysis
import contextily as ctx  # Used in conjuction with matplotlib/geopandas to set a basemap
import matplotlib.cm as cm
import matplotlib.colors as col

def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged
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
            fontsize=15)  # Rotate label


# Helper definitions --- Set dictionaries for fonts

# %% --- Dynamically create a directory named after the file for outputs ---

# Get the absolute filepath
dirname = os.path.dirname(__file__)

# Split by \ to make it into relative
dirname_intermediary = dirname.split("\\")

# Join in a way that would make it relative
separator = r"/"
dirname_final = separator.join(dirname_intermediary[0:5])

# Craft the complete output directory
incomplete_output_directory = dirname_final + "/Data Analysis_Istanbul Parks and Green Areas Map/Media/Plots/"

# Get the name of the script
filename = os.path.basename(__file__)

# Split by _
filename_split = filename.split("_")

# Get the last to get the last folder name
filename_final = filename_split[-1]

# Remove the .py suffix
filename_final_processed = filename_final.split(".")[0]

# Gill Sans MT doesn't work for Turkish charset.
font_axislabels = {'family': 'sans-serif',
                   "fontname": "Arial",
                   'color': 'black',
                   'weight': 'bold',
                   'size': 10}

font_yticks = {'family': 'sans-serif',
               "fontname": "Arial",
               'color': 'black',
               'weight': 'normal',
               'size': 16}

font_xticks = {'family': 'sans-serif',
               "fontname": "Arial",
               'color': 'black',
               'weight': 'bold',
               'size': 16}

complete_output_directory = incomplete_output_directory + filename_final_processed
kernel = np.ones((3, 3), np.uint8)

# Istanbul health services data
greenIndex_fp = "../../../Data/Non-GIS Data/external/district_income.xlsx"
greenIndex = pd.read_excel(greenIndex_fp)

# Istanbul geospatial districts data
istanbul_districts_fp = "../../../Data/GIS data/Processed/istanbul_districts.shp"
istanbul_districts = gpd.read_file(istanbul_districts_fp, )

satellite_2D_istanbul = cv2.imread('../../../Data/Non-GIS Data/external/satellite-map-of-istanbul.jpg')
raw_shapefile_districts = cv2.imread('../../../Data/Non-GIS Data/external/yayilim_with_no_name_tr.jpg', 0)
raw_shapefile_districts_cleaned = cv2.imread('../../../Data/Non-GIS Data/external/districts_cleaned.jpg', 0)

# Istanbul geospatial districts data
istanbul_districts_fp = "../../../Data/GIS data/Processed/istanbul_districts.shp"
istanbul_districts = gpd.read_file(istanbul_districts_fp, )

image_clone = satellite_2D_istanbul.copy()

h, w = raw_shapefile_districts.shape
size = h, w, 1
empty_mat = np.zeros(size, dtype=np.uint8)

blur = cv2.GaussianBlur(raw_shapefile_districts, (1, 1), 0)
edges = auto_canny(blur)

edges = cv2.Canny(raw_shapefile_districts, threshold1=100, threshold2=200)
edges_copy_alt = edges.copy()
closing = cv2.morphologyEx(edges_copy_alt, cv2.MORPH_CLOSE, kernel)

contours, hierarchy = cv2.findContours(raw_shapefile_districts_cleaned, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

font = cv2.FONT_HERSHEY_SIMPLEX
h, w, _ = satellite_2D_istanbul.shape
mask = np.zeros((h + 2, w + 2), np.uint8)
counter = 0
greenRate = -1
minContourArea = 10
image_converted = cv2.cvtColor(satellite_2D_istanbul, cv2.COLOR_BGR2RGB)

for c in contours:
    contourArea = cv2.contourArea(c)
    if contourArea > minContourArea:
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        x, y, w, h = cv2.boundingRect(c)
        ROI = image_clone[y:y + h, x:x + w]
        average = ROI.mean(axis=0).mean(axis=0)
        pixels = np.float32(ROI.reshape(-1, 3))

        n_colors = 1
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
        flags = cv2.KMEANS_RANDOM_CENTERS

        _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
        _, counts = np.unique(labels, return_counts=True)
        dominant = palette[np.argmax(counts)]
        print('Dominant color: ', dominant)
        indices = np.argsort(counts)[::-1]
        gray_avg = (dominant[0] + dominant[1] + dominant[2]) / 3
        if 0 < gray_avg < 25:
            greenRate = 9
        elif 25 <= gray_avg < 50:
            greenRate = 8
        elif 50 <= gray_avg < 75:
            greenRate = 7
        elif 75 <= gray_avg < 100:
            greenRate = 6
        elif 100 <= gray_avg < 125:
            greenRate = 5
        elif 125 <= gray_avg < 150:
            greenRate = 4
        elif 150 <= gray_avg < 175:
            greenRate = 3
        elif 175 <= gray_avg < 200:
            greenRate = 2
        elif 200 <= gray_avg < 225:
            greenRate = 1
        elif 225 <= gray_avg < 256:
            greenRate = 0
        cv2.putText(image_converted, str(greenRate), (cX, cY), font, .3, (0), 1)
        cv2.putText(satellite_2D_istanbul, str(greenRate), (cX, cY), font, .3, (0), 1)
        freqs = np.cumsum(np.hstack([[0], counts[indices] / float(counts.sum())]))
        rows = np.int_(ROI.shape[0] * freqs)
        dom_patch = np.zeros(shape=ROI.shape, dtype=np.uint8)
        for i in range(len(rows) - 1):
            dom_patch[rows[i]:rows[i + 1], :, :] += np.uint8(palette[indices[i]])
        cv2.imwrite("../../../Data/Non-GIS Data/external/stash/dom_patch" + str(counter) + ".png", dom_patch)
        cv2.imwrite("../../../Data/Non-GIS Data/external/stash/roi_" + str(counter) + ".png", ROI)
        counter += 1

cv2.drawContours(image_converted, contours, -1, (0, 0, 255), 0)
cv2.drawContours(satellite_2D_istanbul, contours, -1, (0, 0, 255), 0)
cv2.imwrite(complete_output_directory + r"/" + filename_final_processed + "contoursOverlayed.png",
            satellite_2D_istanbul)

green_area_index_district = greenIndex.loc[:, ['district_eng', 'green_area_index']]

green_area_index_district.rename(columns={"district_eng": "district_e", "green_area_index": "green_area_index"},
                                 inplace=True)

istanbul_districts = istanbul_districts.merge(green_area_index_district,
                                              on="district_e",
                                              how="left")

# Now, this information can be used for both TR and eng

# %% --- Visualization - English ---

# --- Figure Preparation ---

fig = plt.figure(figsize=(19.20, 19.20))

ax_1 = fig.add_subplot(2, 1, 1)

#                            --- MAP: ---

# --- Plot Figure ---

istanbul_districts.plot(ax=ax_1,
                        column="green_area_index",
                        edgecolor="black",
                        alpha=1,
                        cmap=cm.BuGn)
# YlGnBu -> blue schema
# --- Set Basemap ---

ctx.add_basemap(ax_1, zoom=11,  # 16
                crs='epsg:4326',
                source=ctx.providers.Esri.WorldGrayCanvas)

# --- Spine and Grid ---

ax_1.set_axis_off()  # Turn off axis

# --- Map Labels ---

# Select districts that you want labels for
districts_to_label_list = ["Silivri", "Catalca", "Buyukcekmece", "Arnavutkoy", "Eyupsultan", "Sariyer",
                           "Beykoz", "Sile", "Cekmekoy", "Tuzla", "Pendik", "Maltepe", "Basaksehir", "Bahcelievler",
                           "Beyoglu"]

districts_to_label_indexes = [31, 5, 16, 3, 20, 33, 13, 1, 17, 37, 30]

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

#                           --- BAR CHART: ---

# --- Figure Preparation ---
ax_2 = fig.add_subplot(2, 1, 2)

# --- Data Selection ---

# Get labels for x - axis ticks
labels = list(green_area_index_district.loc[:, "district_e"].value_counts().sort_values(ascending=False).index)

# Generate bar positions
from numpy import arange

bar_positions = arange(len(labels)) + 1

# Get bar heights from data
bar_heights = green_area_index_district.loc[:, "green_area_index"].values.astype(int)

# --- Color Information ---

# For health data  when both graphs and maps are used.
sequential_cmap = cm.ScalarMappable(col.Normalize(0, max(bar_heights)), cm.BuGn)

# --- Plot Figure ---

ax_2.bar(bar_positions, bar_heights,
         width=0.7,
         align="center",
         color=sequential_cmap.to_rgba(bar_heights))

# --- Add color legend ---

# Import required toolkit
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# Create an inset_axes instance with different parameters
axins1 = inset_axes(ax_2,
                    width="15%",  # width = 50% of parent_bbox width
                    height="3%",  # height : 5%
                    loc='upper right')

# Create a colormap
cbar = plt.colorbar(sequential_cmap,
                    cax=axins1,
                    # ticks = [] Cna also set ticks like this
                    orientation="horizontal",
                    shrink=0.25,
                    anchor=(30, 10))

cbar.set_label('Yeşil Alan Index Skoru',
               size=14,
               weight="bold")

# --- Set x and y axis ticks ---

# Setting where x-ticks should be at
ax_2.set_xticks(bar_positions)

# Setting x-tick labels and positions
ax_2.set_xticklabels(labels, rotation=90)

# Setting custom y-axis tick intervals
start, end = ax_2.get_ylim()
ax_2.yaxis.set_ticks(np.arange(start, end, 50))

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
ax_2.set_ylabel("Number of parks/green areas",
                fontdict=font_axislabels,
                labelpad=18)

# Add labels to the top of the bars
add_value_labels(ax_2)

# Set xtick font info

ax_2.set_xticklabels(ax_2.get_xticklabels(),
                     font_xticks)

# --- Misc ---

# Remove the empty white-space around the axes
plt.tight_layout()

# -------------
# plt.show()
export_path = complete_output_directory + r"/" + (filename_final_processed + "_figur_koroplet_ve_bar.svg")
plt.savefig(export_path, format="svg", dpi=900, bbox_inches="tight")

# As png
export_path = complete_output_directory + r"/" + (filename_final_processed + "_figur_koroplet_ve_bar.png")
plt.savefig(export_path, format="png", dpi=300, bbox_inches="tight")
