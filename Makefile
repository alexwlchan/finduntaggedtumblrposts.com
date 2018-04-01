BUILD_IMAGE = alexwlchan/finduntaggedtumblrposts.com
SERVE_CONTAINER = finduntaggedtumblrposts_server

RSYNC_HOST = 139.162.244.147
RSYNC_USER = alexwlchan
RSYNC_DIR = /home/alexwlchan/sites/finduntaggedtumblrposts.com

ROOT = $(shell git rev-parse --show-toplevel)
SRC = $(ROOT)/src

$(ROOT)/.docker/build: Dockerfile Gemfile.lock
	docker build --tag $(BUILD_IMAGE) .
	mkdir -p .docker
	touch .docker/build

.docker/build: $(ROOT)/.docker/build


build: .docker/build
	docker run --volume $(SRC):/site $(BUILD_IMAGE) build

serve: .docker/build
	docker run --rm --tty \
		--publish 6060:6060 \
		--volume $(SRC):/site \
		--name $(SERVE_CONTAINER) \
		--hostname $(SERVE_CONTAINER) \
		$(BUILD_IMAGE) \
		serve --host $(SERVE_CONTAINER) --port 6060 --watch

deploy: build
	docker run --rm --tty \
		--volume ~/.ssh/id_rsa:/root/.ssh/id_rsa \
		--volume $(ROOT)/src/_site:/data \
		instrumentisto/rsync-ssh \
		rsync \
		--archive \
		--verbose \
		--compress \
		--delete \
		--exclude=".DS_Store" \
		--rsh="ssh -o StrictHostKeyChecking=no -i ~/.ssh/id_rsa" \
		/data/ "$(RSYNC_USER)"@"$(RSYNC_HOST)":"$(RSYNC_DIR)"

Gemfile.lock: Gemfile
	docker run --rm --tty \
		--volume $(ROOT):/site \
		--workdir /site \
		$(shell cat Dockerfile | grep FROM | awk '{print $$2}') \
		bundle lock --update
