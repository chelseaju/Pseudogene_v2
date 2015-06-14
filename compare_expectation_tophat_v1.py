"""
Usage: python compare_expectation_tophat_v1.py
Input: -d the directory of input and output
Output: d/genes_expected_vs_tophat.txt
	format: sparse_id \t expected_count \t tophat_cout \n
Function: Compile the expected number of reads and the read count reported by tophat
	expected number of reads is recorded in genes_expected_read_count_sparse.txt
	tophat count is recorded as the diagonal values in genes_distribution.mtx
Date: 2015-06-08
Author: Chelsea Ju
"""

import sys, re, os, argparse, datetime

GENES = {}

"""
        Function: helper function to output message with time
""" 
def echo(msg): 
        print "[%s] %s" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(msg))


"""
	Extract expected count
"""
def extract_expected_count(filename):
	fh = open(filename, 'r')
	for line in fh:
		(id, count) = line.rstrip().split()
		GENES[id] = [count]
	fh.close()

	echo("Reading Expected Read Count from %s" %(filename))


"""
	Function: Extract read count from tophat (diagonal values from distribution matrix)
"""
def extract_tophat_count(filename):
	fh = open(filename, 'r')

	## remove the first three lines
	line = fh.readline()
	line = fh.readline()
	line = fh.readline()
	
	for line in fh:
		(from_gene, to_gene, count) = line.split()
		if(from_gene == to_gene):
			if(GENES.has_key(from_gene)):
				GENES[from_gene].append(count)
			else:
				echo("Warning, missing expected count for %s" %(from_gene))

	fh.close()

	echo("Reading Tophat Read Count from %s" %(filename))

"""
	Function: export read count comparison to file
"""
def export_data(filename):
	fh = open(filename, 'wb')
	
	for k in GENES.keys():
		fh.write("%s\t%s\n" %(k, "\t".join(GENES[k])))
	
	fh.close()
	echo("Writing Expected and Tophat Read Count to %s" %(filename))

def main(parser):
	options = parser.parse_args()
	dir = options.dir
	
	## check dir
	if(dir[-1] != "/"):
		dir += "/"
	
	expected_file = dir + "mapping/genes_expected_read_count_sparse.txt"
	matrix_file = dir + "mapping/genes_distribution.mtx"
	outfile = dir + "mapping/genes_expected_tophat_comparison.txt"

	extract_expected_count(expected_file)
	extract_tophat_count(matrix_file)
	export_data(outfile)



if __name__ == "__main__":
        parser = argparse.ArgumentParser(prog='compare_expectation_tophat_v1.py')
        parser.add_argument("-d", "--directory", dest="dir", type=str, help="directory of input files", required = True)
        main(parser)









