# epistemic-cluedo

The game of Cluedo modeled in epistemic logic. This project is part of the course Logical Aspects of Multi-Agent Systems by the University of Groningen 2022. [Project Website](https://lsickert.github.io/epistemic-cluedo/)

## Installation

> IMPORTANT: This project needs a python version of at least 3.9 to run properly. It is also recommended to install the dependencies in a virtual environment

Before starting the game, install the required packages:

```
pip install -r requirements.txt
```

## Starting the game

To start the game run `python main.py` from the root folder of the project and follow the prompts in the command line.

It is strongly advised to follow the default settings when running the game for the first time, as larger configurations can quickly make the game run very slow due to state explosion in the internal Kripke models. In general you can expect the game to speed up as the number of turns progresses due to the increased knowledge of the players, which means that less possible worlds need to be checked.
