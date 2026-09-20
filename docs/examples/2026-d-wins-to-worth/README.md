# From Wins to Worth · 2026 ICM D

[English](README.en.md) · [全部成图](../../../README.md#showcase)

来源论文: *From Wins to Worth: A Quantitative Model of Performance, Attendance, Revenue, and Valuation for Sports Teams* · Finalist · Team 2608869.

[![截断需求、票务收入与现金／债务恒等式，连接到球员行动和滚动状态更新。](overview.png)](overview.png)

截断需求、票务收入与现金／债务恒等式，连接到球员行动和滚动状态更新。

[完整 prompt 与调用记录](full-prompt.md) · [论文依据与图注](brief.json) · [文件校验](integrity-audit.json)

## 论文来源

- [固定版本论文](https://raw.githubusercontent.com/WeiLai-OpsFin/comap-icm-2026-d-finalist-wnba-team-valuation-model/3efa32aa320bbab0569f89a5e080cee2b60b5ea2/docs/2608869.pdf) · [来源仓库](https://github.com/WeiLai-OpsFin/comap-icm-2026-d-finalist-wnba-team-valuation-model/tree/3efa32aa320bbab0569f89a5e080cee2b60b5ea2).
- [COMAP 官方奖项](https://www.contest.comap.com/undergraduate/contests/mcm/contests/2026/results/2026_ICM_Problem_D_Results.pdf): PDF physical page 3, first row: Team 2608869, Problem D, Finalist.
- PDF SHA-256: `af57e494a2cb0713b881c64ebd02b16686f9df0992b33562a7919cd1981fd161`.

已重新核对建模正文（Main pp.1–25, including preceding-turn equation inspection），本轮目视检查公式／图页：13, 14, 16, 19, 20, 24。新图由 ImageGen 生成，不是论文截图，也没有重跑数值实验；奖项属于来源论文。

## 原文依据

| 图中内容 | 物理 PDF 页 / 章节 |
| --- | --- |
| Elo, right-censored lognormal demand and pricing assumptions | pp.9–12, §§5–6 |
| Revenue, profit, simplified cash book, valuation methods and leverage | pp.13–15, Eqs.22–29 |
| Four-component state, action increments, optimization and rolling updates | pp.15–18, Eqs.30–35 |
| Other-revenue market scaling and conflicting valuation/injury descriptions | pp.19–24, §§9–11 |

## 检查与交付

2026-09-20 经用户确认用于项目发布。选定 PNG 为 1536 × 1024，已目视检查；完整 prompt、来源冲突、修订记录和图片哈希保留在上述文件中。旧调用只作历史留档，不作当前绘图依据。

尚未进行物理印刷校样或独立审查。当前交付为位图，放入论文时仍需检查小字与公式；建议置于 Our Work 通栏（180 mm），英文图注见 `brief.json`。
