import os
from os import sep as s
from unittest import result

from matplotlib import pyplot as plt
from matplotlib.text import Text

def string_to_dict(string: str) -> dict:
    """
    Converts a string to a dictionary.
    """
    string = string.removeprefix("{").removesuffix("}\n")
    return {i.split(":")[0]: 4 * int(i.split(":")[1]) for i in string.split(",")}


def plot_title(string: str) -> None:
    """
    Plots a title.
    """
    # Find unique chars in string
    print(string)
    title = "2 agents of orders: "
    if "2" in string:
        title += "2"
        print(string)
        title += ", " if len(string) == 6 else " and "
    if "1" in string:
        title += "1"
        title += " and " if "0" in string else ""
    if "0" in string:
        title += "0"

    print(title)
    return title


full_results = {}
full_pos_results = {}
for folder in os.listdir(f'.{s}results'):
    #Load run.txt in folder
    with open(f'.{s}results{s}{folder}{s}run.txt', 'r') as f:
        while "Results" not in f.readline():
            continue
        results = string_to_dict(f.readline())
        while "Position" not in f.readline():
            continue
        position_results = string_to_dict(f.readline())
        full_results[folder] = results
        full_pos_results[folder] = position_results
    

fig, axs = plt.subplots(2, 2, figsize=(9, 9), sharey=False)
fig.suptitle("Agent order win percentages for game with indicated player setup", fontsize=20)
plt.subplots_adjust(hspace=0.3)
fontsize = 13

for idx, key in enumerate(full_results.keys()):
    ax = axs[(idx // 2), (idx % 2)]
    if idx % 2 == 0:
        ax.set_ylabel("Percentage of wins", fontsize=fontsize)

    ax.bar(full_results[key].keys(), full_results[key].values())
    ax.set_title(str(plot_title(key)), fontsize=fontsize)
    ax.set_xlabel("Order", fontsize=fontsize)
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_formatter("{x:3.0f}%")
    # Add (%) to y-axis labels


plt.savefig(f"plots{s}win_rates_order.png")

