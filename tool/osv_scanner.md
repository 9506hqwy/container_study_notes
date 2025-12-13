# osv-scanner

コンテナイメージの脆弱性をスキャンする。

## インストール

バイナリをダウンロードする。

```sh
mkdir -p ~/.local/bin
OSV_VERSION=$(curl -fsSL "https://api.github.com/repos/google/osv-scanner/releases/latest" | jq -r ".tag_name")
curl -fsSL -o ~/.local/bin/osv-scanner "https://github.com/google/osv-scanner/releases/download/${OSV_VERSION}/osv-scanner_linux_amd64"
chmod +x ~/.local/bin/osv-scanner
```

## コンテナイメージをスキャン

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

コンテナイメージをスキャンする。

```sh
osv-scanner scan image ubuntu:hello
```

```text
Checking if docker image ("ubuntu:hello") exists locally...
Saving docker image ("ubuntu:hello") to temporary file...
Scanning image "ubuntu:hello"
Starting filesystem walk for root:
End status: 660 dirs visited, 3445 inodes visited, 2759 Extract calls, 82.884448ms elapsed, 82.884549ms wall time
Starting filesystem walk for root:
End status: 0 dirs visited, 1 inodes visited, 1 Extract calls, 530.686µs elapsed, 530.734µs wall time

Container Scanning Result (Ubuntu 24.04.3 LTS):
Total 12 packages affected by 15 known vulnerabilities (0 Critical, 2 High, 10 Medium, 2 Low, 1 Unknown) from 1 ecosystem.
0 vulnerabilities can be fixed.


Ubuntu:24.04
+---------------------------------------------------------------------------------------------------------------------------------------+
| Source:os:/var/lib/dpkg/status                                                                                                        |
+----------------+-------------------------+------------------+------------+--------------------------------------------+---------------+
| SOURCE PACKAGE | INSTALLED VERSION       | FIX AVAILABLE    | VULN COUNT | BINARY PACKAGES (COUNT) | INTRODUCED LAYER | IN BASE IMAGE |
+----------------+-------------------------+------------------+------------+-------------------------+------------------+---------------+
| coreutils      | 9.4-3ubuntu6.1          | No fix available |          2 | coreutils               | # 4 Layer        | ubuntu        |
| gnupg2         | 2.4.4-2ubuntu17.3       | No fix available |          1 | gpgv                    | # 4 Layer        | ubuntu        |
| gnutls28       | 3.8.3-1.1ubuntu3.4      | No fix available |          1 | libgnutls30t64          | # 4 Layer        | ubuntu        |
| libgcrypt20    | 1.10.3-2build1          | No fix available |          1 | libgcrypt20             | # 4 Layer        | ubuntu        |
| lz4            | 1.9.4-1build1.1         | No fix available |          1 | liblz4-1                | # 4 Layer        | ubuntu        |
| ncurses        | 6.4+20240113-1ubuntu2   | No fix available |          1 | libncursesw6... (4)     | # 4 Layer        | ubuntu        |
| openssl        | 3.0.13-0ubuntu3.6       | No fix available |          2 | libssl3t64              | # 4 Layer        | ubuntu        |
| pam            | 1.5.3-5ubuntu5.5        | No fix available |          2 | libpam-modules... (4)   | # 4 Layer        | ubuntu        |
| shadow         | 1:4.13+dfsg1-4ubuntu3.2 | No fix available |          1 | login, passwd           | # 4 Layer        | ubuntu        |
| tar            | 1.35+dfsg-3build1       | No fix available |          1 | tar                     | # 4 Layer        | ubuntu        |
| util-linux     | 1:2.39.3-9ubuntu6.3     | No fix available |          1 | bsdutils                | # 4 Layer        | ubuntu        |
| util-linux     | 2.39.3-9ubuntu6.3       | No fix available |          1 | libblkid1... (6)        | # 4 Layer        | ubuntu        |
+---------------------------------------------------------------------------------------------------------------------------------------+

Hiding 1 number of vulnerabilities deemed unimportant, use --all-vulns to show them.
For the most comprehensive scan results, we recommend using the HTML output: `osv-scanner scan image --serve <image_name>`.
You can also view the full vulnerability list in your terminal with: `osv-scanner scan image --format vertical <image_name>`.
```

`--format vertical` をつけると ID も出力される。
