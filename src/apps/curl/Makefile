CURL_VER ?= "8.5.0"
CURL_NAME = curl-$(subst .,_,$(CURL_VER))
DOWNLOAD_URL ?= https://github.com/curl/curl/releases/download/$(CURL_NAME)/curl-$(CURL_VER).tar.gz
PREFIX ?= 
DESTDIR ?= $(PWD)/../dists
DOCKER_IMAGE ?= lx01:latest

.PHONY: build build-in-docker

build-with-docker:
	docker run --rm -v $(PWD)/../:/build -w /build $(DOCKER_IMAGE) sh -c "cd curl && make build"

build:
	rm -rf ../build/curl && mkdir -pv ../build/curl && cd ../build \
	&& wget -c $(DOWNLOAD_URL) -O curl.tar.gz \
	&& tar -xvf curl.tar.gz -C curl --strip-components=1 \
	&& cd curl \
	&& ./configure --host=$(HOST) --prefix=$(PREFIX) --without-ssl \
	&& make -j$(nproc) \
	&& make install DESTDIR=$(DESTDIR) \
	&& cd ../ && rm -rf curl
