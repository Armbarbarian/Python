import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from Bio.SeqUtils import GC
from Bio import SeqIO
import numpy as np

# Read in genome record
record = SeqIO.read("Bsub_168.fasta", "fasta")

# Load GC data into dataframe
df = pd.read_csv('2023-10-25_Bsub_168_GCskew.csv')

# Calculate angle values for dataframe index
df['Angle'] = df['Index'] / len(record) * 2 * np.pi

# Calculate cumulative GC skew
df['Cumulative'] = df['GC']

# Create a new column for hue
df['Sign'] = np.sign(df['Cumulative']).map({-1: 'Negative', 1: 'Positive'})

# Create a copy of the dataframe
df_copy = df.copy()

# Add 0.1 to the Cumulative column for negative values
df_copy.loc[df_copy['Cumulative'] < 0, 'Cumulative'] -= -0.05

# Create plot
fig, ax = plt.subplots(figsize=(5, 5), dpi=150, subplot_kw={'projection': 'polar'}, facecolor='white')


'''# Split data into negative and positive subsets
df_neg = df.query('Cumulative < 0')
df_pos = df.query('Cumulative > 0')

# Plot smoothed cumulative GC against angle with different colors for each subset
sns.lineplot(x='Angle', y='Cumulative', data=df_neg, color='purple')
sns.lineplot(x='Angle', y='Cumulative', data=df_pos, color='green')

'''
# Plot smoothed cumulative GC against angle with different colors for each sign
# Drop the 'hue' argument for only one line, not two
'''
sns.lineplot(x='Angle', y='Cumulative', data=df_copy, color='purple') # Use for one line plot
'''
sns.lineplot(x='Angle', y='Cumulative', data=df_copy, palette=['green', 'purple'],
             hue_order=['Positive', 'Negative'], hue='Sign')

# Set plot title and remove axes
ax.set_title('B.subtilis 168 GC Skew', size=20)
ax.set_rticks([])
ax.set_rlabel_position(0)
ax.set_ylim(-1, 0.3)  # change last value to move GC skew lower or higher
ax.grid(False)
# Remove the legend
ax.legend_.remove()

# new line to change grids
# View
plt.show()

# Save figure
#plt.savefig('2023-10-18_MG1655_GCskew_PurpleGreen_seaborn.png', bbox_inches='tight')
