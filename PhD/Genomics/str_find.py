import regex
import Bio
from Bio import SeqIO
from Bio.Seq import Seq
# Literally using str.find() works and returns the position.

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

# open the genome
with open('MG1655.fasta') as fas:
    for genome in SeqIO.parse(fas, 'fasta'):
        print(genome.id)
        print(len(genome))
        MG1655_seq = genome.seq

with open('UMN026.fasta') as UMN:
    for genome2 in SeqIO.parse(UMN, 'fasta'):
        print(genome2.id)
        print(len(genome2))
        UMN026_seq = genome2.seq

# set the text and ter site
genome1 = str(MG1655_seq)
genome2 = str(UMN026_seq)
terA_fwdstr = str(terA)
terA_revstr = str(terA.reverse_complement())
terB_str = str(terB)
terB_revstr = str(terB.reverse_complement())
terB_revstr

test_findA_fwd = genome1.find(terA_fwdstr)
test_findA_rev = genome1.find(terA_revstr)
test_findB = genome1.find(terB_str)

test_findA_fwd
test_findA_rev
test_findB


# use regex to specify mismatches
match1 = regex.findall(terB_str, genome1)
match1

match2 = regex.findall(terB_revstr, genome2)
match2 # no match found if not exact match
match2_mismatch = regex.findall('(ACTTTAGTTACAACATACTTATT){e<=2}', genome2)
match2_mismatch

new_match2 = genome2.find('GACTTTAGTTACAACATACTAATT')
new_match2
