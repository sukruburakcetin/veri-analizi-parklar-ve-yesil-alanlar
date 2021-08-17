# import the necessary packages
import os

import cv2
import numpy as np
from matplotlib import pyplot as plt


def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged


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

complete_output_directory = incomplete_output_directory + filename_final_processed
kernel = np.ones((3, 3), np.uint8)
image = cv2.imread('../../../Data/Non-GIS Data/external/satellite-map-of-istanbul.jpg')
image_2 = cv2.imread('../../../Data/Non-GIS Data/external/yayilim_with_no_name_tr.jpg', 0)

image_clone = image.copy()

h, w = image_2.shape
size = h, w, 1
empty_mat = np.zeros(size, dtype=np.uint8)

blur = cv2.GaussianBlur(image_2, (1, 1), 0)
edges = auto_canny(blur)
thresh = cv2.threshold(edges, 3, 255, cv2.ADAPTIVE_THRESH_MEAN_C | cv2.THRESH_OTSU)[1]
edges = cv2.Canny(image_2, threshold1=100, threshold2=200)
edges_copy_alt = edges.copy()
closing = cv2.morphologyEx(edges_copy_alt, cv2.MORPH_CLOSE, kernel)
contours, hierarchy = cv2.findContours(closing, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
font = cv2.FONT_HERSHEY_SIMPLEX
h, w, _ = image.shape
mask = np.zeros((h + 2, w + 2), np.uint8)
counter = 0
greenRate = -1
minContourArea = 10
image_converted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

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
        cv2.putText(image_converted, str(greenRate), (cX, cY), font, .5, (0), 2)
        cv2.putText(image, str(greenRate), (cX, cY), font, .5, (0), 2)
        freqs = np.cumsum(np.hstack([[0], counts[indices] / float(counts.sum())]))
        rows = np.int_(ROI.shape[0] * freqs)
        dom_patch = np.zeros(shape=ROI.shape, dtype=np.uint8)
        for i in range(len(rows) - 1):
            dom_patch[rows[i]:rows[i + 1], :, :] += np.uint8(palette[indices[i]])
        cv2.imwrite("../../../Data/Non-GIS Data/external/stash/dom_patch" + str(counter) + ".png", dom_patch)
        cv2.imwrite("../../../Data/Non-GIS Data/external/stash/roi_" + str(counter) + ".png", ROI)
        counter += 1

cv2.drawContours(image_converted, contours, -1, (0, 0, 255), 0)
cv2.drawContours(image, contours, -1, (0, 0, 255), 0)
cv2.imwrite(complete_output_directory + r"/" + filename_final_processed + "contoursOverlayed.png", image)
f, (ax0, ax1) = plt.subplots(1, 2)
ax0.imshow(image_converted, interpolation='nearest')
ax1.imshow(closing, interpolation='nearest')
ax0.set_title("Uydu görüntüsü üzerinden yeşil alan miktarına göre puanlama",
               color="black",
               weight="bold",
               fontsize=5,
               pad=5)

ax0.set_xlabel("Katsayı",
                fontdict=font_axislabels,
                labelpad=18)
#plt.show()
export_path = complete_output_directory + r"/" + (filename_final_processed + "_figure.svg")
plt.savefig(export_path, format="svg", dpi=900, bbox_inches="tight")

# As png
export_path = complete_output_directory + r"/" + (filename_final_processed + "_figure.png")
plt.savefig(export_path, format="png", dpi=300, bbox_inches="tight")
