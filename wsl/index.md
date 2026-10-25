# Windows Subsystem for Linux

## インストール

管理者権限で下記のコマンドを実行する。

```sh
wsl --update
```

```text
ダウンロード中: Linux 用 Windows サブシステム 3.0.3
インストール中: Linux 用 Windows サブシステム 3.0.3
Linux 用 Windows サブシステム 3.0.3 はインストールされました。
Windows オプション コンポーネントをインストールしています: VirtualMachinePlatform

展開イメージのサービスと管理ツール
バージョン: 10.0.26100.9549

イメージのバージョン: 10.0.26200.9711

機能を有効にしています
[==========================100.0%==========================]
操作は正常に完了しました。
要求された操作は正常に終了しました。変更を有効にするには、システムを再起動する必要があります。
更新プログラムを確認しています。
Linux 用 Windows サブシステムの最新バージョンは既にインストールされています。
```

バージョンを確認する。

```sh
wslc info
```

```text
クライアント:
WSL バージョン: 3.0.3.0
カーネル バージョン: 6.18.54.1-1
Direct3D バージョン: 1.611.1-81528511
DXCore バージョン: 10.0.26100.1-240331-1435.ge-release
Windows バージョン: 10.0.26200.9711
設定ファイル: C:\Users\you\AppData\Local\wslc\settings.yaml

サーバー:
セッション マネージャーのバージョン: 3.0.3
セッション: 0
```

設定ファイル *%LOCALAPPDATA%\wslc\settings.yaml* を確認する。
ファイルが存在しない場合は新規に作成される。

```sh
wslc settings
```

```yaml
session:
```

## コンテナイメージ

コンテナイメージを取得する。

```sh
wslc pull hello-world
```

```text
既定値 (latest) を使用しています
latest: Pulling from library/hello-world
4f55086f7dd0: Pull complete
Digest: sha256:11a3eb1597e864c51b3f56733cb2e8a90bf0c284bfc05f9444d81c558bc848aa
Status: Downloaded newer image for hello-world:latest
docker.io/library/hello-world:latest
```

コンテナイメージを確認する。

```sh
wslc images
```

```text
リポジトリ         タグ        画像 ID          作成済み      サイズ
hello-world   latest    e2ac70e7319a   6 か月前     10.1kB
```

コンテナイメージは *%LOCALAPPDATA%\wslc\sessions\<セッション名>\storage.vhdx* 内に保存される。

## コンテナ

コンテナを起動する。

```sh
wslc run --rm hello-world
```

