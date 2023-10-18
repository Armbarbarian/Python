library(tidyverse)

# Read in raw tab separated data
tsv <- read_tsv("MG1655_gcskew.csv") 

#
df <- data.frame(tsv)
head(df)

# clean into similar format as Bowtie2 output for fork trap app
df_clean <- df %>% 
  rename(GC=3)

#
df_clean


#
write.csv(df_clean, '2023-10-18_MG1655_GCskew.csv')



