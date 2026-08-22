# 跨工具适配器模板（角色模型路由）

按 `references/agents.md` 第五节（工具适配器）的生成规则使用本目录模板：

- 生成前先检测目标配置是否已存在——**已存在则复用，缺失才生成**；
- 模型值取自项目 `.devflow/agents/config.yaml` 的 `models.<角色>.<工具>`；
- 未配置（`""` / `inherit`）→ 使用 `model: inherit` 或不写 model，跟随主会话模型。

| 模板文件 | 目标工具 | 落点 |
|---|---|---|
| `zcode-agent-template.md` | zcode | `~/.zcode/agents/<role>.md`（用户级） |
| `opencode-agent-snippet.json` | opencode | `opencode.json` 的 `"agent"` 段（用户级/项目级） |
| `claude-agent-template.md` | cc (Claude Code) | 项目 `.claude/agents/<role>.md` |
| `dsh-subagents.yaml` | dsh | `.devflow/agents/adapters/dsh-subagents.yaml`（描述符快照） |
| `codex-agents.json` | codex | `.devflow/agents/adapters/codex-agents.json`（描述符快照） |

配置生成后与 config.yaml 一并纳入保鲜联动：角色模型映射变更时同步更新对应工具配置。
