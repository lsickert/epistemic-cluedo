#!/bin/bash

#SBATCH --job-name=train_model
#SBATCH --mem=16000
#SBATCH --time=0:30:00
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=thijsvisee@gmail.com
#SBATCH --array=1
#SBATCH --partition=short
#SBATCH --output=own_all_%j.out

module purge
module load module load Python/3.8.6-GCCcore-10.2.0

source /data/$USER/.envs/first_env/bin/activate

pip install -r requirements.txt
python3 main.py
