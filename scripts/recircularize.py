#!usr/bin/python

import glob
import subprocess
import os

def run_gepard(fasta1, fasta2, output):
    os.chdir("/nobackup1/jbrown/programs/gepard-1.30/")
    gepard_cmd="bash /nobackup1/jbrown/programs/gepard-1.30/gepardcmd.sh -seq1 %s -seq2 %s -matrix /nobackup1/jbrown/programs/gepard-1.30/matrices/edna.mat -outfile %s" % (fasta1, fasta2, output)
    subprocess.call(gepard_cmd.split(" "))

to_cir=glob.glob("/nobackup1/jbrown/nahant_phage_pacbio/contigs/hgap2_to_circularize/*hgap.to_circularize.fasta")
phages=[i.split("/")[-1].split("hgap")[0] for i in to_cir]

cp=zip(to_cir, phages)

if os.path.exists("/nobackup1/jbrown/nahant_phage_pacbio/contigs/hgap2_circularized/")==False:
    os.mkdir("/nobackup1/jbrown/nahant_phage_pacbio/contigs/hgap2_circularized/")

if os.path.exists("/nobackup1/jbrown/nahant_phage_pacbio/comparisons/gepard/recirc/")==False:
    os.mkdir("/nobackup1/jbrown/nahant_phage_pacbio/comparisons/gepard/recirc/")


for split_fasta, phage in cp:
    output_afg="/nobackup1/jbrown/nahant_phage_pacbio/contigs/hgap2_circularized/%shgap2.cir.afg" % phage
    amos_cmd="toAmos -s %s -o %s" % (split_fasta, output_afg)
    minimus_cmd="minimus2 %s" % output_afg.replace(".afg","")

    subprocess.call(amos_cmd.split(" "))
    subprocess.call(minimus_cmd.split(" "))

    illumina_asm="/nobackup1/jbrown/annotation/genomes/%sfinal.fasta" % phage
    cir_asm=output_afg.replace(".afg",".fasta")
    gpd_out="/nobackup1/jbrown/nahant_phage_pacbio/comparisons/gepard/recirc/%sillumina_vs_hgap2circ.png" % phage
    run_gepard(illumina_asm, cir_asm, gpd_out)
