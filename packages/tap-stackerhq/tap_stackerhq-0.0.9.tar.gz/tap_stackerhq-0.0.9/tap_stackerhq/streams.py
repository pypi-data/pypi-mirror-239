"""Stream type classes for tap-stackerhq."""

from __future__ import annotations

import typing as t
from pathlib import Path

from tap_stackerhq.client import StackerHQStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class Fines(StackerHQStream):
    """Define custom stream."""

    name = "fines"
    path = "/object.custom.fines/records/"
    primary_keys: t.ClassVar[list[str]] = ["_sid"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "fines.json"

class Assets(StackerHQStream):
    """Define custom stream."""

    name = "assets"
    path = "/object.custom.assets/records/"
    primary_keys: t.ClassVar[list[str]] = ["_sid"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "assets.json"

class Region(StackerHQStream):
    """Define custom stream."""

    name = "regions"
    path = "/object.custom.people/records/"
    primary_keys: t.ClassVar[list[str]] = ["_sid"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "regions.json"

class Rental(StackerHQStream):
    """Define custom stream."""

    name = "rentals"
    path = "/object.custom.rentals/records/"
    primary_keys: t.ClassVar[list[str]] = ["_sid"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "rentals.json"

class Damages(StackerHQStream):
    """Define custom stream."""

    name = "damages"
    path = "/object.custom.damages/records/"
    primary_keys: t.ClassVar[list[str]] = ["_sid"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "damages.json"

class Investigations(StackerHQStream):
    """Define custom stream."""

    name = "investigations"
    path = "/object.custom.onderzoeken/records/"
    primary_keys: t.ClassVar[list[str]] = ["_sid"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "investigations.json"

class InvestigationsRegions(StackerHQStream):
    """Define custom stream."""

    name = "investigations_regions"
    path = "/object.custom.regions/records/"
    primary_keys: t.ClassVar[list[str]] = ["_sid"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "investigations_regions.json"