requirements.txt: requirements.in
	docker run --rm --volume $(CURDIR):/src micktwomey/pip-tools
