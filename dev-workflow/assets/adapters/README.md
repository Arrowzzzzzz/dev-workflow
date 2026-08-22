# 跨工具适配器模板（角色模型路由）

按 `references/agents.md` 第五节（工具适配器）的生成规则使用本目录模板：

- **模型值取自项目 `.devflow/agents/config.yaml` 的 `models.<角色>.<工具>`**；未配置（`""` / `inherit`）→ 使用 `model: inherit` 或不写 model，跟随主会话模型；
- 生成前先检测目标配置是否已存在——已存在则复用，缺失才生成。

## 自动同步（agents.md 5.6）

config.yaml 变更后**不会**被各工具原生配置自动感知；同步由执行 AI 在运行时按 5.6 指令自动完成：

| 模板文件 | 目标工具 | 落点 | 同步方式 |
|---|---|---|---|
| `zcode-agent-template.md` | zcode | `~/.zcode/agents/<role>.md`（用户级） | AI 比对并重生成对应角色段；写不了用户级目录时降级 prompt 注入 |
| `opencode-agent-snippet.json` | opencode | `opencode.json` / `opencode.jsonc` 的 `"agent"` 段 | AI 只增改本技能管理的角色键，保留用户原有注释与配置 |
| `claude-agent-template.md` | cc (Claude Code) | 项目 `.claude/agents/<role>.md` | AI 比对并重生成对应角色段 |
| `dsh-subagents.yaml` | dsh | `.devflow/agents/adapters/dsh-subagents.yaml` | 快照类：允许整体重生成（可用下方脚本） |
| `codex-agents.json` | codex | `.devflow/agents/adapters/codex-agents.json` | 快照类：允许整体重生成（可用下方脚本） |

## 可选辅助脚本 sync.py

只覆盖快照类落点（dsh / codex），零第三方依赖：

```bash
python3 assets/adapters/sync.py [项目根目录]   # 重生成两份快照文件
python3 assets/adapters/sync.py --check        # 只校验一致性，不写入
```

其余工具配置由执行 AI 按 agents.md 5.6 指令同步。同步结果纳入保鲜联动，并在任务声明中注明。
