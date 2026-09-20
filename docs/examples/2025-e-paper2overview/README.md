# From Forest to Farm · 2025 ICM E

[English](README.en.md) · [全部成图](../../../README.md#showcase)

森林氮循环 → 农业管理 → 七类生物食物网。以农田、根系与土壤氮库为主体，右侧区分模型情景与讨论建议。

## 原图与当前成图

| 论文作者原图 · Figure 2, PDF p4 | ModelAtlas · 场景式总览 |
| :---: | :---: |
| [![论文原图](../../assets/reference-overviews/2025-e-2515324-overview.jpg)](../../assets/reference-overviews/2025-e-2515324-overview.jpg) | [![当前生成图](overview.png)](overview.png) |

[完整 prompt](full-prompt.md) · [论文依据与图注](brief.json) · [文件校验](integrity-audit.json)

## 来源与设计

论文：*From Forest to Farm: Modeling Nitrogen Dynamics for Sustainable Agriculture*。2025 ICM E，Team 2515324，Finalist。

[作者仓库](https://github.com/LUKEQ420/MCM-ICM-2025-E-Nitrogen-Cycling-Model) · [固定版本论文](https://github.com/LUKEQ420/MCM-ICM-2025-E-Nitrogen-Cycling-Model/blob/fb579acd7107706e055c8a10f921f9f56498a06a/paper/2515324.pdf) · [COMAP 结果](https://www.contest.comap.com/undergraduate/contests/mcm/contests/2025/results/2025_ICM_Problem_E_Results.pdf)（物理第 6 页）。

重读全文 25 页，并查看第 4、6、7、13、16、17、18、21、23 页的原图与公式。借鉴 Sivia 的对象细节和局部操作表达，不借入无关科研机制。完整设计 prompt 为 31,816 字符，随后进行了两次局部编辑。

这是已知参考论文的重设计，不是盲测或数值实验复现。根瘤菌、草蛉与秸秆利用仍属于讨论建议；原文摄取项的符号歧义及逐页依据保留在 brief 中。源 PDF 和页面渲染不发布。

## 展示确认与待修项

用户于 **2026-09-21** 确认“这个很不错,可以推送”。此确认用于项目展示，不把科学审查状态 `needs_revision` 改为通过，也不将此图加入来源知识库。

- 蝙蝠到蛇的长连线仍贴近鸟，鸟到蛇的独立路径不够清楚。
- 施肥的“作物存在时启用”条件括号与另外两行断开。
- 森林小图局部颜色语义需统一；草叶为环境示意，不是额外状态。

输出为 **1536 × 1024 PNG**，非原生可编辑矢量。未进行独立审稿或实际印刷尺寸校样，不标为论文终稿。文件校验不替代科学与视觉审查。

## 记录

README 仅显示当前图。历史输出保存在 [初版](overview-v1.png)、[上一版](overview-v2.png)、[场景初稿](overview-scene-v1.png) 和 [第一次修正](overview-scene-v2.png)。

[完整调用记录](full-prompt.md) 保留五次调用；[精确提交文本](scene-prompt-records.json) 和 [模板检查](scene-prompt-check.json) 对应本次三次调用。[历史 brief](brief-before-scene.json) 保留旧版记录，当前图注与审查见 [brief.json](brief.json)。

奖项与研究主张属于来源论文作者，不表示作者背书。[原图署名与 MIT 许可](../../assets/reference-overviews/README.md)。
