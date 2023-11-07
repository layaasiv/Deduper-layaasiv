#!/usr/bin/env python

# import necessary libraries 
import re
import argparse

# set up argpase
def get_args():
    parser = argparse.ArgumentParser(description="A program to remove PCR duplicates from a SAM file. The user must sort the SAM file by chromosome and position using samtools prior to loading into this program. The program will output 2 files: a deduped SAM file containing only unique reads--the user will pass the name of this file when running the program; a dupes.txt file containing all the duplicates that were removed.")
    parser.add_argument("-f", "--saminput", help="file name of input SAM file containing duplicates, sorted by chromosome and position", required=True)
    parser.add_argument("-u", "--umilist", help="file name of text file containing all expected UMIs", required=True)
    parser.add_argument("-o", "--outputfile", help="file name of deduped SAM output file", required=True)
    return parser.parse_args()

args = get_args()
val_umis = args.umilist
sam_og = args.saminput
sam_new = args.outputfile

# define functions
def cigar_sep(str):
    '''Given a CIGAR string, this function will split it into the number of bases in each feature.
    Each number/feature pair will be saved in a tuple, and all tuples will be saved in a list.'''

    feature = re.findall('[A-Z]+', str)
    n = re.findall('[0-9]+', str)

    cigar = []

    for i in range(len(feature)): 
        pair = (n[i], feature[i])
        cigar.append(pair)
    
    return cigar

def strandedness(flag): 
    '''Given the flag from a SAM record, returns True if the sequence aligns to the forward (+) strand and False
    if the sequences aligns to the reverse (-) strand'''

    flag = int(flag)
    if ((flag & 16) == 16):
        return False
    else:
        return True

def adj_pos(flag, cigar, pos): 
    '''Given the bitwise flag and left-most start position from the SAM record for a sequence and 
    the product of the sep_ciagr function, this function will determine whether the sequence aligned 
    to the + or - strand, and adjust the 5' start position to account for soft clipping accordingly.'''

    adj_start = int(pos)
    flag = int(flag)

    if ((flag & 16) == 16):
        if cigar[0][1] == 'S':
            for i in range(1,len(cigar)):
                if cigar[i][1] == 'I':
                    continue
                else:
                    adj_start += int(cigar[i][0])
        else:
            for i in range(len(cigar)):
                if cigar[i][1] == 'I':
                    continue
                else:
                    adj_start += int(cigar[i][0])
    else:
        if cigar[0][1] == 'S':
            adj_start -= int(cigar[0][0])
    
    return str(adj_start)

def create_umi_list(txtfile):
    '''Create a list of expected UMIs given a text file that contains them (one UMI on each line).'''

    umi_list = []
    with open(txtfile, 'r') as fh:
        for line in fh:
            line = line.strip('\n')
            umi_list.append(line)
    
    return umi_list

def umi_finder(qname):
    '''Extract the UMI given the QNAME of a record from a SAM file and checks if it is also in the 
    umi_list (output of create_umi_list function). Returns the UMI as a string and its presence in
    the umi_list as a bool.'''

    umi = re.findall(':[ACTG]+', qname)
    umi = str(umi[0])[1:]
    
    return umi, umi in umi_list

# set up global variables
current_chr = {}
umi_list = create_umi_list(val_umis)
chrom_var = ''

# iterate through the SAM file, saving all unique reads in one chromosome at a time
with open(sam_og, 'r') as sam_og, open('dupes.txt', 'w') as dupes, open(sam_new, 'w') as sam_new, open('invalid.txt', 'w') as inv:
    for line in sam_og:
        # write out the headers
        if line.startswith('@'): 
            sam_new.write(line)
        # if the line is not a header, parse the information needed from the line and put through functions defined above to enable comparison to identify duplicates.
        else:
            line_split = line.split('\t')
            umi, valid = umi_finder(line_split[0])
            chro = line_split[2]
            flag = line_split[1]
            strand = strandedness(flag)
            pos = line_split[3]
            cigarstr = line_split[5]
            cigar_list = cigar_sep(cigarstr)
            adj_position = adj_pos(flag, cigar_list, pos)

            # save the prospective currrent_chr dict key into a variable
            thing = (umi, flag, chro, adj_position)
            
            # only selecting the lines with valid UMIs 
            if valid: 
                # this condition will determine whether the read is unique or not, and write it to the appropriate file. Will also work for the very first record in the file since we have set chrom_var (global variable) as an empty string.
                if chro == chrom_var:
                    if thing in current_chr.keys():
                        dupes.write(line)
                    else:
                        current_chr[thing] = 1
                        sam_new.write(line)
                
                # first encounter of a new chro, so clear the dict and add this key to it. set chrom_var to the current chro for comparison to future reads
                elif chro != chrom_var:
                    chrom_var = chro
                    current_chr.clear()
                    current_chr[thing] = 1
                    sam_new.write(line)

                else: 
                    raise Exception('Valid UMI but did no meet other conditions.')
            
            # invalid UMIs are written to invalid file
            else:
                inv.write(line)

sam_og.close()
dupes.close()
sam_new.close()
inv.close()