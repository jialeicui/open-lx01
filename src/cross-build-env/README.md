# 小爱音箱app交叉编译环境

需要本机支持 docker

使用方法

```sh
make
```

如果网络不佳, 需要使用代理

```sh
make HTTPS_PROXY=http://x.x.x.x:xxxx
```

执行成功后会生成一个 `lx01:latest` 的 docker image, 内部有使用 `musl 1.1.14` 版本的各种编译链接的 toolchain

```sh
$ docker run -it lx01 sh -c 'ls -lh /opt/cross/bin' 
total 139M
-rwxr-xr-x 1 root root 5.6M Jan 23 10:02 armv7l-linux-musleabihf-addr2line
-rwxr-xr-x 2 root root 5.9M Jan 23 10:02 armv7l-linux-musleabihf-ar
-rwxr-xr-x 2 root root 9.1M Jan 23 10:02 armv7l-linux-musleabihf-as
-rwxr-xr-x 2 root root 6.2M Jan 23 10:01 armv7l-linux-musleabihf-c++
-rwxr-xr-x 1 root root 5.6M Jan 23 10:02 armv7l-linux-musleabihf-c++filt
lrwxrwxrwx 1 root root   27 Jan 23 10:02 armv7l-linux-musleabihf-cc -> armv7l-linux-musleabihf-gcc
-rwxr-xr-x 1 root root 6.2M Jan 23 10:01 armv7l-linux-musleabihf-cpp
-rwxr-xr-x 1 root root 284K Jan 23 10:02 armv7l-linux-musleabihf-elfedit
-rwxr-xr-x 2 root root 6.2M Jan 23 10:01 armv7l-linux-musleabihf-g++
-rwxr-xr-x 2 root root 6.2M Jan 23 10:01 armv7l-linux-musleabihf-gcc
-rwxr-xr-x 2 root root 6.2M Jan 23 10:01 armv7l-linux-musleabihf-gcc-9.4.0
-rwxr-xr-x 1 root root 184K Jan 23 10:01 armv7l-linux-musleabihf-gcc-ar
-rwxr-xr-x 1 root root 184K Jan 23 10:01 armv7l-linux-musleabihf-gcc-nm
-rwxr-xr-x 1 root root 184K Jan 23 10:01 armv7l-linux-musleabihf-gcc-ranlib
-rwxr-xr-x 1 root root 5.2M Jan 23 10:01 armv7l-linux-musleabihf-gcov
-rwxr-xr-x 1 root root 3.5M Jan 23 10:01 armv7l-linux-musleabihf-gcov-dump
-rwxr-xr-x 1 root root 3.7M Jan 23 10:01 armv7l-linux-musleabihf-gcov-tool
-rwxr-xr-x 1 root root 6.3M Jan 23 10:02 armv7l-linux-musleabihf-gprof
-rwxr-xr-x 4 root root 7.6M Jan 23 10:02 armv7l-linux-musleabihf-ld
-rwxr-xr-x 4 root root 7.6M Jan 23 10:02 armv7l-linux-musleabihf-ld.bfd
-rwxr-xr-x 2 root root 5.7M Jan 23 10:02 armv7l-linux-musleabihf-nm
-rwxr-xr-x 2 root root 6.5M Jan 23 10:02 armv7l-linux-musleabihf-objcopy
-rwxr-xr-x 2 root root 8.8M Jan 23 10:02 armv7l-linux-musleabihf-objdump
-rwxr-xr-x 2 root root 5.9M Jan 23 10:02 armv7l-linux-musleabihf-ranlib
-rwxr-xr-x 2 root root 3.5M Jan 23 10:02 armv7l-linux-musleabihf-readelf
-rwxr-xr-x 1 root root 5.6M Jan 23 10:02 armv7l-linux-musleabihf-size
-rwxr-xr-x 1 root root 5.6M Jan 23 10:02 armv7l-linux-musleabihf-strings
-rwxr-xr-x 2 root root 6.5M Jan 23 10:02 armv7l-linux-musleabihf-strip
```

感谢项目:

- https://github.com/richfelker/musl-cross-make

这里我没有使用 glibc, 使用的是 musl, 好处是编译完成的 binary 可以直接拷贝到音箱里直接运行

```sh
root@LX01:~# ldd 
musl libc (armhf)
Version 1.1.14
Dynamic Program Loader
Usage: ldd [options] [--] pathname
```

如果想使用 glibc, 可以使用 https://github.com/duhow/xiaoai-patch, 项目设计非常科学, 最后我可能会基于这个项目做一个自己的固件  
(编译之后的程序无法直接拷贝到音箱原生固件里运行, 需要根据项目说明重新打包自己一个固件刷进去, 原生的服务就无法运行了)
