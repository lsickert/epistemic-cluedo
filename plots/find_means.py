import os
from os import sep as s

from numpy import mean
import matplotlib.pyplot as plt

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

lib = get_means()

results = []
results.append(lib['1100']['1'])
results.append(lib['1100']['0'])
results.append(lib['2200']['2'])
results.append(lib['2200']['0'])
results.append(lib['2211']['2'])
results.append(lib['2211']['1'])
results.append(lib['221100']['2'])
results.append(lib['221100']['1'])
results.append(lib['221100']['0'])

plt.plot(results[0])
plt.plot(results[1])

plt.savefig(f"plots{s}1100plot.png")

plt.clf()
plt.plot(results[2])
plt.plot(results[3])

plt.savefig(f"plots{s}2200plot.png")

plt.clf()
plt.plot(results[4])
plt.plot(results[5])

plt.savefig(f"plots{s}2211plot.png")

plt.clf()
plt.plot(results[6])
plt.plot(results[7])
plt.plot(results[8])

plt.savefig(f"plots{s}221100plot.png")

