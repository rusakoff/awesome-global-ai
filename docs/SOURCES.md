# Source strategy

The catalog uses discovery sources to find candidates and primary sources to verify accepted entries.

## Global discovery sources

- [Stanford AI Index 2026](https://hai.stanford.edu/ai-index/2026-ai-index-report) for global research and industry coverage.
- [Epoch AI model database](https://epoch.ai/data/ai-models) for notable and frontier model developers.
- [Epoch AI company database](https://epoch.ai/data/ai-companies) for foundation model companies.
- [ACM Awards](https://awards.acm.org/) and official university profiles for established researchers.
- Official conference sites including [NeurIPS](https://neurips.cc/) and [ICML](https://icml.cc/).
- Community candidate lists such as [Best AI YouTube Channels](https://github.com/best-of-ai/best-ai-youtube-channels) and [Awesome Scientific Machine Learning](https://github.com/MartinuzziFrancesco/awesome-scientific-machine-learning).

## Regional discovery sources

- [AI Singapore](https://aisingapore.org/) and [A*STAR](https://www.a-star.edu.sg/) for Southeast Asia.
- [CENIA](https://cenia.cl/en/) for Chile and the Latam-GPT network.
- [Deep Learning Indaba](https://deeplearningindaba.com/) and [Masakhane](https://www.masakhane.io/) for African research communities.
- [Yandex Research](https://research.yandex.com/about) and [AIRI](https://airi.net/) for Russian-language research.
- Official pages of national institutes and universities across Europe East Asia South Asia the Middle East Latin America and Oceania.

Discovery lists are never copied wholesale. Each accepted entry is normalized and linked to an official website or primary profile in its `verification_url` field.

## Link checking

`scripts/validate_catalog.py --check-links` probes primary websites. Timeouts bot protection and older TLS configurations are reported as warnings because an automated HTTP failure does not prove that a source is invalid. HTTP 404 and DNS failures are reviewed manually.

