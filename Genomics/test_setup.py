import pandas as pd

my_dict = {'A': (1, 2, 3), 'B': (2, 3, 4), 'C': (5, 6, 7)}

my_df = pd.DataFrame(my_dict)

my_df

dict2 = {'A': (45, 54, 45), 'B': (5, 6, 6), 'C': (3, 3, 3)}

df2 = pd.DataFrame(dict2)

df2

# ______________________________________________________________________
# Testing classes
# ______________________________________________________________________


class Strain:
    def __init__(self, species, name, access_code):
        self.species = species
        self.name = name
        self.access_code = access_code


strain1 = Strain('E.coli', 'MG1655', 'U00096.3')
strain2 = Strain('Salmonella', 'RSK2980', 'CP000880.1')


strain1.species
