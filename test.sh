#!/bin/sh

./formatgamebook.py test.json test.debug
cat test.debug

./formatgamebook.py test.json test.dot
dot -Tpng test.dot > test.png && open test.png

./formatgamebook.py test.json test.tex

#./formatgamebook.py test.json test.rtf


