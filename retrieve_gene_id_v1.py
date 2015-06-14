"""
Usage: python retrieve_gene_id_v1.py -d directory -i input -o output
Input: -d the directory of input and output
	-i input filename
	-o output filename
Output: A list of gene names based on the input id
Function: Decompress the sparse matrix by retrieving the gene name of a list of give IDs
Date: 2015-06-01
Author: Chelsea Ju
"""

import sys, re, os, argparse, datetime

GENES = []
"""
	Function: helper function to output message with time
"""
def echo(msg):
        print "[%s] %s" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(msg))

"""
	Function: build reference database
"""
def build_IDs(ref):
	ref_fh = open(ref, 'r')
	line = ref_fh.readline()
	colnames = ref_fh.readline()
	for c in colnames.rstrip().split():
		GENES.append(c)
	ref_fh.close()

	echo("Building reference from %s" %(ref))

"""
	Function: retrieve gene names from database
"""
def retrieve_names(infile, outfile):
	infh = open(infile, 'r')
	outfh = open(outfile, 'w')

	for line in infh:
		line = line.rstrip().split()
		outfh.write("%s\n" %(GENES[int(line[0])]))

	outfh.close()
	infh.close()
	
	echo("Writing gene names to %s" %(outfile))

def main(parser):
	options = parser.parse_args()
	dir = options.dir
	input = options.input
	output = options.output
	
	## check dir
	if(dir[-1] != "/"):
		dir += "/"

	infile = dir + "results/community/" + input
	outfile = dir + "results/community/" + output
	refile = dir + "mapping/genes_distribution.name"
	build_IDs(refile) 	
	retrieve_names(infile, outfile)



if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog='retrieve_gene_id_v1.py')
	parser.add_argument("-d", "--directory", dest="dir", type=str, help="directory of input files", required = True)
	parser.add_argument("-i", "--inputfile", dest="input", type=str, help="input filaname", required = True)
	parser.add_argument("-o", "--outfile", dest="output", type=str, help="output filename", required = True)
	main(parser)

