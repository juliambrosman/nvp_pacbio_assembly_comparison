#!usr/bin/python

import os
import glob
import shutil

from read_coverage import *

phages=open("K2.151228_PacBio_Nahant_Phages.txt").readlines()
phages=[i.replace("\r\n","") for i in phages]

for p in phages:

    cir_fasta = "/nobackup1/jbrown/nahant_phage_pacbio/contigs/hgap2_circularized/%shgap2.cir.fasta" % p
    
    if os.path.exists(cir_fasta) and os.path.getsize(cir_fasta)==0:
        print "%s failed circularization" % p
        hgap2_contig = "/nobackup1/jbrown/nahant_phage_pacbio/contigs/%s/%s_kkhgap2.fasta" % (p, p)
    elif os.path.exists(cir_fasta) and os.path.getsize(cir_fasta)>0:
        print "%s circularized" % p
        hgap2_contig = cir_fasta
    elif os.path.exists("/nobackup1/jbrown/nahant_phage_pacbio/contigs/%s/%s_kkhgap2.fasta" % (p, p)):
        hgap2_contig = "/nobackup1/jbrown/nahant_phage_pacbio/contigs/%s/%s_kkhgap2.fasta" % (p, p)
        print "%s not circularized" % p
    else:
        print "contig for %s not present in kkhgap2 assembly" % p
        hgap2_contig = None

    if hgap2_contig != None:
        fastq = glob.glob("/nobackup1/jbrown/nahant_phage_reads/%s*.fastq" % p)[0]
        output = "/nobackup1/jbrown/nahant_phage_pacbio/illuminacov/%s_kkhgap_illumina_readrecruitment.txt" % p        
        recruit_reads(fastq, hgap2_contig, output)
        output1 = "/nobackup1/jbrown/nahant_phage_pacbio/illuminacov/%s_illumina_final_contig_readrecruitment.txt" % p
        contig = "/nobackup1/jbrown/annotation/genomes/%sfinal.fasta" % p
        recruit_reads(fastq, contig, output1)
        shutil.copyfile(hgap2_contig, "/nobackup1/jbrown/nahant_phage_pacbio/contigs/%s/%s_kkhgap2_best.fasta" % (p, p))
        