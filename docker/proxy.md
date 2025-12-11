# プロキシ

Docker はサーバ・クライアント方式のためデーモンとクライアントにプロキシを設定する。

## デーモン

プロキシは下記に設定できる。

- 設定ファイル (*/etc/docker/daemon.json*)
- CLI (`--http-proxy`, `--https-proxy`, `--no-proxy`)
- 環境変数

コンテナイメージを `pull` するときに利用する。

### デーモンの設定ファイル

設定ファイルを作成する。

```sh
cat <<EOF | sudo tee /etc/docker/daemon.json
{
    "proxies": {
        "http-proxy": "http://proxy1.home.local:8080",
        "https-proxy": "http://proxy1.home.local:8080"
    }
}
EOF
```

サービスを再起動する。

```sh
sudo systemctl daemon-reload
sudo systemctl restart docker
```

dockerd の設定を確認する。

```sh
docker info | grep proxy
```

```text
 HTTP Proxy: http://proxy1.home.local:8080
 HTTPS Proxy: http://proxy1.home.local:8080
```

コンテナイメージを `pull` する。プロキシは存在しないので失敗する。

```sh
docker pull ubuntu
```

```text
Error response from daemon: failed to resolve reference "docker.io/library/ubuntu:latest": failed to do request: Head "https://registry-1.docker.io/v2/library/ubuntu/manifests/latest": proxyconnect tcp: dial tcp: lookup proxy1.home.local on 172.24.96.1:53: no such host
```

### デーモンの CLI

systemd の設定ファイルを作成する。
デーモンの設定ファイルにプロキシ設定があるとサービスが起動できないのでデーモンの設定ファイルは削除する。

```sh
sudo mkdir -p /etc/systemd/system/docker.service.d
cat <<EOF | sudo tee /etc/systemd/system/docker.service.d/override.conf
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock --http-proxy=http://proxy2.home.local:8080 --https-proxy=http://proxy2.home.local:8080
EOF
```

サービスを再起動する。

```sh
sudo systemctl daemon-reload
sudo systemctl restart docker
```

dockerd の設定を確認する。

```sh
docker info | grep proxy
```

```text
 HTTP Proxy: http://proxy2.home.local:8080
 HTTPS Proxy: http://proxy2.home.local:8080
```

コンテナイメージを `pull` する。プロキシは存在しないので失敗する。

```sh
docker pull ubuntu
```

```text
Error response from daemon: failed to resolve reference "docker.io/library/ubuntu:latest": failed to do request: Head "https://registry-1.docker.io/v2/library/ubuntu/manifests/latest": proxyconnect tcp: dial tcp: lookup proxy2.home.local on 172.24.96.1:53: no such host
```

### デーモンの環境変数

systemd の設定ファイルを追加する。

```sh
sudo mkdir -p /etc/systemd/system/docker.service.d
cat <<EOF | sudo tee /etc/systemd/system/docker.service.d/http-proxy.conf 
[Service]
Environment="HTTP_PROXY=http://proxy3.home.local:8080"
Environment="HTTPS_PROXY=http://proxy3.home.local:8080"
EOF
```

サービスを再起動する。

```sh
sudo systemctl daemon-reload
sudo systemctl restart docker
```

systemd の設定を確認する。

```sh
systemctl show --property=Environment docker
```

```text
Environment=HTTP_PROXY=http://proxy3.home.local:8080 HTTPS_PROXY=http://proxy3.home.local:8080
```

dockerd の設定を確認する。

```sh
docker info | grep proxy
```

```text
 HTTP Proxy: http://proxy3.home.local:8080
 HTTPS Proxy: http://proxy3.home.local:8080
```

コンテナイメージを `pull` する。プロキシは存在しないので失敗する。

```sh
docker pull ubuntu
```

```text
Error response from daemon: failed to resolve reference "docker.io/library/ubuntu:latest": failed to do request: Head "https://registry-1.docker.io/v2/library/ubuntu/manifests/latest": proxyconnect tcp: dial tcp: lookup proxy3.home.local on 172.24.96.1:53: no such host
```

コンテナイメージのビルド時にベースイメージを `pull` するときは、
実行時のシェルの環境変数が参照される。

```sh
HTTP_PROXY=http://proxy4.home.local:8080 HTTPS_PROXY=http://proxy4.home.local:8080 docker build - <<EOF
FROM ubuntu
RUN echo Hello, World.
EOF
```

```text
ERROR: failed to build: failed to solve: failed to fetch anonymous token: Get "https://auth.docker.io/token?scope=repository%3Alibrary%2Fubuntu%3Apull&service=registry.docker.io": proxyconnect tcp: dial tcp: lookup proxy4.home.local on 172.24.96.1:53: no such host
```

`docker pull` の場合はシェルの環境変数は影響を受けない。

### デーモン設定の優先順位

設定の優先順位は下記となる。

1. 設定ファイル / CLI
2. 環境変数(システム)
3. 環境変数(実行時のシェル)

### `NO_PROXY` 形式

環境変数 `NO_PROXY` は下記の形式を指定できる。

- IP アドレス
- ドメインとそのサブドメイン
- サブドメインのみ (ドットで始まる場合)
- アスタリスクのみ (すべてプロキシしない)
- CIDR ?

## クライアント

