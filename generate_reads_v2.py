"""
Usage: python generate_reads_v2.py -d directory
Input: -d the directory of input and output files -l read_length
Output: reads in fasta format
Funtion: generate reads for a list of given genes in a sliding window approach (not randomly selected from a position). The output is in fasta format.
Date: 2015-05-16
Author: Chelsea Ju
"""

import sys, re, argparse, datetime

"""
	Function : helper function to output message with time
"""
def echo(msg):
	print "[%s] %s" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(msg))


"""
	Function : convert to reverse complimentary sequence
"""
def rc(seq):
	seq = seq[::-1]

	seq = seq.replace("A", "Z")
	seq = seq.replace("T", "A")
	seq = seq.replace("Z", "T")
	seq = seq.replace("C", "Z")	
	seq = seq.replace("G", "C")
	seq = seq.replace("Z", "G")
	
	return seq




"""
	Function : Sliding window approach to retrieve sequence
"""
def sliding_window(seq, name, readL, fh):

	for index in xrange(0, len(seq) - readL + 1 ):
		fh.write(">%s_%d_%d\n" %(name, index, index+readL))
		fh.write("%s\n" %(seq[index:index+readL]))

#		print name, seq[index:index+readL] // for debugging

"""
	Function : generate reads using sliding window approach
"""
def read_generation(input, output, readL):
	infh = open(input, 'r')
	outfh = open(output, 'w')

	enst_name = ""
	for line in infh:
		line = line.rstrip()
		header_match = re.match(r"^>(.*)", line)

		if(header_match):
			enst_name = header_match.group(1)

		else:
			sliding_window(line.upper() , enst_name + ":FORWARD", readL, outfh)
			sliding_window(rc(line.upper()), enst_name + ":REVERSE", readL, outfh)
	
	infh.close()
	outfh.close()

def main(parser):
	options = parser.parse_args()
	dir = options.dir
	readL = options.readL

	##check dir
	if(dir[-1] != "/"):
		dir += "/"

	## list of transcripts in fasta format
	enst_fa = dir + "SELECT_ENST.fa"
	read_fa = dir + "READS_" + str(readL) + "L.fa"	

	read_generation(enst_fa, read_fa, readL)

	echo("Writing reads to %s" %(read_fa))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="generate_reads_v2.py")
	parser.add_argument("-d", "--directory", dest="dir", type=str, help="directory of input files", required = True)
	parser.add_argument("-l", "--readlength", dest = "readL", type=int, help="read length", required = True)

	main(parser)
