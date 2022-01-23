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
# p1 = subprocess.run('dir', shell=True, capture_output=True)
# print(p1.stdout.decode())


# os.chdir('C:\\Users\\Danie\\Documents\\GitHub\\Python\\Genomics\\BLAST_App')
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
    [sg.Text('Specify task: ', font=font), sg.Combo(['blastn', 'blastn-short'], key='-task-')],
    #[sg.Text('Specify other: ', font=font), sg.InputText(key='-kwargs-')],
    [sg.Text('Specify E value: ', font=font), sg.Combo([10e-9, 10e-8, 10e-7, 10e-6, 10e-5, 10e-4, 10e-3, 10e-2], key='-e_val-', font=font)],
    [sg.Text('Save CSV as: ', font=font), sg.InputText(key='-csv_savename-')],
    [sg.Text('Select directory to save image: ', font=font),
        sg.FileBrowse(key='-save_image-')],
    [sg.Button('Run', font=font)]
]


# run the window
window1 = sg.Window('BLAST', layout, resizable=True)
while True:
    event, values = window1.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Run':
        if not values['-csv_savename-']:
            csv_savename = 'blast_out'+day+'-'+month+'.csv'
        else:
            csv_savename = values['-csv_savename-']+'.csv'

        try:
            # Save to directory
            dir_path = os.path.dirname(os.path.realpath(values['-save_image-']))
            os.chdir(dir_path)
            makedb = NcbimakeblastdbCommandline(cmd=makedb_path, dbtype='nucl', input_file=values['-db-'], out='db'+day+'-'+month)
            # sg.popup('makedb: ' + str(makedb))
            cmd1 = subprocess.run(str(makedb), shell=True, capture_output=True)
            # cmd1.stdout.decode()
            blastn = NcbiblastnCommandline(cmd=blastn_path, query=values['-query-'], db='db'+day+'-'+month,
                                           outfmt="10 stitle qseqid sseqid sstart send sstrand evalue sseq length btop", out=csv_savename, task=values['-task-'], evalue=values['-e_val-'])
            cmd2 = subprocess.run(str(blastn), shell=True, capture_output=True)
            # cmd2.stdout.decode()

        except:
            sg.popup('Fail', font=font)
        try:
            # Add column names as the header
            blast_output = pd.read_csv(csv_savename,
                                       names=['stitle', 'qseqid', 'sseqid', 'sstart', 'send', 'sstrand', 'evalue', 'sseq', 'length', 'btop'])
            blast_output.to_csv(csv_savename, index=False)
        except:
            sg.popup('Failed to alter blast output')
        sg.popup('Finished')
        # opem the file we have just created.
        subprocess.Popen(csv_savename, shell=True)
