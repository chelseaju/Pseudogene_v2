""" global_genes_mapper_v1.py
Usage: python global_genes_mapper_v1.py -d directory 
Input: -d input/output directory 
Output: lines of gene region or unknown region with {name \t chr \t start \t end \n}
Function: 1. intersect a list of reads to ensembl gene database
          2. collapse the unmatch reads to create unknown region 

Date: 2014-03-02
Author: Chelsea Ju
Update from gene_identifier.py
"""
import sys, re, os, subprocess, random, argparse, datetime

# LAB
#DB = "/home/chelseaju/Database/Pseudogene/ParentENSG_Pseudogene_74.bed"
#ENSEMBL_GENE = "/home/chelseaju/Database/Ensembl/ENSG_74.bed"
#PARENT_GENE = "/home/chelseaju/Database/Pseudogene/Parent_ENST_74.bed"
#PSEUDO_GENE = "/home/chelseaju/Database/Pseudogene/Pseudogene_74.bed"

# HOFFMAN
#DB = "/u/home/c/chelseaj/project/database/Pseudogene/ParentENSG_Pseudogene_74.bed"
ENSEMBL_GENE = "/u/home/c/chelseaj/project/database/Ensembl/ENSG_79.bed"
ENST_ENSG_ENSP="/u/home/c/chelseaj/project/database/Ensembl/ENST_ENSG_ENSP_79.txt"
#PARENT_GENE = "/u/home/c/chelseaj/project/database/Pseudogene/Parent_ENSG_74.bed"
#PSEUDO_GENE =  "/u/home/c/chelseaj/project/database/Pseudogene/Pseudogene_74.bed"

# MAC
#ENSEMBL_GENE = "/Users/Chelsea/Bioinformatics/CJDatabase/Ensembl/ENST_74.bed"
#PARENT_GENE = "/Users/Chelsea/Bioinformatics/CJDatabase/Pseudogene/Parent_ENST_74.bed"
#PSEUDO_GENE = "/Users/Chelsea/Bioinformatics/CJDatabase/Pseudogene/Pseudogene_74.bed"

GENELIST = {}
ENST_REF = {}

"""
    Function : helper function to output message with time
"""
def echo(msg):
    print "[%s] %s" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(msg))

"""
	Function : build the reference for ENST to ENSG conversion
"""
def build_ENST_ref():
	fh = open(ENST_ENSG_ENSP, "r")
	for line in fh:
		(ENST, ENSG, ENSP) = line.split("\t")
		ENST_REF[ENST] = ENSG
	fh.close()


"""
    Function: map reads to known gene    
"""
def map_reads_to_gene(input_file, database):

	unknown = []  

	if(os.stat(input_file)[6]!=0):
		# needs to convert bam to bed first
		mapping = subprocess.check_output(["bedtools", "intersect", "-wb", "-loj", "-a", input_file, "-b", database])
		mapping_data = mapping.split("\n")

		for m in mapping_data:
			data = m.split("\t")
			if(len(data) > 2 and len(data[3]) > 3):
				mapped_gene_name = data[9]
				read_name = data[3]

				prefix_match = re.match(r"(.*)/\d", read_name)
				if(prefix_match):
					read_name = prefix_match.group(1)
				
				# found mapped gene
				if(mapped_gene_name != "-1" and mapped_gene_name != "."):
					## calculate overlapped interval => end - start
					## end = min(seq_end, read_end)
					## start = max(seq_start, read_start)
					if(GENELIST.has_key(read_name)):
						GENELIST[read_name].append(mapped_gene_name)
					else:
						GENELIST[read_name] = [mapped_gene_name]
				else:
					unknown.append("%s\t%s\t%s\t%s\t%s\t%s\n" %(data[0], data[1], data[2], data[3], data[4], data[5])) 

	return  unknown


