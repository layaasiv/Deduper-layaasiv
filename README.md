# Deduper

In this repository, I have created an algorithm to identify and remove PCR duplicates that are produced during the process of library prep.

## Problem 

During the RNA-seq workflow, PCR duplicates can arise from the amplification step. These are a result of PCR bias -- some sequences are simply easier to replicate in PCR than others. This can disproportionately inflate the genecounts after alignment, leading to inaccurate RNA-seq data analysis.

Goal: Identify and remove PCR duplicates after alignment to the reference genome (this makes identification more efficient) such that only 1 copy of each of these sequences that have been duplicated remain in the SAM file.

## Proposed Solution
In a SAM file, PCR duplicates will: 
* Align to the same chromosome (RNAME, col 3) 
* Align to the same left-most start position on the chromosome (POS, col 4) (provided there is no 5' soft clipping (CIGAR string, col 6, denoted with 'S')) 
* Align to the same strand (provided the library is strand-specific) (FLAG, col 2) 
* Have the same UMI (QNAME, col 1)

Plan: Write a script that will identify PCR duplicates reliably using criteria above, and remove them from the SAM file, keeping the original (one copy per UMI). 

**Assumptions**
* A SAM file usually has a lot of lines in the beginning with irrelevant information for our purposes (all these lines will start with "@"). Could possibly remove these lines in bash before loading file into python script, but for now, I will assume we are not doing that.
* Saving only the first record of a duplicate encoutered. 
* samtools sort would have sorted the records by chromosome and position.

## What is in this repository 
* [sivakumar_deduper.py](https://github.com/layaasiv/Deduper-layaasiv/blob/master/sivakumar_deduper.py): The final deduper algorithm. 
* [STL96.txt](https://github.com/layaasiv/Deduper-layaasiv/blob/master/STL96.txt): A list of the valid UMIs present in this dataset.
* [deduper_pseudocode](https://github.com/layaasiv/Deduper-layaasiv/blob/master/deduper_pseudocode.md): A rough pseudocode of my plan for the algorithm when I first began writing the script.
* test.sam & my_test.sam: Test SAM file inputs to verify proper function of the algorithm.
* test_output.sam: Output of the algorithm when it is given my_test.sam as input.
* [dedpuer_slurm.sh](https://github.com/layaasiv/Deduper-layaasiv/blob/master/deduper_slurm.sh): Slurm script to run the algorithm on HPC.

## How to use this algorithm 
Given a SAM file of uniquely mapped reads, and a text file containing the known UMIs, [Deduper](https://github.com/layaasiv/Deduper-layaasiv/blob/master/sivakumar_deduper.py) removes all PCR duplicates (retain only a single copy of each read). It will assume a sorted SAM file, therefore, ```samtools sort``` must be applied to the SAM file before passing it into this script. The algorithm will account for soft clipping and information in CIGAR string. In addition to deduping, this algorithm also filters only for those reads that contain valid UMIs (those specifiec in the text file input). Those reads that have been filtered out 

The algorithm can be executed like this: 

```
./sivakumar_deduper.py -u <umi.txt> -f <in.sam> -o <out.sam>
```
The output will be: 
* A deduped SAM file
* A text file containing identified duplicate reads
* A text file containing reads that were removed for carrying invalid UMIs
