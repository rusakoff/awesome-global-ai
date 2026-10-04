# Contributing

Contributions are welcome through pull requests.

## Inclusion checklist

- The entry is globally influential, regionally important, scientifically useful, or a strong specialist source.
- At least one primary or official verification URL is supplied.
- Social profiles are official or clearly owned by the listed person or organization.
- Descriptions are neutral, specific, and no longer than one sentence.
- `focus` uses existing slugs from `data/taxonomy.yml` when possible.
- Links do not contain tracking parameters.
- The entry is not a duplicate, subsidiary profile, product page, or renamed version of an existing record.

## Workflow

1. Edit the relevant CSV file in `data/`.
2. Run `python3 scripts/validate_catalog.py`.
3. Run `python3 scripts/generate_catalog.py`.
4. Review the generated `CATALOG.md` and `docs/STATS.md`.

Unverified suggestions belong in `data/candidates.csv`, not the main catalog.