"""
	Function: Compute read distribution on gene level and output to file
"""
def compute_distribution(file, title):

	distribution = {}
	for g in GENELIST.keys():
		# conver the origin to ENSG
		prefix_match = re.match(r"(.*?):.*", g)
		if(prefix_match):
			origin_enst = prefix_match.group(1)
			origin_ensg = ENST_REF[origin_enst]	

			if(not distribution.has_key(origin_ensg)):
				distribution[origin_ensg] = {}

			# iterate through all mapped loci
			for loci in set(GENELIST[g]):
				if(distribution[origin_ensg].has_key(loci)):
					distribution[origin_ensg][loci] = distribution[origin_ensg][loci]  + 1
				else:
					distribution[origin_ensg][loci] = 1
	
	# write data to file
	fh = open(file, 'w')
	colnames = []
	rownames = []
	for k in sorted(distribution):
		rownames.append(k)
		for l in distribution[k]:
			fh.write("%s\t%d\t%s\n" %(k, distribution[k][l], l))
			colnames.append(l)

	fh.close()
	echo("Write to Distribution File: %s" %(file))

	# write column and row name to file
	title_fh = open(title, 'w')
	for name in rownames:
		title_fh.write("%s\t" %(name))	
	title_fh.write("\n")

	for name in rownames:
		title_fh.write("%s\t" %(name))
	
	for name in sorted(set(colnames)):
		if(not name in rownames):
			title_fh.write("%s\t" %(name))
	title_fh.write("\n")

	title_fh.close()

	echo("Write Column/Row name to file: %s" %(title))
	

""" 
	Function : Collapse unknown region
"""
def collapse_unknown(unknown):
	
	# sort
	unknown = sorted(unknown)
	previous_chr = "0"
	previous_start = 0
	previous_end = 0
	reads = []
	
	for u_data in unknown:
		(current_chr, current_start, current_end, current_name, current_num, current_strand) = u_data.split("\t")
		
#		prefix_match = re.match(r"(.*):", current_name)
#		if(prefix_match):
#			current_name = prefix_match.group(1)

		# check if they mapped to the same chromosome
		## check if they overlapped or the overlapped is within 80bp gap
		if((previous_chr == current_chr) and (int(current_start) - int(previous_end) < 80)):
			previous_start = current_start
			previous_end = current_end
			reads.append(current_name)
		else:
			if(not previous_chr == "0"):
				name = "unknown_" + previous_chr + "_" + str(previous_start) + "_" + str(previous_end)
				for r in reads:
					if(GENELIST.has_key(r)):
						GENELIST[r].append(name)
					else:
						GENELIST[r] = [name]		

	
			previous_chr = current_chr
			previous_start = current_start
			previous_end = current_end
			reads = [current_name]

	if(not previous_chr == "0"):
		name = "unknown_" + previous_chr + "_" + str(previous_start) + "_" + str(previous_end)
		for r in reads:
			if(GENELIST.has_key(r)):
				GENELIST[r].append(name)
			else:
				GENELIST[r] = [name]


       
def main(parser):

	options = parser.parse_args()
	dir = options.dir

	## check dir
	if(dir[-1] != "/"):
		dir += "/"

	## input file
	input_file = dir + "accepted_hits.bed" 

	## output file
	output_file = dir + "genes_distribution.txt"
	output_title = dir + "genes_distribution.name"

	# map to parents and pseudogene
#	unknown = map_reads_to_gene(input_file, DB)
#	export_temp_unknown(unknown, output_temp)

	# map to all genes
#	unknown = map_reads_to_gene(output_temp, ENSEMBL_GENE)
	unknown = map_reads_to_gene(input_file, ENSEMBL_GENE)	

	# collapse unknown
	collapse_unknown(unknown)

	# build reference file to convert ENST to ENSG
	build_ENST_ref()
	
	# output distribution
	compute_distribution(output_file, output_title)


if __name__ == "__main__":   
   
    parser = argparse.ArgumentParser(prog='global_genes_mapper_v1.py')
    parser.add_argument("-d", "--directory", dest="dir", type=str, help="directory of input and output files", required = True)

    main(parser)
