#!/bin/bash

#SBATCH -t ?mast_walltime?
#SBATCH -J ?mast_name?
#SBATCH -N ?mast_nodes?
#SBATCH -n ?mast_processors?
#SBATCH -p ?mast_queue?
#SBATCH --ntasks-per-node=?mast_ppn?
?mast_exec?
