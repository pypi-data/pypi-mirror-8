"""Tests for the template tags of the ``outlets`` app."""
from django.test import TestCase

from . import factories
from ..templatetags import outlets_tags


class GetOutletCountriesTestCase(TestCase):
    """Tests for the ``get_outlet_countries`` template tag."""
    longMessage = True

    def setUp(self):
        self.country = factories.OutletCountryFactory()

    def test_tag(self):
        self.assertEqual(
            list(outlets_tags.get_outlet_countries()),
            [self.country], msg='Should return all the countries.')
