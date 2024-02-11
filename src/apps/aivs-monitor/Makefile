TOP_DIR ?= $(PWD)/../..
include $(TOP_DIR)/scripts/config.mk

define copy_to_rootfs
	install -d $(DEST_ROOTFS)/usr/bin
	install -m 0755 aivs-monitor $(DEST_ROOTFS)/usr/bin
	# copy json-c lib (curl exist in lx01 rootfs)
	install -d $(DEST_ROOTFS)/usr/lib
	install -m 0755 $(EXTRA_LIB_DIR)/libjson-c.so.5 $(DEST_ROOTFS)/usr/lib
endef

.PHONY: build build-with-docker test clean lint host-build

LIBS := -lcurl -ljson-c
EXEC := aivs-monitor
TEST_EXEC := test

MAIN_SRCS := main.c json.c monitor.c
TEST_SRCS := CuTest.c json.c test.c monitor.c

MAIN_OBJS := $(MAIN_SRCS:.c=.o)
TEST_OBJS := $(TEST_SRCS:.c=.o)


build-with-docker:
	docker run --rm -v $(TOP_DIR):/build -w /build $(BUILD_IMAGE) sh -c "cd $(MAKEFILE_DIR) && make build"

build: $(MAIN_OBJS)
	$(CC) -I $(EXTRA_INCLUDE_DIR) -I . -L $(EXTRA_LIB_DIR) $(LIBS) $^ -o $(EXEC)
	$(copy_to_rootfs)

test: $(TEST_OBJS)
	$(CC) -I $(EXTRA_INCLUDE_DIR) -I . -L $(EXTRA_LIB_DIR) $(LIBS) $^ -o $(TEST_EXEC)
	./$(TEST_EXEC)

%.o: %.c
	$(CC) -I $(EXTRA_INCLUDE_DIR) -L $(EXTRA_LIB_DIR) -c $< -o $@

lint:
	cppcheck --std=c99 --language=c --error-exitcode=1 --suppress=missingIncludeSystem .

host-build: $(MAIN_OBJS)
	$(CC) -I . $(LIBS) $^ -o $(EXEC)

host-test: $(TEST_OBJS)
	$(CC) -I . $(LIBS) $^ -o $(TEST_EXEC)
	./$(TEST_EXEC)

clean:
	rm -f $(MAIN_OBJS) $(TEST_OBJS) $(EXEC) $(TEST_EXEC)

