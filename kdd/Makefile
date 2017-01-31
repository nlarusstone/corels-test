TARGETS = kdd17

TEXFILES = $(wildcard *.tex)
BIBFILES = $(wildcard *.bib)
FIGFILES = $(wildcard figs/*.png)
PDFS = $(addsuffix .pdf,$(TARGETS))

%.pdf: %.tex $(TEXFILES) $(BIBFILES) $(FIGFILES)
	pdflatex $*
	bibtex $*
	pdflatex $*
	pdflatex $*

all: $(PDFS)

a: kdd17.pdf

spell:
	$(shell for i in $(TEXFILES); do ispell $(i); done)

clean:
	rm -f *.aux *.bbl *.log *.blg *.out *.cut

flush: clean
	rm -f $(PDFS)

.PHONY: all a
