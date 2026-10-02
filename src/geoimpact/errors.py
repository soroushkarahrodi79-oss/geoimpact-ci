"""Domain errors that the CLI maps to a controlled exit-2 failure.

A ``GeoImpactError`` marks an *expected* user, input, or domain failure that
the command-line boundary may translate into a concise ``GeoImpact error: ...``
message and exit code 2. Unexpected programming failures must not subclass it,
so they stay visible instead of being disguised as controlled CLI errors.
"""

from __future__ import annotations


class GeoImpactError(Exception):
    """Base class for expected GeoImpact domain/input/usage failures."""


class InputError(GeoImpactError):
    """Malformed, unsupported, or invalid analysis input data."""
