"""This module handles all functions related to creating, updating and validating the Kripke model underlying the game"""
import copy
from mlsolver.kripke import KripkeStructure, World


def create_multi_kripke_model(possible_worlds: list, num_players: int) -> KripkeStructure:
    """
    creates a new Kripke model from a list of possible worlds and a number of players.
    An S5-model is created, meaning that reflexive, transitive and symmetric relations are added for all worlds.
    """
    worlds = _create_worlds(possible_worlds)
    relations = _create_multi_relations(worlds, num_players)

    model = KripkeStructure(worlds, relations)
    return model


def create_single_kripke_model(possible_worlds: list) -> KripkeStructure:
    """
    creates a new Kripke model from a list of possible worlds.
    An S5-model is created, meaning that reflexive, transitive and symmetric relations are added for all worlds.
    """
    worlds = _create_worlds(possible_worlds)
    relations = _create_single_relations(worlds)

    model = KripkeStructure(worlds, relations)
    return model


def update_kripke_model(old_model: KripkeStructure, formula) -> KripkeStructure:
    """
    Update a kripke model so that it satisfies a given formula.
    Simpler rewrite of mlsolver.kripke.solve because of issues with that formula creating a power set of worlds (OOM error)
    """
    new_model = KripkeStructure(
        old_model.worlds.copy(), copy.deepcopy(old_model.relations))
    inconsistent_nodes = old_model.nodes_not_follow_formula(formula)

    for node in inconsistent_nodes:
        _remove_node_by_name(new_model, node)

    return new_model


def remove_agent_relation(model: KripkeStructure, agent: str, world_1: str, world_2: str, symmetric: bool = False):
    """
    Removes a single relation from a Kripke model. If the `symmetric` argument is supplied, the relation will be removed in both directions.
    """
    if isinstance(model.relations, dict):
        raise TypeError(
            "The provided kripke model should contain multiple agents")

    if symmetric:
        model.relations[str(agent)].discard((world_1, world_2))
        model.relations[str(agent)].discard((world_2, world_1))
    else:
        model.relations[str(agent)].discard((world_1, world_2))


def remove_relation(model: KripkeStructure, world_1: str, world_2: str, symmetric: bool = False):
    """
    Removes a single relation from a Kripke model. If a multi-agent model is supplied, the relation is removed for all agents.
    If the `symmetric` argument is supplied, the relation will be removed in both directions.
    """
    if isinstance(model.relations, set):
        if symmetric:
            model.relations.discard((world_1, world_2))
            model.relations.discard((world_2, world_1))
        else:
            model.relations.discard((world_1, world_2))

    if isinstance(model.relations, dict):
        for agent in model.relations.values():
            if symmetric:
                agent.discard((world_1, world_2))
                agent.discard((world_2, world_1))
            else:
                agent.discard((world_1, world_2))


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


def _create_multi_relations(worlds: list, num_players: int) -> dict:
    """Create reflexive, transitive and symmetric relations for for multiple agents for a list of worlds."""
    n_worlds = len(worlds)

    relations = {}

    for p in range(1, num_players+1):
        p_relations = set()

        for i in range(0, n_worlds):
            for j in range(0, n_worlds):
                relation = (worlds[i].name, worlds[j].name)

                p_relations.add(relation)

        relations[str(p)] = p_relations

    return relations


def _create_single_relations(worlds: list) -> set:
    """Create reflexive, transitive and symmetric relations for a list of worlds."""
    n_worlds = len(worlds)

    relations = set()

    for i in range(0, n_worlds):
        for j in range(0, n_worlds):
            relation = (worlds[i].name, worlds[j].name)

            relations.add(relation)

    return relations


def _nodes_follow_formula(model: KripkeStructure, formula) -> list:
    """Returns a list with all worlds of a Kripke structure, where the formula is satisfiable"""

    nodes_follow_formula = []

    for node in model.worlds:
        if formula.semantics(model, node.name):
            nodes_follow_formula.append(node.name)

    return nodes_follow_formula


def _remove_node_by_name(model, node_name):
    """Removes ONE node from a  Kripke model.
    Rewrite of mlsolver.kripke.remove_node_by_name to (slightly) improve performance
    """
    for world in model.worlds.copy():
        if node_name == world.name:
            model.worlds.remove(world)
            break

    if isinstance(model.relations, set):
        new_relations = set()
        for (start_node, end_node) in model.relations.copy():
            if not (start_node == node_name or end_node == node_name):
                new_relations.add((start_node, end_node))
        model.relations = new_relations

    if isinstance(model.relations, dict):
        for key, value in model.relations.items():
            new_relations = set()
            for (start_node, end_node) in value.copy():
                if not (start_node == node_name or end_node == node_name):
                    new_relations.add((start_node, end_node))
            model.relations[key] = new_relations
