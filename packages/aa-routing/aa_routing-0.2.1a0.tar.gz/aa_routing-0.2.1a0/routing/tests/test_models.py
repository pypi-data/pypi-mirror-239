from django.test import TestCase

from routing.models import SolarSystem, SolarSystemConnection


class SolarSystemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        SolarSystem.objects.create(id=1, security=0.5)

    def test_security_label(self):
        solarsystem = SolarSystem.objects.get(id=1)
        field_label = solarsystem._meta.get_field('security').verbose_name
        self.assertEqual(field_label, 'Security Status')

    def test_security_max_value(self):
        solarsystem = SolarSystem.objects.get(id=1)
        max_value = solarsystem._meta.get_field('security').validators[1].limit_value
        self.assertEqual(max_value, 1.0)


class SolarSystemConnectionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        SolarSystem.objects.create(id=1, security=0.5)
        SolarSystem.objects.create(id=2, security=0.7)
        SolarSystemConnection.objects.create(
            fromsolarsystem_id=1,
            tosolarsystem_id=2,
            p_shortest=1,
            p_safest=1,
            p_less_safe=1)

    def test_p_shortest_default(self):
        connection = SolarSystemConnection.objects.get(id=1)
        default_value = connection._meta.get_field('p_shortest').default
        self.assertEqual(default_value, 1)

    def test_safest_default(self):
        connection = SolarSystemConnection.objects.get(id=1)
        default_value = connection._meta.get_field('p_safest').default
        self.assertEqual(default_value, 1)

    def test_p_less_safe_default(self):
        connection = SolarSystemConnection.objects.get(id=1)
        default_value = connection._meta.get_field('p_less_safe').default
        self.assertEqual(default_value, 1)
