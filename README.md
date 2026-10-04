# Awesome Global AI

A verified and structured directory of leading AI organizations, researchers, scientific resources, media, and official social accounts from around the world.

**382 entries:** 175 organizations · 103 people · 47 media sources · 57 scientific resources.

> Snapshot verified on 2026-10-04. This is a curated discovery directory rather than a definitive ranking.

## Browse

- **[Full catalog](CATALOG.md)** — organizations, people, media, conferences, journals, benchmarks, and databases.
- **[Statistics](docs/STATS.md)** — coverage by entity type, region, country, tier, and focus.
- **[Methodology](docs/METHODOLOGY.md)** — inclusion, tiers, verification, and maintenance.
- **[Sources](docs/SOURCES.md)** and **[editorial notes](docs/EDITORIAL_NOTES.md)** — discovery inputs and snapshot limitations.
- **[Русская справка](docs/README.ru.md)**.
- **[Canonical data](data/)** — reusable CSV files and a generated combined JSON export.

## Scope

The directory includes frontier model labs, Big Tech research teams, universities, independent institutes, open-source communities, AI infrastructure, robotics, AI for science, safety and governance organizations, researchers, YouTube channels, podcasts, newsletters, conferences, journals, paper discovery tools, model hubs, datasets, and benchmarks.

Each entry separates its **entity type** from its **focus tags**, making the data useful for both people and software. Social links are attached to their owning entity instead of being duplicated as standalone recommendations.

## Quality model

- **A:** global leader or field-defining contributor.
- **B:** major international or regional contributor.
- **C:** authoritative specialist.
- **D:** emerging project tracked for breadth.
- **Reference:** infrastructure for research discovery that should not be ranked competitively.

Every accepted entry has an official or primary verification URL and a verification date. Unresolved suggestions go to `data/candidates.csv`.

## Validate and regenerate

```bash
python3 scripts/validate_catalog.py
python3 scripts/generate_catalog.py
```

Optional live website probe:

```bash
python3 scripts/validate_catalog.py --check-links
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Contributions should add primary sources and avoid promotional language. The catalog data is available under [CC BY 4.0](LICENSE).
