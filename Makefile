BASEDIR=$(CURDIR)
OUTPUTDIR=$(BASEDIR)/_output

help:
	@echo 'Makefile for "Find Untagged Tumblr Posts                                  '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make html                           (re)generate the web site          '
	@echo '   make serve                          serve site at http://localhost:8000'

html:
	@python make_pages.py

serve:
	@cd $OUTPUTDIR
	python -m http.server
