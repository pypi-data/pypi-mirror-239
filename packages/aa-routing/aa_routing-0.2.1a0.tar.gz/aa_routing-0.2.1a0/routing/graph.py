from networkx import DiGraph

from routing.models import SolarSystem, SolarSystemConnection

from .static_data import precomputed_graph


def build(static_cache: bool = False) -> DiGraph:
    if static_cache:
        G = DiGraph(precomputed_graph)
        return G
    else:
        G = DiGraph()
        for node in SolarSystem.objects.values_list("id", "security"):
            G.add_node(node[0], security=node[1], type="solar_system")

        for edge in SolarSystemConnection.objects.values_list(
            "fromsolarsystem",
            "tosolarsystem",
            "p_shortest",
            "p_safest",
            "p_less_safe"
        ).all():
            G.add_edge(edge[0], edge[1], p_shortest=edge[2], p_safest=edge[3], p_less_safe=edge[4], type="Stargate")

        return G
