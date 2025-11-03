PIP?=pip3
WHEELS_DIR?=$(PWD)/wheels
PACKAGES_DIR?=$(PWD)/packages

WHEEL_TARGETS = sphinxcontrib-adadomain-wheel laldoc-wheel

all: $(WHEEL_TARGETS)
.PHONY: $(WHEEL_TARGETS)

sphinxcontrib-adadomain-wheel:
	$(PIP) wheel \
	    --wheel-dir=$(WHEELS_DIR) \
	    --no-deps \
	    --find-links=$(PACKAGES_DIR) \
	    --no-index \
	    --no-cache-dir \
	    .

laldoc-wheel:
	$(PIP) wheel \
	    --wheel-dir=$(WHEELS_DIR) \
	    --no-deps \
	    --find-links=$(PACKAGES_DIR) \
	    --no-index \
	    --no-cache-dir \
	    ./laldoc
