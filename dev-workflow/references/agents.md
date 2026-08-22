# 角色 Agent 体系手册（按职责分工与协作）

> 本手册在总纲（SKILL.md）底线之上执行。机制：本技能按项目人员职责定义 8 个角色；场景判定后，实施与沟通阶段按任务性质分配执行角色；**需求实现与修改代码之前，相关角色必须完成「跨角色沟通评审」**。角色知识库存于项目 `.devflow/agents/`（生成 / 更新流程见 agent-knowledge-template.md），模型配置见 `.devflow/agents/config.yaml`（未配置则使用当前 HARNESS 平台默认模型）。

## 一、角色定义表

| 角色 | 职责 | 适用任务 | 知识文件 | 配置键 |
|---|---|---|---|---|
| 前端 UI | 页面 / 组件 / 状态管理 / 样式 / 交互 | 前端页面与交互实现、样式调整 | `frontend.md` | `models.frontend` |
| 后端开发 | 接口 / 业务逻辑 / 服务层 | 后端接口与业务实现 | `backend.md` | `models.backend` |
| 数据库 DBA | 表结构 / 索引 / 迁移 / SQL 优化 | 数据模型与迁移变更 | `database.md` | `models.database` |
| 测试 QA | 测试策略 / 用例设计 / 执行 | 测试设计、自动化用例、回归验证 | `qa.md` | `models.qa` |
| 架构师 | 系统设计 / 方案评审 / 技术选型 | 架构决策、跨模块方案评审 | `architect.md` | `models.architect` |
| DevOps 运维 | 部署 / CI-CD / 监控 / 环境配置 | 部署配置、流水线、环境变更 | `devops.md` | `models.devops` |
| 安全 | 安全审查 / 安全编码 | 安全相关改动与审查 | `security.md` | `models.security` |
| 产品 | 需求澄清 / 验收标准 / 方向 | 需求边界、验收口径 | `product.md` | `models.product` |

## 二、角色路由

- 场景判定后，按任务性质分配**执行角色**；一个任务可涉及多个角色（如"加一个查询接口 + 前端列表页"涉及 后端开发 + 前端 UI + 测试 QA）；
- 执行角色加载自身知识文件（`.devflow/agents/<role>.md`），按角色知识约束编码 / 做事；知识缺失或过期先更新再动手（见 agent-knowledge-template.md）；
- **跨角色边界不越界**：前端不擅改后端接口契约、后端不擅改表结构——越界先切换角色、按对应角色知识执行，并在协作纪要中说明；
- **模型声明**：执行某角色任务前检查 `.devflow/agents/config.yaml`——已配置模型则任务声明注明"以 X 角色、模型 Y 执行"；未配置则声明"以 X 角色、平台默认模型执行"（实际模型切换由运行平台按声明执行，本技能只输出声明）。

## 三、跨角色沟通评审（需求实现与修改代码之前，强制执行）

**触发时机**：场景 A 阶段 3 方案输出后（阶段 3.5）；场景 B 第 3 步修复方案输出后；场景 C 确认修复清单后按问题归属执行。

**步骤**：

1. **判定受影响角色**：由方案改动范围判定（涉及前端文件 → 前端 UI；涉及接口契约 → 前端 + 后端；涉及表结构 → DBA + 后端；涉及部署配置 → DevOps；依此类推）；
2. **各角色依次发言**：每个角色加载自身知识库，按关注点矩阵输出评审意见：

| 角色 | 关注点 |
|---|---|
| 前端 UI | 接口契约字段是否够用、交互状态、组件复用、样式规范 |
| 后端开发 | 业务边界、异常路径、幂等、错误码 |
| 数据库 DBA | 表结构、索引、迁移脚本、数据兼容 |
| 测试 QA | 可测性、测试点、回归范围 |
| 架构师 | 与整体架构一致性、技术选型、演进方向 |
| DevOps 运维 | 部署、配置、监控、回滚 |
| 安全 | 注入、越权、敏感信息、审计 |
| 产品 | 需求边界、验收标准 |

3. **汇总协作纪要**：各角色意见（同意 / 建议 / 异议）+ 角色间分歧点 + 推荐裁决（列出各方理由）；
4. **随方案提交用户确认**：协作纪要与实现方案一并提交；用户裁决分歧后，按裁决更新方案再进入确认闸门；
5. 跨角色沟通中的共识（接口契约、数据结构、测试点）写入方案的「待确认项 / 契约」部分，执行阶段以契约衔接，不口头假设。

## 四、执行与协作纪律

