from typing import Tuple

from drifters.app_settings import DRIFTERS_DRIFTERHOLE_WEIGHT
from drifters.models import Wormhole

# Helper functions for AA Routing


def include_drifters_driftercomplexes(weight: float = DRIFTERS_DRIFTERHOLE_WEIGHT) -> list[Tuple]:
    edges = []
    for complex in Wormhole.Complexes:
        for wh in Wormhole.objects.filter(complex=complex):
            edges.append((
                wh.system.id, wh.complex_id,
                {'p_shortest': weight, 'p_safest': weight, 'p_less_safe': weight, "type": "drifter_k"}))
            edges.append((
                wh.complex_id, wh.system.id,
                {'p_shortest': weight, 'p_safest': weight, 'p_less_safe': weight, "type": "drifter_w"}))
    return edges
