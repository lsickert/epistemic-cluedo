"""This module handles all functions related to creating, updating and validating the Kripke model underlying the game"""
import copy
import itertools
from mlsolver.kripke import KripkeStructure, World


def create_multi_kripke_model(possible_worlds: list, num_players: int, exclude_players: list = None) -> KripkeStructure:
    """
    creates a new Kripke model from a list of possible worlds and a number of players.
    An S5-model is created, meaning that reflexive, transitive and symmetric relations are added for all worlds.
    If the `exclude_players` parameter includes any valid player_ids bigger than 0, relations for those players will not be created
    """
    if exclude_players is None:
        exclude_players = []

    worlds = _create_worlds(possible_worlds)
    relations = _create_multi_relations(worlds, num_players, exclude_players)

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

    _remove_nodes_by_name(new_model, inconsistent_nodes)

    return new_model


def remove_agent_relations(model: KripkeStructure, agent: str, world_1: str = None, world_2: str = None, symmetric: bool = False):
    """
    Removes relations from a Kripke model. If the `symmetric` argument is supplied, the relation will be removed in both directions.
    If only one of the `world_1` or `world_2` arguments is supplied, all relations starting or ending with this world will be removed (except reflexive relations).
    In combination with the `symmetric` argument this will effectively separate this world from all other worlds for one agent
    """

    if world_1 is None and world_2 is None:
        raise TypeError(
            "Either `world_1` or `world_2` need to be set")

    if world_2 is None and not symmetric:
        new_relations = set()
        for (start_node, end_node) in list(model.relations[str(agent)].copy()):
            if not start_node == world_1:
                new_relations.add((start_node, end_node))

        new_relations.add((world_1, world_1))
        model.relations[str(agent)] = new_relations

    if world_1 is None and not symmetric:
        new_relations = set()
        for (start_node, end_node) in list(model.relations[str(agent)].copy()):
            if not end_node == world_2:
                new_relations.add((start_node, end_node))

        new_relations.add((world_2, world_2))
        model.relations[str(agent)] = new_relations

    if world_1 is None or world_2 is None:
        remove_world = world_1 if world_2 is None else world_2

        new_relations = set()
        for (start_node, end_node) in list(model.relations[str(agent)].copy()):
            if not (start_node == remove_world or end_node == remove_world):
                new_relations.add((start_node, end_node))

        new_relations.add((remove_world, remove_world))
        model.relations[str(agent)] = new_relations

    if isinstance(model.relations, set):
        raise TypeError(
            "The provided kripke model should contain multiple agents")

    if symmetric:
        model.relations[str(agent)].discard((world_1, world_2))
        model.relations[str(agent)].discard((world_2, world_1))
    else:
        model.relations[str(agent)].discard((world_1, world_2))


def remove_relations(model: KripkeStructure, world_1: str = None, world_2: str = None, symmetric: bool = False):
    """
    Removes relations from a Kripke model. If a multi-agent model is supplied, the relation is removed for all agents.
    If the `symmetric` argument is supplied, the relation will be removed in both directions.
    If only one of the `world_1` or `world_2` arguments is supplied, all relations starting or ending with this world will be removed (except reflexive relations).
    In combination with the `symmetric` argument this will effectively separate this world from all other worlds
    """
    if world_1 is None and world_2 is None:
        raise TypeError(
            "Either `world_1` or `world_2` need to be set")

    if world_2 is None and not symmetric:

        if isinstance(model.relations, set):
            new_relations = set()
            for (start_node, end_node) in list(model.relations.copy()):
                if not start_node == world_1:
                    new_relations.add((start_node, end_node))

            new_relations.add((world_1, world_1))
            model.relations = new_relations

        if isinstance(model.relations, dict):
            for key, value in model.relations.items():
                new_relations = set()
                for (start_node, end_node) in list(value.copy()):
                    if not start_node == world_1:
                        new_relations.add((start_node, end_node))

                new_relations.add((world_1, world_1))
                model.relations[key] = new_relations

        return

    if world_1 is None and not symmetric:

        if isinstance(model.relations, set):
            new_relations = set()
            for (start_node, end_node) in list(model.relations.copy()):
                if not end_node == world_2:
                    new_relations.add((start_node, end_node))

            new_relations.add((world_2, world_2))
            model.relations = new_relations

        if isinstance(model.relations, dict):
            for key, value in model.relations.items():
                new_relations = set()
                for (start_node, end_node) in list(value.copy()):
                    if not end_node == world_2:
                        new_relations.add((start_node, end_node))

                new_relations.add((world_2, world_2))
                model.relations[key] = new_relations

        return

    if world_1 is None or world_2 is None:
        remove_world = world_1 if world_2 is None else world_2

        if isinstance(model.relations, set):
            new_relations = set()
            for (start_node, end_node) in list(model.relations.copy()):
                if not (start_node == remove_world or end_node == remove_world):
                    new_relations.add((start_node, end_node))

            new_relations.add((remove_world, remove_world))
            model.relations = new_relations

        if isinstance(model.relations, dict):
            for key, value in model.relations.items():
                new_relations = set()
                for (start_node, end_node) in list(value.copy()):
                    if not (start_node == remove_world or end_node == remove_world):
                        new_relations.add((start_node, end_node))

                new_relations.add((remove_world, remove_world))
                model.relations[key] = new_relations

        return

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


def _create_multi_relations(worlds: list, num_players: int, exclude_players: list) -> dict:
    """Create reflexive, transitive and symmetric relations for for multiple agents for a list of worlds."""
    world_names = [world.name for world in worlds]

    relations = {}

    for p in range(1, num_players+1):

        if p in exclude_players:
            continue

        p_relations = set(itertools.product(world_names, repeat=2))

        relations[str(p)] = p_relations

    return relations


def _create_single_relations(worlds: list) -> set:
    """Create reflexive, transitive and symmetric relations for a list of worlds."""
    world_names = [world.name for world in worlds]

    relations = set(itertools.product(world_names, repeat=2))

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
        for (start_node, end_node) in list(model.relations.copy()):
            if not (start_node == node_name or end_node == node_name):
                new_relations.add((start_node, end_node))
        model.relations = new_relations

    if isinstance(model.relations, dict):
        for key, value in model.relations.items():
            new_relations = set()
            for (start_node, end_node) in list(value.copy()):
                if not (start_node == node_name or end_node == node_name):
                    new_relations.add((start_node, end_node))
            model.relations[key] = new_relations


def _remove_nodes_by_name(model, nodes):
    """Removes multiple nodes from a  Kripke model.
    This makes the function a lot faster than removing single nodes.
    """
    node_set = set(nodes)
    for world in model.worlds.copy():
        if world.name in node_set:
            model.worlds.remove(world)

    if isinstance(model.relations, set):
        new_relations = set()
        for (start_node, end_node) in model.relations.copy():
            if not ((start_node in node_set) or (end_node in node_set)):
                new_relations.add((start_node, end_node))
        model.relations = new_relations

    if isinstance(model.relations, dict):
        for key, value in model.relations.items():
            new_relations = set()
            for (start_node, end_node) in value.copy():
                if not ((start_node in node_set) or (end_node in node_set)):
                    new_relations.add((start_node, end_node))
            model.relations[key] = new_relations
