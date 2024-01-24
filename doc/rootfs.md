# RootFS 内的组成

```sh
drwxr-xr-x  2 root root 4.0K Jan 19 15:05 bin # 一些系统级别的程序
drwxr-xr-x  2 root root 4.0K Oct 28  2021 data # 持久化数据存储位置
drwxr-xr-x  2 root root 4.0K Oct 28  2021 dev # 各种设备, 目前只需要关注 /dev/snd 中的设备(声音录播)
drwxr-xr-x 30 root root 4.0K Jan 18 18:43 etc # 各种配置
drwxr-xr-x 11 root root 4.0K Jan 18 18:40 lib # 系统级别的依赖库
drwxr-xr-x  2 root root 4.0K Oct 28  2021 mnt
drwxr-xr-x  2 root root 4.0K Oct 28  2021 overlay
drwxr-xr-x  2 root root 4.0K Oct 28  2021 proc
drwxrwxr-x  2 root root 4.0K Oct 28  2021 rom
drwxr-xr-x  3 root root 4.0K Jan 18 18:43 root
drwxr-xr-x  2 root root 4.0K Jan 18 17:55 sbin
drwxr-xr-x  2 root root 4.0K Oct 28  2021 sys
drwxrwxrwt  2 root root 4.0K Oct 28  2021 tmp
drwxr-xr-x 10 root root 4.0K Jan 19 14:59 usr # 用户级别的程序和lib
lrwxrwxrwx  1 root root    4 Oct 28  2021 var -> /tmp # tmpfs, 各种临时文件, 一共60MB 左右, 好用
drwxr-xr-x  2 root root 4.0K Oct 28  2021 www
```

添加注释的目录着重关注
