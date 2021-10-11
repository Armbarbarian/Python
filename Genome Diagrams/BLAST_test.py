# BLAST in Python

import os
from Bio.Blast.Applications import NcbiblastnCommandline
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Blast import NCBIXML


os.getcwd()

# SUbject genome to search
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

# blastn
blastx_cline = NcbiblastnCommandline(query=terA, db=genome, evalue=0.001, outfmt=5, out='C:\\Users\\Danie\\Documents\\Python1\\Python\\Genome Diagrams\\test.xml')

blastx_cline

for record in blast_result:
    print(record)
