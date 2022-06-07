"""This module handles all functions related to creating, updating and validating the Kripke model underlying the game"""
import copy
from mlsolver.kripke import KripkeStructure, World


def create_kripke_model(possible_worlds: list, num_players: int) -> KripkeStructure:
    """
    creates a new Kripke model from a list of possible worlds and a number of players.
    An S5-model is created, meaning that reflexive, transitive and symmetric relations are added for all worlds.
    """
    worlds = _create_worlds(possible_worlds)
    relations = _create_relations(worlds, num_players)

    model = KripkeStructure(worlds, relations)
    return model

def update_kripke_model(old_model: KripkeStructure, formula) -> KripkeStructure:
    """
    Update a kripke model so that it satisfies a given formula.
    Simpler rewrite of mlsolver.kripke.solve because of issues with that formula creating a power set of worlds (OOM error)
    """
    new_model = KripkeStructure(old_model.worlds.copy(), copy.deepcopy(old_model.relations))
    inconsistent_nodes = old_model.nodes_not_follow_formula(formula)

    for node in inconsistent_nodes:
        new_model.remove_node_by_name(node)

    return new_model

def _create_worlds(possible_worlds: list) -> list:
    """create a list of worlds from a combination of possible worlds with certain assignments"""
    worlds = []
    world_index = 1

    for world in possible_worlds:
        assignment = {}

        for prop in world:
            assignment[prop] = True

        world_name = "w" + str(world_index)

        new_world = World(world_name, assignment)

        worlds.append(new_world)
        world_index += 1

    return worlds

def _create_relations(worlds: list[World], num_players: int) -> dict:
    """Create reflexive, transitive and symmetric relations for a list of worlds."""
    n_worlds = len(worlds)

    relations = {}

    for p in range(1,num_players+1):
        p_relations = set()

        for i in range(0,n_worlds):
            for j in range(0,n_worlds):
                relation = (worlds[i].name, worlds[j].name)

                p_relations.add(relation)

        relations[str(p)] = p_relations

    return relations
