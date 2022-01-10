# Using genome diagram to create circular images of features in a genbank file
# this script will position ter sites on a circular chromosome track
# the ter sites will be found and their position plotted

from Bio.SeqFeature import SeqFeature, FeatureLocation
from Bio import SeqIO
from Bio.Graphics import GenomeDiagram
from reportlab.lib.units import cm
from reportlab.lib import colors
from tkinter.filedialog import askopenfilename
import os


dir = askopenfilename()
dir_path = os.path.dirname(os.path.realpath(dir))
dir_path
os.chdir(dir_path)
os.getcwd()



# libraries

# read gb file
MG = SeqIO.read(filename, 'genbank')

# feature tracks
mg_diagram = GenomeDiagram.Diagram(MG.id)
mg_track_for_features = mg_diagram.new_track(1, name="Annotated Features")
mg_feature_set = mg_track_for_features.new_set()

# for loop to take out the genes frrom the gb file as features
# using the arrow sigil to show directionality
for feature in MG.features:
    if feature.type != "gene":
        # Exclude this feature
        continue
    if len(mg_feature_set) % 2 == 0:
        color = colors.blue
    else:
        color = colors.lightblue
    mg_feature_set.add_feature(
        feature, sigil="ARROW", color=color, label=True, label_size=1, label_angle=0
    )
for feature in MG.features:
    print(feature)
# I want to include some strandless features,
# ter sites
terA = 'aattagtatgttgtaactaaagt'
terB = 'aataagtatgttgtaactaaagt'
terC = 'atataggatgttgtaactaatat'
terD = 'cattagtatgttgtaactaaatg'
terE = 'ttaaagtatgttgtaactaagca'
terF = 'ccttcgtatgttgtaacgacgat'
terG = 'gtcaaggatgttgtaactaacca'
terH = 'cgatcgtatgttgtaactatctc'
terI = 'aacatggaagttgtaactaaccg'
terJ = 'acgcagtaagttgtaactaatgc'

for site, name, color in [
    (terA, "terA", colors.green),
    (terB, "terB", colors.orange),
    (terC, "terC", colors.red),
    (terD, "terD", colors.blue),
    (terE, "terE", colors.lightblue),
    (terF, "terF", colors.gray),
    (terG, "terG", colors.gray),
    (terH, "terH", colors.gray),
    (terI, "terI", colors.gray),
        (terJ, "terJ", colors.gray)]:
    index = 0
    while True:
        index = MG.seq.find(site, start=index)
        if index == -1:
            break
        feature = SeqFeature(FeatureLocation(index, index + len(site)))
        mg_feature_set.add_feature(
            feature,
            color=color,
            name=name,
            label=True,
            label_size=10,
            label_color=color,
        )
        index += len(site)

# linear
mg_diagram.draw(format="linear", pagesize='A4', fragments=4,
                start=0, end=len(MG))


# draw
'''mg_diagram.draw(
    format="circular",
    circular=True,
    pagesize=(20 * cm, 20 * cm),
    start=0,
    end=len(MG),
    circle_core=0.5,
)
'''
# write
mg_diagram.write("MG1655_circular_ter4.pdf", "PDF")
