import pandas as pd
import numpy as np

'From the VT App'
# _____________________________________
average1 = np.mean([int(values['Colonies_1A']), int(values['Colonies_1B'])])
average2 = np.mean([int(values['Colonies_2A']), int(values['Colonies_2B'])])
vol = float(values['Volume'])
dilutions = np.sum([float(values['Dilution_1']), float(values['Dilution_2'])])
result = np.sum([average1, average2]) / (vol * dilutions)


'Applying to dataset from 2021-12-21'
# ______________________________________
average1 = np.mean([0, 1])
average2 = np.mean([12, 12])
vol = 0.01
vol
dilutions = np.sum([1, 0.1])
vol * dilutions
np.sum([average1, average2])
(vol * dilutions)
result = np.sum([average1, average2]) / (vol * dilutions)
result
