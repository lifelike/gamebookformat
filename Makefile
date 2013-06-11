examples=$(wildcard examples/*.gamebook)

all: rtf pdf html debug png txt

rtf: $(examples:.gamebook=.rtf)
pdf: $(examples:.gamebook=.pdf)
html: $(examples:.gamebook=.html)
debug: $(examples:.gamebook=.debug)
png: $(examples:.gamebook=.png)
txt: $(examples:.gamebook=.txt)

uploadto=$(shell cat .uploadto)

%.rtf: %.gamebook *.py templates/rtf/*.rtf
	./formatgamebook.py --verify $< $@

%.html: %.gamebook *.py templates/html/*.html
	./formatgamebook.py --verify $< $@

%.tex: %.gamebook *.py templates/tex/*.tex
	./formatgamebook.py --verify $< $@

%.dot: %.gamebook *.py templates/dot/*.dot
	./formatgamebook.py --verify $< $@

%.debug: %.gamebook *.py templates/debug/*.debug
	./formatgamebook.py --verify $< $@

%.txt:  %.gamebook *.py templates/txt/*.txt
	./formatgamebook.py --verify $< $@

%.pdf: %.tex
	cd $(dir $<) &&	pdflatex $(notdir $<) && pdflatex $(notdir $<)

%.png: %.dot
	dot -Tpng $< > $@

upload: html png pdf rtf
	if [ -n "$(uploadto)" ]; then \
	 scp examples/*.html examples/*.png examples/*.pdf examples/*.rtf $(uploadto);\
	fi

clean:
	$(RM) $(rtf) $(html) examples/*.tex \
	$(debug) $(pdf) *~ examples/*~ *.pyc \
	examples/*.dot examples/*.aux examples/*.toc $(png) \
	examples/*.map templates/*~ templates/*/*~

fixmes:
	grep FIXME *.py

.PHONY: all clean fixmes uploadto

.PRECIOUS: %.tex %.dot

