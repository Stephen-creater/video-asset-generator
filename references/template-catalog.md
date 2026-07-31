# 参数化模板

| 模板 | 适用内容 | 不适用 |
| --- | --- | --- |
| `evidence-card` | 播客封面、人物、产品、历史图片等真实证据 | 无可靠来源的概念图 |
| `timeline` | 三个有先后或因果关系的节点 | 无顺序的并列观点 |
| `webpage-scroll` | 已核验的官方文章、产品页、技术博客 | 搜索结果页、来源不明截图 |
| `question` | 问句、设问、核心矛盾 | 普通陈述句 |
| `comparison` | 两种方案、前后状态、优劣差异 | 三项以上复杂比较 |
| `cta` | 结尾互动、关注、评论钩子 | 中段信息解释 |
| `multi-node-path` | 四个有顺序的流程、路径或审批节点 | 无顺序的并列观点 |
| `resource-bottleneck` | 上游资源集中流向一处，三个下游同时承压 | 没有明确资源流向的普通因果 |
| `price-evidence` | 两项产品、版本或时间点的旧值与新值 | 来源不明或不可核验的数据 |
| `dilemma-balance` | 两种选择各自带来明确代价 | 可以直接判断优劣的普通对比 |
| `three-metric-proof` | 一个核心指标和两个辅助指标共同证明判断 | 指标之间没有共同结论 |
| `new-player-table` | 三个原有参与者与一个新进入者 | 普通四项并列清单 |
| `document-stack` | 报告、白皮书、研究材料及其页数与覆盖范围 | 需要展示真实原文证据的内容 |
| `lock-in-risk` | 路径依赖、技术债、组织惯性与生态锁定 | 普通风险提醒 |
| `priority-pillars` | 三项有明确高低顺序的战略优先级 | 无法排序的并列事项 |
| `acceptance-gate` | 多项条件共同决定方案是否通过验收 | 只有单一判断条件 |
| `ecosystem-hub` | 一个核心平台连接四类依赖或能力 | 没有中心节点的普通并列关系 |
| `translation-layer` | 一个中间层把统一输入适配到三种底层 | 普通三步线性流程 |
| `knowledge-transfer` | 个人经验经 AI 或系统沉淀为多种组织能力 | 单纯的人物介绍 |

每个目录包含：

- `template.html`：稳定布局、字体路径和动画；
- `example.json`：可替换参数；`evidence-card/archive-example.json` 是历史图片变体。

使用时：

1. 将目标 `template.html` 复制为素材项目的 `index.html`。
2. 将 `example.json` 复制为 `config.json`，只改参数值。
3. 将字体放入 `assets/fonts/`，图片放入 `assets/images/`，固定版本的 `gsap.min.js` 放入 `assets/`。
4. 运行预检和 HyperFrames 检查。
5. 用户确认预览后渲染：

```bash
hyperframes render . --variables-file config.json --strict-variables --strict-all --quality high --output renders/sticker.mp4
```

配置中的素材路径相对于 `index.html`。不要把客户素材、字体或案例文案写回模板。
