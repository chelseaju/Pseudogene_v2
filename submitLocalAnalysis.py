import os
import time
import random
import sys, traceback
import subprocess
from subprocess import Popen, PIPE
import argparse

COVERAGE = [5, 7, 10, 15, 13, 17, 20, 23, 27, 30]
ABUNDANCE = [4, 6, 8, "R1", "R2", "R3"]

#COVERAGE = [5,7,10,13,15,17,20,23,27,30]
#ABUNDANCE = ["R2", "R3"]



TEMPLATE_SERIAL = """
#####################################
#$ -S /bin/bash
#$ -cwd
#$ -N {name}
#$ -e {errfile}
#$ -o {logfile}
#$ -pe make {slots}
#####################################

. /u/local/Modules/default/init/modules.sh
module load samtools
module load python/2.7
module load bedtools

export PATH=$PATH:/u/home/c/chelseaj/project/software/tophat-2.0.9.Linux_x86_64
export PATH=$PATH:/u/home/c/chelseaj/project/software/bowtie2-2.0.6

echo "------------------------------------------------------------------------"
echo "Job started on" `date`
echo "------------------------------------------------------------------------"
{script}
echo "------------------------------------------------------------------------"
echo "Job ended on" `date`
echo "------------------------------------------------------------------------"
"""

def main(parser):

        options = parser.parse_args()
        dir = options.dir

        if(dir[-1] == "/"):
                dir = dir[:len(dir)-1]

        inputPath="/u/scratch/c/chelseaj/Pseudogene_Journal/%s/scripts" %(dir)
        outputPath="/u/scratch/c/chelseaj/Pseudogene_Journal/%s/logs" %(dir)

        if not os.path.exists(inputPath):
                os.makedirs(inputPath)

        if not os.path.exists(outputPath):
                os.makedirs(outputPath)



	for c in COVERAGE:
		for a in ABUNDANCE:
			suffix = "X" + str(c) + "_101L_A" + str(a) 

			#make the bash file to submit
			scriptfile = inputPath + "/" + suffix + "_analysis.qsub"
			logfile = outputPath + "/" + suffix + "_analysis.log"
			errfile = outputPath + "/" + suffix + "_analysis.err"

			script = "bash local_analysis_v1.sh %s %sX_%sL_%sA %s" %(dir, c, "101", a, "101")
			scriptFILEHandler = open(scriptfile, 'wb');
			scriptFILEHandler.write(TEMPLATE_SERIAL.format(script=script, name=suffix, logfile=logfile, errfile=errfile, slots=1))
			scriptFILEHandler.close();
			subprocess.call('qsub -cwd -m ea -l h_rt=24:00:00,h_data=6G ' + scriptfile, shell=True)
			print "qsub -cwd -m ea -l h_rt=24:00:00,h_data=6G %s" %(scriptfile)


if __name__ == "__main__":
        parser = argparse.ArgumentParser(prog='submitLocalAnalysis.py')
        parser.add_argument("-d", "--dir", dest="dir", type=str, help="directory", required = True)
        main(parser)

