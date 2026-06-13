#!/usr/bin/env python3
"""
Agent 脚手架脚本 - 按最佳实践创建新的 Agent 项目。

用法：
    python init_agent.py <agent-name> [--level 0-4] [--path <output-dir>]

示例：
    python init_agent.py my-agent                 # Level 1（4 个工具）
    python init_agent.py my-agent --level 0      # 最小版（只有 bash）
    python init_agent.py my-agent --level 2      # 带 todo
    python init_agent.py my-agent --path ./bots  # 自定义输出目录
"""

import argparse
import sys
from pathlib import Path

# 各复杂度级别的 Agent 模板
TEMPLATES = {
    0: '''#!/usr/bin/env python3
"""
Level 0 Agent - 一个 Bash 就够了（约 50 行）

核心洞察：一个工具（bash）可以完成很多事情。
通过自递归生成子 Agent：python {name}.py "subtask"
"""

from anthropic import Anthropic
from dotenv import load_dotenv
import subprocess
import os

load_dotenv(override=False)

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    base_url=os.getenv("ANTHROPIC_BASE_URL")
)
MODEL = os.getenv("MODEL_NAME", "claude-sonnet-4-20250514")

SYSTEM = """你是代码 Agent。所有事情都通过 bash 完成：
- 读取：cat、grep、find、ls
- 写入：echo 'content' > file
- 子 Agent：python {name}.py "subtask"
"""

TOOL = [{{
    "name": "bash",
    "description": "执行 shell 命令",
    "input_schema": {{"type": "object", "properties": {{"command": {{"type": "string"}}}}, "required": ["command"]}}
}}]

def run(prompt, history=[]):
    history.append({{"role": "user", "content": prompt}})
    while True:
        r = client.messages.create(model=MODEL, system=SYSTEM, messages=history, tools=TOOL, max_tokens=8000)
        history.append({{"role": "assistant", "content": r.content}})
        if r.finish_reason != "tool_calls":
            return "".join(b.text for b in r.content if hasattr(b, "text"))
        results = []
        for b in r.content:
            if b.type == "tool_calls":
                print(f"> {{b.input['command']}}")
                try:
                    out = subprocess.run(b.input["command"], shell=True, capture_output=True, text=True, timeout=60)
                    output = (out.stdout + out.stderr).strip() or "（空输出）"
                except Exception as e:
                    output = f"错误：{{e}}"
                results.append({{"type": "tool_result", "tool_calls_id": b.id, "content": output[:50000]}})
        history.append({{"role": "user", "content": results}})

if __name__ == "__main__":
    h = []
    print("{name} - Level 0 Agent\\n输入 q 退出。\\n")
    while (q := input(">> ").strip()) not in ("q", "quit", ""):
        print(run(q, h), "\\n")
''',

    1: '''#!/usr/bin/env python3
"""
Level 1 Agent - 模型就是 Agent（约 200 行）

核心洞察：4 个工具覆盖 90% 的代码任务。
模型才是 Agent；代码只负责运行循环。
"""

from anthropic import Anthropic
from dotenv import load_dotenv
from pathlib import Path
import subprocess
import os

load_dotenv(override=False)

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    base_url=os.getenv("ANTHROPIC_BASE_URL")
)
MODEL = os.getenv("MODEL_NAME", "claude-sonnet-4-20250514")
WORKDIR = Path.cwd()

SYSTEM = f"""你是运行在 {{WORKDIR}} 的代码 Agent。

规则：
- 优先使用工具，而不是只写解释。行动，不要空谈。
- 不要编造文件路径。不确定时先用 ls/find 查看。
- 保持最小改动，不要过度工程化。
- 完成后总结变更内容。"""

TOOLS = [
    {{"name": "bash", "description": "运行 shell 命令",
     "input_schema": {{"type": "object", "properties": {{"command": {{"type": "string"}}}}, "required": ["command"]}}}},
    {{"name": "read_file", "description": "读取文件内容",
     "input_schema": {{"type": "object", "properties": {{"path": {{"type": "string"}}}}, "required": ["path"]}}}},
    {{"name": "write_file", "description": "把内容写入文件",
     "input_schema": {{"type": "object", "properties": {{"path": {{"type": "string"}}, "content": {{"type": "string"}}}}, "required": ["path", "content"]}}}},
    {{"name": "edit_file", "description": "替换文件中的精确文本",
     "input_schema": {{"type": "object", "properties": {{"path": {{"type": "string"}}, "old_text": {{"type": "string"}}, "new_text": {{"type": "string"}}}}, "required": ["path", "old_text", "new_text"]}}}},
]

def safe_path(p: str) -> Path:
    """防止路径逃逸攻击。"""
    path = (WORKDIR / p).resolve()
    if not path.is_relative_to(WORKDIR):
        raise ValueError(f"路径逃逸工作区：{{p}}")
    return path

def execute(name: str, args: dict) -> str:
    """执行工具并返回结果。"""
    if name == "bash":
        dangerous = ["rm -rf /", "sudo", "shutdown", "> /dev/"]
        if any(d in args["command"] for d in dangerous):
            return "错误：危险命令已被阻止"
        try:
            r = subprocess.run(args["command"], shell=True, cwd=WORKDIR, capture_output=True, text=True, timeout=60)
            return (r.stdout + r.stderr).strip()[:50000] or "（空输出）"
        except subprocess.TimeoutExpired:
            return "错误：超时（60s）"
        except Exception as e:
            return f"错误：{{e}}"

    if name == "read_file":
        try:
            return safe_path(args["path"]).read_text()[:50000]
        except Exception as e:
            return f"错误：{{e}}"

    if name == "write_file":
        try:
            p = safe_path(args["path"])
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(args["content"])
            return f"已写入 {{len(args['content'])}} 字节到 {{args['path']}}"
        except Exception as e:
            return f"错误：{{e}}"

    if name == "edit_file":
        try:
            p = safe_path(args["path"])
            content = p.read_text()
            if args["old_text"] not in content:
                return f"错误：在 {{args['path']}} 中未找到文本"
            p.write_text(content.replace(args["old_text"], args["new_text"], 1))
            return f"已编辑 {{args['path']}}"
        except Exception as e:
            return f"错误：{{e}}"

    return f"未知工具：{{name}}"

def agent(prompt: str, history: list = None) -> str:
    """运行 Agent 循环。"""
    if history is None:
        history = []
    history.append({{"role": "user", "content": prompt}})

    while True:
        response = client.messages.create(
            model=MODEL, system=SYSTEM, messages=history, tools=TOOLS, max_tokens=8000
        )
        history.append({{"role": "assistant", "content": response.content}})

        if response.finish_reason != "tool_calls":
            return "".join(b.text for b in response.content if hasattr(b, "text"))

        results = []
        for block in response.content:
            if block.type == "tool_calls":
                print(f"> {{block.name}}: {{str(block.input)[:100]}}")
                output = execute(block.name, block.input)
                print(f"  {{output[:100]}}...")
                results.append({{"type": "tool_result", "tool_calls_id": block.id, "content": output}})
        history.append({{"role": "user", "content": results}})

if __name__ == "__main__":
    print(f"{name} - Level 1 Agent，工作区：{{WORKDIR}}")
    print("输入 q 退出。\\n")
    h = []
    while True:
        try:
            query = input(">> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if query in ("q", "quit", "exit", ""):
            break
        print(agent(query, h), "\\n")
''',
}

