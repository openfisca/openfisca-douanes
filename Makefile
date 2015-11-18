DOT_FILES := $(wildcard *.dot)

%.svg : %.dot
	dot -Tsvg -o $@ $<
