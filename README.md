# SIVIA ModelAtlas

**面向美赛 MCM/ICM 与数据建模作图的 SIVIA 独立并行项目。**

输入建模论文和数据，检索相近图表案例，制作模型流程图与可复现数据图。继承 SIVIA 的“理解来源 → 设计 → 绘制 → 审查 → 修正 → 配对案例”工作流，拥有独立插件名称、代码、SQLite 知识库和 Git 历史。

## 已实现

- AnySearch 实时学术检索，检索记录与阅读后的知识卡片分开管理。
- 本地 PDF/Markdown/TXT 导入，记录来源哈希和逐页可检索文本。
- 7 条来源、10 张首轮绘图知识卡片，聚焦 MCM C 网球动量、预测与数据分析。
- 八种可执行配方：时间序列、预测对照、散点、残差、情景敏感性、矩阵热图、双目标非支配解、建模流程图。
- CSV/JSON 数据绑定，输出 PNG、保留文本的 SVG、嵌入字体的 PDF。
- 每次运行保存完整 spec、数据快照、prompt、审查与哈希清单；HTML 案例库可筛选并下载实际成图。
- 八个 MCP 工具与四个专用 skills。与原 SIVIA 可并行使用。

当前版本不自动拟合任意模型、不声称 OCR/SHAP/地图/原生 PPTX 已实现。数值图使用输入数据；提供的示例数值均标明 DEMO。规则随年份核对，论文案例不标为未经证实的 O 奖。

## 运行

需要 Python 3.10+。Windows：

```powershell
cd H:\yf\sivia-ModelAtlas
.\scripts\bootstrap.ps1
.\.venv\Scripts\python.exe -m modelatlas search "网球 动量"
.\.venv\Scripts\python.exe scripts\demo.py
```

跨平台安装：

```sh
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows: .venv\Scripts\Activate.ps1
python -m pip install -e '.[mcp,dev]'
modelatlas init
python scripts/demo.py
```

打开 `outputs/demo/gallery.html` 查看八类实际输出。无服务器依赖；HTML 内嵌图片与 SVG/PDF 下载。

## 从新论文到图表

```sh
modelatlas literature "tennis momentum mathematical modeling" --limit 5
modelatlas ingest path/to/paper.pdf --url https://example.org/paper --title "Paper title"
modelatlas evidence paper-SHA_PREFIX --query "Figure"
modelatlas search "prediction forecast"
modelatlas add-card path/to/curated-card.json
modelatlas render examples/forecast.json --output outputs/my-paper
modelatlas gallery --output outputs/gallery.html
modelatlas audit outputs/my-paper/RUN_ID
```

`literature` 调用 AnySearch 的 academic 域，先发现能力。匿名访问可用；可选环境变量 `ANYSEARCH_API_KEY`，程序不保存新密钥、不读原 SIVIA 的凭据。网络/额度失败会明确报错。离线库与绘图可独立运行。

`ingest` 只保存文本和来源；阅读、解释模型与策划图表由宿主 agent 完成。`add-card` 要求来源 ID、定位、主张和建议齐全。检索采用透明的词项匹配，不是嵌入或自动深度理解。

全局 `--workspace` 放在子命令之前，或设置 `MODELATLAS_HOME`。CLI 默认当前目录 `.modelatlas`，MCP 默认用户目录 `.modelatlas`；建议显式配置相同路径以共享库。

## 绑定自己的数据

复制 `examples/` 中匹配用途的 spec，将 `data_status` 设为 `provided` 或 `empirical` 并记录来源。CSV 示例：

```json
{
  "kind": "forecast",
  "title": "Observed vs predicted demand",
  "claim": "Compare supplied forecasts with observed demand.",
  "data_status": "provided",
  "source_note": "My experiment / held-out predictions",
  "x_label": "Day", "y_label": "Demand (units)",
  "data_file": "predictions.csv",
  "columns": {"x": "day", "y": "actual", "predicted": "estimate"}
}
```

数据文件相对于 spec 定位。缺失值、无限值、长度错位、倒序时间或含义不明的区间会被拒绝。敏感性模板画低高参数情景的已计算输出；Pareto 模板只识别提供候选中的非支配解。

## 插件和 MCP

插件源码位于 `plugins/sivia-modelatlas`，含 Codex / Claude Code manifest 与四个 skills：

- `design-mcm-figure`：建模总图与流程依赖。
- `plot-modeling-data`：数据绑定绘图。
- `curate-modeling-knowledge`：论文到知识卡片。
- `audit-modeling-figure`：数值语义和实际图表审查。

源码插件的启动脚本会找到本项目 `.venv`。复制到插件目录后，在宿主 MCP 配置设置 `MODELATLAS_PYTHON` 为已安装本包的 Python 路径；也可直接使用下面的服务器配置（路径替换为你的 checkout）：

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

工具包括 `atlas_status`、`atlas_find_papers`、`atlas_ingest_paper`、`atlas_read_evidence`、`atlas_search_knowledge`、`atlas_add_card`、`atlas_render`、`atlas_audit`。宿主负责模型推理，本项目负责可靠的知识与绘图执行。

## 验证和结构

```sh
python -m pytest -q
python scripts/demo.py
python -m build
```

`src/modelatlas/` 是运行时；`examples/` 是可执行配方；`knowledge-base/` 解释知识组织；`tests/` 包含实际渲染、错误数据、数值计算、篡改检测和 MCP stdio 集成测试。GitHub Actions 配置覆盖 Windows/Linux、Python 3.10/3.12；本地通过不等于远程 CI 已完成。

来源：[COMAP 2024 C 题](https://www.contest.comap.com/undergraduate/contests/mcm/contests/2024/problems/2024_MCM_Problem_C.pdf)、[Lei et al.](https://arxiv.org/abs/2404.13300)、[Lv et al.](https://doi.org/10.1038/s41598-024-69876-5)。卡片记录具体定位；第三方原始论文和图像未随仓库分发。

SIVIA 工作流来源：[exsinger-hub/Sivia](https://github.com/exsinger-hub/Sivia)。本项目新增代码遵循 MIT；第三方材料保留自身许可。
