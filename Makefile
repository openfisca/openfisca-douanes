DOT_FILES := $(wildcard **/*.dot)
SVG_FILES := $(patsubst %.dot, %.svg, $(DOT_FILES))

all: $(SVG_FILES)

%.svg : %.dot
	dot -Tsvg -o $@ $<

clean:
	rm -f $(SVG_FILES)

download_pad:
	wget https://bimestriel.framapad.org/p/openfisca-douanes/export/markdown -O notes/openfisca-douanes-pad-backup.md

.PHONY: clean download_pad
