TARGETS = arxiv kdd17

TEXFILES = $(wildcard *.tex sections/*.tex)
BIBFILES = $(wildcard *.bib)
FIGFILES = $(wildcard figs/*.png)
PDFS = $(addsuffix .pdf,$(TARGETS))

%.pdf: %.tex $(TEXFILES) $(BIBFILES) $(FIGFILES)
	pdflatex $*
	bibtex $*
	pdflatex $*
	pdflatex $*

all: $(PDFS)

a: arxiv.pdf

k: kdd17.pdf

spell:
	$(shell for i in $(TEXFILES); do ispell $(i); done)

clean:
	rm -f *.aux *.bbl *.log *.blg *.out *.cut *.toc

flush: clean
	rm -f $(PDFS)

.PHONY: all a
