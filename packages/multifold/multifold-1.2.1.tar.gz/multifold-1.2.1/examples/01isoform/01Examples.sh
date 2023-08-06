#!/bin/sh
#Last-modified: 13 Nov 2014 11:54:18 AM

####################### Module/Scripts Description ######################
#  
#  Copyright (c) 2008 Yunfei Wang <yfwang0405@gmail.com>
#  
#  This code is free software; you can redistribute it and/or modify it
#  under the terms of the BSD License (see the file COPYING included with
#  the distribution).
#  
#  @status:  experimental
#  @version: $Revision$
#  @author:  Yunfei Wang
#  @contact: yfwang0405@gmail.com
#
#########################################################################

USAGE=" Usage: $0 hg19_demo.gpd hg19_chr1_partial.fa hg19_demo_S.wig hg19_demo_V.wig\n\tFor demo example, run\n\t\t>$0 demo\n\tTo clean demo results, run\n\t\t>$0 clean\n\tPut in real data for your own case.\n"

case $# in
    0)  echo -en $USAGE
		exit;;
	1)  if [ "$1" == "demo" ]; then
			AN=hg19_demo.gpd
			FA=hg19_chr1_partial.fa
			echo "Download demo fasta file..."
			wget --no-clobber --no-verbose "https://db.tt/hrdoPNzf" -O - |gunzip - >hg19_chr1_partial.fa
			S=hg19_demo_S.wig
			V=hg19_demo_V.wig
		else if [ "$1" == "clean" ]; then
				rm -rf workdir *fd *fc *fs *isf *txt *sizes *bw *fa *fai
				exit
			 else
				 echo -en $USAGE
				 exit
			 fi
		fi
        ;;
    2)  echo -en $USAGE
        exit;;
	3)  echo -en $USAGE
		exit;;
    *)  AN=$1
		FA=$2
        S=$3
        V=$4
        ;;
esac

prefix=${S%%.wig}
prefix=${prefix%%.bw}

# Dataset:
#	Gene annotation file: genePred format downloaded from UCSC genome Table
#		Browser (RefSeq track with output format as 'all fields from selected
#		table'.
#	Genome file: Fasta or 2bit format from UCSC genome browser.
#	Wiggle files: RNA footprinting data depth in single base resolution

# 1. Generating FastD file using option 2
echo -e "\n###################################\nStep 1: Generating FastD"
MultiFold FastD generate -a $AN -g $FA -dS $S -dV $V -o ${prefix}.fd

# 2. calculating constraints using 'exclusive' method
echo -e "\n###################################\nStep 2: Generating FastC"
MultiFold FastC generate -i ${prefix}.fd -m e -o ${prefix}.fc

# 3. fold RNA secondary structure using sfold with 2 CPUs
echo -e "\n###################################\nStep 3: Sfold. Be patient. It takes very long time for long transcripts."
MultiFold fold -i ${prefix}.fc -p 3 -o ${prefix}.fs

# 4. Extend FastD/S formats to EFastD/S formats.
# This will generate .efs and .efd files
echo -e "\n###################################\nStep 4: Extend FastD/S formats to EFastD/S formats."
MultiFold isoform extend -g $AN -d ${prefix}.fd -s ${prefix}.fd -p ${prefix}

# 5. Quantification of secondary structures using EFastD/S files
echo -e "\n###################################\nStep 5: Quantification of structures"
MultiFold quantify -d ${prefix}.efd -s ${prefix}.efs -o ${prefix}.txt

# 6. Visualization of RNA secondary structures
echo -e "\n###################################\nStep 6: Visualization of Structures"
MultiFold draw -i ${prefix}.fs -s ${prefix}
