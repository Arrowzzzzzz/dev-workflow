#!/usr/bin/env python3
"""dev-workflow 可选辅助脚本：config.yaml → 快照类适配器文件（dsh / codex）。

用途（见 references/agents.md 第五节「5.6 自动同步」）：
    解析项目 .devflow/agents/config.yaml 的 models.<角色>.<工具> 映射，
    幂等重生成两份快照类落点文件（允许整体重写）：
      .devflow/agents/adapters/dsh-subagents.yaml
      .devflow/agents/adapters/codex-agents.json
    不触碰 zcode / opencode / cc 等工具的活跃配置——那些由执行 AI 按 5.6 指令同步。

用法：
    python3 sync.py [项目根目录]     # 缺省为当前目录
    python3 sync.py --check          # 只校验一致性，不写文件（退出码 1 = 有差异）

说明：
    - 零第三方依赖；仅解析本技能模板产出的简单结构（models.<role>: 或 <role>: {}）；
    - 未配置（留空 "" / inherit）的角色不输出 model 键 = 跟随主会话默认模型；
    - 生成的文件带标记头，可整体重生成，请勿手改。
"""

import json
import re
import sys
from pathlib import Path

ROLES = {
    "frontend": "前端 UI 角色：页面/组件/状态管理/样式/交互",
    "backend": "后端开发角色：接口/业务逻辑/服务层",
    "database": "数据库 DBA 角色：表结构/索引/迁移/SQL 优化",
    "qa": "测试 QA 角色：测试策略/用例设计/执行",
    "architect": "架构师角色：系统设计/方案评审/技术选型",
    "devops": "DevOps 运维角色：部署/CI-CD/监控/环境配置",
    "security": "安全角色：安全审查/安全编码",
    "product": "产品角色：需求澄清/验收标准/方向",
}
TOOLS = ("zcode", "opencode", "dsh", "codex", "cc")
GENERATED_MARK = "<!-- 由 dev-workflow assets/adapters/sync.py 自动生成 —— 请勿手改；源头：.devflow/agents/config.yaml -->"

ROLE_LINE = re.compile(r"^ {2}([a-z]+):\s*(\{\})?\s*(#.*)?$")
TOOL_LINE = re.compile(r"^ {4}([a-z]+):\s*\"?([^\"#]*?)\"?\s*(#.*)?$")


def parse_config(path):
    """解析 models.<角色>.<工具>，返回 {role: {tool: value}}；未列出的键视为空。"""
    mapping = {role: dict.fromkeys(TOOLS, "") for role in ROLES}
    current = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].rstrip() if not raw.lstrip().startswith("#") else ""
        if not line.strip():
            continue
        m = ROLE_LINE.match(line)
        if m:
            role, inline_empty = m.group(1), m.group(2)
            if role not in mapping:
                raise SystemExit(f"错误：config.yaml 出现未知角色 '{role}'（已知：{', '.join(ROLES)}）")
            current = role if not inline_empty else None
            continue
        m = TOOL_LINE.match(line)
        if m and current:
            tool, value = m.group(1), m.group(2).strip()
            if tool in TOOLS:
                mapping[current][tool] = "" if value == "inherit" else value
    return mapping


def render_dsh(mapping):
    lines = ["# dsh subagent 描述符（快照）", GENERATED_MARK.replace("<!--", "#").replace("-->", ""),
             "# provider 取值见 dsh LLM adapter 注册表文档；未配 model = 主会话默认。", "", "subagents:"]
    for role, desc in ROLES.items():
        lines += [
            f"  {role}:",
            f"    description: {desc}",
            f"    persona: 先读项目 .devflow/agents/{role}.md（角色知识库）再执行任务",
            "    agentOptions:",
            "      provider: spawn",
        ]
        model = mapping[role]["dsh"]
        if model:
            lines.append(f"      model: {model}")
        lines += ["    toolFilter: []", ""]
    return "\n".join(lines).rstrip() + "\n"


def render_codex(mapping):
    agents = {}
    for role, desc in ROLES.items():
        entry = {"description": desc,
                 "instructions": f"先读项目 .devflow/agents/{role}.md（角色知识库）再执行任务"}
        if mapping[role]["codex"]:
            entry["model"] = mapping[role]["codex"]
        agents[role] = entry
    doc = {"$comment": GENERATED_MARK.replace("<!--", "[").replace("-->", "]"),
           "agents": agents}
    return json.dumps(doc, ensure_ascii=False, indent=2) + "\n"


def main(argv):
    check_only = "--check" in argv
    roots = [a for a in argv if not a.startswith("-")]
    root = Path(roots[0]) if roots else Path.cwd()
    config = root / ".devflow" / "agents" / "config.yaml"
    if not config.is_file():
        raise SystemExit(f"错误：未找到 {config}（先按 assets/agent-config-template.yaml 生成，"
                         "或由 dev-workflow 技能调用时自动生成）")

    mapping = parse_config(config)
    targets = {"dsh-subagents.yaml": render_dsh(mapping),
               "codex-agents.json": render_codex(mapping)}
    changed = []
    for name, content in targets.items():
        target = root / ".devflow" / "agents" / "adapters" / name
        if target.is_file() and target.read_text(encoding="utf-8") == content:
            continue
        changed.append(target)
        if not check_only:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")

    verb = "待更新（--check 未写入）" if check_only else "已写入"
    for t in changed:
        print(f"{verb}: {t}")
    print("快照与 config.yaml 一致。" if not changed else
          f"共 {len(changed)} 个快照{'需' if check_only else '已'}同步。")
    if check_only and changed:
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
