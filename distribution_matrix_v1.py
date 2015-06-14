"""
Usage: python distribution_matrix_v1.py -d directory -r reference
Input: -d the working directory
	-r reference for column and row names
Output: genes_distribution_sparse.matrix
Function: Reformat the data from distribution.eqn to sparse matix

Author: Chelsea Ju
Date: 2014-01-09
"""
import sys, re, os, random, argparse, glob, datetime
import numpy as np
from scipy import sparse, io as sparse_io


IDs = {}

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
	count = 0
	for name in colnames.rstrip().split():
		IDs[name] = count
		count = count + 1

	return (len(rownames.split()), len(colnames.split()))


"""
	Function: write the distribution matrix to file
"""

def retrieve_distribution(input, output, row_count, col_count):
	row_index = []
	col_index = []
	value = []

	input_fh = open(input, 'rb')
	for line in input_fh:
		(lhs, amount, rhs) = line.split()
#		lhs_unknown = re.match("^unknown", lhs)
#		rhs_unknown = re.match("^unknown", rhs)
		if(IDs.has_key(lhs) and IDs.has_key(rhs)):
			row_index.append(IDs[lhs])
			col_index.append(IDs[rhs])
			value.append(int(amount))
		else:
			echo("Warning, %s %s %s does not exist" %(lhs, amount, rhs))
	input_fh.close()

	# write to sparse matrix COO format
	row = np.array(row_index)
	col = np.array(col_index)
	data = np.array(value)
	mtx = sparse.csr_matrix((data, (row, col)), shape=(col_count, col_count))
	sparse_io.mmwrite(output, mtx)


def main(parser):
    
	options = parser.parse_args()
	dir = options.dir
	ref = options.ref    	

	## check dir
	if(dir[-1] != "/"):
        	dir += "/"

	## build reference
	(row_size, col_size) = build_IDs(ref)

	# distribution equation file
	distribution_list = dir + "genes_distribution.txt"
	distribution_matrix = dir + "genes_distribution"
    	retrieve_distribution(distribution_list, distribution_matrix, row_size, col_size)
    
   	echo("Writing Distribution Matrix to %s.mtx" %(distribution_matrix)) 

if __name__ == "__main__":   
   
	parser = argparse.ArgumentParser(prog='distribution_matrix_v1.py')
	parser.add_argument("-d", "--directory", dest="dir", type=str, help="directory of input files", required = True)
	parser.add_argument("-r", "--reference", dest="ref", type=str, help="reference of column and row name", required = True)

    	main(parser)
