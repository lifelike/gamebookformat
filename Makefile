all: test.rtf test.pdf test.html test.debug test.png

%.rtf: %.gamebook formatgamebook.py
	./formatgamebook.py $< $@

%.html: %.gamebook formatgamebook.py
	./formatgamebook.py $< $@

%.tex: %.gamebook formatgamebook.py
	./formatgamebook.py $< $@

%.dot: %.gamebook formatgamebook.py
	./formatgamebook.py $< $@

%.debug: %.gamebook formatgamebook.py
	./formatgamebook.py $< $@

%.pdf: %.tex
	pdflatex $< && pdflatex $<

%.png: %.dot
	dot -Tpng $< > $@

clean:
	$(RM) *.rtf *.html *.tex *.debug *.pdf *~ *.pyc *.dot \
	*.aux *.toc *.png

fixmes:
	grep FIXME *.py

.PHONY: all clean fixmes

.PRECIOUS: %.tex %.dot

