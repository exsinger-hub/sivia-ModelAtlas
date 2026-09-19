# ModelAtlas 知识库

## 两个主集合

**award 核心库**：官方结果验证的 O／F 美赛论文，逐页读图。
**research 扩展库**：科研论文/预印本的有效图形表达，奖项字段为 null。
检索默认只查 award；使用 research 或 all 显式扩展。普通检索结果不在这两个已审阅集合中。

源数据是 `src/modelatlas/knowledge/corpus.json`。目前 9 篇论文、20 个图例：
8 篇获奖论文（6 O + 2 F）、18 个图例；1 篇科研预印本、2 个图例。
全部图例实际查看过对应 PDF 图页；不代表为当前用户完成了20张新图。

## 分类与检索

先按原始 A–F 题号分库，保留年份和题目；再按图形角色、方法/关系标签以及 problem_targets 检索。
problem_targets 是编辑判断的迁移适用性，不会改变来源论文的真实类别。
A–F 的中文方向是常见任务的导航简介，不是永久官方题目定义。

角色：overview（总览）、mechanism（机制）、algorithm（算法）、
data_plot（数值图）、explanation（模型解释）。统计覆盖同时报告原题图例与可迁移图例，避免混算。

```sh
modelatlas coverage
modelatlas styles --problem E --role overview
modelatlas styles "feedback" --collection all
modelatlas reference d-control-feedback
```

检索为过滤后透明词项匹配，不是向量数据库或自动深度理解。
[逐图目录](CATALOG.md)给出每个可取回案例的 ID 和具体图号。

## 每条证据链

论文记录：题目、年份、队号、原题号、奖项、官方核奖 URL/定位、论文来源、固定版本和 SHA-256、
物理页数、版权说明。镜像明确标成镜像，科研论文保留发表状态。

图例记录：paper_id、物理 PDF 页码、图号、角色、标签、迁移类别、实际读图记录、原创构图分析、
可借鉴内容、不能迁移的模型/结论和源图局限。O/F 标签不意味着图形质量完美。

下载时验证哈希和页数，再用 Poppler 渲染指定页。原文更换版本会失败，需人工/agent 复核后更新。
真实发现过版本陷阱：2024 队2413552的作者仓库里，按队号命名的文件是证书；
另一论文修订版的队号/图号和图页不同。本库使用核对过的固定镜像，不能混用定位。

## 扩库流程

AnySearch 检索 → 取原文 → 核对官方奖项（仅核心库）→ 读图/图注/上下文 → 原创分析 →
分类/固定版本 → 更新 corpus → 运行测试和 coverage → 实际取回图页校验。

当前研究扩展为 Lei 等 arXiv v1 的 overview 与 SHAP 配对图。仅描述可迁移的视觉组织；
预印本不是已同行评审的期刊论文，也没有经验证的获奖身份。后续生态、网络、政策研究可继续加入，
但不能把未阅读的链接提前算成案例。

## 与旧卡片和生产案例的区别

sources.json / cards.json 及 SQLite 保留一般来源、早期数值绘图建议、搜索发现、导入文本和运行记录。
`atlas_add_card` 只写普通卡片，不跳过核奖/读图进入 corpus。

草稿会话在 .modelatlas/drafts；参考 PDF/图页在 .modelatlas/references。实际成图经 pair-overview
保存为图像 + 完整 prompt + 草稿依据 + 图注/放置建议 + review + hashes。
参考图、原创生产图、demo 测试图和未执行 prompt 不混称“成图案例”。

只提交元数据和原创分析。第三方原文/图像、私人草稿、数据及 API 密钥不随 Git 分发。
