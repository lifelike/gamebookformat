#!/bin/sh

./formatgamebook.py test.gamebook test.debug
cat test.debug

./formatgamebook.py test.gamebook test.dot
dot -Tpng test.dot > test.png && open test.png

./formatgamebook.py test.gamebook test.tex
pdflatex test.tex && open test.pdf

./formatgamebook.py test.gamebook test.html
open test.html

./formatgamebook.py test.gamebook test.rtf
open test.rtf


