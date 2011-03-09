#!/usr/bin/make -f
# -*- makefile -*-

build:
	mkdir -p openlp/i18n
	for TSFILE in resources/i18n/*.ts; do\
	    lrelease-qt4 $$TSFILE -qm openlp/i18n/`basename $$TSFILE .ts`.qm;\
	done

install:

clean:

