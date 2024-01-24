DOCKER_IMAGE ?= lx01:latest


.PHONY: build build-curl build-with-docker build-all

build-with-docker:
	docker run --rm -v $(PWD)/../:/build -w /build $(DOCKER_IMAGE) sh -c "cd aivs-monitor && make build"

build-curl:
	make -C ../curl build-with-docker

build:
	${CC} -Os -ldl \
		-I ../dists/include \
		-L ../dists/lib \
		-lcurl \
		-o aivs-monitor \
		main.c

build-all: build-curl build-with-docker