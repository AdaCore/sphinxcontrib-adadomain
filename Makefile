PYTHON=python3
PYTHON_TAG=py3
WHEELS_DIR=wheels

WHEEL_TARGETS = sphinxcontrib-adadomain-wheel laldoc-wheel

all: $(WHEEL_TARGETS)
.PHONY: $(WHEEL_TARGETS)

sphinxcontrib-adadomain-wheel:
	$(PYTHON) setup.py bdist_wheel \
	  -d $(WHEELS_DIR) \
	  --python-tag $(PYTHON_TAG)

laldoc-wheel:
	cd laldoc && $(PYTHON) setup.py bdist_wheel \
	  -d $(WHEELS_DIR) \
	  --python-tag $(PYTHON_TAG)
