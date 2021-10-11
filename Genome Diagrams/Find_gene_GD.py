# finding one gene in the E.coli genome
from Bio.SeqFeature import SeqFeature, FeatureLocation
from Bio import SeqIO
from Bio.Graphics import GenomeDiagram
from reportlab.lib.units import cm
from reportlab.lib import colors
import os
from tkinter.filedialog import askopenfilename

# working directory
os.getcwd()
os.chdir('C:\\Users\\Danie\\Documents\\GitHub\\Python\\Genome Diagrams') # if needed

# open your genbank file manuall if needed
#genome = askopenfilename()

# read gb file
GB = SeqIO.read('MG1655.gb', 'genbank')

# after loading in our sequence we next create an empty diagram,
# then add an (empty) track,
# and to that add an (empty) feature set:
gd_diagram = GenomeDiagram.Diagram("MG1655")
gd_track_for_features = gd_diagram.new_track(1, name="Annotated Features")
gd_feature_set = gd_track_for_features.new_set()
