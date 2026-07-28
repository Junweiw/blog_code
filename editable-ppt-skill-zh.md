---
title: Editable PPT
category: BestPractice
tags: [pptx, editable-slides, infographic, python-pptx]
difficulty: Medium
created: 2026-07-18
updated: 2026-07-18
---

# Editable PPT

把信息图、海报式视觉稿、或「看起来像成品图」的 slide，做成 **PowerPoint 里真正可编辑** 的 `.pptx`。

## 元数据

- **类型**: BestPractice
- **适用场景**: 需要可改字 / 改色 / 换图 / 挪图标的 PPT，而不是一整张扁平原图
- **互补**: 若只要视觉 deck、不需要对象级编辑，用 `workflow_presentation_slides.md`

## 目标

交付分层的 `.pptx`：用户会改的部分是独立对象。

## 核心原则

1. **信息图是像素；可编辑 PPT 是对象栈。** 先拆再组，不要整图硬贴。
2. **文字 → 文本框；结构色块/圆/卡片 → shape；照片面板 → 独立图片；图标笔画 → 透明 glyph。**
3. **圆底/描边尽量用 PPT shape**，不要烤进图标 PNG；glyph 与圆 group。
4. **图标先预览、确认后再组装整页**，避免为抠图标反复重生 deck。
5. **颜色、字体、行业内容跟当次 brief**，不写死在本 skill 里。

## 对象映射

| 视觉上的东西 | PPT 对象 |
|---|---|
| 标题 / 说明 / 指标文案 | Text box |
| 背景、卡片、分隔条 | Shape |
| 面板图 / 插画 | Picture（一张一图） |
| 图标笔画 | 透明底 monochrome PNG |
| 图标圆底 / 描边 | Oval shape（实心或空心）+ glyph，group |

## 验收

- 目标比例正确（默认 16:9）
- 该改的字是文本框
- 该改色的圆/卡片是 shape
- 该换的图是独立 picture
- 图标无脏底（无方块底、无假棋盘格透明）
- 交付可下载（非仅本机 localhost）

## 已知陷阱

| 陷阱 | 应对 |
|------|------|
| 整图当「可编辑」 | 拆对象重组；整图最多作参考页 |
| 图标带不透明方底 | 抽 glyph-only；圆用 shape |
| 先组 PPT 再抠图标 | 图标预览过了再 assemble |
| 给 Cloud/手机 `127.0.0.1` | 用仓库 raw / artifact 下载链接 |

## 一句话

**拆成文字 / 形状 / 图 / 笔画，确认图标，再组装——永远不要用一张平铺大图冒充可编辑 PPT。**
