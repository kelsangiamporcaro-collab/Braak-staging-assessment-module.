# Braak-staging-assessment-module.
Binary classification ML model to distinguish early vs late-stage Alzheimer's disease based on gene expression, specifically focusing on the PHGDH  gene and related pathways.

This is a binary classification model to distinguish early vs late stage 
Alzheimer's disease based on gene expression, specifically focusing on the PHGDH 
gene and related pathways. This gene has been found to play a casual role in 
Alzheimer's disease progression, and this model shows how this gene can 
predict disease stage when compared with other genes.
I wasn't able to find metadata on Braak stage for each individual,
so I classified stage 1-4 as early and 5-6 as late based on the 
file description from the website.

This uses the AD00101 and AD00102 datasets, the datasets being Braak stage 1-4 and 
Braak stage 5-6 respectively, but it can be easily modified for other datasets. 
I encourage further exploration with the rest of the datasets available on the site due
to confounding variables. While this model was written specifically
as a binary classifier for files with different Braak stage ranges, 
if you are somehow magically able to get the Braak stage for each 
individual sample, you could easily modify this into a multi-class classification model.

I gathered data from https://bmblx.bmi.osumc.edu/ssread/downloads and used 
https://github.com/cellannotation/capseuratconverter to convert the original
qsave files into h5ad format for analysis with scanpy (I don't know how to use R).

Author: Kelsan Giamporcaro
Version: 12/3/2025