プロキシは下記に設定できる。

- 設定ファイル (*~/.docker/config.json*)
- CLI (`--build-arg`)
- Dockerfile

コンテナイメージをビルドするときに利用する。

### クライアント設定ファイル (ビルド時)

設定ファイルを作成する。

```sh
cat <<EOF > ~/.docker/config.json
{
    "proxies": {
        "default": {
            "httpProxy": "http://proxy1.home.local:8080",
            "httpsProxy": "http://proxy1.home.local:8080"
        }
    }
}
EOF
```

コンテナイメージをビルドする。

```sh
docker build --no-cache --progress=plain - <<"EOF"
FROM ubuntu
RUN echo $HTTP_PROXY
EOF
```

```text
 :
 :
#5 [2/2] RUN echo $HTTP_PROXY
#5 0.094 http://proxy1.home.local:8080
#5 DONE 0.1s
 :
 :
```

### クライアントの CLI (ビルド時)

`--build-arg` に環境変数を設定する。

```sh
docker build --no-cache --progress=plain --build-arg HTTP_PROXY=http://proxy2.home.local:8080 - <<"EOF"
FROM ubuntu
RUN echo $HTTP_PROXY
EOF
```

```text
 :
 :
#5 [2/2] RUN echo $HTTP_PROXY
#5 0.091 http://proxy2.home.local:8080
#5 DONE 0.1s
 :
 :
```

### Dockerfile (ビルド時)

Dockerfile 内で `ENV` を環境変数を指定する。

```sh
docker build --no-cache --progress=plain - <<"EOF"
FROM ubuntu
ENV HTTP_PROXY=http://proxy3.home.local:8080
RUN echo $HTTP_PROXY
EOF
```

```text
 :
 :
#5 [2/2] RUN echo http://proxy3.home.local:8080
#5 0.091 http://proxy3.home.local:8080
#5 DONE 0.1s
 :
 :
```

### クライアント設定の優先順位

設定の優先順位は下記となる。

1. CLI
2. 設定ファイル
3. Dockerfile

```sh
docker build --no-cache --progress=plain --build-arg HTTP_PROXY=http://proxy2.home.local:8080 - <<"EOF"
FROM ubuntu
ENV HTTP_PROXY=http://proxy3.home.local:8080
RUN echo $HTTP_PROXY
EOF
```

```text
 :
 :
#5 [2/2] RUN echo http://proxy3.home.local:8080
#5 0.131 http://proxy2.home.local:8080
#5 DONE 0.1s
 :
 :
```

## コンテナ

プロキシは下記に設定できる。

- 設定ファイル (*~/.docker/config.json*)
- CLI (`--env`)
- Dockerfile

コンテナ内で利用する。

### クライアント設定ファイル (コンテナ内)

設定ファイルを作成する。

```sh
cat <<EOF > ~/.docker/config.json
{
    "proxies": {
        "default": {
            "httpProxy": "http://proxy1.home.local:8080",
            "httpsProxy": "http://proxy1.home.local:8080"
        }
    }
}
EOF
```

コンテナを起動する。

```sh
docker run --rm ubuntu bash -c 'echo $HTTP_PROXY'
```

```text
http://proxy1.home.local:8080
```

### クライアントの CLI (コンテナ内)

`--env` に環境変数を設定する。

```sh
docker run --rm --env HTTP_PROXY=http://proxy2.home.local:8080 ubuntu bash -c 'echo $HTTP_PROXY'
```

```text
http://proxy2.home.local:8080
```

### Dockerfile (コンテナ内)

Dockerfile 内で `ENV` を環境変数を指定する。

```sh
docker build -t ubuntu:env - <<"EOF"
FROM ubuntu
ENV HTTP_PROXY=http://proxy3.home.local:8080
RUN echo $HTTP_PROXY
EOF
```

コンテナを起動する。

```sh
docker run --rm ubuntu:env bash -c 'echo $HTTP_PROXY'
```

```text
http://proxy3.home.local:8080
```

### コンテナ設定の優先順位

設定の優先順位は下記となる。

1. CLI
2. 設定ファイル
3. Dockerfile

## Docker Compose

`compose` でビルド時とコンテナ内の環境変数を指定する。

```sh
docker compose -f <(cat <<"EOF"
services:
  app:
    build:
      dockerfile_inline: |
        FROM ubuntu
        ENV HTTP_PROXY=http://proxy2.home.local:8080
        RUN echo $$HTTP_PROXY
    environment:
      HTTP_PROXY: http://proxy3.home.local:8080
    command: bash -c 'echo $$HTTP_PROXY'
EOF
) run --build --rm app
```

```text
 :
 :
=> CACHED [2/2] RUN echo http://proxy2.home.local:8080
 :
 :
http://proxy3.home.local:8080
```

`command` はコンテナ内のシェルで実行されないため明示的にシェルを起動する。
シェル実行前に変数は展開されないように `$` をエスケープする。

## 参考

- [Daemon proxy configuration](https://docs.docker.com/engine/daemon/proxy/)
- [Use a proxy server with the Docker CLI](https://docs.docker.com/engine/cli/proxy/)
- [We need to talk: Can we standardize NO_PROXY?](https://about.gitlab.com/blog/we-need-to-talk-no-proxy/)
