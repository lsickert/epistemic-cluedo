"""This module handles all functions related to creating, updating and validating the Kripke model underlying the game"""
from mlsolver.kripke import KripkeStructure, World


def create_kripke_model(possible_worlds: list, num_players: int):
    worlds = _create_worlds(possible_worlds)
    relations = _create_relations(worlds, num_players)

    model = KripkeStructure(worlds, relations)
    return model

def _create_worlds(possible_worlds: list):

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

    n_worlds = len(worlds)

    relations = {}

    for p in range(1,num_players+1):
        p_relations = {}

        for i in range(0,n_worlds):
            for j in range(0,n_worlds):
                relation = (worlds[i].name, worlds[j].name)

                p_relations.add(relation)

        relations[str(p)] = p_relations

    return relations
