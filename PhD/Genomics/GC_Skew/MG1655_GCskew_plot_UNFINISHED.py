from Bio import SeqIO
import pandas as pd
import csv
from reportlab.lib import colors
from reportlab.lib.units import cm
from Bio.Graphics import GenomeDiagram
from Bio.SeqUtils import GC
from Bio import SeqIO
from Bio.SeqFeature import SeqFeature, FeatureLocation


# Read in genome record
record = SeqIO.read("MG1655.fasta", "fasta")

# read in csv with pd
df = pd.read_csv('2023-10-18_MG1655_GCskew.csv')

#
df

# Create diagram
gd_diagram = GenomeDiagram.Diagram(record.id)

# Add feature track
feature_track = gd_diagram.new_track(1, greytrack=False)
feature_track.name = "Annotated Features"

# Add GC skew track
skew_track = gd_diagram.new_track(2, greytrack=False)
skew_track.name = "GC Skew"

# Create graph set
skew_graphset = skew_track.new_set(type="graph")

# Get GC skew data
gc_data = [(row['Index'], row['GC']) for i, row in df.iterrows()]
gc_data

# Add GC skew graph
graph = skew_graphset.new_graph(data=gc_data, name="GC Skew",
                                altcolor=colors.red,
                                center=0)
len(record)

gd_diagram.draw(format='circular', start=int(0), end=float(len(record)), circle_core=0.6)

'''
UNFINISHED
this is the furthest I MG1655_oriC_Blast
'''
