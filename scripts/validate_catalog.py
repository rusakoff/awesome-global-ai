#!/usr/bin/env python3
"""Validate catalog structure and optionally probe website availability."""

from __future__ import annotations

import argparse
import re
import socket
import ssl
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from catalog_lib import (
    FILES,
    REQUIRED_COMMON,
    STATUSES,
    TIERS,
    URL_FIELDS,
    all_rows,
    load_catalog,
)


ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def valid_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc) and " " not in value


def probe(url: str, timeout: float) -> tuple[str, str]:
    request = Request(url, headers={"User-Agent": "awesome-global-ai-link-check/1.0"})
    context = ssl.create_default_context()
    try:
        with urlopen(request, timeout=timeout, context=context) as response:
            return url, str(response.status)
    except HTTPError as exc:
        return url, str(exc.code)
    except (URLError, TimeoutError, socket.timeout, OSError, ValueError) as exc:
        return url, f"ERROR {type(exc).__name__}: {exc}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-links", action="store_true", help="Probe primary websites over HTTP")
    parser.add_argument("--timeout", type=float, default=12.0)
    parser.add_argument("--workers", type=int, default=12)
    args = parser.parse_args()

    catalog = load_catalog()
    errors: list[str] = []
    warnings: list[str] = []
    seen_ids: dict[str, str] = {}
    seen_websites: dict[str, tuple[str, str]] = {}

    for entity_type, path in FILES.items():
        rows = catalog[entity_type]
        if not rows:
            errors.append(f"{path.name}: no rows")
            continue
        missing_headers = REQUIRED_COMMON - set(rows[0])
        if missing_headers:
            errors.append(f"{path.name}: missing headers {sorted(missing_headers)}")

    for entity_type, row in all_rows(catalog):
        label = f"{entity_type}:{row.get('id') or '<missing-id>'}"
        for field in REQUIRED_COMMON:
            if not row.get(field):
                errors.append(f"{label}: missing {field}")
        record_id = row.get("id", "")
        if record_id and not ID_RE.fullmatch(record_id):
            errors.append(f"{label}: id must be a lowercase slug")
        if record_id in seen_ids:
            errors.append(f"{label}: duplicate id also used by {seen_ids[record_id]}")
        else:
            seen_ids[record_id] = entity_type
        if row.get("tier") not in TIERS:
            errors.append(f"{label}: invalid tier {row.get('tier')!r}")
        if row.get("status") not in STATUSES:
            errors.append(f"{label}: invalid status {row.get('status')!r}")
        checked = row.get("verified_at", "")
        if checked and not DATE_RE.fullmatch(checked):
            errors.append(f"{label}: invalid verified_at {checked!r}")
        elif checked:
            try:
                if date.fromisoformat(checked) > date.today():
                    warnings.append(f"{label}: verification date is in the future")
            except ValueError:
                errors.append(f"{label}: invalid calendar date {checked!r}")
        for field in URL_FIELDS & set(row):
            value = row.get(field, "")
            if value and not valid_url(value):
                errors.append(f"{label}: malformed {field} URL {value!r}")
        website = row.get("website", "").rstrip("/").lower()
        if website and website in seen_websites:
            previous_type, previous_label = seen_websites[website]
            if previous_type == entity_type and entity_type != "people":
                warnings.append(f"{label}: website also used by {previous_label}")
        elif website:
            seen_websites[website] = (entity_type, label)
        if len(row.get("description", "")) > 180:
            warnings.append(f"{label}: description is longer than 180 characters")

    if args.check_links:
        urls = sorted({row["website"] for _, row in all_rows(catalog) if row.get("website")})
        print(f"Probing {len(urls)} primary websites...")
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {pool.submit(probe, url, args.timeout): url for url in urls}
            for future in as_completed(futures):
                url, result = future.result()
                if result.startswith("ERROR") or result in {"404", "410"}:
                    warnings.append(f"link: {url} -> {result}")

    total = sum(len(rows) for rows in catalog.values())
    print(f"Validated {total} entries across {len(catalog)} files.")
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1
    print(f"Validation passed with {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
