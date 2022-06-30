#!/bin/bash

#SBATCH --job-name=train_model
#SBATCH --mem=16000
#SBATCH --time=0:50:00
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=thijsvisee@gmail.com
#SBATCH --array=1
#SBATCH --partition=gpushort
#SBATCH --gres=gpu:1
#SBATCH --output=own_all_%j.out


pip install -r requirements.txt
python3 main.py
