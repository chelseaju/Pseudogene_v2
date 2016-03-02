## library needed

module load bedtools
module load samtools
module load python/2.7

export PATH=$PATH:/u/home/c/chelseaj/project/software/tophat-2.0.9.Linux_x86_64
export PATH=$PATH:/u/home/c/chelseaj/project/software/bowtie2-2.0.6


# Randomly select parent genes
shuf -n 300 /u/home/c/chelseaj/project/database/Pseudogene/Parent_ENST_79.txt > SELECT_PARENTS_ENST.txt

# adding pseudogene
grep -Ff SELECT_PARENTS_ENST.txt /u/home/c/chelseaj/project/database/Ensembl/ENST_ENSG_ENSP_79.txt  | cut -f3 > SELECT_PARENTS_ENSP.txt
grep -Ff SELECT_PARENTS_ENSP.txt /u/home/c/chelseaj/project/database/Pseudogene/Human79.txt | cut -f1 > POTENTIAL_PGOHUM.txt
grep -Ff POTENTIAL_PGOHUM.txt /u/home/c/chelseaj/project/database/Pseudogene/Transcribed_Pseudogene_79.txt | cut -f1 > SELECT_PSEUDO_ENST.txt

# merge two list
cat SELECT_PARENTS_ENST.txt SELECT_PSEUDO_ENST.txt > SELECT_ENST.txt

# convert to bed file
grep -Ff SELECT_ENST.txt /u/home/c/chelseaj/project/database/Ensembl/ENST_79.bed > SELECT_ENST.bed

# convert to fasta file
bedtools getfasta -fi /u/home/c/chelseaj/project/database/Ensembl/Genome/79/Homo_sapiens_GRCh38_79_genome.fa -bed SELECT_ENST.bed -fo SELECT_ENST.fa -name -split -s

# convert gtf file
grep -Ff SELECT_ENST.txt /u/home/c/chelseaj/project/database/Ensembl/Homo_sapiens.GRCh38.79.gtf > SELECT_ENST.gtf


# data preparation: prepare reads for community detection
python submitPreparation.py -d select_genes_600

# data analysis:
python submitGlobalAnalysis.py -d select_genes_600
python submitLocalAnalysis.py -d select_genes_600

# run community detection
R --no-save --slave < community_detection.R --args select_genes_600/mapping/genes_distribution.mtx select_genes_600/mapping

# community evaluataion

# run training + validation
mkdir select_genes_600/betweenness select_genes_600/infomap select_genes_600/none
R --no-save --slave < trainning_none.R --args select_genes_600 nrow ncol rep
R --no-save --slave < trainning_betweenness.R --args select_genes_600 nrow ncol rep
R --no-save --slave < trainning_infomap.R --args select_genes_600 nrow ncol rep


# post data examination:
# examine sequence similarity after community detection
# notice that group_XX_ids.txt and group_XX_names.txt are stored at results/community/
python retrieve_gene_id.py -d select_genes_600 -i group_58_ids.txt -o group_58_names.txt

#convert to enst
python /u/home/c/chelseaj/project/database/Ensembl/script/ENSG2ENST.py -i group_58_names.txt -d /u/home/c/chelseaj/project/database/Ensembl/ENST_ENSG_ENSP_79.txt -o group_58_enst.txt

# convert to bed file and fasta file
grep -Ff group_58_enst.txt /u/home/c/chelseaj/project/database/Ensembl/ENST_79.bed > group_58_enst.bed
bedtools getfasta -fi /u/home/c/chelseaj/project/database/Ensembl/Genome/79/Homo_sapiens_GRCh38_79_genome.fa -bed group_58_enst.bed -fo group_58_enst.fa -name -split -s


# post data examination:
# examine the signature similarity after comunity detection
python pairwise_distance_v1.py -d select_genes_600 -i group_58_ids.txt -o group_58_corr.txt



