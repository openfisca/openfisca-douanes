DOT_FILES := $(wildcard **/*.dot)
SVG_FILES := $(patsubst %.dot, %.svg, $(DOT_FILES))

all: $(SVG_FILES)

%.svg : %.dot
	dot -Tsvg -o $@ $<

clean:
	rm -f $(SVG_FILES)

.PHONY: clean
