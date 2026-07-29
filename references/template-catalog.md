# 参数化模板

| 模板 | 适用内容 | 不适用 |
| --- | --- | --- |
| `evidence-card` | 播客封面、人物、产品、历史图片等真实证据 | 无可靠来源的概念图 |
| `timeline` | 三个有先后或因果关系的节点 | 无顺序的并列观点 |
| `webpage-scroll` | 已核验的官方文章、产品页、技术博客 | 搜索结果页、来源不明截图 |
| `question` | 问句、设问、核心矛盾 | 普通陈述句 |
| `comparison` | 两种方案、前后状态、优劣差异 | 三项以上复杂比较 |
| `cta` | 结尾互动、关注、评论钩子 | 中段信息解释 |

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
