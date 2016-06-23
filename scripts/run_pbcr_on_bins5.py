#!usr/bin/python

import subprocess
import glob
import os

#os.mkdir("./binned_read_assemblies")

def run_illumina_read_conversion(illumina_input, libname):
    iconvert_input="fastqToCA -libraryname illumina_%s -insertsize 200 50 -technology illumina -type sanger -innie -mates %s" % (libname, illumina_input)
    output=open(illumina_input.replace(".fastq",".frg"),"w")
    subprocess.call(iconvert_input.split(" "), stdout=output)
    output.close()
    print "%s converted" % illumina_input
    
#fastqToCA -libraryname MATED -type illumina -insertsize 200 20 -mates /nobackup1/fatimah/45_C7_Data/45_C7_Illumina_noAdapters/10N.261.45.C7_TAAGGCGAACTGCATA_1_trimmed.fastq1,/nobackup1/fatimah/45_C7_Data/45_C7_Illumina_noAdapters/10N.261.45.C7_TAAGGCGAACTGCATA_2_trimmed.fastq2 > 45_C7_try2.frg
    
    
def run_pbcr_with_read_correction(pb_subreads, illumina_output, run_name, genome_size):
    pbcr_input="PBcR -length 1000 -partitions 200 -l %s -s /nobackup1/jbrown/nahant_phage_pacbio/pacbio.spec -threads 20 -fastq %s %s genomeSize=%s" % (run_name, pb_subreads, illumina_output, genome_size)
    subprocess.call(pbcr_input.split(" "))
             
phages=open("/nobackup1/jbrown/nahant_phage_pacbio/K2.151228_PacBio_Nahant_Phages.txt").readlines()

phages=[i.replace("\r\n","") for i in phages]

igenome_ldict={}

with open("igenome_lengths.txt") as infile:
    for l in infile:
        phage=l.split("\t")[0]
        length=l.split("\t")[1].replace("\n","")
        igenome_ldict[phage]=length

for p in phages[20:40]:
    #if p!="1.020.O.":
        illumina_input=glob.glob("/nobackup1/jbrown/nahant_phage_reads/%s*.fastq" % p)[0]
        run_name="nvp_%s_binned_asm_try2" % p

        run_illumina_read_conversion(illumina_input, run_name)

        illumina_output=illumina_input.replace(".fastq",".frg")
        pb_subreads="/nobackup1/jbrown/nahant_phage_pacbio/binned_reads2/%s_pb_subreads.fastq" % p
        genome_size=igenome_ldict[p]

        run_pbcr_with_read_correction(pb_subreads, illumina_output, run_name, genome_size)

        

#PBcR -length 500 -partitions 200 -l lambdaIll -s pacbio.spec -fastq pacbio.filtered_subreads.fastq genomeSize=50000

