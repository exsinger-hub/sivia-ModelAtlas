# SIVIA ModelAtlas

**给已有的美赛论文草稿画图：Draft → Overview。**

SIVIA 的独立并行项目。读取论文草稿，参考真实 O／F 获奖论文的图形表达，设计并绘制
Our Work / overview、模型机制图与数据图。**不负责把题目变成论文，也不自动解题。**

主入口是插件 skill **`draft2overview`**（兼容“craft 2 overview”的调用表达）。
延续 SIVIA 的草稿理解 → 参考图阅读 → 设计 → ImageGen 成图 → 审查修正 → 图像/prompt 配对流程。
概念 overview 默认由宿主的图像生成能力执行；真实数值图走独立的数据绘图路径。

## 已构建的知识库

首批实际核对、逐图审阅：**8 篇 O/F 论文、18 个获奖图例；1 篇科研预印本、2 个扩展图例**。
每个图例记录固定 PDF 版本/哈希、物理页码、图号、构图、可借鉴内容、不可照搬内容和局限。

| 分类入口（常见方向，非永久题型定义） | 核心论文 | 原题所属图例 |
| --- | --- | --- |
| A：连续变化、动力学 | 2024 O · 2400996 | 2 |
| B：离散决策、优化 | 2024 O · 2419984 | 2 |
| C：数据洞察、统计建模 | 2024 O · 2401919；2026 F · 2627351 | 6 |
| D：网络系统、运筹控制 | 2024 O · 2417831 | 2 |
| E：环境、生态、可持续性 | 2024 O · 2413552；2025 F · 2515324 | 4 |
| F：政策、社会决策 | 2024 O · 2422054 | 2 |

奖项与论文队号已匹配官方结果；**题目 F 不等于奖项 F（Finalist）**。
科研扩展单独标记，不冒称获奖。图例还可按 overview / mechanism / algorithm / data_plot /
explanation、模型关系和跨类适用性检索。例如 E 类物质循环图可用于 A 类机制表达，但原始类别不变。

这是可追溯的种子库，不是全历年获奖论文全集，也不是每类都有 O 和 F。
科研扩展目前来自网球机器学习论文，可向生态、网络和政策等方向继续积累。
[逐图目录](knowledge-base/CATALOG.md) · [入库标准](knowledge-base/README.md)

## 怎么用

安装源码插件后，对支持图像生成的宿主说：

> 用 SIVIA ModelAtlas 读这份美赛论文草稿，参考同类 O/F 论文，为 Introduction 末尾画一张 overview；
> 保留完整绘图 prompt，检查模型关系和箭头，不替我改模型或写论文。

宿主负责读懂草稿、选择/查看参考图、生成与检查图片。本项目提供 skill、分类知识库、来源取回、
草稿快照及真实成图的配对归档。**命令行的 draft2overview 只是准备入口，不是“一条命令自动画完”。**
没有图像生成工具时会明确交付设计/prompt，不能报成图完成。插入/改写原稿需另获授权。

### 安装运行

Python 3.10+；读取参考图页另需 Poppler 的 `pdftoppm` 可在 PATH 找到。

```sh
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
python -m pip install -e '.[mcp,dev]'
modelatlas coverage
modelatlas styles --problem C --role overview
modelatlas styles "循环" --problem E --role mechanism
modelatlas styles "SHAP" --collection research
modelatlas reference c-infer-compare-redesign
modelatlas draft2overview path/to/draft.pdf --problem C
```

Windows 也可运行 `scripts/bootstrap.ps1`。全局 `--workspace` 应放在子命令之前；
或设置 `MODELATLAS_HOME`。CLI 默认当前目录 .modelatlas，MCP 默认用户目录 .modelatlas；
建议明确配置相同目录。所有草稿/PDF/页面缓存默认本地保存，不提交 Git。

`reference` 实际下载固定版本 PDF，验证 SHA-256 后渲染指定页；宿主必须打开图片阅读。
`--pdf-only` 可只取 PDF。没有 Poppler 时返回明确错误，不谎报图页审阅完成。

### 保存 overview 的完整配对

按 skill 的 [制作契约](plugins/sivia-modelatlas/skills/draft2overview/references/production-contract.md)
写好完整 prompt 和 brief，在宿主实际生成图片后执行：

```sh
modelatlas pair-overview SESSION_DIR --image actual-overview.png --prompt prompt.md --brief brief.json
modelatlas audit-overview PAIRED_BUNDLE_DIR
```

