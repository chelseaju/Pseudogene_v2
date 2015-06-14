"""abundance_assigner.py
Usage: python abundance_assigner.py -i genelist -a abundance -o output
Input: -i a list of ENST ids
	 -a abundance, could be number or RANDOM
Output: -o a list of ENST ids with their abundance separated by space
Function: assign abundance to the gene of interests
Author: Chelsea Ju
Date: 2014-03-11
"""

import sys, os, re, argparse, random

MIN = 5
MAX = 10

"""
	Function : assign abundance to each gene
		If abundance = RANDOM, random abundance is assigned
		Otherwise, fix number of abundance is used
"""
def assigner(infh, outfh, abundance):
	if(abundance[0] == "R"):
		for line in infh:
			line = line.rstrip()
			a = random.randint(MIN, MAX)

			outfh.write("%s %d\n" %(line, a))

	else:
		a = int(abundance)
		for line in infh:
			line = line.rstrip()
			outfh.write("%s %d\n" %(line, a))


def main(parser):
	options = parser.parse_args()
	infile = options.input
	outfile = options.output
	abundance = options.abundance

	infh = open(infile, 'rb')
	outfh = open(outfile, 'w')

	assigner(infh, outfh, abundance)	

	infh.close()
	outfh.close()

	print ""
	print "Abundance Data Written in %s" %(outfile)


if __name__ == "__main__":   
   
    parser = argparse.ArgumentParser(prog='abundance_assigner.py')
    parser.add_argument("-i", "--input", dest="input", type=str, help="file with gene ids", required = True)
    parser.add_argument("-a", "--abundance", dest="abundance", type=str, help="singer integer or RXX", required = True)
    parser.add_argument("-o", "--output", dest="output", type=str, help="gene ids and their abundance", required = True)

    main(parser)

