"""REST client handling, including DelightedStream base class."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Iterable

import requests
import delighted
from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.tap_base import Tap
from singer_sdk.streams import Stream

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class DelightedStream(Stream):
    """Delighted stream class."""
    
    def __init__(self, tap: Tap):
        super().__init__(tap)
        delighted.api_key = self.config.get("auth_token")