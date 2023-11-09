from django.test import TestCase

from routing.routing import (
    route_check_edencom, route_check_triglavian, route_length,
    route_path_gates, route_path_nodes, systems_range,
)


class TestModels(TestCase):
    def test_route_path(self):

        # Jita to b170

        self.assertEqual(route_path_nodes(30000142, 30004590, mode="p_shortest", static_cache=True),[30000142, 30000138, 30001379, 30001376, 30002813, 30045346, 30045345, 30045353, 30045338, 30045344, 30003837, 30003836, 30003841, 30004046, 30004044, 30004043, 30004042, 30004040, 30004589, 30004586, 30004584, 30004554, 30004552, 30004553, 30004555, 30004557, 30004573, 30004574, 30004575, 30004578, 30004581, 30004583, 30004590])
        self.assertEqual(route_path_gates(30000142, 30004590, mode="p_shortest", static_cache=True),[(30000142, 30000138, 'Stargate'), (30000138, 30001379, 'Stargate'), (30001379, 30001376, 'Stargate'), (30001376, 30002813, 'Stargate'), (30002813, 30045346, 'Stargate'), (30045346, 30045345, 'Stargate'), (30045345, 30045353, 'Stargate'), (30045353, 30045338, 'Stargate'), (30045338, 30045344, 'Stargate'), (30045344, 30003837, 'Stargate'), (30003837, 30003836, 'Stargate'), (30003836, 30003841, 'Stargate'), (30003841, 30004046, 'Stargate'), (30004046, 30004044, 'Stargate'), (30004044, 30004043, 'Stargate'), (30004043, 30004042, 'Stargate'), (30004042, 30004040, 'Stargate'), (30004040, 30004589, 'Stargate'), (30004589, 30004586, 'Stargate'), (30004586, 30004584, 'Stargate'), (30004584, 30004554, 'Stargate'), (30004554, 30004552, 'Stargate'), (30004552, 30004553, 'Stargate'), (30004553, 30004555, 'Stargate'), (30004555, 30004557, 'Stargate'), (30004557, 30004573, 'Stargate'), (30004573, 30004574, 'Stargate'), (30004574, 30004575, 'Stargate'), (30004575, 30004578, 'Stargate'), (30004578, 30004581, 'Stargate'), (30004581, 30004583, 'Stargate'), (30004583, 30004590, 'Stargate')])
        self.assertEqual(route_check_edencom(30000142, 30004590, mode="p_shortest", static_cache=True),False)
        self.assertEqual(route_check_triglavian(30000142, 30004590, mode="p_shortest", static_cache=True),False)
        self.assertEqual(route_length(30000142, 30004590, mode="p_shortest", static_cache=True), 32)

        self.assertEqual(route_path_nodes(30000142, 30004590, mode="p_safest", static_cache=True),[30000142, 30000144, 30000139, 30002791, 30002805, 30002803, 30002768, 30002765, 30002764, 30002762, 30004974, 30004973, 30004975, 30003830, 30003833, 30003827, 30003829, 30003836, 30003841, 30004046, 30004044, 30004043, 30004042, 30004040, 30004589, 30004586, 30004584, 30004554, 30004552, 30004553, 30004555, 30004557, 30004573, 30004574, 30004575, 30004578, 30004581, 30004583, 30004590])
        self.assertEqual(route_path_gates(30000142, 30004590, mode="p_safest", static_cache=True),[(30000142, 30000144, 'Stargate'), (30000144, 30000139, 'Stargate'), (30000139, 30002791, 'Stargate'), (30002791, 30002805, 'Stargate'), (30002805, 30002803, 'Stargate'), (30002803, 30002768, 'Stargate'), (30002768, 30002765, 'Stargate'), (30002765, 30002764, 'Stargate'), (30002764, 30002762, 'Stargate'), (30002762, 30004974, 'Stargate'), (30004974, 30004973, 'Stargate'), (30004973, 30004975, 'Stargate'), (30004975, 30003830, 'Stargate'), (30003830, 30003833, 'Stargate'), (30003833, 30003827, 'Stargate'), (30003827, 30003829, 'Stargate'), (30003829, 30003836, 'Stargate'), (30003836, 30003841, 'Stargate'), (30003841, 30004046, 'Stargate'), (30004046, 30004044, 'Stargate'), (30004044, 30004043, 'Stargate'), (30004043, 30004042, 'Stargate'), (30004042, 30004040, 'Stargate'), (30004040, 30004589, 'Stargate'), (30004589, 30004586, 'Stargate'), (30004586, 30004584, 'Stargate'), (30004584, 30004554, 'Stargate'), (30004554, 30004552, 'Stargate'), (30004552, 30004553, 'Stargate'), (30004553, 30004555, 'Stargate'), (30004555, 30004557, 'Stargate'), (30004557, 30004573, 'Stargate'), (30004573, 30004574, 'Stargate'), (30004574, 30004575, 'Stargate'), (30004575, 30004578, 'Stargate'), (30004578, 30004581, 'Stargate'), (30004581, 30004583, 'Stargate'), (30004583, 30004590, 'Stargate')])
        self.assertEqual(route_check_edencom(30000142, 30004590, mode="p_safest", static_cache=True),False)
        self.assertEqual(route_check_triglavian(30000142, 30004590, mode="p_safest", static_cache=True),False)
        self.assertEqual(route_length(30000142, 30004590, mode="p_safest", static_cache=True), 38)

        self.assertEqual(route_path_nodes(30000142, 30004590, mode="p_less_safe", static_cache=True),[30000142, 30000138, 30001379, 30001376, 30002813, 30045346, 30045345, 30045353, 30045338, 30045344, 30003837, 30003836, 30003841, 30004046, 30004044, 30004043, 30004042, 30004040, 30004589, 30004586, 30004584, 30004554, 30004552, 30004553, 30004555, 30004557, 30004573, 30004574, 30004575, 30004578, 30004581, 30004583, 30004590])
        self.assertEqual(route_path_gates(30000142, 30004590, mode="p_less_safe", static_cache=True),[(30000142, 30000138, 'Stargate'), (30000138, 30001379, 'Stargate'), (30001379, 30001376, 'Stargate'), (30001376, 30002813, 'Stargate'), (30002813, 30045346, 'Stargate'), (30045346, 30045345, 'Stargate'), (30045345, 30045353, 'Stargate'), (30045353, 30045338, 'Stargate'), (30045338, 30045344, 'Stargate'), (30045344, 30003837, 'Stargate'), (30003837, 30003836, 'Stargate'), (30003836, 30003841, 'Stargate'), (30003841, 30004046, 'Stargate'), (30004046, 30004044, 'Stargate'), (30004044, 30004043, 'Stargate'), (30004043, 30004042, 'Stargate'), (30004042, 30004040, 'Stargate'), (30004040, 30004589, 'Stargate'), (30004589, 30004586, 'Stargate'), (30004586, 30004584, 'Stargate'), (30004584, 30004554, 'Stargate'), (30004554, 30004552, 'Stargate'), (30004552, 30004553, 'Stargate'), (30004553, 30004555, 'Stargate'), (30004555, 30004557, 'Stargate'), (30004557, 30004573, 'Stargate'), (30004573, 30004574, 'Stargate'), (30004574, 30004575, 'Stargate'), (30004575, 30004578, 'Stargate'), (30004578, 30004581, 'Stargate'), (30004581, 30004583, 'Stargate'), (30004583, 30004590, 'Stargate')])
        self.assertEqual(route_check_edencom(30000142, 30004590, mode="p_less_safe", static_cache=True),False)
        self.assertEqual(route_check_triglavian(30000142, 30004590, mode="p_less_safe", static_cache=True),False)
        self.assertEqual(route_length(30000142, 30004590, mode="p_less_safe", static_cache=True), 32)

        # Jita to Amarr
        self.assertEqual(route_length(30000142, 30002187, mode="p_shortest", static_cache=True), 11)

        self.assertEqual(route_length(30000142, 30002187, mode="p_safest", static_cache=True), 45)

        self.assertEqual(route_length(30000142, 30002187, mode="p_less_safe", static_cache=True), 40)

        self.assertEqual(systems_range(30000142, 1, static_cache=True), [30000138, 30000140, 30000143, 30000144, 30000145, 30001363, 30002780])
