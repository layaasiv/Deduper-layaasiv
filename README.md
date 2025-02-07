# Deduper

In this repository, I have created an algorithm to identify and remove PCR duplicates that are produced during the process of library prep.

## Problem 

During the RNA-seq workflow, PCR duplicates can arise from the amplification step. These are a result of PCR bias -- some sequences are simply easier to replicate in PCR than others. This can disproportionately inflate the genecounts after alignment, leading to inaccurate RNA-seq data analysis.

Goal: Identify and remove PCR duplicates after alignment to the reference genome (this makes identification more efficient) such that only 1 copy of each of these sequences that have been duplicated remain in the SAM file.

## Solution
In a SAM file, PCR duplicates will: 
* Align to the same chromosome (RNAME, col 3) 
* Align to the same left-most start position on the chromosome (POS, col 4) (provided there is no 5' soft clipping (CIGAR string, col 6, denoted with 'S')) 
* Align to the same strand (provided the library is strand-specific) (FLAG, col 2) 
* Have the same UMI (QNAME, col 1)

Plan: Write a script that will identify PCR duplicates reliably using criteria above, and remove them from the SAM file, keeping the original (one copy per UMI). 

# Psuedocode
**Assumptions**
* A SAM file usually has a lot of lines in the beginning with irrelevant information for our purposes (all these lines will start with "@"). Could possibly remove these lines in bash before loading file into python script, but for now, I will assume we are not doing that.
* Saving only the first record of a duplicate encoutered. 
* samtools sort would have sorted the records by chromosome and position.
