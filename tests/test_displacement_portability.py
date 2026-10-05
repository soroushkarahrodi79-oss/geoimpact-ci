import json
from pathlib import Path

from shapely.geometry import shape

from geoimpact.geometry_change import measure_primary_change


FIXTURE = Path(__file__).parent / "fixtures" / "displacement_portability_pair.geojson"


def test_sierra_derived_compact_pair_has_canonical_displacement() -> None:
    pair = json.loads(FIXTURE.read_text(encoding="utf-8"))
    by_state = {
        feature["properties"]["state"]: shape(feature["geometry"])
        for feature in pair["features"]
    }

    result = measure_primary_change(
        {"sierra-window": by_state["base"]},
        {"sierra-window": by_state["candidate"]},
    )

    assert result["max_boundary_displacement_m"] == 368.82509547712834
