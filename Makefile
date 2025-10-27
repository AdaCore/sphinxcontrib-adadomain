PYTHON=python3
WHEELS_DIR=$(PWD)/wheels

WHEEL_TARGETS = sphinxcontrib-adadomain-wheel laldoc-wheel

all: $(WHEEL_TARGETS)
.PHONY: $(WHEEL_TARGETS)

sphinxcontrib-adadomain-wheel:
	$(PYTHON) -m build --wheel \
		--outdir $(WHEELS_DIR) \
		--installer pip

laldoc-wheel:
	cd laldoc && $(PYTHON) -m build --wheel \
		--outdir $(WHEELS_DIR) \
		--installer pip
