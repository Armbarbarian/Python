import pycircos
import matplotlib.pyplot as plt
from Bio import SeqIO
Garc = pycircos.Garc
Gcircle = pycircos.Gcircle

# Read in genome record
record = SeqIO.read("MG1655.fasta", "fasta")

# Create Gcircle object
circle = pycircos.Gcircle(figsize=(8, 8))

# Create Garc object for genome
genome = pycircos.Garc(arc_id="genome", interspace=0, raxis_range=(935, 985), labelposition=80, label_visible=True)

# Add genome to circle
circle.add_garc(genome)

# Set garcs position
circle.set_garcs(-65, 245)

# Add ticks for genome
circle.tickplot("genome", raxis_range=(985, 1000), tickinterval=20000000, ticklabels=None)

# Create Garc object for GC values
gc = pycircos.Garc(arc_id="gc", interspace=0, raxis_range=(900, 930), labelposition=80, label_visible=True)

# Add GC values to gc using line plot
gc.lineplot(record.seq, window_size=1000)

# Add gc to circle
circle.add_garc(gc)

# Show and save figure
plt.show()
circle.figure.savefig("MG1655_GC_circos.png", bbox_inches="tight")
