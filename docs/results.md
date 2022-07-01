---
layout: page
title: Results
permalink: /results/
---

Firstly we found that almost all games will end by a player making a suggestion that no other player has on their hand and therefore winning the game by default before a player was actually able to fully deduct the goal deck. While this usually does not happen as much with human players, it is a result of the technical limitations of our implementation, where players will only make an accusation when they have ruled out all but one possible card combination in the goal deck.


Having run four simulation setups 25 times, the win rates for each order represented by the agents is shown. In the left-top plot, we can see that the 2 agents of order 2 have a combined win percentage of 96%, against 4% for the agents of order 0.

![Win rates for different setups](/assets/win_rates_order.png)

Every agent considers a specific amount of worlds possible during each turn. 
