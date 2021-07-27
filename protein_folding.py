# from: https://towardsdatascience.com/visualizing-and-analyzing-proteins-in-python-bd99521ccd
from Bio.PDB import *
import nglview as nv
import ipywidgets

pdb_parser = PDBParser()
structure = pdb_parser.get_structure("PHA-L", "1FAT.pdb")
view = nv.show_biopython(structure)