ENV_TEMPLATE = '''# API 配置
ANTHROPIC_API_KEY=sk-xxx
ANTHROPIC_BASE_URL=https://api.anthropic.com
MODEL_NAME=claude-sonnet-4-20250514
'''


def create_agent(name: str, level: int, output_dir: Path):
    """创建新的 Agent 项目。"""
    # 校验级别
    if level not in TEMPLATES and level not in (2, 3, 4):
        print(f"错误：脚手架暂未实现 Level {level}。")
        print("可用级别：0（最小版）、1（4 个工具）")
        print("Level 2-4 请从 Beya 模板资产补齐。")
        sys.exit(1)

    # 创建输出目录
    agent_dir = output_dir / name
    agent_dir.mkdir(parents=True, exist_ok=True)

    # 写入 Agent 文件
    agent_file = agent_dir / f"{name}.py"
    template = TEMPLATES.get(level, TEMPLATES[1])
    agent_file.write_text(template.format(name=name))
    print(f"已创建：{agent_file}")

    # 写入 .env.example
    env_file = agent_dir / ".env.example"
    env_file.write_text(ENV_TEMPLATE)
    print(f"已创建：{env_file}")

    # 写入 .gitignore
    gitignore = agent_dir / ".gitignore"
    gitignore.write_text(".env\n__pycache__/\n*.pyc\n")
    print(f"已创建：{gitignore}")

    print(f"\nAgent '{name}' 已创建到 {agent_dir}")
    print("\n下一步：")
    print(f"  1. cd {agent_dir}")
    print("  2. cp .env.example .env")
    print("  3. 编辑 .env，填入你的 API key")
    print("  4. pip install anthropic environment-variable support")
    print(f"  5. python {name}.py")


def main():
    parser = argparse.ArgumentParser(
        description="创建新的 AI coding agent 项目脚手架",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
级别：
  0  最小版（约 50 行） - 单 bash 工具，通过自递归实现子 Agent
  1  基础版（约 200 行） - 4 个核心工具：bash、read、write、edit
  2  Todo（约 300 行）   - 增加 todo，用于结构化规划
  3  子 Agent（约 450）  - 增加 Task 工具，用于上下文隔离
  4  Skills（约 550）    - 增加 Skill 工具，用于领域知识
        """
    )
    parser.add_argument("name", help="要创建的 Agent 名称")
    parser.add_argument("--level", type=int, default=1, choices=[0, 1, 2, 3, 4],
                       help="复杂度级别（默认：1）")
    parser.add_argument("--path", type=Path, default=Path.cwd(),
                       help="输出目录（默认：当前目录）")

    args = parser.parse_args()
    create_agent(args.name, args.level, args.path)


if __name__ == "__main__":
    main()
