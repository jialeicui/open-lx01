HTTPS_PROXY ?=

.PHONY: *

image:
	docker build . -t lx01 --build-arg HTTPS_PROXY=${HTTPS_PROXY}

