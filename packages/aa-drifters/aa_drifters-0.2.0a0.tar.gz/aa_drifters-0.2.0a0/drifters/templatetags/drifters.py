from eveuniverse.models.universe_2 import EveRegion, EveSolarSystem
from routing.routing import systems_range

from django import template

from drifters.app_settings import DRIFTERS_POI_SEARCH_RANGE
from drifters.models import Wormhole

register = template.Library()


@register.simple_tag()
def find_closest_holes(system: EveSolarSystem, complex: Wormhole.Complexes):
    holes = Wormhole.objects.filter(system__in=systems_range(system.id, DRIFTERS_POI_SEARCH_RANGE, include_source=True), complex=complex, archived=False)
    if holes.count() == 0:
        return None
    else:
        return holes


@register.simple_tag()
def region_holes(region: EveRegion, complex: Wormhole.Complexes):
    holes = Wormhole.objects.filter(system__eveconstellation__everegion=region, complex=complex, archived=False)
    if holes.count() == 0:
        return None
    else:
        return holes
