# インストール

## Python のインストール

Python 3.10 以降をインストールする。

```sh
dnf install -y python3.14 python3.14-pip
```

## RamaLama のインストール

仮想環境を作成する。

```sh
python3.14 -m venv ramalama
source ramalama/bin/activate
```

RamaLama をインストールする。

```sh
pip install ramalama
ramalama version
```

```text
ramalama version 0.17.1
```
