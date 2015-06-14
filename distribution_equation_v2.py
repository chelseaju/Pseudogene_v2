"""
Usage: python distribution_equation.py -d directory
Input: -d the working directory 
Output: genes_distribution.eqn 
Function: formulate the distribution using equation
    for example: 108 * ORIGIN_1 = 100 * REGION_1 + 8 * REGION_2

Author: Chelsea Ju
Date: 2014-01-08
"""

import sys, re, os, random, argparse, glob, datetime

# Each item contains an array of information. 
# The first element is the expected count, and the following elements are tuples of (count, mapped_region)
EQUATION_HASH = {}

"""
    Function : helper function to output message with time
"""
def echo(msg):
    print "[%s] %s" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(msg))


"""
    Function: initiate the equation hash by building the LHS of the equation
        ie     X * ORIGIN = RHS
"""
def equation_LHS(input):
    
    input_fh = open(input, 'rb')
    
    for line in input_fh:
        line = line.strip()
        (id, count) = line.split("\t")
        if(EQUATION_HASH.has_key(id)):
            EQUATION_HASH[id][0] += int(count)
        else:
            EQUATION_HASH[id] = [int(count)]
    input_fh.close()

"""
    Function: build the RHS of the equation
        ie     LHS = X * REGION1 + Y * REGION2 + X * REGION3
"""
def equation_RHS(input):
    
    input_fh = open(input, 'rb')
    for line in input_fh:
        line = line.rstrip()
        (origin, count, mapped) = line.split("\t")
	if(EQUATION_HASH.has_key(origin)):
        	EQUATION_HASH[origin].append((int(count), mapped))
	else:
		EQUATION_HASH[origin] = [0, (int(count), mapped)]
    input_fh.close()

"""
    Function: write data to file
"""
def export_data(output):

    output_fh = open(output, 'w')
    
    for k in sorted(EQUATION_HASH.keys()):
        v = EQUATION_HASH[k]
        # output region with mapped reads
        if(len(v) > 0):
            output_fh.write("%d * %s = " %(v[0], k)) # LHS            
            for (count, name) in v[1:]:
                output_fh.write("%d * %s + " %(count, name))            
            output_fh.write("\n")
    
    output_fh.close()
    
    echo("Writing Distribution Equation: %s" %(output))
    
def main(parser):
    
    options = parser.parse_args()
    dir = options.dir
    
    ## check dir
    if(dir[-1] != "/"):
        dir += "/"

    # file for expected count        
    expected_count_file = dir + "genes_expected_read_count.txt"
    equation_LHS(expected_count_file)

    # distribution count
    observed_count_file = dir + "genes_distribution.txt"
    equation_RHS(observed_count_file)

    # outfile
    outfile = dir + "genes_distribution.eqn"
    export_data(outfile)


if __name__ == "__main__":   
   
    parser = argparse.ArgumentParser(prog='distribution_equation_v2.py')
    parser.add_argument("-d", "--directory", dest="dir", type=str, help="directory of input files", required = True)

    main(parser)
