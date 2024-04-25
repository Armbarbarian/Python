import os
import pandas as pd  # dataframe management
from Bio.Seq import Seq  # for turning into Seq objects
from Bio import SeqIO  # for reading fasta
from Bio import AlignIO
from io import StringIO
from Bio.Align import MultipleSeqAlignment  # aligning seqs
from Bio.SeqRecord import SeqRecord
import Bio.Align.Applications  # alignments command line tools
from Bio import pairwise2


# testing the read_csv function from pandas
df = pd.read_csv('BW2952.csv')
print(df.head())


# testing the Seq() function from Bio.Seq
seq1 = df.seq[1]
test_seq = Seq(seq1)
print(test_seq)
print(type(test_seq))


# testing the in line running
print('it works')

# remembering syntax of python
a = 10
for i in range(a):
    print(i)

# autopep8 save feature
x = 50
print(x, 'hello')


# opening fasta files
with open('ter_seq.fastq') as fas:
    for record in SeqIO.parse(fas, 'fastq'):
        print(record.seq)


# formatted alignment objects using AlignIO
alignments = AlignIO.parse('ter_seq.fastq', 'fastq')
out_handle = StringIO()
AlignIO.write(alignments, out_handle, 'clustal')
clustal_data = out_handle.getvalue()
print(clustal_data)

# MSA using MultipleSeqAlignment
msa = MultipleSeqAlignment(
    [
        SeqRecord(Seq('ATGGGT'), id='seq1'),
        SeqRecord(Seq('T-GGTA'), id='seq2'),
    ]
)
print(msa)

# using MultipleSeqAlignment for large seqs
with open('Ecoli_termination_area.fasta') as termination_area:
    for record in SeqIO.parse(termination_area, 'fasta'):
        print(record.id)

print(record)
