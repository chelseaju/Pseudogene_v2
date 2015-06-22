"""
Usage: python compare_expectation_tophat_v2.py
Input: -x distribution matrx
	-y expectation
	-o output tophat prediction
Output:	format = sparse_id \t expected_count \t tophat_cout \n
Function: Compile the expected number of reads and the read count reported by tophat
	expected number of reads is recorded in X_101L_A_expected_Y.txt
	tophat count is recorded as the column sum of distribution matrix
Date: 2015-06-22
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
		GENES[id] = [int(count)]
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
		if(GENES.has_key(to_gene)):
			GENES[to_gene].append(int(count))

	fh.close()

	echo("Reading Tophat Read Count from %s" %(filename))

"""
	Function: export read count comparison to file
"""
def export_data(filename):

	fh = open(filename, 'wb')
	
	for k in sorted(GENES.keys()):
		expected = GENES[k][0]
		predicted = sum(GENES[k][1:])
		if(expected > 0):
			error = float(abs(predicted - expected)) / float(expected)
		else:
			error = 0
		fh.write("%s\t%d\t%d\t%f\n" %(k, expected, predicted, error))
	
	fh.close()
	echo("Writing Expected and Tophat Read Count to %s" %(filename))

def main(parser):
	options = parser.parse_args()
	x_file = options.d_matrix
	y_file = options.expected
	outfile = options.outfile
	
	extract_expected_count(y_file)
	extract_tophat_count(x_file)
	export_data(outfile)



if __name__ == "__main__":
        parser = argparse.ArgumentParser(prog='compare_expectation_tophat_v2.py')
	parser.add_argument("-x", "--d_matrix", dest="d_matrix", type=str, help="filename of distribution matrix", required = True)
	parser.add_argument("-y", "--expected", dest="expected", type=str, help="expected count", required = True)
	parser.add_argument("-o", "--outfile", dest="outfile", type=str, help="filename of output", required = True)
        main(parser)
