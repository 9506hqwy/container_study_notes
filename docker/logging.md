# ロギング

コンテナのログ出力方法を設定する。

既定のログドライバは `json-path` で */etc/docker/daemon.json* で指定できる。

`local` が推奨される。

```text
For other situations, the local logging driver is recommended as it performs log-rotation by default,
and uses a more efficient file format.
```

## ログドライバ `json-path`

JSON 形式でファイルに出力する。

```sh
docker run --name test --rm -d nginx
```

```text
009ac659bad0aabd268eebf93a964e605185f0b14e319532930ee6c4cb689bc4
```

ログファイルのパスを確認する。

```sh
docker inspect test --format "{{json .LogPath}}"
```

```json
"/var/lib/docker/containers/009ac659bad0aabd268eebf93a964e605185f0b14e319532930ee6c4cb689bc4/009ac659bad0aabd268eebf93a964e605185f0b14e319532930ee6c4cb689bc4-json.log"
```

ログを確認する。

```sh
sudo cat /var/lib/docker/containers/009ac659bad0aabd268eebf93a964e605185f0b14e319532930ee6c4cb689bc4/009ac659bad0aabd268eebf93a964e605185f0b14e319532930ee6c4cb689bc4-json.log
```

```text
{"log":"/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration\n","stream":"stdout","time":"2025-12-12T15:58:08.374283236Z"}
{"log":"/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/\n","stream":"stdout","time":"2025-12-12T15:58:08.374350938Z"}
 :
 :
```

コマンドで同じ内容が確認できる。

```sh
docker logs -f test
```

```text
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
 :
 :
```

## ログドライバ `local`

独自のテキスト形式でファイルに出力する。

```sh
docker run --name test --rm -d --log-driver local nginx
```

```text
373fb8bbf8eeda2351aa0bec3cb2ba8c3fa817c83e4cf75cb2a801bcf7907754
```

ログファイルのパスを確認する。表示されない。

```sh
docker inspect test --format "{{json .LogPath}}"
```

```json
""
```

ログを確認する。単純なテキスト形式ではない。

```sh
sudo cat /var/lib/docker/containers/373fb8bbf8eeda2351aa0bec3cb2ba8c3fa817c83e4cf75cb2a801bcf7907754/local-logs/container.log
```

```text
t
stdout `/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configurationt]
stdoutI/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/]i
 :
 :
```

コマンドで同じ内容が確認できる。

```sh
docker logs -f test
```

```text
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
 :
 :
```

## ログドライバ `journald`

journald に出力する。コンテナホストに journald が起動している必要がある。

```sh
docker run --name test --rm -d --log-driver journald nginx
```

```text
acf6ef1fbd6d57ab4e5f45f381ea1d4ec18cd0bd05c30d292a1ab9bb102c8fdd
```

ログファイルのパスはない。

```sh
docker inspect test --format "{{json .LogPath}}"
```

```json
""
```

ログを確認する。

```sh
journalctl -u docker CONTAINER_NAME=test
```

```text
12月 13 01:21:10 docker.home.local acf6ef1fbd6d[910]: /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
12月 13 01:21:10 docker.home.local acf6ef1fbd6d[910]: /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
 :
 :
```

コマンドで同じ内容が確認できる。

```sh
docker logs -f test
```

```text
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
 :
 :
```

## 参考

- [View container logs](https://docs.docker.com/engine/logging/)
