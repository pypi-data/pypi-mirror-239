"""Stream type classes for tap-delighted."""

from __future__ import annotations

import typing as t
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable
import delighted
from datetime import datetime
import pytz
timezone = pytz.timezone('America/Chicago')

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_delighted.client import DelightedStream

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")
# TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.


class SurveyResponsesStream(DelightedStream):
    """Define custom stream."""

    name = "survey responses"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = "updated_at"
    is_sorted = True

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("person", th.StringType),
        th.Property(
            "score",
            th.IntegerType,
            description="The survey response score",
        ),
        th.Property("created_at", th.IntegerType),
        th.Property("updated_at", th.IntegerType),
        th.Property(
            "person_properties",
            th.ObjectType(
                th.Property("CaseId", th.StringType),
                th.Property("UserId", th.StringType),
                th.Property("UserCountry", th.StringType),
                th.Property("ClosedByEmployee", th.StringType),
                th.Property("Delighted Source", th.StringType),
                th.Property("Delighted Link Name", th.StringType),
                th.Property("Delighted Device Type", th.StringType),
                th.Property("Delighted Operating System", th.StringType),
                th.Property("Delighted Browser", th.StringType)
            )
        )
    ).to_dict()
    
    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        """Return a generator of row-type dictionary objects.
        """
        starting_date = self.get_starting_replication_key_value(context)
        if type(starting_date) == str:
            since = datetime.strptime(starting_date, "%Y-%m-%d")
        else:
            since = datetime.fromtimestamp(starting_date)
        since = since.replace(tzinfo=pytz.UTC)
        response = True
        page = 1
        survey_responses = []

        while response:
            self.logger.info(f'retrieving page {page} of survey responses')
            response = delighted.SurveyResponse.all(
                page = page,
                per_page = 100,
                since = since
            )
            survey_responses.extend(response)
            page += 1
        
        for row in survey_responses:
            yield row
