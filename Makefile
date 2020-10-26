.PHONY: clean build
SHELL=/bin/bash

UPSTREAM_REPO=https://github.com/elastic/ecs.git
UPSTREAM_BRANCH=v1.6.0

all: clean configure build
	cp -R build/generated dist

clean:
	rm -rf build dist

configure:
	git clone --depth 1 --branch $(UPSTREAM_BRANCH) $(UPSTREAM_REPO) build
	cat patches/*.patch | patch -p1 -d build --forward -r - || true
	for FILE in $$(ls docs); do \
		cp "docs/$${FILE}" build/docs/; \
		echo "include::$${FILE}[]" >> build/docs/index.asciidoc; \
	done
	dpkg-parsechangelog -l changelog --show-field Version > build/version

build:
	cd build \
	&& python3 scripts/generator.py --include "../schemas" --template-settings ../templates/default.json \
	&& asciidoc -o generated/index.html docs/index.asciidoc

deps:
	apt install -y --no-install-recommends asciidoc devscripts python3 python3-pip python3-yaml python3-autopep8 python3-git python3-jinja2

dev:
	cd build \
	&& python3 -m venv venv && source venv/bin/activate && pip install -r scripts/requirements.txt \
	&& python3 scripts/generator.py --include "../schemas" --template-settings ../templates/default.json \
	&& asciidoc -o generated/index.html docs/index.asciidoc \
	&& cp -R build/generated dist
