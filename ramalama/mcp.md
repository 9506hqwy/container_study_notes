# MCP

## MCP サーバの起動

[Time MCP Server](./mcp/README.md) を起動する。

```sh
fastmcp run server.py:mcp --transport http --host 0.0.0.0 --port 8001
```

```text
[02/23/26 14:00:12] INFO     Starting MCP server 'Time MCP Server' with transport 'http' on http://0.0.0.0:8001/mcp
```

## コンテナの起動

MCP サーバを指定して起動する。

```sh
ramalama run --image quay.io/ramalama/ramalama --mcp=http://192.168.0.34:8001/mcp gpt-oss:20b
```

プロンプトが起動する。

```sh
Found 1 tool(s) from Time MCP Server

Usage:
  - Ask questions naturally (automatic tool selection)
  - Use '/tool [question]' to manually select which tool to use
  - Use '/bye' or 'exit' to quit
🦭 > /tool 時刻は？

Available tools:

  1. current_timeex
     Inputs: none


Select tool(s) (e.g. 1,2,3) or 'q' to cancel: 1

 current_time -> **現在の時刻**
- **ISO 8601形式**：`2026-02-23T14:14:45.903301`
- **日本語で読むと**：2026 年 2 月 23 日 14時 14分 45秒（小数点以下はミリ秒まで含む）

※ 上記のタイムスタンプは **UTC (協定世界時)** で表現されているため、ローカルタイム（日本時間なら +9 時間）に合わせると 2026 年 2 月 23 日 23時 14分 45秒となります。
🦭 >
```
