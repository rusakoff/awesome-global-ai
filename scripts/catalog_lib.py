#!/usr/bin/env python3
"""Shared helpers for the Awesome Global AI catalog."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FILES = {
    "organizations": DATA / "organizations.csv",
    "people": DATA / "people.csv",
    "media": DATA / "media.csv",
    "resources": DATA / "resources.csv",
}
TIERS = {"A", "B", "C", "D", "Reference"}
STATUSES = {"active", "historical", "inactive"}
URL_FIELDS = {
    "website",
    "github",
    "youtube",
    "x",
    "linkedin",
    "huggingface",
    "scholar",
    "verification_url",
}
REQUIRED_COMMON = {
    "id",
    "name",
    "country",
    "focus",
    "tier",
    "website",
    "status",
    "verified_at",
    "verification_url",
    "description",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [
            {key: (value or "").strip() for key, value in row.items()}
            for row in csv.DictReader(handle)
        ]


def load_catalog() -> dict[str, list[dict[str, str]]]:
    return {name: read_rows(path) for name, path in FILES.items()}


def all_rows(catalog: dict[str, list[dict[str, str]]]) -> Iterable[tuple[str, dict[str, str]]]:
    for entity_type, rows in catalog.items():
        for row in rows:
            yield entity_type, row


def split_tags(value: str) -> list[str]:
    return [tag.strip() for tag in value.split(";") if tag.strip()]


def md(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def link(label: str, url: str) -> str:
    return f"[{md(label)}]({url})" if url else ""


def account_links(row: dict[str, str]) -> str:
    labels = [
        ("GitHub", "github"),
        ("YouTube", "youtube"),
        ("X", "x"),
        ("LinkedIn", "linkedin"),
        ("Hugging Face", "huggingface"),
        ("Scholar", "scholar"),
    ]
    return " · ".join(link(label, row.get(field, "")) for label, field in labels if row.get(field))


def counts(catalog: dict[str, list[dict[str, str]]]) -> dict[str, Counter[str]]:
    countries: Counter[str] = Counter()
    regions: Counter[str] = Counter()
    focus: Counter[str] = Counter()
    tiers: Counter[str] = Counter()
    for _, row in all_rows(catalog):
        countries[row["country"]] += 1
        if row.get("region"):
            regions[row["region"]] += 1
        tiers[row["tier"]] += 1
        focus.update(split_tags(row["focus"]))
    return {"countries": countries, "regions": regions, "focus": focus, "tiers": tiers}

