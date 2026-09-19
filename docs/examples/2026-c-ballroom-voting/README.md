# Behind the Ballroom Scores · 2026 MCM C

[English](README.en.md) · [全部成图](../../../README.md#showcase)

来源论文：*Behind the Ballroom Scores: Reconstructing Fan Voting and Designing Fairer Rules for DWTS* · Finalist · Team 2627351.

| 论文作者原图 · Figure 1, PDF p5 | ModelAtlas · 最终成图 |
| :---: | :---: |
| [![Original](../../assets/reference-overviews/2026-c-2627351-overview.png)](../../assets/reference-overviews/2026-c-2627351-overview.png) | [![ModelAtlas](overview.png)](overview.png) |

可行域解释隐藏票份额；同周对照连接到右侧的条件保护公式。新版放大实际操作，去掉重复模块底板。

[完整 prompt](full-prompt.md) · [论文依据与图注](brief.json) · [文件校验](integrity-audit.json)

## 论文来源

- [固定版本论文](https://raw.githubusercontent.com/alectimison-maker/2026MCM-ICM_C/2fcf7bb344e6fa7c295ec771b5be79c3a9ebd361/2627351_submitted_paper.pdf) · [来源仓库](https://github.com/alectimison-maker/2026MCM-ICM_C).
- [COMAP 官方奖项](https://www.contest.comap.com/undergraduate/contests/mcm/contests/2026/results/2026_MCM_Problem_C_Results.pdf): PDF page 15, Team 2627351, C, Finalist.
- PDF SHA-256: `ab837f28944fce38f7677fe833ed89360ff38da754e47f7f406273dfae31bf55`.

已阅读全文（34 页）并查看原 overview。这里展示的是实际 ImageGen 新成图，不是论文截图，也没有重跑数值实验。奖项属于来源论文。

并排原图的 [MIT 许可与署名](../../assets/reference-overviews/README.md) 单独保留。

## 图中保留什么

| 图中内容 | 物理 PDF 页 / 章节 |
| --- | --- |
| Cleaning observed judge scores, eliminations and contestant metadata; latent fan support is a relative share, not observed vote totals. | PDF pp4–6, §§1–3 |
| Complementary feasible-set intervals and Plackett–Luce point inference with consistency and uncertainty diagnostics. | PDF pp7–10, §4 |
| Same-week contestant-set counterfactuals for Rank, Percentage and Judges' Save, with cross-inference checks. | PDF pp11–14, §5 |
| Mixed-effects models compare judge and inferred-fan outcomes with trait/season effects and pro/celebrity intercepts. | PDF pp14–18, §6 |
| MARS-Soft+Disagreement modifies rank-sum risk only for judge-elite contestants with weaker fan rank; earlier/later season tuning/test split. | PDF pp18–20, §7 |
| Inference sensitivity and season-blocked trait-model validation. | PDF pp21–22, §8 |

## 检查与交付

最终 PNG 为 1536 × 1024，已自审文字、模型边界和连线方向。完整 prompt、实际生成调用、图片哈希和内容取舍留在上述记录中；本页仅展示选定成图。

物理印刷尺寸、独立审查和用户验收仍待确认；当前交付是位图。建议放在 Our Work 通栏位置，英文图注见 `brief.json`。
