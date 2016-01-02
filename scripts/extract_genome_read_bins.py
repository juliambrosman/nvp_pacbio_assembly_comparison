#!usr/bin/python
from collections import defaultdict
from Bio import SeqIO
import os

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

            
#os.mkdir("./binned_reads/")

pairs=open("concat_blast_read_ig_pairs.txt").readlines()

read_dict=defaultdict(lambda: [])

for p in pairs[1:]:
    phage=p.split("\t")[1].split("_")[1]
    read=p.split("\t")[0]
    read_dict[phage]+=[read]            

for p in read_dict.keys():
    reads=set(read_dict[p])
    fastq_out="./binned_reads/%s_pb_subreads.fastq" % p
    write_ids_to_fastq(reads, "all_subreads.fastq", fastq_out)
    
