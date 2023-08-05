#!/bin/bash
#PBS -N defect_group3_q=p2_sp
#PBS -l nodes=1:ppn=1,pvmem=1000mb
#PBS -l walltime=24:00:00
NN=`cat $PBS_NODEFILE | wc -l`
echo "Processors received = "$NN
echo "script running on host `hostname`"
cd $PBS_O_WORKDIR
echo "PBS_NODEFILE"
cat $PBS_NODEFILE
//share/apps/vasp5.2_cNEB > vasp.out
