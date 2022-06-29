---
layout: page
title: The Game
permalink: /game/
---

## Background

Cluedo is a board game for two to six players where the players try to solve a murder case by cleverly combining evidence they obtain through asking questions to the other players.

## How to Play

The base game consists of 6 character, 6 weapon and 9 room cards. Additionally there are 6 player character pieces, 2 dice, the playing board with 9 different rooms on it and 6 weapon pieces.

### Setup

1. The character, weapon and room clue cards are shuffled.

2. The top card from each deck is taken and put aside. These three cards serve as the goal deck that needs to be identified throughout the game.

3. The remaining clue cards get shuffled together into one deck and distributed among the players.

4. The player and weapon pieces are set up on the board. While each player has a determined starting point, the weapons are distributed randomly across the rooms.

### Game Process

After each player chooses their character piece, they roll a dice. The player with the highest number then starts the game.

At the beginning of the turn a player rolls the two dice and may move their character up to as many fields as the number they have rolled. It is also possible to stay at the same position. When the player manages to reach a room in their turn, they can decide to enter it and make a *suggestion* about the character, weapon and room in the goal deck. To do so, they openly announce a character, a weapon and the room they are currently standing in to the other players. The weapon and character piece that are in the suggestion are then moved to the suggested room the player (who made the suggestion) is currently in.

As a response to the *suggestion*, the player to the left of the current player has to show the suggesting player one of the three named cards if he holds at least one of them. If they do not hold any of the cards, the process continues clockwise until either one player is able to show a card or the round arrives back at the suggesting player. After that the next player begins their turn.

Once a player believes that they know the character, the weapon and the room inside the goal deck, they can make an *accusation* at any point in their turn by publicly announcing the character, the weapon and the room they believe are in the deck. They then privately check the goal deck. If their *accusation* was correct, they win the game. However, if their accusation was incorrect, they remain in the game, but cannot make any further *suggestions* or *accusations*, effectively losing the game. They still have to show any matching cards to other players suggestions. If all players except one made incorrect accusations, that player wins by default.

### Rules

* It is not allowed for two players to stand on the same field outside of the rooms, making it possible for players to block access for other players.

* Some rooms contain secret passages that allow it to move directly between the two connected rooms.

* It is only allowed to make a *suggestion* while standing in a specific room.

* While a player is allowed to choose any character and weapon in a *suggestion*, they can only suggest the room they are currently in.


### Limitations

Since modelling the full game of Cluedo is quite computationally expensive and would require significant development efforts, there are a number of limitations we will be making for our implementation, which are explained below:

* Players will only make an accusations once they are certain about the contents of the goal deck. While it might be possible to model premature accusations with a certain risk and probability factor, this would be too complex to implement for now. We assume the players within the model are perfect logicians.

* Players will correctly remember all suggestions and actions made by other players. With human players it might happen that a player incorrectly notes down or forgets a suggestion another player makes, this would significantly complicate the underlying epistemic logic formulas, which is why we will not model this possibility.

* Players will only make suggestions with cards that are not in their own hand and of which they do not know yet whether they are in the goal deck. With human players it might be a strategy to include a card that they have in their own hand to confuse other players or to limit the possibilities of cards they can show, implementing these possibilities would require complex reasoning about not only their own knowledge, but also about the knowledge of other players and weighing both of them against each other. This directly correlates to the next limitation.

* Players will not employ longer-term strategic planning. At each turn a player will choose a suggestion that will bring him the most benefit at the current point of the game. While it is theoretically possible to choose less optimal options that will bring a greater benefit in the future of the game, this would require both strategic reasoning and the heuristic modelling of future possible turns.

* Players will not employ complex pathfinding. Since the main goal of this project is on the logical modelling of players decisions, implementing some form of complex pathfinding algorithm would take up too much effort. Furthermore, dice rolling will not be implemented since it would add a random factor to the modelling of this game. Instead, since our interests are solely on the logical aspects of this model, the players can either stay in the room they are in, move to an ajacent room, use a secret passage, or go into the pathways between rooms to get to rooms that are further away in their next turn. 
