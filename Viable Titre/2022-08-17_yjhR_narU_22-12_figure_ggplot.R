# Plotting the Recombination Rate from the Python App Master_df file
library(tidyverse)

# Set dir and slight tidy getting rid of first column
Set_Directory <- setwd(dirname(file.choose()))
master_df <- read.csv(file.choose())
master_df <- master_df[,-1]
master_df


# plot using ggplot
plot <-  ggplot(data=master_df) +
  geom_bar(aes(reorder(Strain, m_n), m_n, fill = m_n),stat='identity') +
  geom_errorbar(aes(x=Strain, ymin= m_n - Sigma_n ,ymax = m_n + Sigma_n ), width=0.4, colour="black", alpha=0.8, size=0.4) +
  scale_fill_viridis_c(option='H') + # A-E
  xlab('Strain') + ylab('Mutation Rate') +
  ggtitle('Mutation Rate in Double Origin Strain\n2022-08-17') +
  theme(plot.title = element_text(hjust = 0.5), 
        axis.text.x = element_text(angle=50,hjust = 1)) +
  theme_classic() +
  scale_x_discrete(guide = guide_axis(angle=45), labels = c('narU', 'oriZ narU', 'oriX narU',  
                                                            'yjhR', 'oriX yjhR', 'oriZ yjhR'))
  
  

# Call the plot and save
plot
setwd(dirname(file.choose()))
ggsave('2022-08-17_Recombination_Rates_Update.png')
