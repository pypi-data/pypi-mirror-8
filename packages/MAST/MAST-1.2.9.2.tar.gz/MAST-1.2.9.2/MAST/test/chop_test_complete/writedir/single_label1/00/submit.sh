#!/bin/bash
#PBS -N 00
#PBS -l nodes=1:ppn=8,pvmem=1000mb
#PBS -l walltime=24:00:00
##export all environment variables. 
#PBS -V
NN=`cat $PBS_NODEFILE | wc -l`
echo "Processors received = "$NN
echo "script running on host `hostname`"
cd $PBS_O_WORKDIR
echo "PBS_NODEFILE"
cat $PBS_NODEFILE
mpiexec vasp
