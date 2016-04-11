DOT_FILES := $(wildcard **/*.dot)
SVG_FILES := $(patsubst %.dot, %.svg, $(DOT_FILES))

all: $(SVG_FILES)

%.svg : %.dot
	dot -Tsvg -o $@ $<

clean: clean-pyc clean-svg

clean-pyc:
	find . -name '*.pyc' -exec rm \{\} \;

clean-svg:
	rm -f $(SVG_FILES)

test:
	nosetests -x openfisca_douanes/tests

.PHONY: clean clean-pyc clean-svg download_pad test
