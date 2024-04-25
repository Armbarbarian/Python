import GenomeDiagram
from Bio import SeqIO
from Bio.Graphics import GenomeDiagram

# Add a dropdown to select genome
genomes = {'MG1655': 'ecoli_mg1655.gb', 'K12': 'ecoli_k12.gb'}
selected_genome = 'MG1655' # default value

# Add dropdown for ter sites file
ter_files = {'MG1655': 'mg1655_ters.txt', 'K12': 'k12_ters.txt'}
selected_ter_file = ter_files[selected_genome]

record = SeqIO.read(genomes[selected_genome], "genbank")

gd_diagram = GenomeDiagram.Diagram('E. coli ' + selected_genome)
gd_track_for_features = gd_diagram.new_track(1, name='Annotated Features')
gd_feature_set = gd_track_for_features.new_set()

# Add ter sites
ter_set = gd_track_for_features.new_set(name='TER sites')
for feature in SeqIO.parse(selected_ter_file, "bed"):
    ter_set.add_feature(feature, sigil="BIGARROW",
                        color="red", label=True)

# Add genes
for feature in record.features:
    if feature.type == "CDS":
        if len(gd_feature_set) % 2 == 0:
            color = colors.blue
        else:
            color = colors.lightblue
        gd_feature_set.add_feature(feature, sigil="ARROW",
                                   color=color, label=True,
                                   label_size=14, label_angle=0)

# Customize track appearance
gd_track_for_features.height = 0.5
gd_track_for_features.title_spacing = 0.1
gd_track_for_features.label_size = 6

# Save as PDF
gd_diagram.draw(format='linear', pagesize='A4', fragments=4,
                start=0, end=len(record))
gd_diagram.write('ecoli_' + selected_genome + '.pdf', 'PDF')

print('Genome diagram generated for ' + selected_genome)
