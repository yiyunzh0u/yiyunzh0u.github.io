"""Fetch a public Google Scholar profile and write homepage badge data."""

from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

SERPAPI_URL = "https://serpapi.com/search.json"


def parse_profile(data: dict[str, Any], scholar_id: str) -> dict[str, Any]:
    """Validate a Google Scholar Author API response."""
    if data.get("error"):
        raise ValueError(f"SerpAPI error: {data['error']}")

    returned_id = data.get("search_parameters", {}).get("author_id")
    name = data.get("author", {}).get("name")
    citation_table = data.get("cited_by", {}).get("table", [])
    citations = (
        citation_table[0].get("citations", {}).get("all")
        if citation_table
        else None
    )

    if returned_id != scholar_id:
        raise ValueError(f"Unexpected Scholar author ID: {returned_id!r}")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Scholar response has no author name")
    if type(citations) is not int or citations < 0:
        raise ValueError("Scholar response has no integer all-time citation count")

    return {
        "container_type": "Author",
        "source": "AUTHOR_PROFILE_PAGE",
        "scholar_id": scholar_id,
        "name": name.strip(),
        "citedby": citations,
        "updated": datetime.now(timezone.utc).isoformat(),
    }


def fetch_author(
    scholar_id: str, api_key: str, attempts: int = 3
) -> dict[str, Any]:
    """Fetch an author profile through SerpAPI with bounded retries."""
    last_error = "unknown error"

    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(
                SERPAPI_URL,
                params={
                    "engine": "google_scholar_author",
                    "author_id": scholar_id,
                    "api_key": api_key,
                    "hl": "en",
                    "num": 1,
                },
                timeout=90,
            )
            response.raise_for_status()
            return parse_profile(response.json(), scholar_id)
        except requests.exceptions.RequestException as error:
            status = error.response.status_code if error.response is not None else None
            last_error = (
                f"HTTP status {status}"
                if status is not None
                else type(error).__name__
            )
            if attempt < attempts:
                delay = 15 * attempt
                print(
                    f"Fetch attempt {attempt}/{attempts} failed: {last_error}. "
                    f"Retrying in {delay}s...",
                    file=sys.stderr,
                )
                time.sleep(delay)
        except ValueError as error:
            last_error = str(error)
            if attempt < attempts:
                delay = 15 * attempt
                print(
                    f"Fetch attempt {attempt}/{attempts} failed: {last_error}. "
                    f"Retrying in {delay}s...",
                    file=sys.stderr,
                )
                time.sleep(delay)

    raise RuntimeError(
        f"Google Scholar fetch failed after {attempts} attempts: {last_error}"
    ) from None


def write_results(author: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    with (output_dir / "gs_data.json").open("w", encoding="utf-8") as file:
        json.dump(author, file, ensure_ascii=False, separators=(",", ":"))

    shield = {
        "schemaVersion": 1,
        "label": "citations",
        "message": str(author["citedby"]),
    }
    with (output_dir / "gs_data_shieldsio.json").open(
        "w", encoding="utf-8"
    ) as file:
        json.dump(shield, file, ensure_ascii=False, separators=(",", ":"))

    print(
        f"Fetched {author['name']} ({author['scholar_id']}): "
        f"{author['citedby']} citations"
    )


def main() -> None:
    scholar_id = os.environ.get("GOOGLE_SCHOLAR_ID", "").strip()
    api_key = os.environ.get("SERPAPI_API_KEY", "").strip()
    if not scholar_id:
        raise RuntimeError("GOOGLE_SCHOLAR_ID is missing")
    if not api_key:
        raise RuntimeError(
            "SERPAPI_API_KEY is missing. Add this repository Actions secret "
            "before running the workflow."
        )

    output_dir = Path(os.environ.get("OUTPUT_DIR", "results"))
    write_results(fetch_author(scholar_id, api_key), output_dir)


if __name__ == "__main__":
    main()
