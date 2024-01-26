DOWNLOAD_URL ?= "https://ftp.gnu.org/gnu/ncurses/ncurses-6.4.tar.gz"
PREFIX ?= 
DESTDIR ?= $(PWD)/../dists
DOCKER_IMAGE ?= lx01:latest

NAME=$(shell basename $(shell pwd))

.PHONY: build build-in-docker

build-with-docker:
	docker run --rm -v $(PWD)/../:/build -w /build $(DOCKER_IMAGE) sh -c "cd $(NAME) && make build"

build:
	rm -rf ../build/$(NAME) && mkdir -pv ../build/$(NAME) && cd ../build \
	&& wget -c $(DOWNLOAD_URL) -O $(NAME).tar.gz \
	&& tar -xvf $(NAME).tar.gz -C $(NAME) --strip-components=1 \
	&& cd $(NAME) \
	&& ./configure --prefix=$(PREFIX) --host=$(HOST) \
	&& make -j$(nproc) \
	&& make install DESTDIR=$(DESTDIR)
