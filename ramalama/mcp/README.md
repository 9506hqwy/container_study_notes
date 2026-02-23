# Time MCP Server

## Install

Install dependencies libraray.

```sh
pip install fastmcp
```

## Run

Run MCP server.

```sh
fastmcp run server.py:mcp --transport http --port 8001
```

```text
[02/23/26 13:54:58] INFO     Starting MCP server 'Time MCP Server' with transport 'http' on http://127.0.0.1:8001/mcp
```

## Test

Call MCP server.

```sh
python client.py
```

```python
CallToolResult(
    content=[
        TextContent(
            type='text',
            text='"2026-02-23T13:55:41.075295"',
            annotations=None,
            meta=None)
    ],
    structured_content={'result': '2026-02-23T13:55:41.075295'},
    meta=None,
    data=datetime.datetime(2026, 2, 23, 13, 55, 41, 75295),
    is_error=False
)
```
