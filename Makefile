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
	./formatgamebook.py --seed=1 $< $@

%.html: %.gamebook *.py templates/html/*.html
	./formatgamebook.py --seed=1 $< $@

%.tex: %.gamebook *.py templates/tex/*.tex
	./formatgamebook.py --seed=1 $< $@

%.dot: %.gamebook *.py templates/dot/*.dot
	./formatgamebook.py --seed=1 $< $@

%.debug: %.gamebook *.py templates/debug/*.debug
	./formatgamebook.py --seed=1 $< $@

%.txt:  %.gamebook *.py templates/txt/*.txt
	./formatgamebook.py --seed=1 $< $@

%.pdf: %.tex
	cd $(dir $<) &&	pdflatex $(notdir $<) && pdflatex $(notdir $<)

%.png: %.dot
	dot -Tpng $< > $@

test: unittest checkexpected

expected: all
	$(RM) expected/* && cp examples/*.{rtf,tex,html,debug,txt,dot,map} \
		 expected

checkexpected: clean all
	diff -r -x "*.aux" -x "*.gamebook" -x "*.log" -x "*.out" -x "*.png" \
		-x "*.pdf" -x .gitignore -q examples expected

unittests=test_sections

unittest: *.py
	python2.7 -m unittest $(unittests)

upload: html png pdf rtf
	if [ -n "$(uploadto)" ]; then \
	 scp examples/*.html examples/*.png examples/*.pdf examples/*.rtf $(uploadto);\
	fi

clean:
	$(RM) examples/*rtf examples/*.html examples/*.tex \
	examples/*.txt examples/*.debug examples/*.log \
	examples/*.pdf examples/*.out *~ examples/*~ *.pyc \
	examples/*.dot examples/*.aux examples/*.toc $(png) \
	examples/*.map templates/*~ templates/*/*~ \
	$(examples:.gamebook=.png)

fixmes:
	grep FIXME *.py

.PHONY: all clean fixmes uploadto expected checkexpected test unittest

.PRECIOUS: %.tex %.dot

