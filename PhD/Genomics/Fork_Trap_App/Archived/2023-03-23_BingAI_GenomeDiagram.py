from Bio import SeqIO
from reportlab.lib import colors
from reportlab.lib.units import cm
from Bio.Graphics import GenomeDiagram

# Read in reference genome fasta file
reference_genome = SeqIO.read("reference_genome.fasta", "fasta")

# Read in query fasta file with positional information
query = SeqIO.read("query.fasta", "fasta")
query_start = # start position of query on reference genome
query_end = # end position of query on reference genome

# Create GenomeDiagram object and add track and feature set
gd_diagram = GenomeDiagram.Diagram(reference_genome.id)
gd_track_for_features = gd_diagram.new_track(1, name="Annotated Features")
gd_feature_set = gd_track_for_features.new_set()

# Add arrow feature for query gene on reference genome
feature = SeqFeature(FeatureLocation(query_start, query_end), strand=1) # change strand to -1 if gene is on reverse strand
gd_feature_set.add_feature(feature, name=query.id, label=True,
                           label_size=14, label_angle=0,
                           color=colors.blue) # change color as desired

# Draw diagram to file
gd_diagram.draw(format="linear", pagesize=(25*cm, 10*cm), fragments=4,
                start=0, end=len(reference_genome))
gd_diagram.write("genome_map.png", "PNG")


'''
This code reads in a reference genome fasta file and a query fasta file with positional information. It then creates a GenomeDiagram object and adds a track and feature set. An arrow feature is added for the query gene on the reference genome using the positional information. The diagram is then drawn to a PNG file.
You can modify this code to add additional functionality such as allowing for multiple queries and custom colors for queried genes.
'''
