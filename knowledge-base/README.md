# 插图知识库

为 Paper → Overview 提供构图参考，按原始题号 A–F、年份和图形角色分类。

- 获奖论文：26 篇（23 O、3 F），36 个图例。
- 科研扩展：3 篇，4 个图例；不标美赛奖项。
- 2025 覆盖 A–F；2026 已有 C、D，A/B/E/F 待补。

[逐图目录](CATALOG.md) · [近期来源与缺口](SOURCES.md) · [结构化索引](../src/modelatlas/knowledge/corpus.json)

## 查找与读图

```sh
modelatlas styles --year 2025 --problem A
modelatlas styles --year 2026 --problem D
modelatlas styles "循环" --problem E --role mechanism
modelatlas styles --collection research --role all
modelatlas reference d-wins-to-value-chain
```

默认检索 O/F 库中的 Overview。机制、算法和数据图可作为局部表达参考，不提供独立绘制功能。
`--year` 按原论文年份筛选；题号过滤包含标注为可迁移的参考，来源真实题号不变。
文本匹配分数相同，优先原题号相同的案例，再按年份从新到旧排序。

取回参考时校验 SHA-256 与 PDF 页数，再渲染指定物理页。必须打开图片，核对图注及上下文。
扫描页可以直接读图；返回 `page_rendered_not_reviewed` 不等于当前使用者已审阅。

## 入库要求

每篇论文保存来源 URL、固定版本、SHA-256、页数与权利说明；获奖论文另保留官方 COMAP 队号、题号、奖项及证据位置。
O 为 Outstanding Winner，F 为 Finalist，不与题号 F 混淆。

每个图例记录物理页、图号或未编号位置、构图、适用布局、不可移植内容、原图局限及实际读图记录。
科研参考单列出版状态和版本。参考图只帮助组织表达，当前论文决定科学内容和每条箭头。

来源发现使用 AnySearch；完成原文、奖项与图页核验后才入库。来源内容变化时复核版本，不静默替换哈希。

## 图片与版权

README 展示两张有作者 MIT 许可的原图，见[来源与许可](../docs/assets/reference-overviews/README.md)。
其余来源只保存元数据和原创读图分析；第三方 PDF、水印扫描页和私人稿件不自动上传。

本库参考与[ModelAtlas 实际生成示例](../docs/examples/2025-e-paper2overview/README.md)分开记录。
