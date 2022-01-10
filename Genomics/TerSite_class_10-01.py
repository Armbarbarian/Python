import pandas as
from tkinter.filedialog import askopenfilename
from reportlab.lib import colors
from reportlab.lib.units import cm
from Bio.Graphics import GenomeDiagram
from Bio import SeqIO
from Bio.SeqFeature import SeqFeature, FeatureLocation

'''
Great tutorial on how to get started here:

https://biopython-tutorial.readthedocs.io/en/latest/notebooks/17%20-%20Graphics%20including%20GenomeDiagram.html
'''


MG_fas = list(SeqIO.parse(open('MG1655.fasta'), 'fasta'))
len(MG_fas[0])

MG_ter_csv = pd.read_csv('ter_MG1655.csv')
MG_ter_csv
terA_pos = int(MG_ter_csv[MG_ter_csv.qname == 'terA'].pos)


class TerSite():
    def __init__(self, name, csv):
        self.name = name
        self.start = int(csv[csv.qname == name].pos)
        self.stop = int(csv[csv.qname == name].pos)+23
        self.strand = csv[csv.qname == name].strand
        self.seq = csv[csv.qname == name].seq
        self.csv = csv[csv.qname == name]


# create TerSites
terA = TerSite('terA', MG_ter_csv)
terB = TerSite('terB', MG_ter_csv)
terC = TerSite('terC', MG_ter_csv)

# ___________________
# Genome Diagram using TerSite class
# ___________________
gd_diagram = GenomeDiagram.Diagram('MG1655 ter sites')
gd_features1 = gd_diagram.new_track(1, greytrack=False)
gd_set1 = gd_features1.new_set()
#

# Add the terA TerSite class information into the Track
# No GB file needed!
terA_feat = SeqFeature(FeatureLocation(terA.start, terA.stop), strand=-1)
gd_set1.add_feature(terA_feat, name=terA.name, label=True,
                    label_size=25, sigil="ARROW")
terB_feat = SeqFeature(FeatureLocation(terB.start, terB.stop), strand=+1)
gd_set1.add_feature(terB_feat, name=terB.name, label=True, label_size=25)
terC_feat = SeqFeature(FeatureLocation(terC.start, terC.stop), strand=+1)
gd_set1.add_feature(terC_feat, name=terC.name, label=True, label_size=25)

gd_diagram.draw(format='circular', start=0, end=len(MG_fas[0]))
gd_diagram.write('MG1655_cicular_terABC_10-01.png', 'png')

# fragments=3, pagesize=(15*cm, 4*cm)