每次归档使用新目录，保存实际图像、完整 prompt、草稿依据、引用方式、图注、审查与哈希清单。
检查文件哈希不等于科学结论正确、视觉合格或用户认可。

## 插件与 MCP

插件源码：`plugins/sivia-modelatlas`，独立名称，不覆盖原 SIVIA。
包含 Codex / Claude Code manifests、stdio MCP 启动器和五个 skills：

- `draft2overview`：主要入口，从草稿到 overview。
- `design-mcm-figure`：兼容入口，转入主流程；简单 SVG 流程图按需使用。
- `curate-modeling-knowledge`：O/F 核心库与科研扩展库入库。
- `plot-modeling-data`：真实数据驱动的数值图。
- `audit-modeling-figure`：实际图像、科学语义和可追溯性审查。

源码启动器会找到 checkout 的 .venv。复制到插件安装目录后，可配置 `MODELATLAS_PYTHON`
指向已安装本包的 Python。下面也可作为直接 MCP 配置（替换成本机绝对路径）：

```json
{
  "mcpServers": {
    "modelatlas": {
      "command": "H:/yf/sivia-ModelAtlas/.venv/Scripts/python.exe",
      "args": ["-m", "modelatlas.server"],
      "env": {"MODELATLAS_HOME": "H:/yf/sivia-ModelAtlas/.modelatlas"}
    }
  }
}
```

14 个工具共享同一 Python 实现。核心新增工具是 `atlas_search_styles`、
`atlas_style_coverage`、`atlas_fetch_reference`、`atlas_prepare_draft`、
`atlas_pair_overview` 和 `atlas_audit_overview`。
源码可用不等于已在所有宿主全局安装；图像生成由宿主提供，项目不内置模型 API 密钥。

## AnySearch 与后续扩库

使用 AnySearch 3.1.1 对应接口：先发现 academic 能力，再搜索；学术检索与获奖来源网页检索分开。

```sh
modelatlas literature "tennis momentum visualization" --mode academic
modelatlas literature "COMAP 2025 2515324 Finalist" --mode web
modelatlas ingest path/to/paper.pdf --url https://example.org/paper
modelatlas evidence SOURCE_ID --query Figure
```

可选环境变量 `ANYSEARCH_API_KEY`。不会复制原 SIVIA 凭据、保存返回的密钥或把检索结果自动标为获奖。
多路检索可使用完整 AnySearch skill 的 batch/hybrid。新来源必须阅读原图、核奖及版本之后，才加入
`corpus.json`；普通发现记录和旧数值配方卡保留在独立 SQLite，不混入获奖图例。

## 数据作图是辅助路径

保留八种代码绘图配方：时间序列、预测对照、散点、残差、情景敏感性、热图、Pareto、简单流程图。
它们不是主 overview 的八种固定模板。数值由 CSV/JSON 绑定，输出 PNG/SVG/PDF 与数据/配置快照。

```sh
python scripts/demo.py
modelatlas render examples/forecast.json --output outputs/my-paper
modelatlas gallery --output outputs/gallery.html
modelatlas audit outputs/my-paper/RUN_ID
```

示例明确标记 DEMO；不自动拟合任意模型，不让 ImageGen 编造经验数据，不声称原生 PPTX、
OCR、SHAP 计算或自动插入论文已实现。SHAP 参考案例仅用于设计指导，需当前模型真实计算结果。

## 验证与许可

```sh
python -m pytest -q
python -m build
```

测试包括 A–F 分类/奖项约束、来源校验、草稿快照、图像-prompt 配对与篡改检测、实际数值渲染、
运行时及插件启动器的真实 MCP stdio 往返。远程 CI 覆盖 Windows/Linux 与 Python 3.10/3.12。

[架构](docs/architecture.md) · [发布变更](docs/CHANGELOG.md)

[COMAP 2024 官方结果](https://www.contest.comap.com/undergraduate/contests/mcm/contests/2024/results/)、
[2025 E 官方结果](https://www.contest.comap.com/undergraduate/contests/mcm/contests/2025/results/2025_ICM_Problem_E_Results.pdf)、
[2026 C 官方结果](https://www.contest.comap.com/undergraduate/contests/mcm/contests/2026/results/2026_MCM_Problem_C_Results.pdf)；
科研扩展：[Lei et al., arXiv v1](https://arxiv.org/abs/2404.13300)。

工作流源自 [SIVIA](https://github.com/exsinger-hub/Sivia)。本项目新增代码/原创分析遵循 MIT。
第三方论文、页面图像和用户草稿保留自身权利；公开可下载不代表允许随仓库再分发。
