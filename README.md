# Open-LX01

让小爱音箱mini成为一个完全自主控制的音箱

步骤:
1. [获取控制权](#获取控制权)
2. [刷自己的第一个固件](#刷自己的第一个固件)
3. [自主控制三步走](./doc/README.md)
    - [x] [只替换大模型](./doc/README.md#step-1) (基本完成)
    - [ ] 只用原生的唤醒功能, 使用自己的 ASR 和 TTS
    - [ ] 使用自己的唤醒程序, 全部都是自己的服务

琐碎的点:

- [x] [主要服务分析](./doc/services.md)
- [x] [逆向方法](./doc/reverse-engineering.md)
- [x] [交叉编译环境](./src/cross-build-env/)
- [x] [音箱上的自定义程序](./src/apps/aivs-monitor/)
    - [x] 自动上传交互文字到 server
    - [x] 根据 server 应答播放文字 (官方tts)
    - [x] 关键词匹配跳过上传（比如开灯/停等）
- [x] [Web Server](./src/server/)
    - [x] 接收音箱对话记录
    - [x] 声音检测 (目前未用到)
    - [x] 大语言模型
        - [x] [Moonshot](https://platform.moonshot.cn)
        - [x] [Github Copilot](https://github.com/features/copilot)
    - [ ] 支持各种配置的UI (进行中)
- [ ] gdb-server(host=arm) + gdb(target=arm)
- [ ] open-mico-aivs-lab
- [ ] open-mipns-sai (使用 [porcupine](https://github.com/Picovoice/porcupine) 或 [kaldi](https://github.com/kaldi-asr/kaldi))


https://github.com/jialeicui/open-lx01/assets/3217223/b5e0a511-1a28-42c8-9462-f9f20279fd30

---

### 获取控制权

具体步骤可以参考[B站 system-player 的文章](https://www.bilibili.com/read/cv16072149/)

总结步骤如下:

1. 淘宝买一个 USB 转 TTL 的刷机线, 3块钱-7块钱不等 (小爱音箱mini咸鱼30块钱左右, 电烙铁+焊锡20块钱)
2. 拆机, 找到电路板上的 TX/RX/GND 焊接上刷机线
    - 这里注意电路板上 TX/RX 标识不止一处, 使用MI标识右下角的那组
    - GND -> GND
    - TX -> RX
    - RX -> TX
3. USB 插电脑, 安装必要软件
    - Windows
        - 需要安装驱动, 淘宝店家一般都会给链接 CH340 / PL2304 之类的驱动(功能一样, 只不过是国产还是非国产的区别)
        - 安装好之后, 插上 USB 在设备管理器应该能看到串口, 记下 COMX 里的 X
        - 下载 [PuTTY](https://putty.org/) 连接方式选串口, 地址写 COMX (X是个数字), 波特率写 115200, 确认
        - 给音箱上电之后应该能看到打印了
    - macOS
        - 不需要装驱动
        - 和串口交互的软件使用 screen 命令行就够: brew install screen
        - USB 串口设备一般是 /dev/cu.xxxx, ls 一下应该就能看到一个
        - screen /dev/cu.xxxx 115200
        - 音箱上电看是否有打印
    - Linux
        - PuTTY 和 screen 均可 (我倾向于 screen, 可以直接在当前终端 tmux 中各种嵌入)
        - 串口设备一般是 /dev/ttyUSBX, X是一个数字
        - 如果没有这个设备, 可以执行 sudo dmesg -w, 插拔 USB, 看打印的日志就能找到这个 device
        - PuTTY 或者 screen 按照前面类似的配置好
        - 音箱商店看是否有打印
4. 进 shell (在串口打印正常的前提下)
    - 如果你的音箱固件一直没有升级过 (就是在小爱音箱app里点升级), 可能按几次回车直接就能进到 shell, 看到类似 `root@LX01:~#` 的提示符, 那本步骤就可以结束, 后面不用看
    - 大概率会来到这步, 需要输入账户名和密码
        - 网上有很多如何计算密码的教程, 根据不同的型号, 不同的固件有不同的方式, 但是大概率已经失效了, 如何确认失效了? 下面:
        - 如果输入账户 root 回车之后, 有 `magic xxx` 之类的提示, 或者随便输入密码, 有 `dsa verify faile` 类似字样, 就说明我们基本没办法得知密码了, 只能刷机

### 刷自己的第一个固件

这步我们的目的可能是让音箱默认开 ssh, 也可能是因为我们不知道密码, 想进 shell, 这里一起搞定  
(下面几个步骤的自动化脚本参考 [打包](./src/pack/))

1. 下载官方固件, 
    - [1.56.1](https://cdn.cnbj1.fds.api.mi-img.com/xiaoqiang/rom/lx01/mico_firmware_c1cac_1.56.1.bin)
    - [1.62.6](https://cdn.cnbj1.fds.api.mi-img.com/xiaoqiang/rom/lx01/mico_firmware_4215788a8_1.62.6.bin)
    - 如果还想下载其他的版本, 知道版本号的前提下, 可以使用[这个脚本](https://github.com/duhow/xiaoai-patch/blob/master/tools/mico_download.py), 逻辑是暴力尝试, 效果不太好

    后续都假设基于 1.56.1
2. 解压固件
    - 懒人方法, 使用 [这个脚本](https://github.com/duhow/xiaoai-patch/blob/e3b71821366bf56f23d9360ab23726d3401c474c/tools/mico_firmware.py), 执行 `/path/to/mico_firmware.py -e /path/to/mico_firmware_c1cac_1.56.1.bin -d /path/to/extract`
    - 自助方法, 使用 binwalk (binwalk 需要安装, 根据自己的系统自行搜索)
    ```sh
    $ binwalk mico_firmware_c1cac_1.56.1.bin 
    DECIMAL       HEXADECIMAL     DESCRIPTION
    --------------------------------------------------------------------------------
    23944         0x5D88          uImage header, header size: 64 bytes, header CRC: 0x32556CD8, created: 1970-01-01 00:00:00, image size: 2944424 bytes, Data Address: 0x40008000, Entry Point: 0x40008000, data CRC: 0xCBE58ED2, OS: Linux, CPU: ARM, image type: OS Kernel Image, compression type: none, image name: "ARM OpenWrt Linux-3.4.39"
    24008         0x5DC8          Linux kernel ARM boot executable zImage (little-endian)
    40299         0x9D6B          gzip compressed data, maximum compression, from Unix, last modified: 1970-01-01 00:00:00 (null date)
    4195272       0x4003C8        Squashfs filesystem, little endian, version 4.0, compression:xz, size: 27150277 bytes, 2061 inodes, blocksize: 262144 bytes, created: 2021-10-28 13:55:53
    ```

    可以看到4行, 其实是两部分, 前3行是 kernel, 最后一行是 rootfs  
    第一行显示是一个 uImage, 是用于 uboot 引导的映像格式, zImage 是一个压缩过的的映像, uImage 就是 zImage 加了一些头信息, 让 uboot 更方便的加载  

    通常来讲 kernel 不用升级, 我们只关注 rootfs 即可

    ```sh
    $ dd if=mico_firmware_c1cac_1.56.1.bin bs=1 skip=4195272 of=rootfs.img
    27263264+0 records in                      
    27263264+0 records out                     
    27263264 bytes (27 MB, 26 MiB) copied, 30.5024 s, 894 kB/s

    sudo unsquashfs rootfs.img
    1968 inodes (1545 blocks) to write
    created 1389 files
    created 93 directories
    created 578 symlinks
    created 1 device
    created 0 fifos
    created 0 sockets
    created 0 hardlinks
    ```
3. 修改固件

    说明: 
    - squashfs 是只读的, 进入系统之后, 系统内的 rootfs 分区都是只读, 意味着对于 rootfs 的修改我们都必须通过固件完成, 进入系统之后是无法修改的  
    - 进入系统之后, /tmp 和 /data 都是可写的, /tmp 是挂载的内存, /data 是可以持久化的, 挂载点和大小如下
    ```sh
    $ df -h
    Filesystem                Size      Used Available Use% Mounted on
    rootfs                   26.0M     26.0M         0 100% /
    /dev/root                26.0M     26.0M         0 100% /
    tmpfs                    60.2M    692.0K     59.6M   1% /tmp
    tmpfs                   512.0K         0    512.0K   0% /dev
    /dev/by-name/UDISK       13.3M     10.5M      2.1M  83% /data
    ```
    - rootfs.img 不能超过 32MB, 超过的话, 刷入会把其他的部分刷坏

    开始修改:
    - #### 无密码直接进 shell (如果想保留密码, 跳过此步骤)

        修改 `squashfs-root/etc/inittab`  
        把 `::askconsole:/bin/login` 改成 `::askconsole:/bin/sh`
    
    - #### 修改密码 (如果想 ssh 正常登录, 此步必须)

        先生成一个密码, 自己定好 salt 和你自己的密码, 这里以 xiaoai/root 为例:   
        `openssl passwd -1 -salt "xiaoai" "root"`, 会生成字符串: `$1$xiaoai$803hWklCcQwX7v5gYP6pB0`  
        说明: 1 是计算方式 MD5, 具体可以 `man openssl-passwd` 查看更多帮助

        修改 `squashfs-root/etc/shadow` 的 root 那一行, 改成
        `root:$1$xiaoai$803hWklCcQwX7v5gYP6pB0:18128:0:99999:7:::` 保存

        这样就把 root 的密码修改成了 root, 如果前面我们尝试登陆的时候发现是 dsa 校验, 那么我们还需要修改校验方式为默认, 修改方法如下:

        修改 `squashfs-root/etc/pam.d/common-auth`, 将 `libmico-pam.so` 相关的行注释掉(前面加 #)  
        把 `auth  [success=1 default=ignore]  pam_unix.so nullok_secure` 取消注释 (删掉前面的 #)  
        保存
    
    - #### enable sshd

        说明: 固件里使用 dropbear 作为 ssh server (轻量)
        修改 etc/init.d/dropbear 启动脚本(较复杂, 可参考 [patch](./src/pack/patches/001.patch))
        
        ```sh
        # 自动启动
        sudo ln -s ../init.d/dropbear squashfs-root/etc/rc.d/S96dropbear
        ```
    
    - #### 打包
        mksquashfs squashfs-root patch.img -comp xz -b 256k
        我们会看到一个叫做 patch.img 的文件, 文件大小应该没有太大变化 (没有往里塞东西)

4. 刷固件
    
    软件准备:
    - 电脑端需要安装 fastboot: 搜 android platform tools, 进到 [Android 的网站](https://developer.android.com/tools/releases/platform-tools) 按照提示根据不同的平台安装 (注意 Windows 还需要装一个[驱动](https://developer.android.com/studio/run/win-usb)才行)

    - 进 fastboot 模式: 打开串口输入框, 重启小爱, 同时按住 s 键, 会进入到 uboot 的命令行, 提示符为 `sunxi#` (记得把输入的一大堆 s 删掉)
    - 敲命令 `fastboot_test`, 音箱就进入了 fastboot 模式
    - 在电脑端执行 `fastboot devices` 应该能看到 `Android Fastboot         Android Fastboot`
    - 执行 `fastboot flash rootfs1 patch.img` 等 7s 左右提示成功
    - 串口命令行中 Ctrl-C, 执行命令: `run setargs_first boot_first` 会使用 rootfs1 重启 (这个命令执行一次之后系统会记住启动分区, 以后再刷固件直接执行 `boot` 即可)

    重启之后, 我们应该就可以进去 shell 了 (是否需要登陆取决于是否修改了 inittab)

    ```sh
    BusyBox v1.24.1 () built-in shell (ash)

    _____  _              __    __ __ ___ ___
    |     ||_| ___  ___   |  |  |  |  |   |_  |
    | | | || ||  _|| . |  |  |__|-   -| | |_| |_
    |_|_|_||_||___||___|  |_____|__|__|___|_____|
    ----------------------------------------------
        ROM Type:release / Ver:1.56.1
    ----------------------------------------------
    root@LX01:/# 
    ```

    ifconfig 查看是否已经连接到了局域网 (如果刷机之前就没有连接到局域网, 可以刷之前连一次, 或者看后续"手动连家里wifi"的步骤)  
    `ps | grep dropbear` 应该也能看到进程, 这时候我们就可以 `ssh root@x.x.x.x` 到小爱音箱了

    可能遇到的问题:
    - no matching host key type found. Their offer: ssh-rsa  
        增加ssh参数, 使用类似 `ssh -oHostKeyAlgorithms=+ssh-rsa root@x.x.x.x` 即可

### 您可能感兴趣的链接:

- https://github.com/duhow/xiaoai-patch
- https://github.com/yihong0618/xiaogpt
- https://github.com/Yonsm/MiService
- https://github.com/richfelker/musl-cross-make
