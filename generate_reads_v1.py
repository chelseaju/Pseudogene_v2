"""
Usage: python generate_reads_v1.py -d directory
Input: -d the directory of input and output files -l read_length
Output: reads in BED format
Funtion: generate reads for a list of given genes in a sliding window approach (not randomly selected from a position). The output is in bed format, and can be converted to fasta through bedtool.
Date: 2015-05-12
Author: Chelsea Ju
"""

import sys, re, argparse, datetime

"""
	Function : helper function to output message with time
"""
def echo(msg):
	print "[%s] %s" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(msg))


"""
	Function : generate reads using sliding window approach
"""
def read_generation(input, output, readL):
	infh = open(input, 'r')
	outfh = open(output, 'w')

	for line in infh:
		data = line.rstrip().split()
		chr = data[0]
		g_start = int(data[1])
		g_end = int(data[2])
		name = data[3]
		strand = data[4]
		sizes = data[10].split(",")
		starts = data[11].split(",")


		#### need more time to debug
		for block_index in xrange(len(starts)):
			(block_start, block_end) = (int(starts[block_index]), int(starts[block_index] + sizes[block_index]))

			for i in xrange(block_start, block_end):
				print "=============================== %d ======================" %(i)
				if( (i + readL) < g_end):
					read_current_start = i
					remain_length = readL
					block_examine = block_index
					block_examine_end = int(starts[block_examine]) + int(sizes[block_examine])

					# write reads into bed format
					read_block_start = []
					read_block_size = []

				 	while(block_examine < len(starts) and ((read_current_start + remain_length) >= block_examine_end)):
						# keep track of the segmant of each block
						read_block_start.append(read_current_start)
						read_block_size.append(block_examine_end - read_current_start)

						# move to the next block
						remain_length = remain_length - (block_examine_end - read_current_start)
						block_examine = block_examine + 1

						if(block_examine < len(starts)):
							block_examine_end = int(starts[block_examine]) + int(sizes[block_examine])
							read_current_start = int(starts[block_examine])

					if( remain_length > 0 and block_examine < len(starts)):
						# add the remaining to the block
						read_block_start.append(read_current_start)
						read_block_size.append(remain_length)


					if(sum(read_block_size) == readL):
						print name, read_block_start[0] + g_start, read_block_start[-1] + read_block_size[-1] + g_start
						print name, ",".join(str(st+g_start) for st in read_block_start)
						print name, read_block_size





def main(parser):
	options = parser.parse_args()
	dir = options.dir
	readL = options.readL

	##check dir
	if(dir[-1] != "/"):
		dir += "/"

	## list of gene in bed format
	enst_bed = dir + "SELECT_ENST.bed"
	read_bed = dir + "reads_" + str(readL) + "L.bed"	

	read_generation(enst_bed, read_bed, readL)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="generate_reads_v1.py")
	parser.add_argument("-d", "--directory", dest="dir", type=str, help="directory of input files", required = True)
	parser.add_argument("-l", "--readlength", dest = "readL", type=int, help="read length", required = True)

	main(parser)
