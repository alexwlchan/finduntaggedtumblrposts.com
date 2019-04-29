BUILD_IMAGE = jekyll/jekyll:minimal

RSYNC_HOST = 139.162.244.147
RSYNC_USER = alexwlchan
RSYNC_DIR = /home/alexwlchan/sites/finduntaggedtumblrposts.com

ROOT = $(shell git rev-parse --show-toplevel)
SRC = $(ROOT)/src


build:
	docker run --volume $(SRC):/site --workdir /site $(BUILD_IMAGE) jekyll build

serve:
	docker run --rm --tty \
		--publish 6060:6060 \
		--volume $(SRC):/site \
		--workdir /site \
		$(BUILD_IMAGE) \
		jekyll serve --port 6060 --watch

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
