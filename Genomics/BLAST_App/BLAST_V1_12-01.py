from Bio.Blast.Applications import NcbiblastnCommandline
from Bio.Blast.Applications import NcbimakeblastdbCommandline
import io
import os
import subprocess
from datetime import datetime
import pandas as pd
import numpy as np
import PySimpleGUI as sg

makedb_path = 'C:\\Program Files\\NCBI\\BLAST\\bin\\makeblastdb.exe'
blastn_path = 'C:\\Program Files\\NCBI\\BLAST\\bin\\blastn.exe'
#p1 = subprocess.run('dir', shell=True, capture_output=True)
# print(p1.stdout.decode())


os.getcwd()
# date and time
now = datetime.now()
day = now.strftime("%d")
month = now.strftime("%m")

# SG specifics:
sg.theme('DarkBlue1')  # DarkGrey14, DarkGrey, Reddit, LightBlue, DarkBlue1
font = ('Calibri', 14)
font_small = ('Calibri', 12)

# window layout
layout = [
    [sg.Text('Select genome to make into database: ', font=font), sg.FileBrowse(key='-db-')],
    [sg.Text('Select query fasta file: ', font=font), sg.FileBrowse(key='-query-')],
    [sg.Text('Specify E value: ', font=font), sg.Combo([10e-9, 10e-8, 10e-7, 10e-6, 10e-5, 10e-5], key='-e_val-', font=font)],
    [sg.Button('Run', font=font)]
]


# run the window
window1 = sg.Window('BLAST', layout, resizable=True)
while True:
    event, values = window1.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Run':
        try:
            makedb = NcbimakeblastdbCommandline(cmd=makedb_path, dbtype='nucl', input_file=values['-db-'], out='db'+day+'-'+month)
            #sg.popup('makedb: ' + str(makedb))
            cmd1 = subprocess.run(str(makedb), shell=True, capture_output=True)
            # cmd1.stdout.decode()
            blastn = NcbiblastnCommandline(cmd=blastn_path, query=values['-query-'], db='db'+day+'-'+month,
                                           outfmt="10 stitle qseqid sseqid sstart send sstrand evalue sseq length btop", out='blast_out'+day+'-'+month+'.csv')
            cmd2 = subprocess.run(str(blastn), shell=True, capture_output=True)
            # cmd2.stdout.decode()
        except:
            sg.popup('Fail', font=font)
        sg.popup('Finished')
