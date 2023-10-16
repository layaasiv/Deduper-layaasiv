# Problem
During the RNA-seq workflow, PCR duplicates can arise from the amplification step. These are a result of PCR bias -- some sequences are simply easier to replicate in PCR than others. This is can inproportionately inflate the genecounts after alignment, leading to inaccurate RNA-seq data analysis. 

Goal: Identify and remove PCR duplicates after alignment to the reference genome (this makes identification more efficient) such that only 1 copy of each of these sequences that have been duplicated remain in the SAM file.

# Solution
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
* Sam tools sort would have sorted the records by chromosome and position.

**Variables:**
* dict = {umi:[strand, chr, pos, adj_pos]}
* umi = [all 96 UMIs] 

With open SAM file and read line by line. Every line is 1 record in the SAM file. 

Check if line starts.with("@"). If yes, write it to the deduplicated SAM file and move on to the next line.

For each line (record), line.split by tab. This results in a list of the different SAM columns. 

For the first record, if the UMI is in umi list, add the relevant information to the dict (col 1, 2, 3, 5). Write the record to the deduplicated SAM file. 

For the the next record, check if umi, chr, strand and adj_pos are the same. \
    If true, skip and move onto next record. \
    If false and the UMI is in the umi list, write the record to the deduplicated SAM file. At this point, also clear the dict and replace it with the information from the current record. 

**To determine adj_pos:**
    Want to pair the feature and the number of bases within that feature, independent of the other features so that the CIGAR string becomes searchable (i.e., in a list of tuples: [(3, S), (40, M)]). \
    We only care about soft clipping when it happens at the 5' end. 
    
    If the seq aligned to the positive strand: 
        Thus, 5' soft clipping will be the first feature noted in the CIGAR string. 
        So, check if the first tuple in the list has an S in [1]. If it does, grab the number saved in [0] and subtract it from pos. Save the new value in adj_pos (alternatively, can save it as the new value of pos).
    
    If seq aligned to the negative strand:
        Thus, 5' soft clipping will be the last feature noted in the CIGAR string. 
        So, check if the last tuple in the list has an S in [1]. If it does, grab the number saved in [0] and add it to pos. Save the new value in adj_pos (alternatively, can save it as the new value of pos).


**Functions**

```
def cigar(str) -> list of tuples: 

    '''Put letter and number pairs as separate tuples within a list when given a string (in this case, it will be a cigar string)'''

    list_of_tuples = lst 
    return list_of_tuples 

    Test example: '25M246N41M' 
    Expected output: [(25, M), (256, N), (41, M)]
```

