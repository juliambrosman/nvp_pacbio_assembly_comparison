#!usr/bin/python

import os
import glob
import subprocess

ilens=open("igenome_lengths.txt").readlines()
phages=[i.split("\t")[0] for i in ilens[1:]]
lens=[int(i.split("\t")[1].replace("\n","")) for i in ilens[1:]]
i_lens=dict(zip(phages, lens))

tkbs=[i for i in i_lens.keys() if i_lens[i]<11000]
tkbs

if os.path.exists("./spades/")==False:
    os.mkdir("./spades/")

for phage in tkbs:    

    if os.path.exists("./spades/%s" % phage)==False:
        os.mkdir("./spades/%s" % phage)

    output_dir="./spades/%s" % phage
    illumina_reads=glob.glob("/nobackup1/jbrown/nahant_phage_reads/%s*.fastq" % phage)[0]
    pb_reads="/nobackup1/jbrown/nahant_phage_pacbio/binned_reads2/%s_pb_subreads.fastq" % phage

    spades_input="spades.py -o %s --12 %s --pacbio %s" % (output_dir, illumina_reads, pb_reads)
    subprocess.call(spades_input.split(" "))