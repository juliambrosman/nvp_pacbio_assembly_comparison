#!usr/bin/python
from collections import defaultdict
from Bio import SeqIO
import os
import sys

'''
Program sorts reads into individual fastq files based on an input pairs file.  Binned fastq files will be placed in a specified folder.  

The pairs file should be a tab-delimited file with two columns.  Column one is a read name and column 2 is the bin that the read should be sorted into.  Reads can belong to multiple bins.

Inputs are: target folder, pairs file, original fastq file with all reads

Input should be written:
python extract_genome_read_bins.py target_folder pairs_file original_fastq_file
'''

target_folder=sys.argv[1]
pairs_file=sys.argv[2]
full_fastq=sys.argv[3]

def write_ids_to_fastq(id_list, fastq_in, fastq_out):
    out_recs=[]
    for record in SeqIO.parse(open_fastq(fastq_in), "fastq"):
        if record.id in id_list:
            out_recs.append(record)
            
    out=open(fastq_out, "w")
    SeqIO.write(out_recs, out, "fastq")
    out.close()
    
def open_fastq(fastq):
    if fastq.endswith(".gz"):
        fastq=gzip.open(fastq, "rU")
    else:
        fastq=open(fastq, "rU")
    return fastq

if os.path.exists(target_folder)==False:
    os.mkdir(target_folder)

pairs=open(pairs_file).readlines()

read_dict=defaultdict(lambda: [])

for p in pairs[1:]:
    phage=p.split("\t")[1].split("_")[1]
    read=p.split("\t")[0]
    read_dict[phage]+=[read]            

for p in read_dict.keys():
    reads=set(read_dict[p])
    fastq_out="%s/%s_pb_subreads.fastq" % (target_folder, p)
    write_ids_to_fastq(reads, "all_subreads.fastq", fastq_out)
    
