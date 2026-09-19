# 插图知识库 · 服务于 Paper → Overview

知识库完整保留。目标是为论文 overview 提供经过读图的视觉组织参考，不是通用作图平台。

## 核心库与扩展库

**award**：官方结果核验的 O/F 美赛论文。**research**：科研论文/预印本，奖项字段为 null。
源数据为 `src/modelatlas/knowledge/corpus.json`：8 篇获奖论文（6 O + 2 F）、18 个图例；
1 篇科研预印本、2 个扩展图例，共 9 篇 / 20 例。均读过实际 PDF 图页，不是20张新生成的图。

按原始年份及 A–F 题号分类，再记录角色、关系/方法标签与迁移类别 problem_targets。
A–F 中文方向只是常见问题的导航；迁移到另一类别不改变来源论文的真实题号或奖项。

[逐图目录](CATALOG.md)列出实际案例 ID、来源、PDF 页码、图号与原创读图分析。

## 读取参考图

```sh
modelatlas styles --problem E
modelatlas styles "循环" --problem E --role mechanism
modelatlas styles --collection research --role all
modelatlas reference e-model-inheritance-overview
```

默认查 overview + award。原有 mechanism、algorithm、data_plot、explanation 图例继续作为
局部表达参考，不提供对应独立绘制功能。检索是过滤后的词项匹配，不是自动深度理解。

取回来源时校验固定 SHA-256 与页数，再渲染指定物理页。必须打开实际页面并读图注和上下文；
返回 page_rendered_not_reviewed 不等于当前 agent 已看图。缓存文件只留在本地。

## 入库证据

论文记录保留年份、题号、队号、官方奖项证明 URL/行或页码、作者源/镜像说明、固定 PDF 版本、
哈希、页数和权利说明。O 是 Outstanding Winner，F 是 Finalist；题目 F 不是奖项。

图例保留物理 PDF 页、图号、构图、可迁移原则、不应移植的科学内容、原图局限及实际读图记录。
物理页码与纸面印刷页码不能混用；版本变化需复核，不能静默重设哈希。
2024 队2413552的作者仓库存在证书和不同论文修订版，本库定位只针对已固定的镜像版本。

科研扩展单独记录出版状态和 DOI/版本；当前 Lei 等 arXiv v1 提供 overview 与 SHAP 配对图参考，
不冒称同行评审期刊文章或已核验获奖论文。

扩库流程：AnySearch 发现 → 读取原文 → 核验官方奖项（核心库）→ 查看图与上下文 →
原创分析/分类 → 固定版本 → 更新 corpus → 测试与实际图页取回验证。

## 与成图记录分开

参考案例是他人论文的读图分析。生产案例必须是本项目实际生成的 overview，
配对完整 prompt、输入论文依据、图注与审查，不能用参考页面或未执行 prompt 充数。

README 按用户要求展示两张有作者 MIT 许可的原始 overview，附来源及完整许可，
见 [展示图记录](../docs/assets/reference-overviews/README.md)。它们不是本项目生成结果。
除此之外，仓库保存元数据与原创分析；PDF、页面缓存和私人论文不自动上传。
旧数值配方卡片/SQLite 接口已从运行时代码删除，已有本地数据库和输出文件未清理。
