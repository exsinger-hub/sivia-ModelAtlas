# 真实论文测试：2025 ICM E

本例测试 ModelAtlas 的 Paper → Overview 全链路：已有论文输入、全文理解、参考图阅读、
实际 ImageGen 生成、视觉检查与修正、图片/prompt/证据配对。不是解题、写论文或重跑仿真。

![新生成的 overview 修订版](overview.png)

## 输入与来源

- 论文：*From Forest to Farm: Modeling Nitrogen Dynamics for Sustainable Agriculture*。
- 2025 ICM E，Team 2515324，Finalist。
- [作者仓库](https://github.com/LUKEQ420/MCM-ICM-2025-E-Nitrogen-Cycling-Model)；
  [固定版本论文](https://github.com/LUKEQ420/MCM-ICM-2025-E-Nitrogen-Cycling-Model/blob/fb579acd7107706e055c8a10f921f9f56498a06a/paper/2515324.pdf)。
- [COMAP 官方结果](https://www.contest.comap.com/undergraduate/contests/mcm/contests/2025/results/2025_ICM_Problem_E_Results.pdf)：物理第 6 页，2515324，E，Finalist。
- PDF 共 25 页，正文、方程、结果、参考文献和致农民信均已读取；PDF SHA-256：
  `2c566c95c1d4a1b4292176805253ad4f09ccfe9154e8809beb86f399347a8cdc`。
- 本次用 AnySearch 的 URL 提取核对作者来源；获奖身份沿用知识库已有官方逐行核验。
  缓存 PDF 与提取全文仅保存在本地，不随此示例发布。

这是**已知参考论文的重设计测试**，不是未见样本盲测，不能由单例推断通用成功率。
使用的图片都是本次新生成；作者原 overview 仍在 README 的参考知识库区，二者不混淆。

## 执行与修正

1. 实际运行 `modelatlas paper2overview`：提取 25 页，0 个空文本页，保留源文件哈希。
2. 阅读全文，查看知识库 `e-model-inheritance-overview`、`e-nitrogen-cycle`，
   并检查原文第 16 页 Figure 9 的七节点食物网。
3. 冻结 [初始设计](design-spec.json) 和 [第一次完整 prompt](prompt.md)；
   调用内置 ImageGen，生成 [第一版](overview-v1.png)。
4. 自审发现收获箭头靠近杂草、分析入口箭头脱离模型、部分字号偏小；
   使用 [修正 prompt](correction-prompt.md) 实际编辑第一版。
5. 查看最终 [overview.png](overview.png)：主流程改为 a → b → c → d → e → f，
   下排从右向左读；收获箭头从作物冠层右侧引出。
6. 使用 `pair-overview` 配对真实图片、[两轮完整 prompt](full-prompt.md)、
   [证据 brief](brief.json)，再运行 `audit-overview` 检查文件完整性。

内置 ImageGen 真实返回 1536 × 1024 PNG；没有把 prompt 当成执行结果，没有调用其他付费生成后端。
保存两个版本是为了让修正过程可检查，不代表两个独立风格候选。

## 论文依据与内容取舍

| 图中表达 | 物理 PDF 页 / 原文章节 | 边界 |
| --- | --- | --- |
| 森林氮循环与总氮守恒 | pp4–8，§2、§4，Eq2–5 | 消费者层级聚合；分解者过程可见，不声称展示全部状态变量 |
| 作物/杂草、季节、播种、收获、化肥、化学品 | pp9–15，§5，Eq6–14 | 农田是开放氮收支；化学干预在有作物时施用 |
| 七节点食物网及九条营养传递边 | pp16–18，Fig9、Eq15–20 | 箭头从被捕食者指向捕食者；竞争用钝头线区分 |
| Euler 数值解、情景比较、两个氮指标 | pp18–21，§6.1.3–6.3.1 | 氮周转是论文采用的稳定性代理，不是外部验证 |
| 作物/杂草竞争敏感性 | pp22–23，§8 | 参数敏感性不是新数据拟合 |
| 根瘤菌/豆科和秸秆利用 | pp21–22，§7 | 明确为文献支持的建议，不画成已仿真的干预组 |

没有生成数值曲线、精度、百分比或“最优方案”。原文 Eq5 的摄取项与相邻文字/Eq2 存在符号不一致；
本图按照文字定义表达分室关系，没有更改原论文方程，也没有声称验证数值结果。

## 审查结果

本次完成的是实际成图测试。可见内容自审核对了三个模型缩写、氮收支边界、
食物网 9/9 条边、三种情景的并列关系及“已模拟 / 文献延伸”的区别。
整体更接近论文的概念 overview，而非数据结果图。

**正式出版审查仍为 pending**：未进行独立、不知设计意图的灰度读图测试，也未做 180 mm
物理印刷 proof。小注释字号仍需在真实排版中确认；高分辨率不能替代字号检查。
当前是栅格候选图，不是原生可编辑矢量，也尚未取得用户验收。

完整生成链、图像哈希、具体检查项和待验证事项均在 [brief.json](brief.json)；
文件哈希校验与科学内容自审分开记录，不把前者当成后者的证明。
[实际文件配对校验结果](integrity-audit.json)：图片、prompt、brief 三项均通过。
项目回归检查为 **42 passed**，其中两项核对本例图像、生成链、来源绑定与待验收状态；
自动化检查不替代视觉审查。

## 图注与放置

建议放在 §1.3 Our Work，位于假设及模型定义之前，通栏排版。
英文图注见 [brief.json](brief.json) 的 `caption` 字段，可直接作为修改起点。

## 复现文件

- `prompt.md`：第一次调用的原样 prompt。
- `overview-v1.png`：第一次实际生成结果，也是编辑调用的输入。
- `correction-prompt.md`：第二次调用的原样修正 prompt。
- `full-prompt.md`：两次调用的完整顺序记录，不声称是单次调用。
- `overview.png`：第二次调用返回的实际 PNG。
- `design-spec.json`：生成前设计；第二轮布局变化以修正 prompt 为准。
- `brief.json`：论文依据、模型关系、图注、真实生成记录和审查边界。

图中的研究框架与主张归属来源论文作者；新绘制的图用于说明 ModelAtlas 工作流，不表示原作者背书。
参考原图的 MIT 许可保留在 [作者参考图许可记录](../../assets/reference-overviews/README.md)。
