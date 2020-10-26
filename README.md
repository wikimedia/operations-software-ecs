Elastic Common Schema
===
Wrapper for [ECS upstream](https://github.com/elastic/ecs) to provide WMF-specific customizations to the Elastic Common Schema.

Requirements
---
`apt install -y --no-install-recommends make && make deps`

Layout
---
* `./docs/` Custom documentation files to include.
* `./patches/` Patches to upstream.
* `./schemas/` Custom schema definitions.
* `./templates/` Base index template templates.
* `./changelog` Debian-formatted schema changelog.
