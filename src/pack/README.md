## 打包基础固件脚本

- uart 免密登录
- ssh 自动开启
- root 密码设置成 root

需要安装 squashfs 相关的工具

```sh
sudo ./pack.sh
```

执行成功后会在本目录下生成一个 rootfs.img
