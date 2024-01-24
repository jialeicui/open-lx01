# 如何在音箱和 PC 之间传送文件

1. scp (推荐)

    音箱内置了 scp 命令, 可以方便的通过 ssh 协议拷贝文件  
使用方式是在音箱 shell 里执行: `scp foo@bar:/path/to/file /path/to/local/file`

    可能遇到的问题:

    - no matching host key type found
        server, 也就是 PC 上的 sshd 版本比较高, 默认没有开 rsa  
        可以修改 `/etc/ssh/sshd_config`, 在里边增加一行: `HostKeyAlgorithms ssh-rsa,ssh-dss`, 重启 sshd 服务即可

    - 从 PC scp 报错, 提示 `/usr/libexec/sftp-server: not found`, 这个目前还没查原因, 猜测是 dropbear 没有支持, 以及音箱里也没有这个bin

2. nc

    音箱内置的 nc 只支持往外传, 没办法监听本地端口然后从外边往里传, 所以需要自己编译一个全功能的 nc scp 替换内置的才行
