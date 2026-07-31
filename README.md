# Video Asset Generator Skill

面向口播、文章、课程和解说视频的视觉素材导演 Skill。它帮助 AI 在动态图形、AI 生图、图文融合、真实素材和混合形式之间做选择，并把字体授权、移动端安全区、动画稳定性、批量渲染和最终成片抽帧验收设为明确的质量闸门。

仓库同时提供可直接加载的 Skill 源文件和 `.skill` 安装包。

## 它能做什么

- 为长短视频建立素材地图与视觉节奏，而不是逐句生成“会动的 PPT”
- 在动态图形、电影感生图、图文融合、真实素材之间选择合适媒介
- 规划关键词、章节标题、金句和字幕之间的分工
- 约束 1080×1920 竖屏安全区、文字容器、对比结构和动画时序
- 指导 HyperFrames / GSAP 的确定性实现、分段渲染与抽帧验收
- 提供证据、流程、瓶颈、价格、两难、指标、市场格局等 12 类参数化模板
- 预检中文字体、危险定位、随机动画和本地绝对路径
- 计算中英文口播时间并生成 SRT
- 将 VTT、ASS/SSA 和常见纯文本时间戳转换为 SRT

## 目录结构

```text
video-asset-generator/
├── AGENTS.md -> CLAUDE.md
├── CLAUDE.md
├── README.md
├── SKILL.md
├── checksums.txt
├── assets/
│   └── templates/
│       ├── comparison/
│       ├── cta/
│       ├── dilemma-balance/
│       ├── evidence-card/
│       ├── multi-node-path/
│       ├── new-player-table/
│       ├── price-evidence/
│       ├── question/
│       ├── resource-bottleneck/
│       ├── three-metric-proof/
│       ├── timeline/
│       └── webpage-scroll/
├── dist/
│   └── video-asset-generator.skill
├── examples/
│   └── ai-content-template-test/
├── references/
│   ├── hyperframes-rules.md
│   ├── quality-gates.md
│   ├── template-catalog.md
│   └── visual-playbook.md
└── scripts/
    ├── calc_timing.py
    ├── preflight.py
    └── srt_convert.py
```

| 路径 | 作用 |
| --- | --- |
| `SKILL.md` | Skill 主入口，定义完整工作流、选择标准和交付要求 |
| `references/visual-playbook.md` | 传播任务、媒介选择、构图与生图提示词手册 |
| `references/hyperframes-rules.md` | HyperFrames / GSAP 实现约束 |
| `references/quality-gates.md` | 渲染前、构图、动画、技术和分发验收表 |
| `references/template-catalog.md` | 12 类模板的适用边界与使用流程 |
| `assets/templates/` | 参数化 HTML 模板和示例 JSON |
| `scripts/preflight.py` | 扫描字体与常见布局、确定性风险 |
| `scripts/calc_timing.py` | 根据中英文文本估算时长并生成 SRT |
| `scripts/srt_convert.py` | 将 VTT、ASS/SSA、纯文本时间戳转换为 SRT |
| `dist/video-asset-generator.skill` | 当前源码生成的可分发安装包 |

## 安装

### 方式一：从 GitHub 克隆到 Codex Skills

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/Stephen-creater/video-asset-generator.git \
  ~/.codex/skills/video-asset-generator
```

若目标目录已经存在，请先确认其中是否有需要保留的本地修改，不要直接覆盖。

### 方式二：安装 `.skill` 包

下载 [`dist/video-asset-generator.skill`](dist/video-asset-generator.skill)，使用支持 `.skill` 包的客户端导入。该文件是 ZIP 格式，解包后的核心目录为：

```text
video-asset-generator/
├── SKILL.md
├── assets/
│   └── templates/
├── references/
└── scripts/
```

安装后重启或刷新客户端，让 Skill 列表重新加载。

## 使用

在支持 Skills 的 AI 客户端中提出类似请求：

```text
请使用 video-asset-generator，为这段 10 分钟口播建立竖屏素材地图，
给出每个插入点的传播任务、媒介、文字策略和主动作。
```

```text
请使用 video-asset-generator，为这段字幕规划 HyperFrames 动态素材，
先做字体预检，再按质量闸门验收最终 MP4。
```

Skill 会先检查字体。含中文文字的最终成片默认要求项目内存在并自托管阿里巴巴普惠体；找不到时会阻断含字最终渲染。字体能用于成片不代表允许随 Skill 再分发，本仓库不包含任何字体文件。

### 参数化模板

复制一个模板目录中的 `template.html` 为项目 `index.html`，复制 `example.json` 为 `config.json`，替换文字和素材路径：

```bash
npx hyperframes render . \
  --variables-file config.json \
  --strict-variables \
  --strict-all \
  --quality high \
  --output renders/sticker.mp4
```

模板不包含字体、GSAP 或业务素材；项目必须提供 `assets/fonts/`、固定版本的 `assets/gsap.min.js` 和需要的 `assets/images/`。

复用示例见 [`examples/ai-content-template-test/`](examples/ai-content-template-test/)。

## 工具脚本

要求 Python 3.9 或更高版本，脚本仅使用 Python 标准库。

### 项目预检

```bash
python3 scripts/preflight.py /path/to/video-project
```

它会检查：

- 中文内容是否同时存在本地普惠体文件和对应 CSS 声明
- 未批准的系统字体回退
- `translate(-50%)`、GSAP `xPercent/yPercent`
- `Math.random()` 和常见本地绝对路径

预检是保守的静态检查，不能证明字体授权，也不能替代最终 MP4 的视觉验收。

### 文本生成 SRT

```bash
python3 scripts/calc_timing.py input.txt -o output.srt
```

可选参数：

```text
--cps    中文字/秒，默认 4.5
--wps    英文词/秒，默认 3.0
--gap    段落间隔秒数，默认 0.5
--pause  标点停顿秒数，默认 0.2
```

### 字幕转换

```bash
python3 scripts/srt_convert.py input.vtt -o output.srt
python3 scripts/srt_convert.py input.ass -o output.srt
python3 scripts/srt_convert.py timestamps.txt -o output.srt
```

也可用 `--format vtt|ass|plain|auto` 显式指定输入格式。

## 安全与隐私

发布前已逐文件审查当前版本：

- 不访问网络，不上传数据
- 不读取 SSH、云服务、浏览器或其他凭据
- 不调用 shell、`eval` 或 `exec`
- 不安装第三方依赖
- 不修改系统配置
- 只读取命令行中明确指定的输入；指定 `-o/--output` 时写出 SRT 文件

对陌生项目运行 `preflight.py` 时，它会递归读取该项目内的 HTML、CSS、JS、TS、TSX、JSX 和字体文件名用于静态检查。请只对你有权读取的目录运行。

## 完整性

当前 `.skill` 包的 SHA-256：

```text
e0d986a5c8de0fd45e3cf599d4abb893701f05e4787c2e600e8c96163f189674
```

可运行以下命令核验：

```bash
shasum -a 256 dist/video-asset-generator.skill
```

## 来源与许可说明

当前内容来自用户提供的 `video-asset-generator.skill` 文件。原包未声明作者、版本号或许可证，本仓库没有擅自补充许可证。仓库设为 public 只表示内容可公开查看，不自动授予复制、修改或再分发许可；如需开放给他人复用，请由权利人另行选择并添加合适的许可证。
