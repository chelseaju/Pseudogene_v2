#!/bin/bash
## bash new_preparation_v2.sh DIR COVERAGE READLEN ABUNDANCE

DIR=$1
COVERAGE=$2
READLEN=$3
ABUNDANCE=$4
SUBDIR=$COVERAGE"X_"$READLEN"L_"$ABUNDANCE"A"
TOPOUT="tophat_out"

SIMULATOR="/u/home/c/chelseaj/project/software/RNAseqSim-CJ.jar"
GENOME="/u/home/c/chelseaj/project/database/Ensembl/Genome/79/Homo_sapiens_GRCh38_79_genome.fa"
GENOMEINDEX="/u/home/c/chelseaj/project/database/Ensembl/Bowtie2Index/79/genome"
ERROR1="/u/home/c/chelseaj/project/database/SequenceQuality/paired_$READLEN/hiseq_1.fastq"
ERROR2="/u/home/c/chelseaj/project/database/SequenceQuality/paired_$READLEN/hiseq_2.fastq"
GTF="$DIR/SELECT_ENST.gtf"
SIMCONFIG="$DIR/$SUBDIR/config.txt"
GENELIST="$DIR/SELECT_ENST.txt"
EXPRESSION="$DIR/$SUBDIR/abundance.txt"


## Step 0: Create directory
echo ""
echo "Step 0 - Creating Directories"
mkdir -p "$DIR/$SUBDIR"
mkdir -p "$DIR/$SUBDIR/$TOPOUT"
echo "$DIR/$SUBDIR created"
echo "$DIR/$SUBDIR/$TOPOUT created"

## Step 1: Generate reads using simulator
echo ""
echo "Step 1 - Generating Reads"
python abundance_assigner.py -i $GENELIST -a $ABUNDANCE -o $EXPRESSION
java -Xmx1G -jar $SIMULATOR $SIMCONFIG -GTF_File=$GTF -FASTA_File=$GENOME -Chromosome=[0-9XYMT]* -Chromosome_Matching=Fuzzy -Abundance_File=$EXPRESSION -Abundance_Overwritten=No -Expressed_Transcript_Percentage=1 -Read_ID_Prefix=ENST- -Read_Length=$READLEN -Coverage_Factor=$COVERAGE -Quality_Generator=Real -Real_Quality_Score_Fastq_1=$ERROR1 -Real_Quality_Score_Fastq_2=$ERROR2 -Flip_And_Reverse=Yes -Unknown_Factor=0.0001 -Output_Fastq_1=$DIR/$SUBDIR/1.fq -Output_Fastq_2=$DIR/$SUBDIR/2.fq

## Step 2: Mapping the reads using tophat
echo ""
echo "Step 2 - Mapping Reads"
tophat2 -o $DIR/$SUBDIR/$TOPOUT $GENOMEINDEX $DIR/$SUBDIR/1.fq $DIR/$SUBDIR/2.fq


echo "Preparation Completed"
