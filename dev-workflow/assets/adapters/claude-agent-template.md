---
name: <role>
description: <角色名> 角色（agent teams 队友或 subagent 委派）
model: inherit       # 队友遵守该 model（取自 .devflow/agents/config.yaml 的 models.<role>.cc；书写示例 sonnet / opus / haiku）；未配=跟随负责人
tools: Read, Edit, Write, Bash, Glob, Grep, WebFetch
---

角色知识库：项目 `.devflow/agents/<role>.md`（执行前先读）。

职责：<从角色知识文件摘录的职责要点>

执行约定：

- 先读角色知识库，按角色知识约束编码/做事；
- 超出本角色边界时不擅自越界，回报负责人补一轮轻量跨角色沟通。

## agent teams 启用说明

- 启用：`settings.json` 中 `env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`（实验性）；
- 未启用时走 subagent 委派（本文件同一定义可作 subagent），模型声明降级为 prompt 注入；
- 派发示例：`Spawn a teammate using the <role> agent type to <任务描述>, use <model>`。
