TARGETS = arxiv

TEXFILES = $(wildcard *.tex)
BIBFILES = $(wildcard *.bib)
PDFS = $(addsuffix .pdf,$(TARGETS))

%.pdf: %.tex $(TEXFILES) $(BIBFILES)
	pdflatex $*
	bibtex $*
	pdflatex $*
	pdflatex $*

all: $(PDFS)

a: arxiv.pdf

spell:
	$(shell for i in $(TEXFILES); do ispell $(i); done)

clean:
	rm -f *.aux *.bbl *.log *.blg *.out

flush: clean
	rm -f $(PDFS)

.PHONY: all a
