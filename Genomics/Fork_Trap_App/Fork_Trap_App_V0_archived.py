import io
import os
from datetime import datetime
import pandas as pd
import numpy as np
from tkinter.filedialog import askopenfilename
from reportlab.lib import colors
from reportlab.lib.units import cm
from Bio.Graphics import GenomeDiagram
from Bio import SeqIO
from Bio.SeqFeature import SeqFeature, FeatureLocation

# set the date and time
now = datetime.now()
day = now.strftime("%d")
month = now.strftime("%m")

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
        self.stop = int(csv[csv.qname == name].pos)+20000
        self.strand_pos = csv[csv.qname == name].strand.tolist()[0]
        self.seq = csv[csv.qname == name].seq
        self.csv = csv[csv.qname == name]
        if self.strand_pos == '-':
            self.strand = +1
        if self.strand_pos == '+':
            self.strand = -1



# create TerSites
terA = TerSite('terA', MG_ter_csv)
terB = TerSite('terB', MG_ter_csv)
terC = TerSite('terC', MG_ter_csv)
terD = TerSite('terD', MG_ter_csv)
terE = TerSite('terE', MG_ter_csv)
terF = TerSite('terF', MG_ter_csv)
terG = TerSite('terG', MG_ter_csv)
terH = TerSite('terH', MG_ter_csv)
terI = TerSite('terI', MG_ter_csv)
terJ = TerSite('terJ', MG_ter_csv)


# ___________________
# Genome Diagram using TerSite class
# ___________________
gd_diagram = GenomeDiagram.Diagram('MG1655 ter sites')
gd_features1 = gd_diagram.new_track(1, greytrack=False)
gd_set1 = gd_features1.new_set()
#

# set up my own class to make it eaaier to add features to set
class FeatureToSet():
    def __init__(self, set, ter_site, colour):
        self.set = set
        self.ter_site = ter_site
        self.colour = colour
        feature = SeqFeature(FeatureLocation(ter_site.start, ter_site.stop), strand=ter_site.strand)
        set.add_feature(feature, name=ter_site.name, label=True, label_size=25, label_position="end", sigil="ARROW", color=colour, arrowhead_length=1000)


FeatureToSet(gd_set1, terA, 'red')
FeatureToSet(gd_set1, terB, 'blue')
FeatureToSet(gd_set1, terC, 'purple')
FeatureToSet(gd_set1, terD, 'green')
FeatureToSet(gd_set1, terE, 'gray')
FeatureToSet(gd_set1, terF, 'gray')
FeatureToSet(gd_set1, terG, 'gray')
FeatureToSet(gd_set1, terH, 'gray')
FeatureToSet(gd_set1, terI, 'gray')
FeatureToSet(gd_set1, terJ, 'gray')


# Add the terA TerSite class information into the Track

gd_diagram.draw(format='circular', start=0, end=len(MG_fas[0]), circle_core = 0.8)
gd_diagram.write('output_'+day+'-'+month+'.pdf', 'pdf')

# fragments=3, pagesize=(15*cm, 4*cm)
