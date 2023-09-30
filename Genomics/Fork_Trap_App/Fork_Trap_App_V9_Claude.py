import Bio.Graphics
from Bio.Graphics import GenomeDiagram
from Bio.SeqFeature import SeqFeature, FeatureLocation
import io
import os
import subprocess  # to open the pdf after creating in automatically.
from datetime import datetime
import pandas as pd
import numpy as np
from reportlab.lib import colors
from reportlab.lib.units import cm
from Bio.Graphics import GenomeDiagram
from Bio.SeqUtils import GC
from Bio import SeqIO
from Bio.SeqFeature import SeqFeature, FeatureLocation



####################
#    Ter classes
####################


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

# set up my own class to make it eaaier to add features to set


class TerToSet():
    def __init__(self, set, ter_site, colour):
        self.set = set
        self.ter_site = ter_site
        self.colour = colour
        feature = SeqFeature(FeatureLocation(
            ter_site.start, ter_site.stop), strand=ter_site.strand)
        set.add_feature(feature, name=ter_site.name, label=True, label_size=25,
                        label_position="end", sigil="ARROW", color=colour, arrowhead_length=1000)


####################
#    BLAST classes
####################

class BlastSite():
    def __init__(self, csv):
        self.csv = csv
        name_list = []
        for i in csv.qseqid:
            name_list.append(i)
        self.name = name_list
        self.start = int(csv.sstart)
        self.stop = int(csv.send)
        self.strand_pos = csv.sstrand.to_list()[0]
        self.seq = csv.sseq

        if self.strand_pos == 'NA':
            self.strand = +1
        if self.strand_pos == 'plus':
            self.strand = +1
        if self.strand_pos == 'minus':
            self.strand = -1


class BlastToSet():
    def __init__(self, set, site, colour):
        self.set = set
        set_list = []
        for i in range(0, len(site.qseqid)):
            feature = SeqFeature(FeatureLocation(
                site.start[i], site.stop[i]), strand=site.strand[i])
            set_list.append(feature)
        self.site = site
        self.colour = colour
        feature = SeqFeature(FeatureLocation(
            site.start, site.stop), strand=site.strand)
        set.add_feature(feature, name=site.name, label=True, label_size=25,
                        label_position="end", color=colour)


####################
#    BT2 classes
####################


class ChiSite():
    def __init__(self, csv, name='chi'):
        self.csv = csv
        # start
        start_list = []
        for i in csv.pos:
            start_list.append(int(i))
        self.start = start_list
        # end
        end_list = []
        for i in csv.pos:
            end_temp = int(i) + 8
            end_list.append(end_temp)
        self.stop = end_list

        strand_list = []
        for i in csv.strand:
            # strand_pos = i.tolist()[0]
            # self.csv = csv[csv.qname == name]
            if i == '-':
                strand_list.append(-1)
            if i == '+':
                strand_list.append(1)
        self.strand = strand_list

        name_list = []
        for i in csv.qname:
            name_list.append(i)
        self.name = name_list


class ChiToSet():
    def __init__(self, set, chi_site, colour):
        self.set = set
        self.chi_site = chi_site
        self.colour = colour

# cannot find a for loop to add all features in one go, works when i subset one individual.
        feature_list = []
        for i in range(0, len(chi_site.start)):
            feature = SeqFeature(FeatureLocation(
                chi_site.start[i], chi_site.stop[i]), strand=chi_site.strand[i])
            feature_list.append(feature)

        for i in range(0, len(chi_site.start)):
            set.add_feature(
                feature_list[i], name=chi_site.name[i], label=False, color=colour, label_size=25)



# Read in genome sequence
genome_record = SeqIO.read("MG1655.fasta", "fasta")
ter_csv = pd.read_csv('ter_MG1655.csv')
chi_csv = pd.read_csv('Chi_MG1655.csv')
chi_csv

# ___________________
# Genome Diagram using TerSite class
# ___________________
gd_diagram = GenomeDiagram.Diagram('Chromosome Map')
gd_features1 = gd_diagram.new_track(1, greytrack=False)
gd_set1 = gd_features1.new_set()
# gd_set2 = gd_features1.new_set('other')

# create Sites
# Ter specific sites
terA = TerSite('terA', ter_csv)
terB = TerSite('terB', ter_csv)
terC = TerSite('terC', ter_csv)
terD = TerSite('terD', ter_csv)
terE = TerSite('terE', ter_csv)
terF = TerSite('terF', ter_csv)
terG = TerSite('terG', ter_csv)
terH = TerSite('terH', ter_csv)
terI = TerSite('terI', ter_csv)
terJ = TerSite('terJ', ter_csv)

# Chi sites
ChiToSet(gd_set1, chi_csv, 'lightblue')



# Add features like ter sites, chi sites, etc based on input csv data
# For example ter sites:
for ter_site in ter_csv:
    feature = SeqFeature(FeatureLocation(ter_site['start'], ter_site['end']),
                        strand=ter_site['strand'])
    gd_feature_set.add_feature(feature, name=ter_site['name'],
                               color=ter_site['color'])

# Draw and save image
gd_diagram.draw(circle_core=0.5)
gd_diagram.write('output.png', 'png')
