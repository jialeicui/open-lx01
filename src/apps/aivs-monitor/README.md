# aivs-monitor

功能很简单, 算是一个交叉编译的 hello world, 功能是监控对话记录, 发送到指定服务器

需要依赖交叉编译环境, [参考](../../cross-build-env/)

```sh
# 如果已经 build 了所有依赖, 只是想重新编译 aivs-monitor, 那么在当前目录 make 即可
make

# 如果 build 报错提示找不到 libcurl 等依赖, 那么在上层文件夹, 也就是 app 目录 make 等待所有依赖 build 完成即可
```

注: make 出来的是目标 arm 平台的 binary, 需要拷贝到音箱上才能执行 

TODO

- [ ] 服务器地址可配置(最好音箱能serve一个web服务) [lighttpd](../lighttp/)
