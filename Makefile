BASEDIR=$(CURDIR)
OUTPUTDIR=$(BASEDIR)/_output

help:
	@echo 'Makefile for "Find Untagged Tumblr Posts"                                 '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make html                           (re)generate the web site          '
	@echo '   make clean                          remove the generated files         '
	@echo '   make serve                          serve site at http://localhost:8000'
	@echo '   make github                         upload the web site via gh-pages   '

html: clean
	@python make_pages.py

clean:
	[ ! -d $(OUTPUTDIR) ] || rm -rf $(OUTPUTDIR)

serve:
	@cd $(OUTPUTDIR) && python -m SimpleHTTPServer

github: html
	ghp-import -p $(OUTPUTDIR)

