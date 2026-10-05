"""Build the bounded Gate 8 fixture from frozen official snapshots.

Research-only utility. Requires pyshp; it does not call GeoImpact.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import tarfile
from pathlib import Path

import shapefile
from pyproj import Transformer
from shapely.geometry import shape
from shapely.ops import transform

BASE_ARCHIVE_SHA256 = "7c1f43a0e9adf1ccc99b66051482b7c2a3f8ffdf7f42aeb4eedd3c554a1dc67b"
CANDIDATE_WFS_SHA256 = "2f64c939d0052076d3bb4ddb02e9230cffeafdc606c36c673612a90686add834"
DEPENDENCY_WFS_SHA256 = "02aadfc63c7f48ed67f84aa8b1c7c4ba5069c25b737e5f0e829d977c28b5eb5e"
TARGET_CODE = "69"
TARGET_NAME = "SIERRA DE BAZA"
TARGET_FIGURE = "Parque Natural"
ANALYSIS_CRS = "EPSG:25830"
GEOJSON_CRS = "OGC:CRS84"
CHANGE_ENVELOPE_CONTEXT_M = 10_000


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_hash(path: Path, expected: str) -> None:
    actual = sha256(path)
    if actual != expected:
        raise SystemExit(f"snapshot hash mismatch for {path}: {actual}")


def read_base_polygon(archive: Path):
    temp = archive.parent / "gate8-base-extract"
    temp.mkdir(exist_ok=True)
    with tarfile.open(archive, "r:gz") as bundle:
        bundle.extractall(temp, filter="data")
    source = temp / "EENNPP/InfGeografica/InfVectorial/Shapes/ETRS89_30/EENNPP.shp"
    reader = shapefile.Reader(str(source), encoding="latin1")
    fields = [field[0] for field in reader.fields[1:]]
    matches = []
    for record, shp in zip(reader.iterRecords(), reader.iterShapes()):
        attributes = dict(zip(fields, record))
        if (
            str(attributes["CODIGOESPA"]) == TARGET_CODE
            and attributes["NOMBRE"] == TARGET_NAME
            and attributes["FIGURA"] == TARGET_FIGURE
        ):
            matches.append(shape(shp.__geo_interface__))
    if len(matches) != 1:
        raise SystemExit(f"expected one BASE target polygon, found {len(matches)}")
    return matches[0]


def read_current_polygon(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("crs", {}).get("properties", {}).get("name") != "urn:ogc:def:crs:EPSG::3042":
        raise SystemExit("unexpected candidate WFS CRS")
    matches = [
        feature
        for feature in data["features"]
        if str(feature["properties"].get("CODIGOESPA")) == TARGET_CODE
        and feature["properties"].get("NOMBRE") == TARGET_NAME
        and feature["properties"].get("FIGURA") == TARGET_FIGURE
    ]
    if len(matches) != 1:
        raise SystemExit(f"expected one CANDIDATE target polygon, found {len(matches)}")
    return shape(matches[0]["geometry"])


def as_feature(geometry, source_crs: str, identifier: str, id_field: str) -> dict:
    project = Transformer.from_crs(source_crs, GEOJSON_CRS, always_xy=True).transform
    lonlat = transform(project, geometry)
    if lonlat.is_empty or not lonlat.is_valid:
        raise SystemExit(f"invalid geometry for {identifier}")
    return {
        "type": "Feature",
        "geometry": lonlat.__geo_interface__,
        "properties": {id_field: identifier},
    }


def write_collection(path: Path, features: list[dict]) -> None:
    features.sort(key=lambda feature: str(next(iter(feature["properties"].values()))))
    payload = {"type": "FeatureCollection", "features": features}
    path.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, default=Path(__file__).parent)
    args = parser.parse_args()
    archive = args.raw_dir / "EENNPP_2015.tar.gz"
    candidate = args.raw_dir / "EENNPP_current_WFS.geojson"
    dependency = args.raw_dir / "equipamientos_2026-10-05_WFS.geojson"
    verify_hash(archive, BASE_ARCHIVE_SHA256)
    verify_hash(candidate, CANDIDATE_WFS_SHA256)
    verify_hash(dependency, DEPENDENCY_WFS_SHA256)

    base = read_base_polygon(archive)
    candidate_polygon = read_current_polygon(candidate)
    current_to_analysis = Transformer.from_crs(3042, ANALYSIS_CRS, always_xy=True).transform
    candidate_analysis = transform(current_to_analysis, candidate_polygon)
    if not base.is_valid or not candidate_analysis.is_valid or base.is_empty or candidate_analysis.is_empty:
        raise SystemExit("target source geometry is invalid or empty")
    changed = base.symmetric_difference(candidate_analysis)
    min_x, min_y, max_x, max_y = changed.bounds
    box = (
        min_x - CHANGE_ENVELOPE_CONTEXT_M,
        min_y - CHANGE_ENVELOPE_CONTEXT_M,
        max_x + CHANGE_ENVELOPE_CONTEXT_M,
        max_y + CHANGE_ENVELOPE_CONTEXT_M,
    )

    dep_data = json.loads(dependency.read_text(encoding="utf-8"))
    if dep_data.get("crs", {}).get("properties", {}).get("name") != "urn:ogc:def:crs:EPSG::3042":
        raise SystemExit("unexpected dependency WFS CRS")
    dep_to_analysis = Transformer.from_crs(3042, ANALYSIS_CRS, always_xy=True).transform
    dependency_features = []
    for feature in dep_data["features"]:
        if feature["geometry"] is None or feature["geometry"]["type"] != "Point":
            continue
        x, y = transform(dep_to_analysis, shape(feature["geometry"])).coords[0]
        if box[0] <= x <= box[2] and box[1] <= y <= box[3]:
            identifier = str(feature["properties"]["CODIGOEQUI"])
            dependency_features.append(
                as_feature(shape(feature["geometry"]), "EPSG:3042", identifier, "CODIGOEQUI")
            )
    ids = [f["properties"]["CODIGOEQUI"] for f in dependency_features]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate selected dependency stable IDs")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_collection(
        args.out_dir / "base.geojson",
        [as_feature(base, ANALYSIS_CRS, TARGET_CODE, "CODIGOESPA")],
    )
    write_collection(
        args.out_dir / "candidate.geojson",
        [as_feature(candidate_polygon, "EPSG:3042", TARGET_CODE, "CODIGOESPA")],
    )
    write_collection(args.out_dir / "dependencies.geojson", dependency_features)
    print(
        json.dumps(
            {
                "base_features": 1,
                "candidate_features": 1,
                "changed_footprint_area_m2": changed.area,
                "change_envelope_context_m": CHANGE_ENVELOPE_CONTEXT_M,
                "selected_dependencies": len(dependency_features),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
