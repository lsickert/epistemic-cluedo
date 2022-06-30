#!/bin/bash

#SBATCH --job-name=train_model
#SBATCH --mem=50000
#SBATCH --time=0:30:00
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=thijsvisee@gmail.com
#SBATCH --array=1
#SBATCH --partition=short
#SBATCH --output=%j.out


python3 main.py < medium_game.txt
