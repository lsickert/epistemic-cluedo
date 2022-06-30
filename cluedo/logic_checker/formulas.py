"""Modal logic formula module

This module unites all operators from propositional and modal logic.
"""


class Atom:
    """
    This class represents propositional logic variables in modal logic formulas.
    """

    def __init__(self, name):
        self.name = name

    def semantic(self, ks, world_to_test):
        """Function returns assignment of variable in Kripke's world.
        """
        for world in ks.worlds:
            if world.name == world_to_test:
                return world.assignment.get(self.name, False)

    def __eq__(self, other):
        return isinstance(other, Atom) and other.name == self.name

    def __str__(self):
        return str(self.name)


class Box:
    """
    Describes box operator of modal logic formula and it's semantics
    """

    def __init__(self, inner):
        self.inner = inner

    def semantic(self, ks, world_to_test):
        result = True
        for relation in ks.relations:
            if relation[0] == world_to_test:
                result = result and self.inner.semantic(ks, relation[1])
        return result

    def __eq__(self, other):
        return isinstance(other, Box) and self.inner == other.inner

    def __str__(self):
        if isinstance(self.inner, Atom):
            return u"\u2610" + " " + str(self.inner)
        else:
            return u"\u2610" + "(" + str(self.inner) + ")"


class Box_a:
    """
    Describes box operator of modal logic formula and it's semantics for Agent a
    """

    def __init__(self, agent, inner):
        self.inner = inner
        self.agent = agent

    def semantic(self, ks, world_to_test):
        result = True
        for relation in ks.relations.get(self.agent, {}):
            if relation[0] == world_to_test:
                result = result and self.inner.semantic(ks, relation[1])
        return result

    # TODO
    def __eq__(self, other):
        raise NotImplementedError

    # TODO
    def __str__(self):
        raise NotImplementedError


class Box_star:
    """
    Describes semantic of multi modal Box^* operator.
    Semantic(Box_star phi) = min(Box Box ... Box phi, for all n in /N)
    Simplification with n = 1: Box_star phi = phi and Box_a phi and Box_b phi ... and Box_n phi
    """

    def __init__(self, inner):
        self.inner = inner

    def semantic(self, ks, world_to_test, depth=1):
        f = self.inner
        for agents in ks.relations:
            f = And(f, Box_a(agents, self.inner))
        return f.semantic(ks, world_to_test)

    # TODO
    def __eq__(self, other):
        raise NotImplementedError

    # TODO
    def __str__(self):
        raise NotImplementedError


class Diamond:
    """
    Describes diamond operator of modal logic formula and it's semantics
    """

    def __init__(self, inner):
        self.inner = inner

    def semantic(self, ks, world_to_test):
        result = False
        for relation in ks.relations:
            if relation[0] == world_to_test:
                result = result or self.inner.semantic(ks, relation[1])
        return result

    def __eq__(self, other):
        return isinstance(other, Diamond) and self.inner == other.inner

    def __str__(self):
        if isinstance(self.inner, Atom):
            return u"\u25C7" + " " + str(self.inner)
        else:
            return u"\u25C7" + "(" + str(self.inner) + ")"


class Diamond_a:
    """
    Describes diamond operator of modal logic formula and it's semantics for Agent a
    """

    def __init__(self, agent, inner):
        self.inner = inner
        self.agent = agent

    def semantic(self, ks, world_to_test):
        result = False
        for relation in ks.relations.get(self.agent, {}):
            if relation[0] == world_to_test:
                result = result or self.inner.semantic(ks, relation[1])
        return result

    # TODO
    def __eq__(self, other):
        raise NotImplementedError

    # TODO
    def __str__(self):
        raise NotImplementedError


