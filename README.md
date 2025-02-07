## Deduper

In this repository, I have created an algorithm to identify and remove PCR duplicates that are produced during the process of library prep.

### Problem 

During the RNA-seq workflow, PCR duplicates can arise from the amplification step. These are a result of PCR bias -- some sequences are simply easier to replicate in PCR than others. This can disproportionately inflate the genecounts after alignment, leading to inaccurate RNA-seq data analysis.

Goal: Identify and remove PCR duplicates after alignment to the reference genome (this makes identification more efficient) such that only 1 copy of each of these sequences that have been duplicated remain in the SAM file.