- 执行阶段按确认后的方案与协作纪要执行；发现需超出本角色边界时，补一轮轻量跨角色沟通（只补受影响角色意见）；
- 完成后由执行角色输出完成报告，测试 QA 角色确认回归门禁执行情况（回归测试硬门禁不变，见总纲第 6 条）；
- 角色知识文件与交接文档、图表一样纳入保鲜联动（变更后增量更新，见 agent-knowledge-template.md 第三节）。

## 五、工具适配器（跨工具模型路由）

> config.yaml 是单一真相源；本技能运行时按当前工具选择适配器，把角色→模型映射
> 转成该工具能消费的配置，并在派发子任务时注入角色段（知识 + 模型声明）。
> 所有工具都会执行 prompt——prompt 注入是所有工具的通用通道；工具级配置实现"真切换"。

### 5.1 五工具子任务模型能力（官方文档确认，2026-08）

| 工具 | 子任务换模型 | 机制落点 |
|---|---|---|
| zcode | ✅ | `~/.zcode/agents/<role>.md` frontmatter `model` |
| opencode | ✅ | `opencode.json` 的 `"agent"` 段（agent 级 model 覆盖全局） |
| dsh | ✅ | subagent 描述符 `agentOptions.provider/model`（LLM adapter 注册表；含 spawn/fork/acp/codex/claude-code 提供方） |
| codex | ✅ | Codex agent 配置（per-agent model） |
| cc | ✅（实验性） | agent teams：提示指定模型 / /config 默认队友模型 / subagent 定义 `model` 字段（需 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 启用） |

### 5.2 适配器生成规则

派发子任务前：

1. 检测当前工具（环境/平台标识；无法检测时默认走 prompt 注入通道）；
2. 查 `config.yaml` 的 `models.<role>.<tool>` → 模型值；
3. 生成/使用对应工具配置（见 5.3 落点表）；**配置已存在则复用，缺失则按本规则生成**；
4. 子任务 prompt 头部**固定注入角色段**：

```
【角色】frontend
【知识】先读 .devflow/agents/frontend.md（角色知识库）
【模型】该角色在本工具（opencode）应使用 opencode-go/deepseek-v4-flash-vision-exp；
        若本工具不支持切换则使用当前默认模型并说明
```

### 5.3 各工具配置落点

| 工具 | 配置文件 | 生成内容 |
|---|---|---|
| zcode | `~/.zcode/agents/<role>.md` | frontmatter：`name`/`description`/`model`/`tools`；正文=角色知识摘要 + 指向 `.devflow/agents/<role>.md` |
| opencode | `opencode.json` 的 `agent` 段 | `"agent": { "<role>": { "model": "..." } }`（agent 级 model 覆盖全局） |
| dsh | `.devflow/agents/adapters/dsh-subagents.yaml`（模板） | subagent 描述符模板：provider/model 快照说明 |
| codex | `.devflow/agents/adapters/codex-agents.json`（模板） | per-agent model 配置模板 |
| cc | 项目 `.claude/agents/<role>.md` | frontmatter：`name`/`description`/`model`/`tools`；正文=角色知识；附 agent teams 提示模板（Spawn teammate using <role> type, use <model>） |

各工具生成模板见 `assets/adapters/`（zcode / opencode / cc / dsh / codex）。

### 5.4 降级规则

- 工具不支持某角色切换（如 cc 未启用 agent teams）→ prompt 注明"本工具单模型/未启用，使用当前默认模型，角色知识已注入"；
- config.yaml 未配置某角色某工具 → `inherit`/默认（跟随主会话模型）；
- 无法检测工具 → 仅 prompt 注入通道（声明 + 知识，模型用默认）。

### 5.5 配置示例（写进 config.yaml 供后配置者参考）

见 `.devflow/agents/config.yaml` 注释示例（模板：`assets/agent-config-template.yaml`）。

## 自检清单

- [ ] 已按任务性质分配执行角色，并加载对应角色知识文件
- [ ] 跨角色沟通评审已在实施前完成，协作纪要随方案提交用户确认
- [ ] 跨角色边界未越界；越界已切换角色并说明
- [ ] 已按 config.yaml 声明角色与模型（未配置声明平台默认）
- [ ] 角色知识文件已按保鲜联动增量更新
- [ ] 已按当前工具选择适配器生成/复用角色配置（zcode/opencode/dsh/codex/cc）
- [ ] 子任务 prompt 已注入角色段（角色 + 知识路径 + 模型声明）
- [ ] 工具不支持切换时已注明降级（默认模型 + 知识注入）
- [ ] config.yaml 分工具映射与各工具实际配置一致（保鲜联动）
