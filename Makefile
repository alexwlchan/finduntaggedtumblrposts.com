requirements.txt: requirements.in
	docker run --rm --volume $(CURDIR):/src micktwomey/pip-tools

test_requirements.txt: test_requirements.in
	docker run --rm --volume $(CURDIR):/src micktwomey/pip-tools \
		pip-compile test_requirements.in
