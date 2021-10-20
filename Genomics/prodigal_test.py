# Prodigal through python using pyrodigal
import numpy
import Bio
from Bio import SeqIO
import pyrodigal

# training method (not sure how this works)
#p = pyrodigal.Pyrodigal()
# p.train(bytes(record.seq))
#genes = p.find_genes(bytes(record.seq))

# Meta methos using a genbank or fasta sequence (hopefully fasta works)
record = SeqIO.read('MG1655.fasta', 'fasta')  # I am getting the same gene over and over again...
p = pyrodigal.Pyrodigal(meta=True)

for i, gene in enumerate(p.find_genes(bytes(record.seq))):
    print(f">{record.id}_{i+1}")
    print(record.translate())
