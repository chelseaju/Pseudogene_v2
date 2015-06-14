"""
Usage: python pairwise_distance_v1.py -d directory -i input_gene_ids -o output -m jaccard
Input: -d the directory of input and output
	-i input filename
	-o output filename
	-m distance measure
Output: A distance matrix
Function: Compute the distance between genes
Date: 2015-06-05
Author: Chelsea Ju
"""

import sys, re, os, argparse, datetime

GENES = []
DISTRIBUTION = {}



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
	Function: build distribution reference
"""
def build_distribution(distfile):
	dist_fh = open(distfile, 'r')
	
	# skip three lines
	line = dist_fh.readline()
	line = dist_fh.readline()
	line = dist_fh.readline()

	for line in dist_fh:
		(row_id, col_id, count) = line.split()
		if(not DISTRIBUTION.has_key(int(row_id))):
			DISTRIBUTION[int(row_id)] = {}
		DISTRIBUTION[int(row_id)][int(col_id)] = int(count)
	
	dist_fh.close() 		
	
	echo("Building distribution from %s" %(distfile))

"""
	Function: compute dimilarity with given methods
"""
def compute_similarity(infile, method, outfile):
	
	ids = []
	infh = open(infile, 'r')
	for line in infh:
		ids.append(int(line.rstrip()))
	infh.close()

	outfh = open(outfile, 'wb')

	# print out column names
	for c_id in ids:
		outfh.write("%s\t" %(GENES[c_id]))
	outfh.write("\n")

	for r_id in ids:
		outfh.write("%s\t" %(GENES[r_id]))
		for c_id in ids:
			
			coef = 0
			if(method == "jaccard"):
				coef = jaccard_similarity(r_id, c_id)
				print coef


			outfh.write("%d\t" %(10))
		outfh.write("\n")
	outfh.close()

	echo("Similarity Matrix is written to %s" %(outfile))

"""
	Function: compute the jaccard similarity
	J(A, B) = (A and B) / (A or B)
"""
def jaccard_similarity(A, B):
	AA = 0
	AB = 0
	BA = 0
	BB = 0

	if(DISTRIBUTION.has_key(A)):
		if(DISTRIBUTION[A].has_key(A)):
			AA = DISTRIBUTION[A][A]
		if(DISTRIBUTION[A].has_key(B)):
			AB = DISTRIBUTION[A][B]
	
	if(DISTRIBUTION.has_key(B)):
		if(DISTRIBUTION[B].has_key(A)):
			BA = DISTRIBUTION[B][A]
		if(DISTRIBUTION[B].has_key(B)):
			BB = DISTRIBUTION[B][B]
		
	if( AB + BA == 0):
		return 0
	else:
		return float(AB + BA) / float(AA + AB + BA + BB)


def main(parser):
	options = parser.parse_args()
	dir = options.dir
	input = options.input
	output = options.output
	method = options.method

	## check dir
	if(dir[-1] != "/"):
		dir += "/"

	infile = dir + "results/community/" + input
	outfile = dir + "results/community/" + output
	refile = dir + "mapping/genes_distribution.name"
	distfile = dir + "mapping/genes_distribution.mtx"
	build_IDs(refile)
	build_distribution(distfile)
	compute_similarity(infile, method, outfile)




if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog='pairwise_distance_v1.py')
	parser.add_argument("-d", "--directory", dest="dir", type=str, help="directory of input files", required = True)
	parser.add_argument("-i", "--inputfile", dest="input", type=str, help="input filename", required = True)
	parser.add_argument("-o", "--outputfile", dest="output", type=str, help="output filename", required = True)
	parser.add_argument("-m", "--method", dest="method", type=str, help="similarity method", required = True)
	main(parser)

