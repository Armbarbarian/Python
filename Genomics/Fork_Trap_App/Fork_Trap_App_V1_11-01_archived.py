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
import PySimpleGUI as sg

# set the date and time
now = datetime.now()
day = now.strftime("%d")
month = now.strftime("%m")

'''
Great tutorial on how to get started here:

https://biopython-tutorial.readthedocs.io/en/latest/notebooks/17%20-%20Graphics%20including%20GenomeDiagram.html
'''

# ________________________________________________________________________
# Back end code

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
'''
class BlastSite():
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


class BlastToSet():
    def __init__(self, set, site, colour):
        self.set = set
        self.sit = site
        self.colour = colour
        feature = SeqFeature(FeatureLocation(
            site.start, site.stop), strand=site.strand)
        set.add_feature(feature, name=site.name, label=True, label_size=25,
                        label_position="end", sigil="ARROW", color=colour, arrowhead_length=1000)
'''

# ________________________________________________________________________
# GUI
# ________________________________________________________________________
sg.theme('DarkGrey')  # DarkGrey14, DarkGrey, Reddit, LightBlue, DarkBlue1
font = ('Calibri', 14)
font_heading = ('Calibri', 24)
font_small = ('Calibri', 12)

layout_text = [
    [sg.Text('Fork Trap App', font=font_heading)],
    [sg.Text('Select Genome (fasta): ', font=font)],
    [sg.Text('Ter BT2 csv: ', font=font)],
    [sg.Text('BLAST csv: ', font=font)],
    [sg.Text('Chromosome Shape: ', font=font)],
    [sg.Text(' '*20)],
    [sg.Text('Save file as: ', font=font)],
    [sg.Text('Select directory to save image: ', font=font)]
]

layout_input = [
    [sg.Text(' '*20, font=font_heading)],
    [sg.FileBrowse(key='-genome1-')],
    [sg.FileBrowse(key='-BT2_csv-')],
    [sg.FileBrowse(key='-BLAST_csv-')],
    # [sg.Combo(['All', 'terA', 'terB', 'terC', 'terD', 'terE', 'terF', 'terG', 'terH', 'terI', 'terJ'],key = '-ter_input-')],
    [sg.Combo(['linear', 'cicular'], key='-chromosome_shape-', font=font)],
    [sg.Text(' '*20)],
    [sg.InputText(key='-image_name-', font=font)],
    [sg.FileBrowse(key='-save_image-')],
]

# layout pad pad=((0, 0), (40, 0)))

layout_cols = [
    [sg.Column(layout_text), sg.Column(layout_input)],
    [sg.Button('Run', font=font)]
]

window1 = sg.Window('Fork Trap App', layout_cols, resizable=True)
while True:
    event, values = window1.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Run':
        try:
            BLAST_csv = pd.read_csv(values['-BLAST_csv-'])
        except:
            pass
        try:
            ter_csv = pd.read_csv(values['-BT2_csv-'])
        except:
            sg.popup('Error with BT2 csv file...', font=font)
        try:
            fas = list(SeqIO.parse(open(values['-genome1-']), 'fasta'))
            sg.popup('Genome size: ' + str(len(fas[0])))
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

            # BLAST sites
            #
            #
            #

            # ___________________
            # Genome Diagram using TerSite class
            # ___________________
            gd_diagram = GenomeDiagram.Diagram('ter sites')
            gd_features1 = gd_diagram.new_track(1, greytrack=False)
            gd_set1 = gd_features1.new_set()
            #
            TerToSet(gd_set1, terA, 'red')
            TerToSet(gd_set1, terB, 'blue')
            TerToSet(gd_set1, terC, 'purple')
            TerToSet(gd_set1, terD, 'green')
            TerToSet(gd_set1, terE, 'gray')
            TerToSet(gd_set1, terF, 'gray')
            TerToSet(gd_set1, terG, 'gray')
            TerToSet(gd_set1, terH, 'gray')
            TerToSet(gd_set1, terI, 'gray')
            TerToSet(gd_set1, terJ, 'gray')
        except:
            sg.popup('Something Went Wrong..', font=font)
        # Change directory to save in custom location
        dir_path = os.path.dirname(os.path.realpath(values['-save_image-']))
        os.chdir(dir_path)
        # Draw the actual image.
        # Add the terA TerSite class information into the Track
        gd_diagram.draw(format=values['-chromosome_shape-'],
                        start=0, end=len(fas[0]), circle_core=0.8)

        if not values['-image_name-']:
            gd_diagram.write('output_'+day+'-'+month+'.pdf', 'pdf')
            gd_diagram.write('output_'+day+'-'+month+'.png', 'png')
        else:
            gd_diagram.write(values['-image_name-']+'.pdf', 'pdf')
            gd_diagram.write(values['-image_name-']+'.png', 'png')

# fragments=3, pagesize=(15*cm, 4*cm)
