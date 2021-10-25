# BLAST in Python

import os
import subprocess
from Bio.Blast.Applications import NcbiblastnCommandline
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Blast import NCBIXML

# get current dir
os.getcwd()

# Subject genome to search
# wild type in this case
with open('MG1655.fasta') as fas:
    for genome in SeqIO.parse(fas, 'fasta'):
        print(genome.id)
        print(len(genome))
        sequence1 = genome.seq

# ter site objects
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
terA

# Build a database using command line from python
subprocess.call(["date"])


# blastn
blastx_cline = NcbiblastnCommandline(query=terA, db=genome, evalue=0.001, outfmt=10, out='C:\\Users\\Danie\\Documents\\Python1\\Python\\Genomics\\BLAST_results\\test.csv')

blastx_cline

for record in blast_result:
    print(record)






#____________________________________________________________________________________________________________________

# other local alignments

# read in the 'gene' fasta
with open('MG1655.fasta') as MG1655_fas:
    for genome in SeqIO.parse(MG1655_fas, 'fasta'):
        MG1655_seq = genome.seq
len(MG1655_seq) # works


# pairwise2
# find terA within MG1655
# VERY SLOW python has difficulties here even locating one ter site
from Bio import Align, AlignIO
from Bio import pairwise2
from Bio.pairwise2 import format_alignment
from Bio import SeqIO
from Bio.Align import substitution_matrices
blosum62 = substitution_matrices.load("BLOSUM62")

# set the aligner
aligner = Align.PairwiseAligner()
aligner.open_gap_score = -10
aligner.extend_gap_score = -1
aligner.substitution_matrix = substitution_matrices.load("BLOSUM62")
aligner.mode = 'local'
seq1 = terB
seq2 = MG1655_seq
score = aligner.score(seq1, seq2)
alignments_terA = aligner.align(seq1, seq2)
len(alignments_terA)
type(alignments_terA)
alignments_terA.format('sam')


# try writing to a file
try:
    SeqIO.write(alignments_terA, "alignments_terA.fasta", 'fasta')
except:
    print('not working')





#________________________________________________________________________
# Blast over the web
from Bio.Blast import NCBIWWW
result_handle
