import os
import io
from Bio import SeqIO
from Bio.Seq import Seq
import pandas as pd
import numpy as np
from datetime import datetime
import PySimpleGUI as sg


'''
- Could I quantify the similarity of the ter sites themselves, then quantify the similarity of the extended regions to give us a value that might show the ter sites are 'more conserved' compared with their extended regions.
- OMGenomics has a bit about this using edit distance.
- If I get a return value of the edit distance between ter sites, say 22 in a comparison with only one SNP, I can calculate that there is a 95.6% similarity.
- Then I concatenate 10 bases either side of the ter site (slice it out effectively) leaving a 20 base string. Perform the same analysis and compare what I see. If there is a drastically reduced similarity then the ter site itself is more conserved.
'''

# specify MG1655 ter sites
terA = Seq('AATTAGTATGTTGTAACTAAAGT')
terB = Seq('AATAAGTATGTTGTAACTAAAGT')
terC = Seq('ATATAGGATGTTGTAACTAATAT')
terD = Seq('CATTAGTATGTTGTAACTAAATG')
terE = Seq('TTAAAGTATGTTGTAACTAAGCA')
terF = Seq('CCTTCGTATGTTGTAACGACGAT')
terG = Seq('GTCAAGGATGTTGTAACTAACCA')
terH = Seq('CGATCGTATGTTGTAACTATCTC')
terI = Seq('AACATGGAAGTTGTAACTAACCG')
terJ = Seq('ACGCAGTAAGTTGTAACTAATGC')


# Given two strings s and t, calculate the edit distance
# this is a dynamic programming approach that other bioinformaticians would be happy with.
# from GitHub copilot OMGenomics example
'''
This can work where s and t are different lengths
May be better to use hamming_distance() if the strings are the same length.
'''


def edit_distance(s, t):
    d = [[0 for j in range(len(t)+1)] for i in range(len(s)+1)]
    for i in range(1, len(s)+1):
        d[i][0] = i
    for j in range(1, len(t)+1):
        d[0][j] = j
    for i in range(1, len(s)+1):
        for j in range(1, len(t)+1):
            if s[i-1] == t[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                d[i][j] = 1 + min(d[i-1][j], d[i][j-1], d[i-1][j-1])
    return d[len(s)][len(t)]


edit_distance('PLEASANTLY', 'MEANLY')


# edit distance on ter sites from MG1655
edit_distance(str(terA), str(terB))  # 1
edit_distance(str(terA), str(terE))  # 7


# Hamming distance
'''
This requires the same string length fro both s and t
'''


def hamming_distance(s, t):
    return sum(1 for i in range(len(s)) if s[i] != t[i])


hamming_distance(str(terA), str(terB))


####################################################################
#
#           compare two ter sites from different genomes
#
####################################################################
os.chdir('C:\\Users\\Danie\\Documents\\Python1\\Python\\Genomics\\Extended_ter_analysis')


# read in the csv files with their sequence from bowtie2 in R
MG1655 = pd.read_csv('MG1655.csv')
BW2952 = pd.read_csv('BW2952.csv')
REL606 = pd.read_csv('REL606.csv')

# B1
APEC078 = pd.read_csv('APEC078.csv')
IAI1 = pd.read_csv('IAI1.csv')
E11368 = pd.read_csv('E11368.csv')

# B2
S88 = pd.read_csv('S88.csv')
UTI89 = pd.read_csv('UTI89.csv')
E2348 = pd.read_csv('E2348.csv')

# D
IAI39 = pd.read_csv('IAI39.csv')
SMS35 = pd.read_csv('SMS35.csv')
UMN026 = pd.read_csv('UMN026.csv')
CE10 = pd.read_csv('CE10.csv')
D042 = pd.read_csv('D042.csv')

# E
TW14359 = pd.read_csv('TW14359.csv')
Sakai = pd.read_csv('Sakai.csv')
EDL933 = pd.read_csv('EDL933.csv')

# two dustantly related genomes, one pathogenic and one comensal
MG1655
Sakai

# terA analysis
MG_terA = MG1655[(MG1655.qname == 'terA')].seq
Sakai_terA = Sakai[(Sakai.qname == 'terA')].seq
edit_distance(str(MG_terA), str(Sakai_terA))  # 1


# read in extended ter nt csv from R bt2 program
Ecoli_exTer = pd.read_csv('Ecoli_extended_ter_26-10.csv')
MG1655_ter = Ecoli_exTer[Ecoli_exTer.rname == 'MG1655']
Sakai_ter = Ecoli_exTer[Ecoli_exTer.rname == 'Sakai']

# terA extended analysis
MG_terAx = MG1655_ter[MG1655_ter.qname == 'terA'].seq
Sakai_terAx = Sakai_ter[Sakai_ter.qname == 'terA'].seq
edit_distance(str(MG_terAx), str(Sakai_terAx))  # 5

# analyse the dataframes directly instead of writing them manually
my_dict = {'MG1655': [], 'Sakai': []}

for seq1 in MG1655_ter.seq:
    my_dict['MG1655'].append(seq1)
for seq2 in Sakai_ter.seq:
    my_dict['Sakai'].append(seq2)
my_df = pd.DataFrame(my_dict)
my_df[0:1]


# using hamming_distance instead of edit_distance
# terA analysis
MG_terA = MG1655[(MG1655.qname == 'terA')].seq
Sakai_terA = Sakai[(Sakai.qname == 'terA')].seq
hamming_distance(str(MG_terA), str(Sakai_terA))  # 1
# terA extended analysis
MG_terAx = MG1655_ter[MG1655_ter.qname == 'terA'].seq
Sakai_terAx = Sakai_ter[Sakai_ter.qname == 'terA'].seq
hamming_distance(str(MG_terAx), str(Sakai_terAx))  # 66
[MG_terAx]


# next put these results into another table, sort of like a distance matrix / array


# checking where the ter site is located inside the extended string
len(my_df.MG1655[0][48:])


#_____________________________________________________________________________________________________________________________
#                                                   GUI for Edit vs Hamming Distance
#_____________________________________________________________________________________________________________________________

# add window colour
# 'DarkTeal9', 'DarkGrey14', 'LightBlue2', 'LightBlue8'
sg.theme('LightBlue2')

font = ('Calibri', 14)
font_small = ('Calibri', 12)


# clear function paired with clear button
def clear_input():
    for key in checked:
        window[key]('')
    return None



# Layout for window
Layout1 = [
    [sg.Text('Edit and Hamming Distance of FASTA sequences', font=font)]
]

# set up the window and the layout to use for the window
window = sg.Window('Viable Titre GUI', layout1)  # size=(600, 450)



while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        close_popup = sg.popup_yes_no('Have you saved your work?', font=font)
        if close_popup == 'No':
            continue
        else:
            break
    if event == 'Clear':
        clear_input()
