# Day 3 of 30 Days of Charts 2025
#
# Circle
#
#
# First install libraries
import pandas as pd
import os # for changing working directory
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Change the working directory to the correct path
os.chdir("c:/Users/clint/OneDrive/Code/Python/2025 30DCC Python/03 circle/")

# Call dataset vtm for Vermont Mammals (really, just moose and black bear)
vtm = pd.read_csv("moose_and_black_bear_counts.csv")
print(vtm.head())

# Create the figure with two subplots side by side
fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'polar'}] * 2],
                    subplot_titles=None)  # Remove subplot titles, we'll add them manually below

# --- Radial Bar chart for Moose ---
fig.add_trace(go.Barpolar(
    r=vtm['moose_scaled'],
    theta=vtm['month_name'][::-1], # Reverse month order for clockwise
    name='Moose 19,670',
    marker_color='#00441b'),
    row=1, col=1
)

# --- Radial Bar chart for Black Bear ---
fig.add_trace(go.Barpolar(
    r=vtm['black_bear_scaled'],
    theta=vtm['month_name'][::-1], # Reverse month order for clockwise
    name='Black Bear 2,059',
    marker_color='#40004b'),
    row=1, col=2
)

# Update layout for better presentation
fig.update_layout(
    title=None,  # Remove title from here - we'll add it as an annotation
    showlegend=False, # Remove the legend
    polar=dict(
        radialaxis=dict(
            visible=False, # Remove radial labels
            range=[0, vtm[['moose_scaled', 'black_bear_scaled']].max().max() + 0.05] # Adjust range as needed
        ),
        angularaxis=dict(
            tickfont=dict(size=14, color='#999999'), # Make month labels larger
            rotation=120, # Rotate to start at the top
            direction='counterclockwise' # Set the direction to clockwise
        ),
        bgcolor='white'  # Remove gray background
    ),
    polar2=dict(
        radialaxis=dict(
            visible=False, # Remove radial labels
            range=[0, vtm[['moose_scaled', 'black_bear_scaled']].max().max() + 0.05] # Ensure both have the same scale
        ),
        angularaxis=dict(
            tickfont=dict(size=14, color='#999999'), # Make month labels larger
            rotation=120, # Rotate to start at the top
            direction='counterclockwise' # Set the direction to clockwise
        ),
        bgcolor='white'  # Remove gray background
    ),
    margin=dict(t=200, b=200, l=50, r=50), # Significantly increased top and bottom margins
    height=1000,  # Increased height to 1000px as suggested
    annotations=[
        # Main title - left aligned and higher
        dict(
            text="Who's Out and About? Tracking Vermont's Big Two by Month",
            showarrow=False,
            xref="paper", yref="paper",
            x=0.0, y=1.15, # Positioned higher
            xanchor="left",
            yanchor="top",
            font=dict(size=30, color="#003960"),
        ),
        # Subtitle - left aligned and higher
        dict(
            text="While moose are a year-round presence, black bears hibernate during the winter months",
            showarrow=False,
            xref="paper", yref="paper",
            x=0.0, y=1.08, # Positioned higher but below the main title
            xanchor="left",
            yanchor="top",
            font=dict(size=20, style="italic", color="#003960"),
        ),
        # Chart titles - positioned lower
        dict(
            text='<span style="color:#00441b">Moose (19,670 Observations)</span>',
            showarrow=False,
            xref="paper", yref="paper",
            x=0.05, y=-0.01, # Positioned lower
            font=dict(size=20),
        ),
        dict(
            text='<span style="color:#40004b">Black Bear (2,059 Observations)</span>',
            showarrow=False,
            xref="paper", yref="paper",
            x=0.95, y=-0.01, # Positioned lower
            font=dict(size=20),
        ),
        # Data source with larger font
        dict(
            text="Data Source: <a href='https://www.sciencebase.gov/catalog/item/663ce56cd34e77890839e1c8'>https://www.sciencebase.gov/catalog/item/663ce56cd34e77890839e1c8</a><br>Observations are from trail cameras located in Caledonia, Essex, and Orleans Counties, (2014-2022).",
            showarrow=False,
            xref="paper", yref="paper",
            x=0.5, y=-0.18, # Positioned lower
            font=dict(size=16, color="#003960"), # Increased from 10 to 14
        )
    ]
)

# Save the figure as an HTML file
fig.write_html("radial_charts.html")