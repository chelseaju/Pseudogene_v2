"""
Usage: python convert_expected_counter_v1.py -d directory -r reference
Input: -d the directory of input and output
	-r reference of gene name to sparse matrix ID
Output: A list of expected count with sparse matrix ID instead of gene name
Function: convert the gene name to sparse matrix ID, and sorted based on row ID
Date: 2015-05-22
Author: Chelsea Ju
"""

import sys, re, pysam, os, random, argparse, datetime

IDs= {}

"""   
    Function : helper function to output message with time
""" 
def echo(msg):
	print "[%s] %s" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(msg))


"""
        Function: build the reference column and row names from general matrix
"""     
def build_IDs(ref):
        ref_fh = open(ref, 'rb')
        rownames = ref_fh.readline()
        colnames = ref_fh.readline()
        count = 1
        for name in colnames.rstrip().split():
                IDs[name] = count
                count = count + 1

"""
	Function: convert the gene name to row ID
"""
def convert_data(infile, outfile):

	output = []
	in_fh = open(infile, 'rb')
	for line in in_fh:
		(name, amount) = line.rstrip().split()
		output.append((IDs[name], amount))

	in_fh.close()

	output = sorted(output, key=lambda x:x[0])
	out_fh = open(outfile, 'w')
	for data in output:
		out_fh.write("%s\t%s\n" %(data[0], data[1]))
	out_fh.close()

def main(parser):
	options = parser.parse_args()
	dir = options.dir
	ref = options.ref

    	## check dir
    	if(dir[-1] != "/"):
        	dir += "/"

	infile = dir + "genes_expected_read_count.txt"
	outfile = dir + "genes_expected_read_count_sparse.txt"
	build_IDs(ref)
	convert_data(infile, outfile)
        
	echo("Writing data to %s" %(outfile))

if __name__ == "__main__":
        
	parser = argparse.ArgumentParser(prog='convert_expected_counter_v1.py')
	parser.add_argument("-d", "--directory", dest="dir", type=str, help="directory of input files", required = True)
        parser.add_argument("-r", "--reference", dest="ref", type=str, help="reference", required = True)
    	main(parser)

