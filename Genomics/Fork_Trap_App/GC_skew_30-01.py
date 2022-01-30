import io
import os
import subprocess  # to open the pdf after creating in automatically.
from datetime import datetime
import pandas as pd
import numpy as np
from tkinter.filedialog import askopenfilename
from reportlab.lib import colors
from reportlab.lib.units import cm
from Bio.Graphics import GenomeDiagram
import Bio
from Bio.SeqUtils import *
from Bio.SeqUtils import GC
from Bio import SeqIO
from Bio.SeqFeature import SeqFeature, FeatureLocation
import PySimpleGUI as sg

os.chdir('C:/Users/Danie/OneDrive/Documents/GitHub/termination/Genomes/Ecoli')
os.getcwd()
# load genome sequence
gen = SeqIO.read('MG1655.fasta', 'fasta')

# GC_skew
gc_data = Bio.SeqUtils.GC_skew(gen.seq, window=100)
gc = Bio.SeqUtils.GC(gen.seq)
gc

type(gc_data[1])
# Draw
diagram = GenomeDiagram.Diagram('MG1655 GC Skew')
features = diagram.new_track(1, greytrack=False)
set = features.new_set('graph')

feature_temp = []
for i in gc_data:
    x = SeqFeature(i)
    feature_temp.append(x)

set.add_feature(i)


graph1 = set.new_graph(data=gc_data)


# one line graphic, but python crashes when I run this after the image is generated, why?
Bio.SeqUtils.xGC_skew(gen.seq, window=20000)
