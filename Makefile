examples=$(wildcard examples/*.gamebook)

all: rtf pdf html debug png txt

rtf: $(examples:.gamebook=.rtf)
pdf: $(examples:.gamebook=.pdf)
html: $(examples:.gamebook=.html)
debug: $(examples:.gamebook=.debug)
png: $(examples:.gamebook=.png)
txt: $(examples:.gamebook=.txt)

uploadto=$(shell cat .uploadto)

readme.html: readme.org
	emacs -Q --batch --visit=readme.org --funcall org-export-as-html-batch

%.rtf: %.gamebook *.py templates/rtf/*.rtf
	./formatgamebook.py --no-shuffle $< $@

%.html: %.gamebook *.py templates/html/*.html
	./formatgamebook.py --no-shuffle $< $@

%.tex: %.gamebook *.py templates/tex/*.tex
	./formatgamebook.py --no-shuffle $< $@

%.dot: %.gamebook *.py templates/dot/*.dot
	./formatgamebook.py --no-shuffle $< $@

%.debug: %.gamebook *.py templates/debug/*.debug
	./formatgamebook.py --no-shuffle $< $@

%.txt:  %.gamebook *.py templates/txt/*.txt
	./formatgamebook.py --no-shuffle $< $@

%.pdf: %.tex
	cd $(dir $<) &&	pdflatex $(notdir $<) && pdflatex $(notdir $<)

%.png: %.dot
	dot -Tpng $< > $@

test: unittest checkexpected templatejstest

expected: all
	$(RM) expected/* && cp examples/*.{rtf,tex,html,debug,txt,dot,map} \
		 expected

checkexpected: clean all
	diff -r -x "*.aux" -x "*.gamebook" -x "*.log" -x "*.out" -x "*.png" \
		-x "*.pdf" -x .gitignore -q examples expected

unittests=$(wildcard test_*.py)

unittest: *.py
	python2.7 -m unittest $(unittests:.py=)

upload: html png pdf rtf
	if [ -n "$(uploadto)" ]; then \
	 scp examples/*.html examples/*.png examples/*.pdf examples/*.rtf \
	   $(uploadto);\
	fi

test/templatejs/htmlscripts.js: $(wildcard templates/html/*script.html)
	./templates.py html script > $@

templatejstest: test/templatejs/htmlscripts.js \
	test/templatejs/testhtmlscripts.js
	node test/templatejs/testhtmlscripts.js

clean:
	$(RM) examples/*rtf examples/*.html examples/*.tex \
	examples/*.txt examples/*.debug examples/*.log \
	examples/*.pdf examples/*.out *~ examples/*~ *.pyc \
	examples/*.dot examples/*.aux examples/*.toc $(png) \
	examples/*.map templates/*~ templates/*/*~ \
	$(examples:.gamebook=.png) readme.html

fixmes:
	grep FIXME *.py

.PHONY: all clean fixmes uploadto expected checkexpected test unittest

.PRECIOUS: %.tex %.dot

