MODULE_NAME = hutch-security
SHELL := /usr/bin/env bash -euo pipefail -c

.PHONY: lint
lint:
	tox -e linters

.PHONY: test
test:
	tox

.PHONY: documentation
documentation:
	rm -rf docs/source/hutch.*.rst
	rm -rf docs/source/modules.rst
	rm -rf docs/api/
	sphinx-apidoc --implicit-namespaces --module-first --separate -q -o docs/source/ hutch/ 
	if [ "`uname`" == "Darwin" ]; then \
		find docs/source/*.rst -type f -print0 | \
			xargs -0 \
				sed -Ei '' 's/^([a-z0-9_]+\.)+([a-z0-9_]+) (package|module)/\2 \3/g' ; \
	else \
		find docs/source/*.rst -type f -print0 | \
			xargs -0 \
				sed -ri 's/^([a-z0-9_]+\.)+([a-z0-9_]+) (package|module)/\2 \3/g' ; \
	fi

	sphinx-build -b html docs/source/ docs/api/

.PHONY: clean
clean:
	rm -rf \
		.coverage \
		.eggs \
		.mypy_cache \
		.pytest_cache \
		.tox \
		build \
		htmlcov \
		package \
		test-reports \
		$(MODULE_NAME).egg-info
