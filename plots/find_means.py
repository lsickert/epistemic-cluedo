import os
from os import sep as s

from numpy import mean

def averages_for_file(filename, agent_order):
    vals = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            values = [int(x) for x in line.split(' ')[:-1]]
            for idx, value in enumerate(values):
                if len(vals) <= idx // 2:
                    vals.append([])
                vals[idx // 2].append(value)
    
    means = []
    for val in values:
        means.append(mean(val))
    return means
    

def get_means():
    means = {}
    for folder in os.listdir(f'.{s}results'):
        #Load run.txt in folder
        means[folder] = {}
        for filename in os.listdir(f".{s}results{s}{folder}"):
            if "run" in filename:
                continue

            filepath = f".{s}results{s}{folder}{s}{filename}"
            means[folder][filename[0]] = averages_for_file(filepath, folder)

    for k, v in means.items():
        print(k)
        print(v)
        print('')

get_means()