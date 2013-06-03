#!/bin/sh

make clean all

cat test.debug

dot -Tpng test.dot > test.png && open test.png

open test.pdf

open test.html

open test.rtf


