# 03 · From Wins to Worth

2026 ICM D · Finalist · Team 2608869

球场容量解释需求截断，票据和账本连接收入、利润、现金与债务，底部保留滚动决策。

![最终成图](overview.png)

[来源论文](https://raw.githubusercontent.com/WeiLai-OpsFin/comap-icm-2026-d-finalist-wnba-team-valuation-model/3efa32aa320bbab0569f89a5e080cee2b60b5ea2/docs/2608869.pdf) · [获奖记录](https://www.contest.comap.com/undergraduate/contests/mcm/contests/2026/results/2026_ICM_Problem_D_Results.pdf) · [完整 prompt](full-prompt.md) · [逐次调用](scene-prompt-records.json) · [来源与核对记录](brief.json) · [English](README.en.md)

## 图注

有限座位容量限制实际入场人数，期望入场量由 E[min(需求, 容量) | 特征] 给出，再与票价结合形成票务收入。票务及其他收入进入经营账本，利润、借款和还款分别更新现金与债务。不同估值口径支持杠杆判断，球员行动和可行性约束随新信息滚动更新。图为机制示意，不填补论文中定价与估值汇总口径的不一致，也不生成新的估计结果。

## 本次修订

用匹配标记对应票务小计与入账项，清除穿过账本标题的旧连线，并整理容量点和新观测标签。

2026-09-21 · 已检查实际成图；未进行实体印刷或独立终审。本次仅更新展示，不将生成图加入知识库。
