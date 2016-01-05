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

download_pad:
	wget https://bimestriel.framapad.org/p/openfisca-douanes/export/markdown -O notes/openfisca-douanes-pad-backup.md

.PHONY: clean clean-pyc clean-svg download_pad
