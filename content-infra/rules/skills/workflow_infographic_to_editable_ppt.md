---
title: 信息图转可编辑 PPT
category: Workflow
tags: [pptx, infographic, editable-slides, python-pptx, asset-assembly]
difficulty: Medium
created: 2026-07-18
updated: 2026-07-18
---

# 信息图 → 可编辑 PPT

把一张（或一组）信息图 / 海报式视觉稿，转成 **PowerPoint 里可点选、可改字、可换图、可改色** 的 slide(s)。

## 元数据

- **类型**: Workflow
- **适用场景**: 用户给了 AI 生成信息图、设计稿截图、或「看起来像海报」的 slide，要求变成可编辑 `.pptx`
- **不适用**: 只要视觉成品、不需要改字改色时——那种场景用 [`workflow_presentation_slides.md`](./workflow_presentation_slides.md)（整页渲染成图）更合适
- **和 pptx.skill 的关系**: [`pptx.skill`](https://github.com/grapeot/pptx.skill) 负责读写/编辑 PPTX 的工具层；本 skill 负责「怎么拆信息图、怎么组装」的方法层

## 目标

交付一个（或多个）`.pptx`，其中用户真正会改的部分是独立对象，而不是一整张扁平原图。

## 验收标准

一个没有上下文的 agent 也应能判断是否完成：

1. 目标比例正确（默认 16:9，除非 brief 另有说明）
2. 需要改的文案是文本框，不是烤进图片里的字
3. 需要改色的色块 / 圆 / 卡片是原生 shape
4. 需要换图的面板是独立图片对象
5. 图标若需可改色：笔画是透明底 glyph PNG，圆形底/描边是 PPT shape，并已 group
6. 交付物可下载（仓库 raw / artifact URL），不是仅本机 `127.0.0.1`
7. 没有「可替换图片」占位框留在最终交付里

## 核心模型

信息图是像素；可编辑 PPT 是对象栈。

| 信息图上的东西 | PPT 里应该是 |
|---|---|
| 标题 / 说明 / 指标文字 | Text box |
| 背景、卡片、分隔条、色块圆 | Native shape |
| 照片 / 插画面板 | 独立图片文件 |
| 图标笔画 | 透明底 monochrome glyph PNG |
| 图标圆形底 / 描边 | Shape circle（实心或空心），与 glyph group |

**硬边界：不要把「整张信息图贴进一页」当成可编辑交付。**

## 方法论建议（agent 可调整）

### 先拆再组

1. 读原图 / brief，列出对象清单：文字、结构形状、面板图、图标
2. 和用户确认编辑模型：哪些必须可改字、图标要实心圆还是空心描边、一页还是多页
3. 产出离散素材（面板图、glyph 图标）
4. **先单独预览图标**（深底 / 浅底 / 叠在圆上的 mock），等用户点头
5. 再用 `python-pptx`（或等价工具）按图层组装
6. 交付 `.pptx` + 可重跑脚本（若项目会反复生成）

### 图标处理（高价值）

- 优先只要笔画（白或黑），背景真透明
- 圆底 / 描边留给 PPT shape，方便改色
- 不要把棋盘格「假透明」或深蓝方底烤进 PNG
- 图标没确认前，不要反复重做整份 PPT

### 组装顺序（建议）

背景 shape → 分区卡片/顶底栏 → 文本框 → 图标 group → 面板图片

## 输出规格

- 主交付：`.pptx`（文件名尽量 ASCII，方便跨端下载）
- 素材目录（示例，可按项目改名）：

```text
assets/ppt-parts/
  panels/         # 或 heroes/ photos/
  icons-glyph/    # 透明笔画
```

- 可选：`scripts/create_*_ppt*.py` 以便 regenerate

## 已知陷阱（来自真实返工）

| 陷阱 | 表现 | 应对 |
|------|------|------|
| 整图当可编辑 | 用户打不开文字、改不了布局 | 拆对象重组；整图最多当参考页 |
| AI 图标带方底/棋盘格 | 贴在卡片上像嵌了一块脏图 | 抽 glyph-only；圆用 shape |
| 蓝圆烤进 PNG | 改不了圆环颜色 | glyph 与 circle 分层再 group |
| 先组 PPT 再抠图标 | 来回重生整份 deck | 图标预览 gate 过了再 assemble |
| 本地预览 URL 给手机/Cloud | `127.0.0.1` 404 | 推仓库后给 raw/download 链接 |
| 和「整页 AI 渲染」流程混淆 | 用错 skill | 要可编辑 → 本文件；只要视觉 deck → `workflow_presentation_slides.md` |

## 适用边界

不做：

- 代替品牌设计系统（颜色/字体跟当次 brief，不写死在本 skill）
- 保证与某张 AI 海报像素级一致且同时处处可编辑（视觉素材层 + 可编辑结构层分工）
- 替代专业排版软件的精密控字

## 一句话

**把信息图拆成文字 / 形状 / 图 / 笔画，先确认图标，再组装成分层 PPT——永远不要用一张平铺大图冒充可编辑。**
