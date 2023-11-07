### Lab Notebook: Deduper

SAM File to be deduped: ``/projects/bgmp/layaasiv/bioinfo/Bi624/Deduper-layaasiv/C1_SE_uniqAlign.sam```

To sort the file: ```samtools sort -o <output file name> <input file name>``` in the bgmp_star conda env.

This will sort the records first by chromosome and then by position. Using this structure, we can then read the file into memory chromosome by chromosome without loading the entire file into memory. Another way to do it is to create an intermediate file, but this was not allowed for this assignment.

Number of headers: ```grep "^@" deduped_C1_SE_uniqAlign.sorted.sam | wc -l``` \
Number of unique reads: ```grep -v "^@" deduped_C1_SE_uniqAlign.sorted.sam | wc -l``` \
Number of reads per chromosome/scaffold: ```grep -E "^.+\s[0-9]+\s<chr>\s" deduped_C1_SE_uniqAlign.sorted.sam | wc -l```