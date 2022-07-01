---
layout: page
title: Results
permalink: /results/
---

Firstly we found that almost all games will end by a player making a suggestion that no other player has on their hand and therefore winning the game by default before a player was actually able to fully deduct the goal deck. While this usually does not happen as much with human players, it is a result of the technical limitations of our implementation, where players will only make an accusation when they have ruled out all but one possible card combination in the goal deck.


Having run four simulation setups 25 times, the win rates for each order represented by the agents is shown. In the left-top plot, we can see that the 2 agents of order 2 have a combined win percentage of 96%, against 4% for the agents of order 0.

[![](/docs/assets/win_rates_order.png)Win rates for different setups](/docs/assets/win_rates_order.png)


Every agent considers a specific amount of worlds possible for the goal state during each turn. As the agents are provided with more information each turn, the amount of goal states they still deem possible decreases. This decrease in goal states are plotted below for each setup.

[![](/plots/2200plot.png)Goal states considered possible in the setup with 2 agents of order 2 and 2 agents of order 0](/plots/2200plot.png)
[![](/plots/2211plot.png)Goal states considered possible in the setup with 2 agents of order 2 and 2 agents of order 1](/plots/2211plot.png)
[![](/plots/1100plot.png)Goal states considered possible in the setup with 2 agents of order 1 and 2 agents of order 0](/plots/1100plot.png)
[![](/plots/221100plot.png)Goal states considered possible in the setup with 2 agents of order 2, 2 agents of order 1 and 2 agents of order 0](/plots/221100plot.png)

