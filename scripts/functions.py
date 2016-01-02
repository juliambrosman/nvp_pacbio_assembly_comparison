#!usr/bin/python
from __future__ import division
from pyfaidx import Fasta

def write_read_lengths_to_file(read_fasta_files, output_file):
    out=open(output_file,"w")
    out.write("fasta_file\tseq_id\tread_len\n")
    
    readfiles=list(read_fasta_files)
    for r in readfiles:
        f=Fasta(r)
        for i in f.keys():
            length=len(str(f[i]))
            fasta=r.split("/")[-1]
            sequence=i
            out.write("%s\t%s\t%s\n" % (fasta, sequence, length))
    out.close()

def create_read_length_dict(dict_name, read_length_file):
    rl=open(read_length_file).readlines()
    ldict={}
    for l in rl:
        ldict[l.split("\t")[1]]=l.split("\t")[-1].replace("\n","")
    return ldict

def filter_reads(read_length_dict, blast_file, output_blast_file, pctid_thresh=85, cov_thresh=0.99):
    fblast=open(output_blast_file,"w")
    with open(blast_file) as infile:
        for i in infile:
            vec=i.split("\t")
            aln_len=vec[3]
            read_len=int(ldict[vec[0]])
            qhitlen=int(vec[7])-int(vec[6])
            cov=qhitlen/read_len
            pctid=float(vec[2])
            if cov>cov_thresh and pctid>pctid_thresh:
                fblast.write(i)
    fblast.close()