class Implies:
    """
    Describes implication derived from classic propositional logic
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def semantic(self, ks, world_to_test):
        return not self.left.semantic(ks, world_to_test) or self.right.semantic(ks, world_to_test)

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    def __str__(self):
        return "(" + self.left.__str__() + " -> " + self.right.__str__() + ")"


class Not:
    """
    Describes negation derived from classic propositional logic
    """

    def __init__(self, inner):
        self.inner = inner

    def semantic(self, ks, world_to_test):
        return not self.inner.semantic(ks, world_to_test)

    def __eq__(self, other):
        return self.inner == other.inner

    def __str__(self):
        return u"\uFFE2" + str(self.inner)


class And:
    """
    Describes and derived from classic propositional logic
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def semantic(self, ks, world_to_test):
        return self.left.semantic(ks, world_to_test) and self.right.semantic(ks, world_to_test)

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    def __str__(self):
        return "(" + self.left.__str__() + " " + u"\u2227" + " " + self.right.__str__() + ")"


class Or:
    """
    Describes or derived from classic propositional logic
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def semantic(self, ks, world_to_test):
        return self.left.semantic(ks, world_to_test) or self.right.semantic(ks, world_to_test)

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    def __str__(self):
        return "(" + self.left.__str__() + " " + u"\u2228" + " " + self.right.__str__() + ")"



"""This module contains functions to create the individual formulas used in the game."""


def character_weapon_room_and(character: str, weapon: str, room: str) -> And:
    """Formula to check for (character AND weapon AND room)"""
    return And(Atom(character), And(Atom(weapon), Atom(room)))


def character_weapon_room_or(character: str, weapon: str, room: str) -> Or:
    """Formula to check (character OR weapon OR room)"""
    return Or(Atom(character), Or(Atom(weapon), Atom(room)))


def not_character_weapon_room_and(character: str, weapon: str, room: str) -> Not:
    """Formula to check NOT(character AND weapon AND room)"""
    return Not(And(Atom(character), And(Atom(weapon), Atom(room))))


def has_specific_card(card: str) -> Atom:
    """Formula to check that a player has a specific card"""
    return Atom(card)


def not_has_specific_card(card: str) -> Not:
    """Formula to check that a player does not have a specific card"""
    return Not(Atom(card))


def knows_has_specific_card(card: str) -> Box:
    """Formula to check if a player knows about having a specific cards.
    Only works in single-agent Kripke models, use `agent_knows_has_specific_card()` for multi-Kripke models
    """
    return Box(Atom(card))

def agent_knows_has_specific_card(card: str, agent: str) -> Box_a:
    """Formula to check if a player knows about having a specific cards.
    Only works in multi-agent Kripke models, use `knows_has_specific_card()` for single-Kripke models
    """
    return Box_a(agent, Atom(card))


def knows_not_has_specific_card(card: str) -> Box:
    """Formula to check if a player knows about not having a specific cards
    Only works in single-agent Kripke models, use `agent_knows_not_has_specific_card()` for multi-Kripke models
    """
    return Box(Not(Atom(card)))

def agent_knows_not_has_specific_card(card: str, agent: str) -> Box_a:
    """Formula to check if a player knows about not having a specific cards
    Only works in multi-agent Kripke models, use `knows_not_has_specific_card()` for single-Kripke models
    """
    return Box_a(agent, Not(Atom(card)))

def knows_character_weapon_room_or(character: str, weapon: str, room: str):
    """Formula to check if a player knows about either a character, weapon, or room
        Only works in single-agent Kripke models, use `agent_knows_character_weapon_room_or()` for multi-Kripke models
    """
    return Box(Or(Atom(character), Or(Atom(weapon), Atom(room))))

def agent_knows_character_weapon_room_or(character: str, weapon: str, room: str, agent: str):
    """Formula to check if a player knows about either a character, weapon, or room
        Only works in multi-agent Kripke models, use `knows_character_weapon_room_or()` for single-Kripke models
    """
    return Box_a(agent, Or(Atom(character), Or(Atom(weapon), Atom(room))))

# def not_character_weapon_room_or(character: str, weapon: str, room: str):
#     """Formula to check NOT(character OR weapon OR room)"""
#     return Not(Or(Atom(character),Or(Atom(weapon), Atom(room))))
