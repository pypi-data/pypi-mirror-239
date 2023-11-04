from routing.routing import route_length, systems_range

from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone

from allianceauth.services.hooks import get_extension_logger

from drifters.app_settings import (
    DRIFTERS_BOOKMARK_FOLDER_ID, DRIFTERS_BOOKMARK_FOLDER_NAME,
    DRIFTERS_MOTD_CHANNEL_LINK, DRIFTERS_MOTD_CHANNEL_NAME,
    DRIFTERS_MOTD_SYSTEM_SEARCH_RANGE,
)
from drifters.models import DriftersConfiguration, Wormhole

logger = get_extension_logger(__name__)


def render_complex(request, complex: Wormhole.Complexes) -> str:
    context = {
        "complex": complex,
        "wormholes": Wormhole.objects.filter(complex=complex, archived=False),
        "poi_regions": DriftersConfiguration.get_solo().POI_regions.all(),
        "poi_systems": DriftersConfiguration.get_solo().POI_systems.all(),
    }
    return render_to_string("drifters/complex.html", context, request)


@login_required
@permission_required("drifters.basic_access")
def index(request) -> HttpResponse:
    context = {'complex_renders': []}
    for complex in Wormhole.Complexes:
        context['complex_renders'].append(render_complex(request, complex))
    return render(request, "drifters/index.html", context)


def generate_channel_motd_1() -> str:
    # Generate an ingame channel MOTD with links as needed
    return f"""<font size="13" color="#ff6868e1"><a href="{DRIFTERS_MOTD_CHANNEL_LINK}">{DRIFTERS_MOTD_CHANNEL_NAME}</a></font><font size="13" color="#bfffffff"> (this service will not be available 24/7)<br></font>
<font size="10" color="#ffff0000">--TRAVELs WITH THE WH METRO ONLY AT YOUR OWN RISK!--<br></font>
<font size="12" color="#ffffffff"><b><u>Instructions & Safety Advice:</b></u>
- online & connect to</font><font size="12" color="#ff00a99d"> <a href="bookmarkFolder:{DRIFTERS_BOOKMARK_FOLDER_ID}">{DRIFTERS_BOOKMARK_FOLDER_NAME}</a></font><font size="12" color="#ffffffff">
- burn to entry/exit location and jump through the correct wormhole!<br>- small & fast travel ships with MWD,MJD and cloak are highly recommended!
- Drifter Battleship spawn on the outside of the wormholes and you need to be careful and avoid them at all cost!
- Check the time since last update at the bottom!<br></font>
<font size="10" color="#ff00ff00">Less than 4h, Reliable</font>
<font size="10" color="#ffffff00">More than 4h, Possible/Unconfirmed</font>
<font size="10" color="#ffff0000">More Than 8H Ago, Less Likely<br></font>
<font size="10" color="#ffffffff">% is remaining theoretical max life</font>
<font size="12" color="#ffffffff"><b><u>Active Metro Lines:</b></u></font>
"""


def generate_channel_motd_2() -> str:
    # Generate an ingame channel MOTD with links as needed

    motd_lines = ""

    for complex in Wormhole.Complexes:
        # These three reset to ensure we only post a Complex with >1 System with >= 1 Hole
        motd_lines_per_complex = ""
        valid_hole_count = 0
        valid_system_count = 0
        if Wormhole.objects.filter(complex=complex, archived=False).exists():  # Exit early if we have no Wormholes belonging to a Complex
            motd_lines_per_complex += f"""<br><font size="12" color="#ffffffff"><b>{complex}</b></font>"""
            for motd_system in DriftersConfiguration.get_solo().motd_systems.all():
                # Reset here to only add a System with >0 Holes
                motd_lines_per_complex_per_system = ""
                valid_hole_count = 0
                motd_lines_per_complex_per_system += f"""<br><font size="12" color="#ffffffff"><b>{motd_system}</b><br></font>"""
                for hole in Wormhole.objects.filter(system__in=systems_range(motd_system.id, DRIFTERS_MOTD_SYSTEM_SEARCH_RANGE, include_source=True), complex=complex, archived=False):
                    motd_lines_per_complex_per_system += f"""<font size="12" color="#ffd98d00"><a href="showinfo:5//{hole.system.id}">{hole.system}</a></font><font size="12" color="#ffffffff"> {route_length(motd_system.id, hole.system.id)}J</font> {hole.formatted_lifetime_motd}<br>"""
                    valid_hole_count += 1
                if valid_hole_count >= 1:
                    motd_lines_per_complex += motd_lines_per_complex_per_system
                    valid_system_count += 1

        if valid_system_count > 1:
            motd_lines += motd_lines_per_complex

    return f"""{ motd_lines }<font size="12" color="#bfffffff"><i>Updated {timezone.now()}<br></i></font>"""


@login_required
@permission_required("drifters.basic_access")
def motd(request) -> HttpResponse:
    context = {
        'motd_1': generate_channel_motd_1(),
        'motd_2': generate_channel_motd_2()
    }

    return render(request, "drifters/motd.html", context)
