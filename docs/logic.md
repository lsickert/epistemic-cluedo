---
layout: page
title: Epistemic Logic
permalink: /logic/
---

## Logical Background

For the epistemic models in this game we will employ the rules of S5-models initially, although later stages of the game might deviate from this, since the individual update steps explained below might delete accessibility relations between different worlds. 


When $a \ne 0$, there are two solutions to $(ax^2 + bx + c = 0)$ and they are 
$$ x = {-b \pm \sqrt{b^2-4ac} \over 2a} $$

We identified three aspects of the game that can be modelled well in epistemic logic. These are the knowledge of the agents about the goal deck, their own handcards, and the other players handcards. As described in the [Game](cluedo.md) section, some limitations apply for these models in order to keep them computationally feasible. Additionally, we are splitting the full game knowledge into three distinct Kripke models to model the three aspects described above separately in order to increase performance further. A fully formalised Kripke model containing all of the game knowledge can be restored from these simpler models by multiplication:

Let us assume as an example the goal model contains the world w~1~ = \{*peacock*, *rope*, *library*\} and the individual hand card model for player 1 contains the two worlds w~2~ = \{*peacock*, *rope*, *dagger*, *white*\} and w~3~ = \{*green*, *pistol*, *axe*, *study*\}. A full model would then contain the two worlds  w~1~ = \{*g:peacock*, *g:rope*, *g:library*, *h1:peacock*, *h1:rope*, *h1:dagger*, *h1:white*\} and  w~1~ = \{*g:peacock*, *g:rope*, *g:library*, *h1:green*, *h1:pistol*, *h1:axe*, *h1:study*\}, where each of those new worlds inherits the accessibility relations of the goal model towards all other newly created combined worlds and the accessibility relations of the previous hand card model between the worlds created from this individual combination of one world from the goal model with all worlds of the hand cad model. The same step needs then to be repeated for the hand card models of all other players and their accessibility relations. It is intuitively, easy to see that splitting up the model into several submodels allows us to model a large number of atomic propositions in an performance-effective and humanly-understandable waqy without compromising on any of the knowledge that would be contained in a fully formalized combined model.

## Modelling the Goal Deck

The Kripke model of the goal stack is created by assigning each possible card combination a world and creating reflexive, transitive and symmetric accessibility relations between them. In each world exactly three propositions corresponding to the three cards of this world are true, while the propositions for all other cards are false.

Each player has their own internal representation of this Kripke model which is updated each turn. At the beginning of the game they can already deduce that any world containing at least one of their own hand cards cannot represent the goal deck. After that, there are two main update functions. First, when the player is shown a card by another player, they know that any world containing this card cannot be in the goal deck and second, when a player shows another player a card privately, they know that the combination of the three cards from the suggestion of the other player cannot be in the goal deck.

Once a player has eliminated all worlds except one, they know that the three cards proposed in this world have to be in the goal deck.

## Modelling the Hand Cards

The Kripke models for the hand cards of each other player are created by assigning each possible card combination, a world and creating reflexive, transitive and symmetric accessibility relations between them. In each world, as many propositions as there are hand cards for this player are true, while the propositions for all other cards are false.

Again, each player has their own internal representation of these Kripke models which are updated each turn. At the beginning of the game the player can also again deduce that any world containing at least one of their own hand cards is not possible for the other player. After that, there are also two main update functions. If the player is shown a card by another player, they can deduce that any world that does not contain this card is not possible and second, if a player shows another player a card privately, the player knows that any world in the model that does not contain at least one of these three cards is not possible anymore.

Once a proposition for a specific card is true in all remaining worlds of the Kripke model, the player knows that the other player has to have this card in their hand and can therefore deduce that it cannot be in the goal deck.

## Decision Making

*The contents of this section are still subject to change in later iterations of the game, since their implications are not fully worked out yet*

'higher-order logic players'
At the start of each turn the player will choose the room which is still present in the largest amount of possible worlds and move towards it, since eliminating this room will give them the greatest amount of knowledge. They will make the same decision for the character and weapon.

The lower-order logic players that only use knowledge of their own cards will first move to random room they can directly reach that is still present in their knowledge of possible goal decks, then they make a suggestion that includes the cards of a goal deck they consider possible that includes the room they are in. If they cannot directly reach a room that is within goal decks that they consider possible, then the player will move into the pathways between rooms, which in their next turn can lead them to any room.

## Implementation

All the epistemic logic described on this page is implemented using the [mlsolver](https://github.com/erohkohl/mlsolver) package. In order to enable the computations needed for this project several extensions and optimizations of the package have been developed that can hopefully be integrated into the original project later. All of these extensions can be found in the project repository in the folder `cluedo/logic-checker`.

Firstly, the original function to find a submodel of a Kripke model that satisfies a given formula (`KripkeStructure.solve()`) has been rewritten in a simpler and more effective way. The original function was creating a power set of all posible sets of worlds in the original model to then determine the smallest set of worlds in a model still satisfying a given formula. Since this would quickly lead the program to run out of memory with the amount of possible worlds in our models, we simplified this function by simply iterating over the full model and then removing all worlds that do not satisfy the formula. The actual function to remove these worlds and corresponding relations has also been optimized by simply saving all worlds that satisfy the formula into a set and recreating the relations from this subset instead of iterating over the sets of worlds and relations multiple times to delete all unwanted worlds and relations from them. There are two new functions created for this in the file `kripke_model.py`. The function `_remove_node_by_name()` removes a single world and corresponding relations, it is only marginally (around 10 %) faster than the original function. The function  `_remove_nodes_by_name()` removes all inconsistent worlds at once and is up to five times faster than the original functions. The performance values have been taken from running these functions for a game configuration of 4 players, 6 characters, 6 weapons and 6 rooms with no manual players and averaging over the resulting execution times. Actual execution times in seconds are not given here, since those will vary for each individual game turn. Additionally we created a new function `_nodes_follow_formula()` which provides a contrasting functionality to the original `KripkeStructure.nodes_not_follow_formula()` function of the *mlsolver* package.

Secondly, two new functions to effectively create reflexive, transitive and symmetric accesibility relations between a given set of worlds have been created. The function `_create_single_relations()` will create those relations for a model with only a single agent whereas the function `_create_multi_relations()` will create the relations for a multi-agent model.

Lastly, we created two functions to remove accessibility relations instead of full worlds from a Kripke model, a functionality that was not implemented in the *mlsolver* package. The function `remove_relations()` removes relations for all agents in a multi-agent model and can also be used to remove relations in a single-agent model, whereas the function `remove_agent_relations()` removes relations for a single agent only in a multi-agent model. Both functions accept either a specified start- and end-world to remove a single relation or a wildcard character for either the start- or end-world making it posible to remove all relations to or from a single world at once. It can also be specified if symmetric relations should be fully removed if needed or if only the specified direction of a relation should be removed. Reflexive relations are not removed unless both worlds are explicitly specified in order to keep the resulting model consistent with the common axiom systems of knowledge.
