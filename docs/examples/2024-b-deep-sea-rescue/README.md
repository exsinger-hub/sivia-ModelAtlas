# 01 · Unlocking the Abyss

2024 MCM B · Outstanding Winner · Team 2407038

海水剖面连接同坐标搜索网格：从三维漂移，到 D4 搜索未发现，再转向 E4。

![最终成图](overview.png)

[来源论文](https://raw.githubusercontent.com/yangchunwanwusheng/MCM-ICM--2024-/ffea7fd98c1fbf7d25edcba4dbc834631e9adbf2/2024/B/student%20paper/2407038.pdf) · [获奖记录](https://www.contest.comap.com/undergraduate/contests/mcm/contests/2024/results/) · [完整 prompt](full-prompt.md) · [逐次调用](scene-prompt-records.json) · [来源与核对记录](brief.json) · [English](README.en.md)

## 图注

海流预测、海流与密度的空间回归共同支持受海床约束的三维漂移预测，水平位置用于确定假设搜索场的中心。两张网格保持相同坐标：D4 搜索未发现后被排除，下一时刻的预测位置对应 E4。永久排除依赖论文中的完美探测和不再进入假设；约 300 m 的网格与 30 min 的间隔来自论文示例。色阶只解释搜索机制，不表示重新计算的概率。

## 本次修订

理顺两条垂直投影，使用同名位置标签连接海水剖面与网格，并移除 D4 内重复的位置标记。

2026-09-21 · 已检查实际成图；未进行实体印刷或独立终审。本次仅更新展示，不将生成图加入知识库。
