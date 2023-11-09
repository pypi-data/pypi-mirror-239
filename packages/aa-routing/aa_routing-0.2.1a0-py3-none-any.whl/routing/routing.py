from typing import List, Tuple

from networkx import (
    DiGraph, astar_path, bellman_ford_path, dijkstra_path, get_edge_attributes,
    single_source_dijkstra_path,
)

from routing.models import TrigInvasion

from .graph import build


def _route_path(source: int, destination: int, mode="p_shortest", algorithm="astar", edges: List = [], static_cache: bool = False) -> Tuple[DiGraph, List]:
    """

    Args:
        source (int): From Solar System ID
        destination (int): To Solar System ID
        mode (str, optional): Weighting mode Defaults to "p_shortest". ["p_shortest", "p_safest", "p_less_safe"]
        algorithm (str, optional): Routing Function to use. Defaults to "astar" ["astar", "dijkstra", "bellman_ford"]
        edges (list, optional): Extra edges to load, example [(30100000, 30003841, {'p_shortest': 1.0, 'p_safest': 1.0, 'p_less_safe': 1.0}),]. Defaults to [].
        static_cache (bool, optional): Use Pregenerated Cache. Defaults to False.

    Returns:
        Tuple[DiGraph, List], The DiGraph used to calculate the route and the List of Nodes used
    """
    G = build(static_cache)
    if edges is not {}:
        G.add_edges_from(edges)

    if algorithm == "astar":
        return G, astar_path(G, source, destination, weight=mode)
    elif algorithm == "dijkstra":
        return G, dijkstra_path(G, source, destination, weight=mode)
    elif algorithm == "bellman_ford":
        return G, bellman_ford_path(G, source, destination, weight=mode)
    else:
        return G, astar_path(G, source, destination, weight=mode)


def route_path_nodes(source: int, destination: int, mode="p_shortest", algorithm="astar", edges: List = [], static_cache: bool = False) -> List[Tuple]:
    """Route from Source to Destination and return the Nodes taken

    Args:
        source (int): From Solar System ID
        destination (int): To Solar System ID
        mode (str, optional): Weighting mode Defaults to "p_shortest". ["p_shortest", "p_safest", "p_less_safe"]
        algorithm (str, optional): Routing Function to use. Defaults to "astar" ["dijkstra", "bellman_ford"]
        edges (list, optional): Extra edges to load, example [(30100000, 30003841, {'p_shortest': 1.0, 'p_safest': 1.0, 'p_less_safe': 1.0})]. Defaults to [].
        static_cache (bool, optional): Use Pregenerated Cache. Defaults to False.

    Returns:
        List[tuple]: A list of Node tuples, a node is usually a Solar System
    """
    G, nodes = _route_path(source, destination, mode, algorithm, edges, static_cache)
    return nodes


def route_path_gates(source: int, destination: int, mode="p_shortest", algorithm="astar", edges: List = [], static_cache: bool = False) -> List[Tuple]:
    """Route from Source to Destination and return the gates taken and their type

    Args:
        source (int): From Solar System ID
        destination (int): To Solar System ID
        mode (str, optional): Weighting mode Defaults to "p_shortest". ["p_shortest", "p_safest", "p_less_safe"]
        algorithm (str, optional): Routing Function to use. Defaults to "astar" ["dijkstra", "bellman_ford"]
        edges (list, optional): Extra edges to load, example [(30100000, 30003841, {'p_shortest': 1.0, 'p_safest': 1.0, 'p_less_safe': 1.0})]. Defaults to [].
        static_cache (bool, optional): Use Pregenerated Cache. Defaults to False.

    Returns:
        List[tuple]: A list of Tuples, (fromsystem, tosystem, gatetype)
    """
    path_edges = []
    G, nodes = _route_path(source, destination, mode, algorithm, edges, static_cache)
    edge_type = get_edge_attributes(G, "type")
    for i, node in enumerate(nodes):
        try:
            path_edges.append((node, nodes[i + 1], edge_type[node, nodes[i + 1]]))
        except IndexError:
            pass
            # reached the end of the Path
    return path_edges


def route_length(source: int, destination: int, mode="p_shortest", algorithm="astar", edges: List = [], static_cache: bool = False) -> int:
    """Route from Source to Destination and return the Number of Edges Taken

    Args:
        source (int): From Solar System ID
        destination (int): To Solar System ID
        mode (str, optional): Weighting mode Defaults to "p_shortest". ["p_shortest", "safep_safestst", "p_less_safe"]
        algorithm (str, optional): Routing Function to use. Defaults to "astar" ["dijkstra", "bellman_ford"]
        edges (list, optional): Extra edges to load, example [(30100000, 30003841, {'p_shortest': 1.0, 'p_safest': 1.0, 'p_less_safe': 1.0})]. Defaults to [].
        static_cache (bool, optional): Use Pregenerated Cache. Defaults to False.

    Returns:
        int : the number of JUMPS, this will be one shorter than route_path, as it includes the source system.
    """
    G, nodes = _route_path(source, destination, mode, algorithm, edges, static_cache)
    # Okay this isnt literally the number of edges, but edges are always nodes-1, -1 to remove the source node.
    return len(nodes) - 1


def systems_range(source: int, range: int, mode="p_shortest", edges: list = [], static_cache: bool = False, include_source: bool = False) -> List:
    """Return all the Systems within a specific Jump Range

    Args:
        source (int): _description_
        range (int): _description_
        mode (str, optional): _description_. Defaults to "p_shortest".
        edges (list, optional): _description_. Defaults to [].
        static_cache (bool, optional): _description_. Defaults to False.

    Returns:
        List: _description_
    """
    list = [key for key in single_source_dijkstra_path(build(static_cache), source, float(range), weight=mode)]
    if include_source is False:
        list.remove(source)
    return list


def route_check_triglavian(source: int, destination: int, mode="p_shortest", algorithm="astar", edges: List = [], static_cache: bool = False) -> bool:
    """Check if a given route passes through a Triglavian occupied System

    Args:
        source (int): _description_
        destination (int): _description_
        mode (str, optional): _description_. Defaults to "p_shortest".
        algorithm (str, optional): _description_. Defaults to "astar".
        edges (List, optional): _description_. Defaults to [].
        static_cache (bool, optional): _description_. Defaults to False.

    Returns:
        bool: _description_
    """
    for system in route_path_nodes(source, destination, mode, algorithm, edges, static_cache):
        if TrigInvasion.objects.filter(system_id=system, status__in=[TrigInvasion.Status.FINAL_LIMINALITY, TrigInvasion.Status.TRIGLAVIAN_MINOR_VICTORY]).exists is False:
            return True
        else:
            pass
    return False


def route_check_edencom(source: int, destination: int, mode="p_shortest", algorithm="astar", edges: List = [], static_cache: bool = False) -> bool:
    """Check if a given route passes through an EDENCOM occupied System

    Args:
        source (int): _description_
        destination (int): _description_
        mode (str, optional): _description_. Defaults to "p_shortest".
        algorithm (str, optional): _description_. Defaults to "astar".
        edges (List, optional): _description_. Defaults to [].
        static_cache (bool, optional): _description_. Defaults to False.

    Returns:
        bool: _description_
    """
    for system in route_path_nodes(source, destination, mode, algorithm, edges, static_cache):
        if TrigInvasion.objects.filter(system_id=system, status__in=[TrigInvasion.Status.FORTRESS, TrigInvasion.Status.EDENCOM_MINOR_VICTORY]).exists is False:
            return True
        else:
            pass
    return False
