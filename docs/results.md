---
layout: page
title: Results
permalink: /results/
---

Firstly we found that almost all games will end by a player making a suggestion that no other player has on their hand and therefore winning the game by default before a player was actually able to fully deduct the goal deck. While this usually does not happen as much with human players, it is a result of the technical limitations of our implementation, where players will only make an accusation when they have ruled out all but one possible card combination in the goal deck.

We have created four setups, consisting of the following settings:

1:    2 agents of order 0 and 1 agents of order 2. 6 murderers, 6 weapons and 7 rooms.  
2:    2 agents of order 1 and 2 agents of order 2. 6 murderers, 6 weapons and 7 rooms.  
3:    2 agents of order 0 and 2 agents of order 2. 6 murderers, 6 weapons and 7 rooms.  
4:    2 agents of order 0, 2 agents of order 1 and 2 agents of order 2. 6 murderers, 7 weapons and 8 rooms.  

Having run four simulation setups 25 times, the win rates for each order represented by the agents is shown. In the left-top plot, we can see that the 2 agents of order 2 have a combined win percentage of 96%, against 4% for the agents of order 0 in their setup. The top-right shows the win percentages of 48% for order 2, 52% for order 1 and 0% for the order 0 agents. The bottom left compares the win rate of the 2 order 1 agents (100%) versus the 2 order 0 agents (0%), and the final bottom right plot shows the 52% win rate for the 2 order 2 agents against the 2 order 1 agents with 48%.

![Win rates for different setups](/assets/win_rates_order.png)


Every agent considers a specific amount of worlds possible for the goal state during each turn. As the agents are provided with more information each turn, the amount of goal states they still deem possible decreases. This decrease in goal states are plotted below for each setup, with the graphs showing the average amount of goal states left for both agents over each run. Due to the fact that we consider a right suggestion winning, we nearly never reach an average amount of remaining goal states of 1. 

2 of order 2 and 2 of order 0.
![Goal states considered possible in the setup with 2 agents of order 2 and 2 agents of order 0](/assets/2200plot.png)


2 of order 2 and 2 of order 1.
![Goal states considered possible in the setup with 2 agents of order 2 and 2 agents of order 1](/assets/2211plot.png)


2 or order 1 and 1 of order 0.
![!Goal states considered possible in the setup with 2 agents of order 1 and 2 agents of order 0](/assets/1100plot.png)


2 of order 2, 2 of order 1 and 2 of order 0.
![Goal states considered possible in the setup with 2 agents of order 2, 2 agents of order 1 and 2 agents of order 0](/assets/221100plot.png)
