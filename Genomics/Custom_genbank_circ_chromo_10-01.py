# Using genome diagram to create circular images of features in a genbank file
# this script will position ter sites on a circular chromosome track
# the ter sites will be found and their position plotted

import pandas as pd
from tkinter.filedialog import askopenfilename
from Bio.SeqFeature import SeqFeature, FeatureLocation
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from Bio import SeqIO
import os
os.getcwd()
file = askopenfilename()
dir_path = os.path.dirname(os.path.realpath(file))
os.chdir(dir_path)
# libraries

ter_df = pd.read_csv('ter_MG1655.csv')
ter_df


# Custom genbank from the csv to map
# ter sites
terA_str = 'aattagtatgttgtaactaaagt'
terB_str = 'aataagtatgttgtaactaaagt'
terC_str = 'atataggatgttgtaactaatat'
terD_str = 'cattagtatgttgtaactaaatg'
terE_str = 'ttaaagtatgttgtaactaagca'
terF_str = 'ccttcgtatgttgtaacgacgat'
terG_str = 'gtcaaggatgttgtaactaacca'
terH_str = 'cgatcgtatgttgtaactatctc'
terI_str = 'aacatggaagttgtaactaaccg'
terJ_str = 'acgcagtaagttgtaactaatgc'

# Seq objects
terA_seq = Seq(terA_str)
terB_seq = Seq(terB_str)
terC_seq = Seq(terC_str)
terD_seq = Seq(terD_str)
terE_seq = Seq(terE_str)
terF_seq = Seq(terF_str)
terG_seq = Seq(terG_str)
terH_seq = Seq(terH_str)
terI_seq = Seq(terI_str)
terJ_seq = Seq(terJ_str)

#  record objects
MG1655_record = SeqRecord(terA_seq, id='MG1655', name='ter',
                          description='ter sites found with BT2 in R', annotations={"molecule_type": "DNA"})


# annotation features (ter sites)
terA_feat = SeqFeature(FeatureLocation(start=1, end=3), type='misc_feature')
MG1655_record.features.append(terA_feat)
terB_feat = SeqFeature(FeatureLocation(start=4, end=5), type='misc_feature')
MG1655_record.features.append(terB_feat)


# save GenBank
output_file = open('ter_sites_MG1655.gb', 'w')
SeqIO.write(MG1655_record, output_file, 'genbank')
