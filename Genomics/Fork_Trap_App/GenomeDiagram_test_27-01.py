# set working directory as python scripts 
import os
os.getcwd()
os.chdir('C:\\Users\\Danie\\Documents\\R\\termination\\Python Scripts')

# libraries
from reportlab.lib import colors
from reportlab.lib.units import cm
from Bio.Graphics import GenomeDiagram
from Bio import SeqIO

##########################################################################
#
#                 Basic example from Biopython CookBook
# https://biopython.org/DIST/docs/tutorial/Tutorial.html#sec336
#
##########################################################################


# read in the genbank file
## Plasmid from Y. pestis
record = SeqIO.read("NC_005816.gb", "genbank")

# after loading in our sequence we next create an empty diagram, 
# then add an (empty) track, 
# and to that add an (empty) feature set:
gd_diagram = GenomeDiagram.Diagram("Yersinia pestis biovar Microtus plasmid pPCP1")
gd_track_for_features = gd_diagram.new_track(1, name="Annotated Features")
gd_feature_set = gd_track_for_features.new_set()

# Now the fun part - we take each gene SeqFeature object in our SeqRecord,
# and use it to generate a feature on the diagram. We’re going to color them blue,
# alternating between a dark blue and a light blue.
for feature in record.features:
    if feature.type != "gene":
        # Exclude this feature
        continue
    if len(gd_feature_set) % 2 == 0:
        color = colors.blue
    else:
        color = colors.lightblue
    gd_feature_set.add_feature(feature, color=color, label=True)

# Now we come to actually making the output file
# This happens in two steps, first we call the draw method,
# which creates all the shapes using ReportLab objects.
# Then we call the write method which renders these to the requested file format. 
# Note you can output in multiple file formats:
# draw:
gd_diagram.draw(
    format="linear",
    orientation="landscape",
    pagesize="A4",
    fragments=4,
    start=0,
    end=len(record),
)

# write:
gd_diagram.write("plasmid_linear.pdf", "PDF")
gd_diagram.write("plasmid_linear.eps", "EPS")
gd_diagram.write("plasmid_linear.svg", "SVG")


# Provided you have the dependencies installed, you can also do bitmaps
#for example:
gd_diagram.write("plasmid_linear.png", "PNG")


# Notice that the fragments argument which we set to four controls how many pieces the genome gets broken up into.


# If you want to do a circular figure, then try this:
gd_diagram.draw(
    format="circular",
    circular=True,
    pagesize=(20 * cm, 20 * cm),
    start=0,
    end=len(record),
    circle_core=0.7,
)
gd_diagram.write("plasmid_circular.pdf", "PDF")



##########################################################################
#                       Using E.coli genbank file
##########################################################################

#####################
# Bottom up approach
#####################

#read gb file
MG = SeqIO.read('MG1655.gb', 'genbank')

# for loop
# Now the fun part - we take each gene SeqFeature object in our SeqRecord,
# and use it to generate a feature on the diagram. We’re going to color them blue,
# alternating between a dark blue and a light blue.
for feature in MG.features:
    if feature.type != "gene":
        # Exclude this feature
        continue
    if len(mg_feature_set) % 2 == 0:
        color = colors.blue
    else:
        color = colors.lightblue
    mg_feature_set.add_feature(feature, color=color, label=True)


# after loading in our sequence we next create an empty diagram, 
# then add an (empty) track, 
# and to that add an (empty) feature set:

# Create a track, and a diagram
mg_track_for_features = GenomeDiagram.Track(name="Annotated Features")
mg_diagram = GenomeDiagram.Diagram("MG1655 complete chromosome")

# Now have to glue the bits together...
mg_track_for_features.add_set(mg_feature_set)
mg_diagram.add_track(mg_track_for_features, 1)

# draw
# Now we come to actually making the output file
# This happens in two steps, first we call the draw method,
# which creates all the shapes using ReportLab objects.
# Then we call the write method which renders these to the requested file format. 
# Note you can output in multiple file formats:
# draw:
mg_diagram.draw(
    format="circular",
    circular=True,
    pagesize=(20 * cm, 20 * cm),
    start=0,
    end=len(record),
    circle_core=0.7,
)

# write
mg_diagram.write("MG1655_circular5.pdf", "PDF")



#################################################################
#                       A nice example
#################################################################

#Now let’s return to the pPCP1 plasmid from Yersinia pestis biovar Microtus, and the top down approach used in Section 17.1.3, but take advantage of the sigil options we’ve now discussed. This time we’ll use arrows for the genes, and overlay them with strand-less features (as plain boxes) showing the position of some restriction digest sites.

from reportlab.lib import colors
from reportlab.lib.units import cm
from Bio.Graphics import GenomeDiagram
from Bio import SeqIO
from Bio.SeqFeature import SeqFeature, FeatureLocation

record = SeqIO.read("NC_005816.gb", "genbank")

gd_diagram = GenomeDiagram.Diagram(record.id)
gd_track_for_features = gd_diagram.new_track(1, name="Annotated Features")
gd_feature_set = gd_track_for_features.new_set()

for feature in record.features:
    if feature.type != "gene":
        # Exclude this feature
        continue
    if len(gd_feature_set) % 2 == 0:
        color = colors.blue
    else:
        color = colors.lightblue
    gd_feature_set.add_feature(
        feature, sigil="ARROW", color=color, label=True, label_size=14, label_angle=0
    )

# I want to include some strandless features, so for an example
# will use EcoRI recognition sites etc.
for site, name, color in [
    ("GAATTC", "EcoRI", colors.green),
    ("CCCGGG", "SmaI", colors.orange),
    ("AAGCTT", "HindIII", colors.red),
    ("GGATCC", "BamHI", colors.purple),
]:
    index = 0
    while True:
        index = record.seq.find(site, start=index)
        if index == -1:
            break
        feature = SeqFeature(FeatureLocation(index, index + len(site)))
        gd_feature_set.add_feature(
            feature,
            color=color,
            name=name,
            label=True,
            label_size=10,
            label_color=color,
        )
        index += len(site)

gd_diagram.draw(format="linear", pagesize="A4", fragments=4, start=0, end=len(record))
gd_diagram.write("plasmid_linear_nice.pdf", "PDF")
gd_diagram.write("plasmid_linear_nice.eps", "EPS")
gd_diagram.write("plasmid_linear_nice.svg", "SVG")

gd_diagram.draw(
    format="circular",
    circular=True,
    pagesize=(20 * cm, 20 * cm),
    start=0,
    end=len(record),
    circle_core=0.5,
)
gd_diagram.write("plasmid_circular_nice.pdf", "PDF")
gd_diagram.write("plasmid_circular_nice.eps", "EPS")
gd_diagram.write("plasmid_circular_nice.svg", "SVG")
