```text
Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

## ネットワーク

### 既定のネットワーク

既定で作成されるネットワークを確認する。

```sh
wslc network list
```

```text
ネットワーク ID      名前        ドライバー     スコープ
a634b8d0a4d4   bridge    bridge    local
823e4214c623   host      host      local
73e25fc35a12   none      null      local
```

### ポート公開

コンテナの 80 番ポートをコンテナホストの 10080 番ポートで公開する。

```sh
wslc run -d --name web -p 10080:80 nginx
```

```text
イメージ 'nginx' が見つかりません。プルしています
latest: Pulling from library/nginx
ecc510c1e359: Pull complete
113d9139ada2: Pull complete
b19352c60515: Pull complete
188e9077f350: Pull complete
792a76c59dbd: Pull complete
c9ec797c69ed: Pull complete
6a6757ab48b1: Pull complete
Digest: sha256:332d0beea97cff8c0d5d27976c0778a4b00345b9d74c2feaaf8efde548314948
Status: Downloaded newer image for nginx:latest
ff63b485c09396a972456eba7001fea54f520041e31c3f02b02532618f817a47
```

コンテナの起動を確認する。

```sh
wslc ps
```

```text
コンテナー ID       画像        コマンド                     作成済み      状態                  ポート                       名前
ff63b485c093   nginx     "/docker-entrypoint.…"   約 1 分前    Up About a minute   127.0.0.1:10080->80/tcp   web
```

ポートに接続する。

```sh
curl http://127.0.0.1:10080
```

```xml
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<!-- ... -->
</html>
```

### ネットワーク作成

ネットワークを作成する。

```sh
wslc network create nw-bridge
```

```text
nw-bridge
```

## ボリューム

### バインドマウント

コンテナホスト上の *G:\containers\volumes\data* をコンテナ内の */mnt/data* にマウントする。

```sh
wslc run --rm -it -v G:\containers\volumes\data:/mnt/data ubuntu /bin/bash
```

```text
イメージ 'ubuntu' が見つかりません。プルしています
latest: Pulling from library/ubuntu
435bf5c20694: Pull complete
d9d511d19a19: Pull complete
Digest: sha256:c098726dd9b9733f3e885f8de0ef375206a311b0a317eadc40d347b1115fb944
Status: Downloaded newer image for ubuntu:latest
root@b07b590c7876:/#
```

マウント情報を確認する。

```sh
findmnt /mnt/data
```

```text
TARGET    SOURCE                                       FSTYPE   OPTIONS
/mnt/data drvfs[/9a014fb5-cd12-4a98-9956-c72e389e4cf1] virtiofs rw,relatime
```

コンテナ内でファイルを作成して所有者を確認する。

```sh
echo "Hello, World!" > /mnt/data/README.txt
ls -l /mnt/data/README.txt
```

```text
-rw-r--r-- 1 root root 14 Oct 18 09:39 /mnt/data/README.txt
```

コンテナホストでファイルを作成してコンテナ内で所有者を確認する。

```sh
ls -l /mnt/data/host.txt
```

```text
-rwxrwxrwx 1 root root 15 Oct 18 09:41 /mnt/data/host.txt
```

コンテナホスト側から見るファイルの権限に違いは見えない。

### ボリューム作成

ボリュームを作成する。

`--dirver` は `guest` と `vhd` を指定できる。
`guest` は wslc セッションが持つ *storage.vhdx* の中にデータを保持する。
`vhd` は新規に VHD ファイルを作成してデータを保持する。

```sh
wslc volume create --driver vhd -o SizeBytes=10737418240 vol-01
```

```text
vol-01
```

ボリュームを確認する。

```sh
wslc volume inspect vol-01
```

```json
[
  {
    "CreatedAt": "2026-10-25T13:45:52Z",
    "Driver": "vhd",
    "Labels": null,
    "Mountpoint": "/var/lib/docker/volumes/vol-01/_data",
    "Name": "vol-01",
    "Options": {
      "SizeBytes": "10737418240"
    },
    "Scope": "local",
    "Status": {
      "HostPath": "C:\\Users\\you\\AppData\\Local\\wslc\\sessions\\wslc-cli-you\\volumes\\vol-01.vhdx",
      "SizeBytes": "10737418240"
    }
  }
]
```

ボリューム vol-01 をコンテナ内の */mnt/data* にマウントする。

```sh
wslc run --rm -it -v vol-01:/mnt/data ubuntu /bin/bash
```

マウント情報を確認する。

```sh
findmnt /mnt/data
```

```text
/mnt/data /dev/sde ext4   rw,relatime,discard
```

## Dev Containers on Visual Studio Code

`dev.containers.dockerPath` を `wslc` に設定する。

## セッション

セッションを確認する。

```sh
wslc system session list
```

```text
ID        作成者 PID   表示名
1         7124      wslc-cli-you
```

セッションのシェルに接続する。

```sh
wslc system session shell
```

```text
root@ [ / ]#
```

OS 情報を確認する。

```sh
cat /etc/os-release
```

```text
NAME="Microsoft Azure Linux"
VERSION="3.0.20260616"
ID=azurelinux
VERSION_ID="3.0"
PRETTY_NAME="Microsoft Azure Linux 3.0"
ANSI_COLOR="1;34"
HOME_URL="https://aka.ms/azurelinux"
BUG_REPORT_URL="https://aka.ms/azurelinux"
SUPPORT_URL="https://aka.ms/azurelinux"
```

Docker 情報を確認する。

```sh
docker version
```

```text
Client:
 Version:           25.0.7
 API version:       1.44
 Go version:        go1.26.3
 Git commit:        4debf411d1e6efbd9ce65e4250718e9c529a6525
 Built:             Thu May 28 13:45:36 2026
 OS/Arch:           linux/amd64
 Context:           default

Server:
 Engine:
  Version:          25.0.3
  API version:      1.44 (minimum version 1.24)
  Go version:       go1.26.3
  Git commit:       f417435
  Built:            Sun May 31 04:44:36 2026
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          2.2.4
  GitCommit:        193637f7ee8ae5f5aa5248f49e7baa3e6164966e
 runc:
  Version:          1.3.3
  GitCommit:        d842d7719497cc3b774fd71620278ac9e17710e0
 docker-init:
  Version:          0.19.0
  GitCommit:
```

## 参考

- [Windows Subsystem for Linux Documentation](https://learn.microsoft.com/en-us/windows/wsl/)
- [WSL containers is now generally available](https://blogs.windows.com/windowsdeveloper/2026/09/29/wsl-containers-now-generally-available/)
