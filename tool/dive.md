# dive

コンテナイメージレイヤーを調査する。

## インストール

バイナリをダウンロードする。

```sh
mkdir -p ~/.local/bin
DIVE_VERSION=$(curl -fsSL "https://api.github.com/repos/wagoodman/dive/releases/latest" | jq -r ".tag_name")
curl -fsSL -o - "https://github.com/wagoodman/dive/releases/download/${DIVE_VERSION}/dive_${DIVE_VERSION#v}_linux_amd64.tar.gz" | \
    tar -zxf - -O dive >  ~/.local/bin/dive
chmod +x ~/.local/bin/dive
```

## イメージレイヤーの確認

イメージを作成する。

```sh
docker build -t ubuntu:hello - <<"EOF"
FROM ubuntu
RUN echo Hello, World > /a.txt
EOF
```

```text
[+] Building 0.5s (6/6) FINISHED                                                                                              docker:default
 => [internal] load build definition from Dockerfile                                                                                    0.0s
 => => transferring dockerfile: 147B                                                                                                    0.0s
 => [internal] load metadata for docker.io/library/ubuntu:latest                                                                        0.0s
 => [internal] load .dockerignore                                                                                                       0.0s
 => => transferring context: 2B                                                                                                         0.0s
 => CACHED [1/2] FROM docker.io/library/ubuntu:latest@sha256:c35e29c9450151419d9448b0fd75374fec4fff364a27f176fb458d472dfc9e54           0.0s
 => => resolve docker.io/library/ubuntu:latest@sha256:c35e29c9450151419d9448b0fd75374fec4fff364a27f176fb458d472dfc9e54                  0.0s
 => [2/2] RUN echo Hello, World > /a.txt                                                                                                0.2s
 => exporting to image                                                                                                                  0.1s
 => => exporting layers                                                                                                                 0.1s
 => => exporting manifest sha256:872eca8115554ff12b06fb345c153acb72ffba53d26276dcff40b3aa5a96421f                                       0.0s
 => => exporting config sha256:8069a658990f0d39078c7a098294bb1aef18734ff347bc1cb73b7b416efdf829                                         0.0s
 => => exporting attestation manifest sha256:8e1f8b2574d8dff2405c7b594e578aac488ffe295fec47697d7513cdce07b26f                           0.0s
 => => exporting manifest list sha256:bc2381c4de6c883f10d8001e4452529c2c2451d2b23bd8961f670da1983806cb                                  0.0s
 => => naming to docker.io/library/ubuntu:hello                                                                                         0.0s
 => => unpacking to docker.io/library/ubuntu:hello                                                                                      0.0s
 ```

コンテナイメージを調査する。

```sh
dive ubuntu:hello
```

イメージレイヤーごとのディレクトリ構成を確認できる。
追加や変更などの更新単位にフィルタリングしてイメージレイヤーの変更を確認できる。
