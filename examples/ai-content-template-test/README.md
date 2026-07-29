# AI 内容模板复用测试

用一段虚构口播稿测试 6 类参数化视频贴纸。内容与数据均为演示，不代表真实业务结果。

## 目录

```text
ai-content-template-test/
├── README.md
├── mock-script.md
├── assets/
│   ├── mock-template-guide.svg
│   └── mock-template-library.svg
└── configs/
    ├── 01-evidence-card.json
    ├── 02-timeline.json
    ├── 03-webpage-scroll.json
    ├── 04-question.json
    ├── 05-comparison.json
    └── 06-cta.json
```

每个配置文件对应 `assets/templates/<类型>/template.html`。复制模板为项目 `index.html`，再用对应配置渲染。
