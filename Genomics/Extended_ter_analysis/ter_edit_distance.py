import os
from Bio import SeqIO
from Bio.Seq import Seq


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
