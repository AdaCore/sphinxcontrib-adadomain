PIP?=pip3
WHEELS_DIR?=$(PWD)/wheels
PIP_WHEEL_ARGS?=

WHEEL_TARGETS = sphinxcontrib-adadomain-wheel laldoc-wheel

all: $(WHEEL_TARGETS)
.PHONY: $(WHEEL_TARGETS)

sphinxcontrib-adadomain-wheel:
	$(PIP) wheel --wheel-dir=$(WHEELS_DIR) $(PIP_WHEEL_ARGS) .

laldoc-wheel:
	$(PIP) wheel --wheel-dir=$(WHEELS_DIR) $(PIP_WHEEL_ARGS) ./laldoc
