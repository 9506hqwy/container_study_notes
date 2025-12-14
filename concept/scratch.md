# コンテナの作成

名前空間と pivot_root でコンテナを作成する。

## rootfs の準備

コンテナイメージをダウンロードする。

```sh
curl -fsSLO https://cloud.centos.org/centos/10-stream/x86_64/images/CentOS-Stream-Container-Minimal-10-latest.x86_64.tar.xz
```

コンテナイメージを確認する。

```sh
tar -tf CentOS-Stream-Container-Minimal-10-latest.x86_64.tar.xz
```

```text
59efd7a5a7c7e9cbf618345ba7649085e81e9b3863dfdfab1674b823ccc08a23/
59efd7a5a7c7e9cbf618345ba7649085e81e9b3863dfdfab1674b823ccc08a23/VERSION
59efd7a5a7c7e9cbf618345ba7649085e81e9b3863dfdfab1674b823ccc08a23/layer.tar
59efd7a5a7c7e9cbf618345ba7649085e81e9b3863dfdfab1674b823ccc08a23/json
repositories
```

rootfs を展開する。

```sh
mkdir -p centos10
tar -Jx -O -f CentOS-Stream-Container-Minimal-10-latest.x86_64.tar.xz 59efd7a5a7c7e9cbf618345ba7649085e81e9b3863dfdfab1674b823ccc08a23/layer.tar | \
  tar -xf - -C centos10
```

内容を確認する。

```sh
ls -l centos10/
```

```text
合計 8
dr-xr-xr-x.  2 centos10 centos10    6  4月  2  2025 afs
lrwxrwxrwx.  1 centos10 centos10    7  4月  2  2025 bin -> usr/bin
dr-xr-xr-x.  2 centos10 centos10    6  4月  2  2025 boot
drwxr-xr-x.  2 centos10 centos10    6 12月  9 13:32 dev
drwxr-xr-x. 33 centos10 centos10 4096 12月  9 13:32 etc
drwxr-xr-x.  2 centos10 centos10    6  4月  2  2025 home
lrwxrwxrwx.  1 centos10 centos10    7  4月  2  2025 lib -> usr/lib
lrwxrwxrwx.  1 centos10 centos10    9  4月  2  2025 lib64 -> usr/lib64
drwx------.  2 centos10 centos10    6 12月  9 13:32 lost+found
drwxr-xr-x.  2 centos10 centos10    6  4月  2  2025 media
drwxr-xr-x.  2 centos10 centos10    6  4月  2  2025 mnt
drwxr-xr-x.  2 centos10 centos10    6  4月  2  2025 opt
drwxr-xr-x.  2 centos10 centos10    6 12月  9 13:32 proc
dr-xr-x---.  2 centos10 centos10  111 12月  9 13:32 root
drwxr-xr-x.  3 centos10 centos10   18 12月  9 13:32 run
lrwxrwxrwx.  1 centos10 centos10    8  4月  2  2025 sbin -> usr/sbin
drwxr-xr-x.  2 centos10 centos10    6  4月  2  2025 srv
drwxr-xr-x.  2 centos10 centos10    6 12月  9 13:32 sys
drwxr-xr-x.  2 centos10 centos10    6 12月  9 13:32 tmp
drwxr-xr-x. 12 centos10 centos10  144 12月  9 13:32 usr
drwxr-xr-x. 18 centos10 centos10 4096 12月  9 13:32 var
```

## 名前空間の作成

親プロセスを確認する。

```sh
echo $$
```

```text
1915
```

親プロセスの名前空間を確認する。

```sh
ls -l /proc/$$/ns
```

```text
合計 0
lrwxrwxrwx. 1 centos10 centos10 0  1月  1 00:45 cgroup -> 'cgroup:[4026531835]'
lrwxrwxrwx. 1 centos10 centos10 0  1月  1 00:45 ipc -> 'ipc:[4026531839]'
lrwxrwxrwx. 1 centos10 centos10 0  1月  1 00:45 mnt -> 'mnt:[4026531841]'
lrwxrwxrwx. 1 centos10 centos10 0  1月  1 00:45 net -> 'net:[4026531840]'
lrwxrwxrwx. 1 centos10 centos10 0  1月  1 00:45 pid -> 'pid:[4026531836]'
lrwxrwxrwx. 1 centos10 centos10 0  1月  1 00:45 pid_for_children -> 'pid:[4026531836]'
lrwxrwxrwx. 1 centos10 centos10 0  1月  1 00:45 time -> 'time:[4026531834]'
lrwxrwxrwx. 1 centos10 centos10 0  1月  1 00:45 time_for_children -> 'time:[4026531834]'
lrwxrwxrwx. 1 centos10 centos10 0  1月  1 00:45 user -> 'user:[4026531837]'
lrwxrwxrwx. 1 centos10 centos10 0  1月  1 00:45 uts -> 'uts:[4026531838]'
```

名前空間を作成する。

```sh
unshare --mount --uts --ipc --net --pid --user --time --fork \
    --map-user=root \
    --map-group=root \
    --mount-proc=centos10/proc \
    bash
ls -l /proc/$$/ns
```

```text
total 0
lrwxrwxrwx. 1 root root 0 Dec 31 15:59 cgroup -> 'cgroup:[4026531835]'
lrwxrwxrwx. 1 root root 0 Dec 31 15:59 ipc -> 'ipc:[4026532251]'
lrwxrwxrwx. 1 root root 0 Dec 31 15:59 mnt -> 'mnt:[4026532249]'
lrwxrwxrwx. 1 root root 0 Dec 31 15:59 net -> 'net:[4026532253]'
lrwxrwxrwx. 1 root root 0 Dec 31 15:59 pid -> 'pid:[4026532252]'
lrwxrwxrwx. 1 root root 0 Dec 31 15:59 pid_for_children -> 'pid:[4026532252]'
lrwxrwxrwx. 1 root root 0 Dec 31 15:59 time -> 'time:[4026532309]'
lrwxrwxrwx. 1 root root 0 Dec 31 15:59 time_for_children -> 'time:[4026532309]'
lrwxrwxrwx. 1 root root 0 Dec 31 15:59 user -> 'user:[4026532186]'
lrwxrwxrwx. 1 root root 0 Dec 31 15:59 uts -> 'uts:[4026532250]'
```

親プロセスからみた子プロセスを確認する。

```sh
pstree -s -p 1915
```

```text
systemd(1)---sshd(858)---sshd-session(1897)---sshd-session(1914)---bash(1915)---unshare(3194)---bash(3195)
```

## ルートファイルシステムの切り替え

`pivot_root` で rootfs を */* に更新する。

特殊ファイルシステムをマウントする。
`/proc` をマウントしないと `pivot_root` 後の `umount` ができない。

```sh
mount -t proc proc centos10/proc
mount -t sysfs sysfs centos10/sys
mount -t tmpfs tmpfs centos10/tmp
```

`pivot_root` で切り替えるには新しい */* はマウントポイントである必要があるためバインドマウントする。

```sh
mount --bind centos10 centos10
```

*/* を切り替える。
今の */* をマウントするディレクトリは新しい */* の下に作成する必要がある。

```sh
cd centos10/
mkdir -p old_root
pivot_root . old_root
```

元の */* をアンマウントして参照できないようにする。

```sh
/old_root/usr/bin/umount -l /old_root
rm -rf /old_root
```

```{note}
TODO: ネットワークとファイルシステム
```
