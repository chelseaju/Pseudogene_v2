"""
Usage: python expected_counter_v3.py -d directory
Input: -d the directory and prefix of output files
Output: A list of gene with the number of reads. {transcript_name \t number_of_read}
Function: Assuming read with the same prefix (transcript name) comes from the same transcript.
        The script iterates through the bam file and count expected number of read for each transcript.
	Paired-end read are treated as two single reads
Date: 2013-12-29
Author: Chelsea Ju
Note: this script is adopted from fragments_counter
"""

import sys, re, pysam, os, random, argparse, datetime


"""
    Function : helper function to output message with time
"""
def echo(msg):
    print "[%s] %s" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(msg))


"""
    iterate through the bam file, which is sorted by the read name
    the file may contain multiple alignments and pair end mates, so the read is only counted when seen the first time
"""
def expected_read_counter(sorted_input):
    
    expected_hash = {}
    previous_read = ""
    sorted_bam_fh = pysam.Samfile(sorted_input)

    for read in sorted_bam_fh:
        name = read.qname

        # the first time seeing this read  
        # (note: reads contain multiple alignment, but each read is counted once)
	# (note: paired end read is counted once since they have the same read name in bam)
        if(name != previous_read):
            prefix_match = re.match(r"(.*?):.*", name)
            if(prefix_match):
                prefix = prefix_match.group(1)
    
                # if the read name exists
                if(expected_hash.has_key(prefix)):
                    expected_hash[prefix] += 1
                else:
                    expected_hash[prefix] = 1
        
        # update previous_read
        previous_read = name
    
    sorted_bam_fh.close()
    return expected_hash
        
"""
    write the expected counts to file
"""
def export_array(hash, outfile):
    out_fh = open(outfile, "w")

    for k, v in hash.items():
        out_fh.write("%s\t%s\n" %(k,str(v)))
    
    out_fh.close()
    
    echo("Writing Expected Count to File : %s" %(outfile)) 

        

def main(parser):
    
    options = parser.parse_args()
    dir = options.dir
    
    ## check dir
    if(dir[-1] != "/"):
        dir += "/"

    ## start counting the readd
    sorted_bam = dir + "accepted_hits_sortedByName.bam"
    counts_hash = expected_read_counter(sorted_bam)
      
    ## output data
    outfile = dir + "transcripts_expected_read_count.txt"
    export_array(counts_hash, outfile)



if __name__ == "__main__":   
   
    parser = argparse.ArgumentParser(prog='expected_counter.py')
    parser.add_argument("-d", "--directory", dest="dir", type=str, help="directory of input files", required = True)

    main(parser)
