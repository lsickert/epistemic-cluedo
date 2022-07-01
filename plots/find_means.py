import os
from os import sep as s

from numpy import mean

def averages_for_file(filename, agent_order):
    vals = []
    with open(filename, "r") as f:
        lines = f.readlines()
        ix = 0
        for line in lines:
            values = [int(x) for x in line.split(' ')[:-1]]
            for idx, value in enumerate(values):
                if len(vals) <= idx // 2:
                    vals.append([])
                vals[idx // 2].append(value)
    
    means = []
    for val in vals:
        avg = mean(val)
        avg = int(avg) if avg % 1 < 0 else int(avg+1)
        means.append(avg)
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
        
        for x in ['0', '1', '2']:
            if x not in means[folder]:
                means[folder][x] = []

    return means


means = get_means()

print(means['2200']['0'])
print(means['2200']['1'])
print(means['2200']['2'])
print(means['2200'])