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
from Bio.SeqUtils import GC
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

Also someone elses project with good examples:
https://corytophanes.github.io/BIO_BIT_Bioinformatics_209/biopython-genomediagram.html
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
        set.add_feature(feature, name=ter_site.name, label=True, label_size=20,
                        label_position="end", sigil="ARROW", color=colour, arrowhead_length=1000)


####################
#    BLAST classes
####################

class BlastSite():
    def __init__(self, name, csv):
        self.csv = csv
        self.name = name
        self.start = int(csv.sstart)
        self.stop = int(csv.send)+1000
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
        self.site = site
        self.colour = colour
        feature = SeqFeature(FeatureLocation(
            site.start, site.stop), strand=site.strand)
        set.add_feature(feature, name=site.name, label=True, label_size=20,
                        label_position="end", color=colour)


####################
#    BT2 classes
####################


class XSite():
    def __init__(self, csv, name='X'):
        self.csv = csv

        # start
        start_list = []
        for i in csv.pos:
            start_list.append(int(i))
        self.start = start_list

        # wdith
        width_list = []
        for i in csv.qwidth:
            width_list.append(int(i))
        self.width = width_list

        # end
        end_list = []
        for i in csv.pos:
            end_temp = int(i) + 5000
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


class XToSet():
    def __init__(self, set, X_site, colour):
        self.set = set
        self.X_site = X_site
        self.colour = colour

# cannot find a for loop to add all features in one go, works when i subset one individual.
        feature_list = []
        for i in range(0, len(X_site.start)):
            feature = SeqFeature(FeatureLocation(
                X_site.start[i], X_site.stop[i]), strand=X_site.strand[i])
            feature_list.append(feature)

        for i in range(0, len(X_site.start)):
            set.add_feature(
                feature_list[i], name=X_site.name[i], label=False, color=colour, label_size=25)


# ________________________________________________________________________
# GUI
# ________________________________________________________________________
sg.theme('DarkBlue1')  # DarkGrey14, DarkGrey, Reddit, LightBlue, DarkBlue1
font = ('Calibri', 14)
font_heading = ('Calibri', 24)
font_small = ('Calibri', 12)

layout_text = [
    [sg.Text('Fork Trap App', font=font_heading)],
    [sg.Text('Select Genome (fasta): ', font=font)],
    [sg.Text('Ter csv: ', font=font)],
    [sg.Text('X csv: ', font=font)],
    [sg.Text('BLAST csv: ', font=font)],
    [sg.Text('Chromosome Shape: ', font=font)],
    [sg.Text('Select core size: ', font=font)],
    [sg.Text(' '*20)],
    [sg.Text('Save file as: ', font=font)],
    [sg.Text('Select directory to save image: ', font=font)]
]

layout_input = [
    [sg.Text(' '*20, font=font_heading)],
    [sg.FileBrowse(key='-genome1-')],
    [sg.FileBrowse(key='-ter_BT2_csv-')],
    [sg.FileBrowse(key='-X_csv-')],
    [sg.FileBrowse(key='-BLAST_csv-')],
    # [sg.Combo(['All', 'terA', 'terB', 'terC', 'terD', 'terE', 'terF', 'terG', 'terH', 'terI', 'terJ'],key = '-ter_input-')],
    [sg.Combo(['linear', 'cicular'], key='-chromosome_shape-',
              font=font, text_color='black')],
    [sg.InputText(key='-core_size-', font=font,
                  size=(0, 20), text_color='black')],
    [sg.Text(' '*20)],
    [sg.InputText(key='-image_name-', font=font,
                  size=(0, 20), text_color='black')],
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
            ter_csv = pd.read_csv('ter_MG1655.csv')
            #ter_csv = pd.read_csv(values['-ter_BT2_csv-'])
        except:
            sg.popup('Error with ter csv file...', font=font)
        try:
            X_csv = pd.read_csv('Rlooptracker_MG1655.csv')  # R-loops
            X2_csv = pd.read_csv('MG1655_G4s_command5.csv')  # G4s
            #X_csv = pd.read_csv(values['-X_csv-'])
        except:
            sg.popup('Error with other csv file...', font=font)
        try:
            BLAST_csv = pd.read_csv('MG1655_oriC_Blast.csv')
            #BLAST_csv = pd.read_csv(values['-BLAST_csv-'])
        except:
            sg.popup('Error with BLAST csv file...', font=font)
        try:
            fas = list(SeqIO.parse(open('MG1655.fasta'), 'fasta'))
            #fas = list(SeqIO.parse(open(values['-genome1-']), 'fasta'))
            sg.popup('Genome size: ' + str(len(fas[0])))

            # Other BT2
            try:
                # X from BT2
                X = XSite(X_csv)
                X2 = XSite(X2_csv)
            except:
                sg.popup('XSite class not working')

            # BLAST sites
            try:

                blast1 = BlastSite('oriC', BLAST_csv)
            except:
                sg.popup('BlastSite class not working')
            #
            #

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

            # ___________________
            # Genome Diagram using TerSite class
            # ___________________

            gd_diagram = GenomeDiagram.Diagram('MG1655')
            # Track 1
            gd_features1 = gd_diagram.new_track(1, greytrack=False)
            gd_set1 = gd_features1.new_set()
            # Track2
            gd_features2 = gd_diagram.new_track(2, greytrack=False)
            gd_set2 = gd_features2.new_set()

            # Add ter Sites
            TerToSet(gd_set1, terA, 'red')
            TerToSet(gd_set1, terB, 'blue')
            TerToSet(gd_set1, terC, 'purple')
            TerToSet(gd_set1, terD, 'green')
            TerToSet(gd_set1, terE, 'pink')
            TerToSet(gd_set1, terF, 'gray')
            TerToSet(gd_set1, terG, 'pink')
            TerToSet(gd_set1, terH, 'gray')
            TerToSet(gd_set1, terI, 'gray')
            TerToSet(gd_set1, terJ, 'gray')

            try:
                # From BT2 formated csvs
                XToSet(gd_set2, X, 'red')
                XToSet(gd_set2, X2, 'lightgreen')

            except:
                sg.popup('XToSet not working')
            try:
                # From BLAST App
                BlastToSet(gd_set1, blast1, 'black')
            except:
                sg.popup('BlastToSet not working')

        except:
            sg.popup('Something Went Wrong..', font=font)

        # Change directory to save in custom location
        if not values['-save_image-']:
            dir_path = os.path.dirname(os.path.realpath(__file__))
        else:
            dir_path = os.path.dirname(
                os.path.realpath(values['-save_image-']))
        os.chdir(dir_path)

        # Draw the actual image.
        gd_diagram.draw(format=values['-chromosome_shape-'],
                        start=0, end=len(fas[0]), circle_core=float(values['-core_size-']))

        if not values['-image_name-']:
            gd_diagram.write('output_'+day+'-'+month+'.pdf', 'pdf')
            gd_diagram.write('output_'+day+'-'+month+'.png', 'png')
        else:
            gd_diagram.write(values['-image_name-']+'.pdf', 'pdf')
            gd_diagram.write(values['-image_name-']+'.png', 'png')

        # opem the file we have just created.
        subprocess.Popen([values['-image_name-']+'.pdf'], shell=True)

# fragments=3, pagesize=(15*cm, 4*cm)
