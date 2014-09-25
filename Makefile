examples=$(wildcard examples/*.gamebook)

all: rtf pdf html json png txt

rtf: $(examples:.gamebook=.rtf)
tex: $(examples:.gamebook=.tex)
pdf: $(examples:.gamebook=.pdf)
html: $(examples:.gamebook=.html) examples/gamebookformatplay.js \
	examples/gamebookformat.css
json: $(examples:.gamebook=.json)
check: $(examples:.gamebook=.check)
vcheck: $(examples:.gamebook=.vcheck)
dot: $(examples:.gamebook=.dot)
png: $(examples:.gamebook=.png)
txt: $(examples:.gamebook=.txt)
map: $(examples:.gamebook=.map)

uploadto=$(shell cat .uploadto)

readme.html: readme.org
	emacs -Q --batch --visit=readme.org --funcall org-export-as-html-batch

examples/gamebookformatplay.js: gamebookformatplay.js
	cp gamebookformatplay.js $@

examples/gamebookformat.css: gamebookformat.css
	cp gamebookformat.css $@

%.rtf: %.gamebook *.py templates/rtf/*.rtf
	python2.7 ./buildexamplegamebook.py $< $@

%.html: %.gamebook *.py templates/html/*.html
	python2.7 ./buildexamplegamebook.py $< $@

%.tex: %.gamebook *.py templates/tex/*.tex
	python2.7 ./buildexamplegamebook.py $< $@

%.dot: %.gamebook *.py templates/dot/*.dot
	python2.7 ./buildexamplegamebook.py $< $@

%.json: %.gamebook *.py templates/json/*.json
	python2.7 ./buildexamplegamebook.py $< $@

%.check: %.json
	python2.7 ./checkgamebook.py $< > $@ || true

%.vcheck: %.json
	python2.7 ./checkgamebook.py -v $< > $@ || true

%.txt:  %.gamebook *.py templates/txt/*.txt
	python2.7 ./buildexamplegamebook.py $< $@

%.pdf: %.tex
	cd $(dir $<) &&	pdflatex $(notdir $<) && pdflatex $(notdir $<)

%.png: %.dot
	dot -Tpng $< > $@

test: unittest checkexpected templatejstest

expected: rtf tex html json txt dot map check vcheck
	$(RM) expected/* && \
		cp examples/*.{rtf,tex,html,json,txt,dot,map,check,vcheck} \
		 expected

checkexpected: clean rtf tex html json dot txt check vcheck
	diff -r -x "*.aux" -x "*.gamebook" -x "*.log" -x "*.out" -x "*.png" \
		-x "*.pdf" -x .gitignore -x "*.js" -x "*.css" \
		-x "*.options" -q examples expected

unittests=$(wildcard test_*.py)

unittest: *.py
	python2.7 -m unittest $(unittests:.py=)

xmllinthtmlbook: examples/htmlbook.html
	xmllint --noout --schema ../HTMLBook/schema/htmlbook.xsd examples/htmlbook.html

upload: html png pdf rtf
	if [ -n "$(uploadto)" ]; then \
	 scp examples/*.html examples/*.png examples/*.pdf examples/*.rtf \
		*.js *.css \
	   $(uploadto);\
	fi

templatejstest:
	node test/templatejs/testhtmlscripts.js

clean:
	$(RM) examples/*rtf examples/*.html examples/*.tex \
	examples/*.txt examples/*.json examples/*.check examples/*.log \
	examples/*.pdf examples/*.out *~ examples/*~ *.pyc examples/*.vcheck \
	examples/*.dot examples/*.aux examples/*.toc $(png) \
	$(map) templates/*~ templates/*/*~ \
	$(examples:.gamebook=.png) readme.html \
	examples/*.js examples/*.css

fixmes:
	grep FIXME *.py

.PHONY: all clean fixmes uploadto expected checkexpected test unittest \
	templatejstest xmllinthtmlbook check vcheck

.PRECIOUS: %.tex %.dot

