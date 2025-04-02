# Day 1 of 30 Days of Charts 2025
#
# Fractions
#
# First install libraries in terminal with pip install numpy matplotlib seaborn

#########################################################
# Updated attempt with final color support from Claude.ai
#########################################################
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap, LogNorm
import matplotlib.colors as mcolors

# Define the number of rows and columns (now 1 to 10)
num_rows = 10
num_cols = 10

# Create the data array for the heatmap (for color mapping)
data = np.zeros((num_rows, num_cols))

# Create the array for the labels
labels = np.empty((num_rows, num_cols), dtype=object)

# Populate the data and labels arrays
for y in range(1, num_rows + 1):
    for x in range(1, num_cols + 1):
        data[y - 1, x - 1] = y / x
        labels[y - 1, x - 1] = f"{y}/{x}"

# Define the colors for the custom colormap
color_less_than_1 = '#00441b'   # New dark green color
color_greater_than_1 = '#40004b'  # New dark purple color
white = '#FFFFFF'            # White
gray_color = '#CCCCCC'       # 80% gray (actually closer to 80% white/20% black)

# Create two separate colormaps for values < 1 and values > 1
# For values < 1 (from dark green to white)
cmap_less_than_1 = LinearSegmentedColormap.from_list('green_to_white', 
                                                   [color_less_than_1, white])

# For values > 1 (from white to dark purple)
cmap_greater_than_1 = LinearSegmentedColormap.from_list('white_to_purple', 
                                                      [white, color_greater_than_1])

# Combine the colormaps
# Create a nonlinear normalization to make small values more prominent
class NonLinearNorm(mcolors.Normalize):
    def __init__(self, vmin=0, vmax=10, center=1, clip=False):
        super().__init__(vmin, vmax, clip)
        self.center = center
        
    def __call__(self, value, clip=None):
        # Transform values < 1 to make the color gradient more prominent
        result = np.ma.masked_array(np.zeros_like(value, dtype=np.float64), mask=np.ma.getmask(value))
        
        # For values < 1, use a power function to make colors more intense as they approach 0
        less_than_1 = np.where(value < self.center)
        if len(less_than_1[0]) > 0:
            # Scale from 0-0.5 for values between 0-1
            result[less_than_1] = 0.5 * (value[less_than_1] / self.center) ** 0.3
            
        # For values >= 1, linear mapping from 0.5-1.0
        greater_equal_1 = np.where(value >= self.center)
        if len(greater_equal_1[0]) > 0:
            # Max value in data
            max_val = np.max(value)
            # Scale from 0.5-1.0 for values between 1-max
            result[greater_equal_1] = 0.5 + 0.5 * (value[greater_equal_1] - self.center) / (max_val - self.center)
            
        return result

# Create the custom colormap by concatenating the two colormaps
n_bins = 100  # Number of discrete colors
colors_less = cmap_less_than_1(np.linspace(0, 1, n_bins//2))
colors_greater = cmap_greater_than_1(np.linspace(0, 1, n_bins//2))
all_colors = np.vstack((colors_less, colors_greater))
custom_cmap = mcolors.LinearSegmentedColormap.from_list('custom_diverging', all_colors)

# Set up the plot with a gray background
plt.figure(figsize=(6, 6))

# Set the gray color for all text elements
text_color = '#666666'  # 80% gray (40% black)

# Change the default text color for the entire plot
plt.rcParams['text.color'] = text_color
plt.rcParams['axes.labelcolor'] = text_color
plt.rcParams['xtick.color'] = text_color
plt.rcParams['ytick.color'] = text_color

# Create the heatmap using seaborn with the custom colormap, normalization, and labels
norm = NonLinearNorm(vmin=np.min(data), vmax=np.max(data), center=1)
heatmap = sns.heatmap(data, annot=labels, fmt='', cmap=custom_cmap, norm=norm,
            xticklabels=range(1, num_cols + 1),
            yticklabels=range(1, num_rows + 1),
            annot_kws={"fontsize": 8, "color": text_color},
            cbar=False) # Remove the heatmap color bar for clarity

# Get the current axes object
axes = plt.gca()

# Invert the y-axis
axes.invert_yaxis()

# Add labels and title with gray text
plt.xlabel("Denominator", color=text_color)
plt.ylabel("Numerator", color=text_color)
plt.title("Fraction Funhouse: A Heatmap Adventure from 1 to 10", color=text_color)

# Apply gray color to tick labels
for label in (axes.get_xticklabels() + axes.get_yticklabels()):
    label.set_color(text_color)

# Show the plot and save as JPG
plt.tight_layout()
plt.savefig("C:/Users/clint/OneDrive/Code/Python/2025 30DOC Python/01 fractions/01_fractions.jpg", dpi=300, bbox_inches='tight')
plt.show()