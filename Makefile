examples=$(wildcard examples/*.gamebook)

all: $(examples:.gamebook=.rtf) \
	$(examples:.gamebook=.pdf) \
	$(examples:.gamebook=.html) \
	$(examples:.gamebook=.debug) \
	$(examples:.gamebook=.png)

%.rtf: %.gamebook formatgamebook.py
	./formatgamebook.py --verify $< $@

%.html: %.gamebook formatgamebook.py
	./formatgamebook.py --verify $< $@

%.tex: %.gamebook formatgamebook.py
	./formatgamebook.py --verify $< $@

%.dot: %.gamebook formatgamebook.py
	./formatgamebook.py --verify $< $@

%.debug: %.gamebook formatgamebook.py
	./formatgamebook.py --verify $< $@

%.pdf: %.tex
	cd $(dir $<) &&	pdflatex $(notdir $<) && pdflatex $(notdir $<)

%.png: %.dot
	dot -Tpng $< > $@

clean:
	$(RM) examples/*.rtf examples/*.html examples/*.tex \
	examples/*.debug examples/*.pdf *~ examples/*~ *.pyc \
	examples/*.dot examples/*.aux examples/*.toc examples/*.png \
	examples/*.map

fixmes:
	grep FIXME *.py

.PHONY: all clean fixmes

.PRECIOUS: %.tex %.dot

