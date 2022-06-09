---
layout: page
title: Epistemic Logic
permalink: /logic/
---

## Logical Background

For the epistemic models in this game we will employ the rules of 

## Modeling the Goal Deck

The Kripke model of the goal stack is created by assigning each possible card combination a world and creating reflexive, transitive and symmetric accessibility relations between them. In each world exactly three propositions corresponding to the three cards of this world are true, while the propositions for all other cards are false.

Each player has their own internal representation of this Kripke model which is updated each turn. At the beginning of the game he can already deduce that any world containing at least one of his own hand cards cannot represent the goal deck. After that, there are two main update functions. First, when the player is shown a card by another player, he knows that any world containing this card cannot be in the goal deck and second, when a player shows another player a card privately, he knows that the combination of the three cards from the suggestion of the other player cannot be in the goal deck.

Once a player has eliminated all worlds except one, he knows that the three cards proposed in this world have to be in the goal deck.

## Modeling the Hand Cards

The Kripke models for the hand cards of each other player are created by assigning each possible card combination. a world and creating reflexive, transitive and symmetric accessibility relations between them. In each world as many propositions as there are hand cards for this player are true, while the propositions for all other cards are false.

Again, each player has their own internal representation of these Kripke models which are updated each turn. At the beginning of the game the player can also again deduce that any world containing at least one of his own hand cards is not possible for the other player. After that, there are also two main update functions. If the player is shown a card by another player, he can deduce that any world that does not contain this card is not possible and second, if a player shows another player a card privately, the player knows that any world in the model that does not contain at least one of these three cards is not possible anymore.

Once a proposition for a specific card is true in all remaining worlds of the Kripke model, the player knows that the other player has to have this card on his hand and can therefore deduce that it cannot be in the goal deck.

## Decision Making

*The contents of this section are still subject to change in later iterations of the game, since their implications are not fully worked out yet*

At the start of each turn the player will choose among the rooms reachable by him the room which is still present in the largest amount of possible worlds, since eliminating this room will give him the greatest amount of knowledge. He will make the same decision for the character and weapon.
