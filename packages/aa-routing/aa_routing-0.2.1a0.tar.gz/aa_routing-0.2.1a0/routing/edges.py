from ast import Tuple
from typing import List

from routing.app_settings import corptools_active
from routing.models import SolarSystemConnection, TrigInvasion

if corptools_active():
    from corptools.models import MapJumpBridge


def include_titan_bridge(titan_system: int, jump_range: float):
    # return a edges from source to every system in range
    # for system in systeminjumprange:
    #   edges.append((
    #   titan_system, system.to_solar_system_id,
    #   {'p_shortest': weight, 'p_safest': weight, 'p_less_safe': weight, "type": "titan_bridge"}))
    pass


def include_corptools_jumpbridges(weight: float = 1.0) -> list[Tuple]:
    edges = []
    if corptools_active():
        for jb in MapJumpBridge.objects.values_list("from_solar_system_id", "to_solar_system_id").all():
            edges.append((
                jb.from_solar_system_id, jb.to_solar_system_id,
                {'p_shortest': weight, 'p_safest': weight, 'p_less_safe': weight, "type": "jump_bridge"}))
    else:
        return edges

    return edges


def include_eve_scout(system: str = "thera") -> List[Tuple]:
    edges = []
    if system == "thera":
        pass
    elif system == "turnur":
        pass
    return edges
    # return [(30100000, 30003841, {'p_shortest': 1.0, 'p_safest': 1.0, 'p_less_safe': 1.0, type="thera"})]


def avoid_edencom() -> list[Tuple]:
    edges = []
    for system in TrigInvasion.objects.filter(status__in=[TrigInvasion.Status.FORTRESS, TrigInvasion.Status.EDENCOM_MINOR_VICTORY]).values_list("tosolarsystem", flat=True).all():
        for connection in SolarSystemConnection.objects.filter(to_solar_system=system):
            edges.append((
                connection.fromsolarsystem, connection.tosolarsystem,
                {'p_shortest': 50000.0, 'p_safest': 50000.0, 'p_less_safe': 50000.0}))

    return edges


def avoid_triglavian() -> list[Tuple]:
    edges = []
    for system in TrigInvasion.objects.filter(status__in=[TrigInvasion.Status.FINAL_LIMINALITY, TrigInvasion.Status.TRIGLAVIAN_MINOR_VICTORY]).values_list("tosolarsystem", flat=True).all():
        for connection in SolarSystemConnection.objects.filter(to_solar_system=system):
            edges.append((
                connection.fromsolarsystem, connection.tosolarsystem,
                {'p_shortest': 50000.0, 'p_safest': 50000.0, 'p_less_safe': 50000.0}))

    return edges
