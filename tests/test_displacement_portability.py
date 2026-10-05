import json
from pathlib import Path

from pyproj import Transformer
from shapely.geometry import shape
from shapely.ops import transform

from geoimpact.geometry_change import measure_primary_change


FIXTURE = Path(__file__).parent / "fixtures" / "displacement_portability_pair.geojson"


def test_sierra_derived_compact_pair_has_canonical_displacement() -> None:
    pair = json.loads(FIXTURE.read_text(encoding="utf-8"))
    project = Transformer.from_crs(
        pair["coordinate_reference"], "EPSG:25830", always_xy=True
    ).transform
    by_state = {
        feature["properties"]["state"]: transform(project, shape(feature["geometry"]))
        for feature in pair["features"]
    }

    result = measure_primary_change(
        {"sierra-window": by_state["base"]},
        {"sierra-window": by_state["candidate"]},
    )

    assert result["max_boundary_displacement_m"] == 368.82509547712834
