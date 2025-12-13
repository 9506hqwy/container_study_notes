# trivy

コンテナイメージの脆弱性をスキャンする。

## インストール

バイナリをダウンロードする。

```sh
mkdir -p ~/.local/bin
TRIVY_VERSION=$(curl -fsSL "https://api.github.com/repos/aquasecurity/trivy/releases/latest" | jq -r ".tag_name")
curl -fsSL -o - "https://github.com/aquasecurity/trivy/releases/download/${TRIVY_VERSION}/trivy_${TRIVY_VERSION#v}_Linux-64bit.tar.gz" | \
    tar -zxf - -O trivy >  ~/.local/bin/trivy
chmod +x ~/.local/bin/trivy
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
trivy image ubuntu:hello
```

```text
2025-12-13T11:09:35+09:00       INFO    [vulndb] Need to update DB
2025-12-13T11:09:35+09:00       INFO    [vulndb] Downloading vulnerability DB...
2025-12-13T11:09:35+09:00       INFO    [vulndb] Downloading artifact...        repo="mirror.gcr.io/aquasec/trivy-db:2"
77.79 MiB / 77.79 MiB [----------------------------------------------------------------------------------------------------------------------------------] 100.00% 8.20 MiB p/s 9.7s
2025-12-13T11:09:46+09:00       INFO    [vulndb] Artifact successfully downloaded       repo="mirror.gcr.io/aquasec/trivy-db:2"
2025-12-13T11:09:46+09:00       INFO    [vuln] Vulnerability scanning is enabled
2025-12-13T11:09:46+09:00       INFO    [secret] Secret scanning is enabled
2025-12-13T11:09:46+09:00       INFO    [secret] If your scanning is slow, please try '--scanners vuln' to disable secret scanning
2025-12-13T11:09:46+09:00       INFO    [secret] Please see https://trivy.dev/docs/v0.68/guide/scanner/secret#recommendation for faster secret detection
2025-12-13T11:09:47+09:00       INFO    Detected OS     family="ubuntu" version="24.04"
2025-12-13T11:09:47+09:00       INFO    [ubuntu] Detecting vulnerabilities...   os_version="24.04" pkg_num=92
2025-12-13T11:09:47+09:00       INFO    Number of language-specific files       num=0

Report Summary

+-----------------------------+--------+-----------------+---------+
|           Target            |  Type  | Vulnerabilities | Secrets |
+-----------------------------+--------+-----------------+---------+
| ubuntu:hello (ubuntu 24.04) | ubuntu |       11        |    -    |
+-----------------------------+--------+-----------------+---------+
Legend:
- '-': Not scanned
- '0': Clean (no security findings detected)


ubuntu:hello (ubuntu 24.04)

Total: 11 (UNKNOWN: 0, LOW: 6, MEDIUM: 5, HIGH: 0, CRITICAL: 0)

+--------------------+----------------+----------+----------+-------------------------+---------------+-------------------------------------------------------------+
|      Library       | Vulnerability  | Severity |  Status  |    Installed Version    | Fixed Version |                            Title                            |
+--------------------+----------------+----------+----------+-------------------------+---------------+-------------------------------------------------------------+
| coreutils          | CVE-2016-2781  | LOW      | affected | 9.4-3ubuntu6.1          |               | coreutils: Non-privileged session can escape to the parent  |
|                    |                |          |          |                         |               | session in chroot                                           |
|                    |                |          |          |                         |               | https://avd.aquasec.com/nvd/cve-2016-2781                   |
+--------------------+----------------+          |          +-------------------------+---------------+-------------------------------------------------------------+
| gpgv               | CVE-2022-3219  |          |          | 2.4.4-2ubuntu17.3       |               | gnupg: denial of service issue (resource consumption) using |
|                    |                |          |          |                         |               | compressed packets                                          |
|                    |                |          |          |                         |               | https://avd.aquasec.com/nvd/cve-2022-3219                   |
+--------------------+----------------+          |          +-------------------------+---------------+-------------------------------------------------------------+
| libgcrypt20        | CVE-2024-2236  |          |          | 1.10.3-2build1          |               | libgcrypt: vulnerable to Marvin Attack                      |
|                    |                |          |          |                         |               | https://avd.aquasec.com/nvd/cve-2024-2236                   |
+--------------------+----------------+----------+          +-------------------------+---------------+-------------------------------------------------------------+
| libpam-modules     | CVE-2025-8941  | MEDIUM   |          | 1.5.3-5ubuntu5.5        |               | linux-pam: Incomplete fix for CVE-2025-6020                 |
|                    |                |          |          |                         |               | https://avd.aquasec.com/nvd/cve-2025-8941                   |
+--------------------+                |          |          |                         +---------------+                                                             |
| libpam-modules-bin |                |          |          |                         |               |                                                             |
|                    |                |          |          |                         |               |                                                             |
+--------------------+                |          |          |                         +---------------+                                                             |
| libpam-runtime     |                |          |          |                         |               |                                                             |
|                    |                |          |          |                         |               |                                                             |
+--------------------+                |          |          |                         +---------------+                                                             |
| libpam0g           |                |          |          |                         |               |                                                             |
|                    |                |          |          |                         |               |                                                             |
+--------------------+----------------+----------+          +-------------------------+---------------+-------------------------------------------------------------+
| libssl3t64         | CVE-2024-41996 | LOW      |          | 3.0.13-0ubuntu3.6       |               | openssl: remote attackers (from the client side) to trigger |
|                    |                |          |          |                         |               | unnecessarily expensive server-side...                      |
|                    |                |          |          |                         |               | https://avd.aquasec.com/nvd/cve-2024-41996                  |
+--------------------+----------------+          |          +-------------------------+---------------+-------------------------------------------------------------+
| login              | CVE-2024-56433 |          |          | 1:4.13+dfsg1-4ubuntu3.2 |               | shadow-utils: Default subordinate ID configuration in       |
|                    |                |          |          |                         |               | /etc/login.defs could lead to compromise                    |
|                    |                |          |          |                         |               | https://avd.aquasec.com/nvd/cve-2024-56433                  |
+--------------------+                |          |          |                         +---------------+                                                             |
| passwd             |                |          |          |                         |               |                                                             |
|                    |                |          |          |                         |               |                                                             |
|                    |                |          |          |                         |               |                                                             |
+--------------------+----------------+----------+          +-------------------------+---------------+-------------------------------------------------------------+
| tar                | CVE-2025-45582 | MEDIUM   |          | 1.35+dfsg-3build1       |               | tar: Tar path traversal                                     |
|                    |                |          |          |                         |               | https://avd.aquasec.com/nvd/cve-2025-45582                  |
+--------------------+----------------+----------+----------+-------------------------+---------------+-------------------------------------------------------------+
```
