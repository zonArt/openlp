#!/usr/bin/make -f
# -*- makefile -*-

build:
	mkdir -p resources/i18n/qm
	for TSFILE in resources/i18n/*.ts; do\
		lrelease-qt4 $$TSFILE -qm resources/i18n/qm/`basename $$TSFILE .ts`.qm;\
	done

install:
	mkdir -p $(DESTDIR)/usr/share/openlp/i18n
	cd resources/i18n/qm && for QMFILE in*.qm; do\
		mv $QMFILE $(DESTDIR)/usr/share/openlp/i18n;\
	done

clean:
	rm -fR resources/i18n/qm
