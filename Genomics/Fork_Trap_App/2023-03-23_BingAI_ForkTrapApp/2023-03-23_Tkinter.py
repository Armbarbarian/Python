'''

I am a BIOINFORMATICIAN and I am using Python to build a GUI using Tkinter where I parse in a bacterial genome file, as a fasta file, to which I can then map genes of interest and other regions, even ones as small as a primer sequence, then map it to the reference genome. The program should first read in a reference genome fasta, then a query fasta file, with positional information. Then take thake positional information and create a track, in the form of an arrow, showing where exactly that gene resides on the genome. Show the arrow pointing in the direction of which strain of DNA the gene is oriented. Allow the GUI to allow custom colours for the gene being queried. Allow multiple queries on the same reference genome. Use GenomeDiagram package in Python to achive this and build the GUI in python too. Use matplotlib if you need to in order to calculate and store information, but only if there is no other simpler way. Thanks!

Yes, you can build a GUI using the Tkinter library in Python that would allow someone who doesn't know programming to use this method. The GUI can have input fields for the user to specify the reference genome and query fasta files and other parameters such as the start and end positions of the query on the reference genome. The code I provided earlier can be modified to take these inputs from the GUI and run behind the scenes when a button is clicked.

Here is an example of how you can create a simple GUI using Tkinter:
'''

import tkinter as tk
from tkinter import filedialog

def select_reference_genome():
    filename = filedialog.askopenfilename()
    # set reference_genome_entry text to filename

def select_query_fasta():
    filename = filedialog.askopenfilename()
    # set query_fasta_entry text to filename

def generate_diagram():
    # get inputs from GUI
    reference_genome_file = reference_genome_entry.get()
    query_fasta_file = query_fasta_entry.get()
    query_start = int(query_start_entry.get())
    query_end = int(query_end_entry.get())

    # run code to generate diagram using inputs from GUI

root = tk.Tk()

reference_genome_label = tk.Label(root, text="Reference Genome Fasta File")
reference_genome_label.pack()

reference_genome_entry = tk.Entry(root)
reference_genome_entry.pack()

reference_genome_button = tk.Button(root, text="Select File", command=select_reference_genome)
reference_genome_button.pack()

query_fasta_label = tk.Label(root, text="Query Fasta File")
query_fasta_label.pack()

query_fasta_entry = tk.Entry(root)
query_fasta_entry.pack()

query_fasta_button = tk.Button(root, text="Select File", command=select_query_fasta)
query_fasta_button.pack()

query_start_label = tk.Label(root, text="Query Start Position")
query_start_label.pack()

query_start_entry = tk.Entry(root)
query_start_entry.pack()

query_end_label = tk.Label(root, text="Query End Position")
query_end_label.pack()

query_end_entry = tk.Entry(root)
query_end_entry.pack()

generate_button = tk.Button(root, text="Generate Diagram", command=generate_diagram)
generate_button.pack()

root.mainloop()

'''
This code creates a simple GUI with input fields for selecting the reference genome and query fasta files and specifying the start and end positions of the query on the reference genome. When the "Generate Diagram" button is clicked, it gets these inputs from the GUI and runs code to generate a diagram using these inputs.

You can modify this code further to add additional functionality such as allowing for multiple queries and custom colors for queried genes.
'''
