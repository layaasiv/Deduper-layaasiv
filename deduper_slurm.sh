#!/bin/bash

#SBATCH --account=bgmp   ### change this to your actual account for charging
#SBATCH --partition=bgmp       ### queue to submit to
#SBATCH --job-name=bash    ### job name
#SBATCH --output=hostname.out   ### file in which to store job stdout
#SBATCH --error=deduper.err    ### file in which to store job stderr
#SBATCH --time=2:00:00                ### wall-clock time limit, in minutes
#SBATCH --mem=8G              ### memory limit per node, in MB
#SBATCH --nodes=1               ### number of nodes to use
#SBATCH --ntasks-per-node=1     ### number of tasks to launch per node
#SBATCH --cpus-per-task=8       ### number of cores for each task

/usr/bin/time -v /projects/bgmp/layaasiv/bioinfo/Bi624/Deduper-layaasiv/sivakumar_deduper.py \
-f C1_SE_uniqAlign.sorted.sam -u STL96.txt -o deduped_C1_SE_uniqAlign.sorted.sam