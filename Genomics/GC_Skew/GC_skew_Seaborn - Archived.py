import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from Bio.SeqUtils import GC
from Bio import SeqIO
import numpy as np

'''
New code to act more like GC Skew instead of
using GenomeDiagram or circos

'''


# Read in genome record
record = SeqIO.read("MG1655.fasta", "fasta")

# Load GC data into dataframe
df = pd.read_csv('2023-10-18_MG1655_GCskew.csv')

# Calculate angle values for dataframe index
df['Angle'] = df['Index'] / len(record) * 2 * np.pi

# Calculate cumulative GC skew
df['Cumulative'] = df['GC']

# Create plot
fig, ax = plt.subplots(figsize=(5, 5), dpi=150, subplot_kw={'projection': 'polar'}, facecolor='white')

# Plot smoothed cumulative GC against angle
#sns.lineplot(x='Angle', y='Cumulative', data=df, color='blue')


# Split data into negative and positive subsets
df_neg = df.query('Cumulative < 0')
df_pos = df.query('Cumulative > 0')

# Plot smoothed cumulative GC against angle with different colors for each subset
sns.lineplot(x='Angle', y='Cumulative', data=df_neg, color='purple')
sns.lineplot(x='Angle', y='Cumulative', data=df_pos, color='green')

'''# Add shaded regions for Ori and Ter
ax.axvspan(0, np.pi/2, color='blue', alpha=0.1)
ax.axvspan(np.pi, 3*np.pi/2, color='red', alpha=0.1)'''

# Set plot title and remove axes
ax.set_title('MG1655 GC Skew', size=20)
ax.set_rticks([])
ax.set_rlabel_position(0)
ax.set_ylim(-1, 0.2)
ax.grid(False)

# new line to change grids


# View
plt.show()

# Save figure
#plt.savefig('2023-10-18_MG1655_GCskew_PurpleGreen_seaborn.png', bbox_inches='tight')
