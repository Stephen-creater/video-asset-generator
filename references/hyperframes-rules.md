# HyperFrames / GSAP 实现规则

仅在使用 HyperFrames 或 GSAP 时读取。

## 1. 文件与时间线

- 每段使用独立 composition，根节点位于 `<body>` 内并带 `data-composition-id`、尺寸、时长和轨道属性。
- 子段 `data-start="0"`；字幕绝对时间用于剪辑定位，不用于在素材前制造黑屏。
- 子 composition 不用 `<template>` 包裹。
- `window.__timelines[id]` 必须与 composition id 一致。
- 同一轨道上的片段不得时间重叠。
- 依赖脚本只加载一次；先验证当前环境可访问的来源，不把某个 CDN 永久视为可用。

最小结构：

```html
<!doctype html>
<html lang="zh" data-resolution="portrait">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=1080, height=1920" />
  <style>/* @font-face and composition styles */</style>
</head>
<body>
  <div id="root" data-composition-id="seg01" data-start="0"
       data-duration="8" data-width="1080" data-height="1920"
       data-track-index="0">
  </div>
  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    window.__timelines.seg01 = tl;
  </script>
</body>
</html>
```

## 2. 定位与 transform

- 关键文字使用明确的静态 `left/top/width`；不要依赖 `left:50%` + `translate(-50%)`、`xPercent` 或 `yPercent` 居中。
- 固定尺寸图形直接计算左上角；响应式网页式布局不适合固定画布渲染。
- CSS 负责基础布局，GSAP 负责相对位移、透明度、缩放和旋转。不要让两者同时覆盖同一元素的 transform。
- 图片镜头运动与文字分元素实现。不要缩放包含文字的共同父节点。
- 动画目标使用稳定 class/id，不依赖 `nth-of-type`。

## 3. 确定性

- 禁止 `Math.random()`；使用固定数组或基于索引的确定性函数。
- 避免同一元素同一属性的 tween 时间重叠。
- 不用运行时 DOM 尺寸抖动决定关键位置；能预计算就预计算。
- 复杂粒子数量保持克制，优先保证渲染稳定和编码速度。

## 4. 字体实现

```css
@font-face {
  font-family: 'Project Chinese';
  src: url('../assets/fonts/approved-regular.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
}
```

- 实际项目中把 `Project Chinese` 换成已确认字体家族；默认优先阿里巴巴普惠体。
- 不声明不存在的字重，不依赖浏览器伪粗体。
- 字体文件使用相对路径。确认授权允许随成片项目交付后才能打包字体。
- 任何字体替换都会改变字宽，替换后重新抽帧检查。

## 5. 动画时序

- SRT/实际音频是时序真相源。
- 元素出现顺序与口播提及顺序一致；背景可提前建立，结论不得剧透。
- 入场通常在口播点到前约 0.2–0.4 秒启动，并在对应语句结束前完成；按实际语速调整。
- 独立候选素材没有精确音频时，把关键动作设计成容易在剪辑中对齐的清晰节拍点。
- 不要让所有元素在前 1 秒同时出现，也不要只做统一淡入淡出。

## 6. 运动模式

- 空间让位：前项移开，为后项腾出位置。
- 共同基线：对比值从同一位置增长。
- 碰撞/合并：两个来源生成一个结果。
- 原位变形：旧状态在相同空间转化为新状态。
- 路径流动：数据沿真实关系路径移动。
- 回流闭环：输出返回输入端。
- 镜头推进：用纵深揭示规模，文字保持独立稳定。

每段选择一个主模式即可。动画不是模式清单的堆叠。

## 7. 运行顺序

```powershell
python 'scripts/preflight.py' '<素材项目目录>'
npx hyperframes lint
npx hyperframes render -c 'compositions/seg01.html' -o 'renders/seg01.mp4' -q high --strict-all
```

若实际 CLI 版本参数不同，先查看本地帮助，不照抄旧命令。

## 8. 常见致命问题

- timeline 未注册：检查根节点结构、id 和脚本执行位置。
- 文字整体偏右：检查百分比居中是否被 GSAP transform 覆盖。
- 文字在画布内但越过边框：检查容器内宽度与 padding。
- 圆环盖字：检查层级、遮罩和文字 z-index。
- 英文最后一个字母越界：按实际字体原尺寸检查，不靠中文等宽估算。
- 顶部内容被 UI 遮挡：只移动稳定停驻状态；允许入退场轨迹短暂穿越顶部。
- FFmpeg 异常：减少并发、单视频抽帧、限制线程，避免超大多输入滤镜图。
