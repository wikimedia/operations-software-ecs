Elastic Common Schema
===
Wrapper for [ECS upstream](https://github.com/elastic/ecs) to provide WMF-specific customizations to the Elastic Common Schema.

Requirements
---
Debian: `asciidoc devscripts python3 python3-pip python3-yaml python3-autopep8 python3-git python3-jinja2`
Fedora (dnf): `asciidoc devscripts python3-pip python3-yaml python3-autopep8 python3-GitPython python3-jinja2`

Layout
---
* `./docs/` Custom documentation files to include.
* `./patches/` Patches to upstream.
* `./schemas/` Custom schema definitions.
* `./templates/` Base index template templates.
* `./changelog` Debian-formatted schema changelog.
