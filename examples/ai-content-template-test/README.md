# AI 内容模板复用测试

用一段虚构口播稿测试 6 类参数化视频贴纸。内容与数据均为演示，不代表真实业务结果。

网页滚动素材来自 Anthropic Research 2026-07-06 文章：[A global workspace in language models](https://www.anthropic.com/research/global-workspace)。

## 目录

```text
ai-content-template-test/
├── README.md
├── mock-script.md
├── assets/
│   ├── anthropic-global-workspace-2026-07-06.png
│   └── mock-template-library.svg
├── configs/
│   ├── 01-evidence-card.json
│   ├── 02-timeline.json
│   ├── 03-webpage-scroll.json
│   ├── 04-question.json
│   ├── 05-comparison.json
│   └── 06-cta.json
└── renders/
    ├── 01-evidence-card.mp4
    ├── 02-three-step-timeline.mp4
    ├── 03-anthropic-memory-article-scroll.mp4
    ├── 04-reuse-question.mp4
    ├── 05-production-method-comparison.mp4
    └── 06-template-test-cta.mp4
```

每个配置文件对应 `assets/templates/<类型>/template.html`。复制模板为项目 `index.html`，再用对应配置渲染。
