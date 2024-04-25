import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from Bio.Seq import Seq
from Bio import SeqIO
from Bio.SeqUtils import GC
import Bio.AlignIO




# list and for loop
mylist = ['R', 'Python']

for m in mylist:
  print(m+' is awesome')

# updating a for loop to return a multiplication
my_num = [5, 6, 7, 8, 9, 10]


for num in my_num:
  print(num*10)


# load a dataset from seaborn
tips = sns.load_dataset("tips")

#  scatterplot from the tips dataset
sns.scatterplot(x = tips['total_bill'], y = tips['tip'], hue  = tips['day'])
plt.show()


# reading Ecoli Fasta files
# this for loop is a quick way to read in the ecoli genomes fasta files
## then print out the strain and the length of the genome
### This is good for quickly looking at what you have
for seq_record in SeqIO.parse('C:\\Users\\Danie\\Documents\\R\\termination\\Ecoli_genomes.fasta', 'fasta'):
  print(seq_record.id)
  print(len(seq_record))
  #print(repr(seq_record.seq)) # this takes a lot of time and not needed

# turning the genome in seq objects 
## similar to DNAString / DNAStringSet in R ?
### put the seq_record into a list
Ecoli = list(SeqIO.parse('C:\\Users\\Danie\\Documents\\R\\termination\\Ecoli_genomes.fasta', 'fasta'))
MG1655 = Ecoli[0].seq # obtains the genome quickly as a seq object and stored in MG1655
MG1655

# GC content
GC(MG1655)

# Or simply read the fasta directly
## still as a Seqrecord object
fasta = SeqIO.read('C:\\Users\\Danie\\Documents\\R\\termination\\MG1655.fasta', 'fasta')
GC(fasta.seq) # can still ge the GC this way









###################################################################
#           Pairwise alignment using pairwise2
#       Seems pointless as I have BOWTIE2 working in R
#         Or even cmd line BLAST for that matter
###################################################################
from Bio import SeqIO
from Bio import pairwise2
from Bio.Align import substitution_matrices
blosum62 = substitution_matrices.load("BLOSUM62")


seq1 = SeqIO.read("C:\\Users\\Danie\\Documents\\R\\termination\\terB.fasta", "fasta")
seq2 = SeqIO.read("C:\\Users\\Danie\\Documents\\R\\termination\\MG1655.fasta", "fasta")
alignments = pairwise2.align.globalds(seq1.seq, seq2.seq, blosum62, -10, -0.5)

# show alignments
print(pairwise2.format_alignment(*alignments[0]))







######################################################################
#                             Local BLAST
######################################################################
















