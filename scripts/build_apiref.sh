#!/usr/bin/env bash

export DEST=docs/source
#rm -f $DEST/*.rst
rm -rf $DEST/_build
rm -rf $DEST/_static
rm -rf $DEST/_templates

# Just creating conf.py, Makefile and make.bat once, hence commenting below.

#sphinx-quickstart --quiet --author 'Omkar Mestry, Sachin Kharude' --project turfpy \
#	--ext-coverage --ext-autodoc --ext-viewcode --ext-doctest \
#	$DEST

sphinx-apidoc --private --separate --module-first --full -o $DEST turfpy
sphinx-build -b html -D html_theme=sphinx_rtd_theme $DEST $DEST/_build/html
