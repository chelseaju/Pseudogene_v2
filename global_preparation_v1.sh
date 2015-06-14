#!/bin/bash
## sh global_preparation_v1.sh DIR READLEN

DIR=$1
READLEN=$2

GENOME="/u/home/c/chelseaj/project/database/Ensembl/Genome/Homo_sapiens_GRCh38_79_genome.fa"
GENOMEINDEX="/u/home/c/chelseaj/project/database/Ensembl/Bowtie2Index/79/genome"
TOPOUT="tophat_out"

## export path to run tophat2 and bowtie2
#export PATH=$PATH:/u/home/c/chelseaj/project/software/tophat-2.0.9.Linux_x86_64
#export PATH=$PATH:/u/home/c/chelseaj/project/software/bowtie2-2.0.6


## Step 0: Create directory
echo ""
echo "Step 0 - Creating Directories"

mkdir -p "$DIR/$TOPOUT"
echo "$DIR/$TOPOUT created"

## Step 1: Generate reads using the sliding window approach
echo ""
echo "Step 1 - Generating Reads"
python generate_reads_v2.py -d $DIR -l $READLEN


## Step 2: Mapping the reads using tophat
echo ""
echo "Step 2 - Mapping Reads"
tophat2 -o $DIR/$TOPOUT $GENOMEINDEX $DIR/READS_"$READLEN"L.fa


echo "Preparation Completed"
