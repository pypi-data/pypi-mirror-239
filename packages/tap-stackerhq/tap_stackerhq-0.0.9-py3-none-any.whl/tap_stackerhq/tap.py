"""StackerHQ tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_stackerhq import streams


class TapStackerHQ(Tap):
    """StackerHQ tap class."""

    name = "tap-stackerhq"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "auth_token",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="The StackerHQ API token",
        ),
        th.Property(
            "stack_id",
            th.StringType,
            required=True,
            description="Stack ID to read data from",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
        )
    ).to_dict()

    def discover_streams(self) -> list[streams.StackerHQStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.Fines(self),
            streams.Assets(self),
            streams.Region(self),
            streams.Rental(self),
            streams.Damages(self),
            streams.Investigations(self),
            streams.InvestigationsRegions(self),
        ]


if __name__ == "__main__":
    TapStackerHQ.cli()
