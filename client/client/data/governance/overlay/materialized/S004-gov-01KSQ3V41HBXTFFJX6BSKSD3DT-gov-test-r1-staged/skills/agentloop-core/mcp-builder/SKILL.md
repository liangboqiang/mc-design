---
name: mcp-builder
description: MCP Server 构建 Skill
capabilities:
  - tool.workspace.read
  - tool.workspace.write
  - tool.workspace.exec
---

# MCP Server 构建 Skill

你现在具备构建 MCP（Model Context Protocol）服务器的能力。MCP 允许模型通过标准协议调用外部服务。

## MCP 是什么

MCP Server 可以暴露：

- **Tools**：模型可调用的函数，类似 API endpoint。
- **Resources**：模型可读取的数据，例如文件或数据库记录。
- **Prompts**：预置提示模板。

## 快速开始：Python MCP Server

### 1. 创建项目

```bash
mkdir my-mcp-server && cd my-mcp-server
python3 -m venv venv && source venv/bin/activate
pip install mcp
```

### 2. 基础 Server 模板

```python
#!/usr/bin/env python3
"""my_server.py - 一个简单 MCP Server"""

from mcp.server import Server
from mcp.server.stdio import stdio_server

server = Server("my-server")

@server.tool()
async def hello(name: str) -> str:
    """向某人问好。

    Args:
        name: 要问候的名字
    """
    return f"Hello, {name}!"

@server.tool()
async def add_numbers(a: int, b: int) -> str:
    """两个数字相加。"""
    return str(a + b)

async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### 3. 在 Claude 中注册

添加到 `~/.claude/mcp.json`：

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python3",
      "args": ["/path/to/my_server.py"]
    }
  }
}
```

## TypeScript MCP Server

### 1. 初始化

```bash
mkdir my-mcp-server && cd my-mcp-server
npm init -y
npm install @modelcontextprotocol/sdk
```

### 2. 模板

```typescript
// src/index.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({
  name: "my-server",
  version: "1.0.0",
});

server.setRequestHandler("tools/list", async () => ({
  tools: [
    {
      name: "hello",
      description: "向某人问好",
      inputSchema: {
        type: "object",
        properties: {
          name: { type: "string", description: "要问候的名字" },
        },
        required: ["name"],
      },
    },
  ],
}));

server.setRequestHandler("tools/call", async (request) => {
  if (request.params.name === "hello") {
    const name = request.params.arguments.name;
    return { content: [{ type: "text", text: `Hello, ${name}!` }] };
  }
  throw new Error("未知工具");
});

const transport = new StdioServerTransport();
server.connect(transport);
```

## 高级模式

### 外部 API 集成

```python
import httpx
from mcp.server import Server

server = Server("weather-server")

@server.tool()
async def get_weather(city: str) -> str:
    """获取某城市的当前天气。"""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://api.weatherapi.com/v1/current.json",
            params={"key": "YOUR_API_KEY", "q": city}
        )
        data = resp.json()
        return f"{city}: {data['current']['temp_c']}C, {data['current']['condition']['text']}"
```

### 数据库访问

```python
import sqlite3
from mcp.server import Server

server = Server("db-server")

@server.tool()
async def query_db(sql: str) -> str:
    """执行只读 SQL 查询。"""
    if not sql.strip().upper().startswith("SELECT"):
        return "错误：只允许 SELECT 查询"

    conn = sqlite3.connect("data.db")
    cursor = conn.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    return str(rows)
```

### Resources：只读数据

```python
@server.resource("config://settings")
async def get_settings() -> str:
    """应用设置。"""
    return open("settings.json").read()

@server.resource("file://{path}")
async def read_file(path: str) -> str:
    """从工作区读取文件。"""
    return open(path).read()
```

## 测试

```bash
# 使用 MCP Inspector 测试
npx @anthropics/mcp-inspector python3 my_server.py

# 或直接发送测试消息
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | python3 my_server.py
```

## 最佳实践

1. **清晰的工具描述**：模型会根据描述决定何时调用工具。
2. **输入校验**：始终验证并清洗输入。
3. **错误处理**：返回有意义的错误信息。
4. **默认异步**：I/O 操作使用 async/await。
5. **安全边界**：敏感操作必须有鉴权或审批。
6. **幂等性**：工具应尽量可安全重试。
