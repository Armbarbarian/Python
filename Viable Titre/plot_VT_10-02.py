import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('ggplot')

df = pd.read_csv('DG028_DG033_Growth_Cruve_10-02.csv')
df
WTx_data = df.loc[df['Strain'] == 'DG028'].Time
WTx_data
WTy_data = df.loc[df['Strain'] == 'DG028'].Titre

MUTx_data = df.loc[df['Strain'] == 'DG033'].Time
MUTy_data = df.loc[df['Strain'] == 'DG033'].Titre
# plotting
fig = plt.figure(figsize=(7, 5))
plt.plot(MUTx_data, MUTy_data, color='firebrick', marker='o', label='DG033', linewidth=3)
plt.plot(WTx_data, WTy_data, color='royalblue', marker='o', label='DG028', linewidth=3)
plt.yscale('log')
plt.title('DG028 vs DG033 Growth Curve 10/02/2022')
plt.xlabel('Time')
plt.ylabel('Viable Titre')
plt.legend()
plt.show()
fig.savefig('DG028_DG033_log_Growth_Cruve_10-02.png', dpi=fig.dpi)
