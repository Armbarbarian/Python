from Bio.Blast.Applications import NcbiblastnCommandline
from Bio.Blast.Applications import NcbimakeblastdbCommandline
import io
import os
import subprocess
from datetime import datetime
import pandas as pd
import numpy as np
import PySimpleGUI as sg

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
            makedb = NcbimakeblastdbCommandline(dbtype='nucl', input_file='MG1655.fasta', out='db')
            sg.popup('makedb: ' + str(makedb))

            cmd1 = subprocess.call(str(makedb), shell=True)
            sg.popup(str(cmd1))

            blastn = NcbiblastnCommandline(query='OriC_MG1655.fasta', db='db', outfmt=10, out='out'+day+'-'+month+'.csv')
            sg.popup('blatn: ' + str(blastn))

            cmd2 = subprocess.call(str(blastn), shell=True)
            sg.popup(str(cmd2))
        except:
            sg.popup('Fail', font=font)
