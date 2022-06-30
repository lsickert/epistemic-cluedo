---
layout: page
title: Epistemic Logic
permalink: /logic/
---

## Logical Background

For the epistemic models in this game we will employ the rules of S5-models initially, although later stages of the game might deviate from this, since the individual update steps explained below might delete accessibility relations between different worlds.

We identified three aspects of the game that can be modelled well in epistemic logic. These are the knowledge of the agents about the goal deck, their own handcards, and the other players handcards. As described in the [Game](cluedo.md) section, some limitations apply for these models in order to keep them computationally feasible. Additionally, we are splitting the full game knowledge into three distinct Kripke models to model the three aspects described above separately in order to increase performance further. A fully formalised Kripke model containing all of the game knowledge can be restored from these simpler models by multiplication:

Let us assume as an example the goal model contains the world 

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
