VER ?= "0.11-20130402"
DOWNLOAD_URL ?= "https://github.com/json-c/json-c/archive/json-c-$(VER).tar.gz"
PREFIX ?= 
DESTDIR ?= $(PWD)/../dists
DOCKER_IMAGE ?= lx01:latest

NAME=json-c

.PHONY: build build-in-docker

build-with-docker:
	docker run --rm -v $(PWD)/../:/build -w /build $(DOCKER_IMAGE) sh -c "cd $(NAME) && make build"

build:
	rm -rf ../build/$(NAME) && mkdir -pv ../build/$(NAME) && cd ../build \
	&& wget -c $(DOWNLOAD_URL) -O $(NAME).tar.gz \
	&& tar -xvf $(NAME).tar.gz -C $(NAME) --strip-components=1 \
	&& cd $(NAME) \
	&& ./configure --host=$(HOST) --prefix=$(PREFIX) CC=$(CC) \
	&& make -j$(nproc) \
	&& make install DESTDIR=$(DESTDIR) \
	&& cd ../ && rm -rf $NAME
