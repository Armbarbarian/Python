# finding one gene in the E.coli genome
from Bio.SeqFeature import SeqFeature, FeatureLocation
from Bio import SeqIO
from Bio.Seq import Seq
from Bio import pairwise2
from Bio.Graphics import GenomeDiagram
from reportlab.lib.units import cm
from reportlab.lib import colors
import os
from tkinter.filedialog import askopenfilename

# working directory
os.getcwd()
# os.chdir() # if needed

# open your genbank file manuall if needed
#genome = askopenfilename()

# read fasta of MG1655
with open('MG1655.fasta') as fas:
    for genome in SeqIO.parse(fas, 'fasta'):
        print(genome.id)
        print(len(genome))
        sequence1 = genome.seq
len(sequence1)

# read fasta of all E.coli genomes
with open('Ecoli_genomes.fasta') as all_fas:
    for genome in SeqIO.parse(all_fas, 'fasta'):
        print(genome.id)
        print(len(genome))
        print(repr(genome.seq))

##################################
#       Align a ter site
##################################
terA = Seq('AATTAGTATGTTGTAACTAAAGT')
subject = Seq('GGGGGGGAATTAGTATGTTGTAACTAAAGTGGGGGGG')

alignment1 = pairwise2.align.localds(terA, subject)

# after loading in our sequence we next create an empty diagram,
# then add an (empty) track,
# and to that add an (empty) feature set:
gd_diagram = GenomeDiagram.Diagram("MG1655")
gd_track_for_features = gd_diagram.new_track(1, name="Annotated Features")
gd_feature_set = gd_track_for_features.new_set()
