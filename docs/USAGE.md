# 使用说明

## 运行条件

- Python 3.10+。
- 宿主需要读取本地论文、执行工作流，并提供 ImageGen。
- Poppler 的 `pdftoppm` 用于渲染参考 PDF 页。安装后用 `pdftoppm -v` 检查 PATH。
- PDF / Markdown / TXT / TeX 可以直接导入。扫描 PDF 请先 OCR。
- README 的 Quick Start 使用源码工作流，无需先注册插件市场；附带的 SKILL.md 是宿主的执行入口。

项目自身不包含生图模型。CLI 的 `paper2overview` 负责快照、文本提取和参考推荐，
宿主按 skill 阅读、设计并生成图片。没有 ImageGen 时，流程只能交付设计和 prompt。

## 验证安装

Windows PowerShell：

```powershell
.\.venv\Scripts\python.exe -m modelatlas coverage
.\.venv\Scripts\python.exe -m modelatlas styles --problem E
```

macOS / Linux 将 Python 路径换为 `.venv/bin/python`。
以下命令假设虚拟环境已激活，或使用上述 Python 路径加 `-m modelatlas`。

## 论文与参考

```sh
modelatlas paper2overview path/to/paper.pdf --problem E
modelatlas styles --problem E
modelatlas styles --year 2025 --problem A
modelatlas styles --year 2026 --problem D
modelatlas reference e-model-inheritance-overview
modelatlas styles --role all --collection all
```

默认只推荐 Overview。机制、算法和数据图保留作局部表达参考。
题号 A–F 是检索分类，不是固定不变的建模类型；题号 F 与 Finalist 奖项分开记录。
`--year` 按来源论文年份过滤。文本匹配分数相同时，先推荐原题号相同的图例，再按年份从新到旧排序。
`coverage` 同时给出逐年覆盖和缺口。扫描版参考页仍可直接渲染查看，空文本不代表空白页。

## AnySearch

```sh
modelatlas literature "COMAP 2025 2515324 Finalist" --mode web
modelatlas literature "mathematical modeling overview" --mode academic
```

用于公开论文和图例的来源检索。可选 `ANYSEARCH_API_KEY`。
检索结果不会直接变成已审核图例；不要发送私人稿件或凭据。

## 归档成图

```sh
modelatlas pair-overview SESSION_DIR --image overview.png --prompt prompt.md --brief brief.json
modelatlas audit-overview BUNDLE_DIR
```

[制作规范](../plugins/sivia-modelatlas/skills/paper2overview/references/production-contract.md)给出 prompt 与 brief 的要求。
归档记录实际图片、生成指令、正文依据和审查情况。文件完整性、视觉自审、独立审查及用户验收分别记录。

<a id="editable-ppt"></a>

## Overview → 可编辑 PPT 矢量图

先确认 Overview 图片，再明确要求制作 PPT。这是接续 **Sivia** 的可选复刻步骤，
不由 ModelAtlas 的 CLI 或七个 MCP 工具执行；ModelAtlas 不内置 PNG → PPTX 转换器。

### 准备

- 按 [Sivia 安装说明](https://github.com/exsinger-hub/Sivia#安装)安装插件，并让当前会话能够调用它。
- 准备 Node.js 和可用的 PowerPoint / WPS 后端，由 Sivia 在执行前检测。指定 WPS 时不自动切换到 PowerPoint。
- 提供已确认的图片、对应完整 prompt、论文依据，以及要重绘的图表数据（如有）；说明目标软件和输出位置。

确认图片只表示认可视觉稿，不会自动启动 PPT 制作。[README 第 4 步](../README.md#quick-start)提供可复制指令。
复刻时保持原图比例、分区、配色和模型关系；只重建这张 Overview，不扩展为汇报幻灯片。
默认新建独立文件，后台执行且不抢焦点。若缺少后端或不能满足后台要求，先说明限制并等待选择。

### 可编辑范围

- 文字、公式、几何形状、箭头使用原生文本、公式或可编辑形状组合。
- 图表有真实数据时重绘；不从示意曲线猜测数值。
- 照片和复杂插画可保留为独立位图，标签、边框和连线单独绘制；交付时列明位图部分。

不能用整页或整面板截图代替可编辑对象。插入 SVG 也不代表其内部元素可以分别编辑。

### 交付与检查

交付 `overview-editable.pptx`、从该 PPTX 导出的预览图，以及保留位图的对象清单。
检查文字可修改、形状和连接线可独立选中，再将预览与确认稿同尺度对照，修正溢出、遮挡和连线偏移。
文件已保存、预览已检查、应用内编辑已验证应分别说明；没有实际生成 PPTX 时，不标记转换完成。

## MCP

插件源码在 [plugins/sivia-modelatlas](../plugins/sivia-modelatlas)，主 skill 为 `paper2overview`。
以下示例路径需替换为本机项目目录：

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

七个工具用于准备论文、检索图例、查看覆盖、获取参考页、搜索来源、配对成图和校验文件。
MCP 提供资料与归档能力，生图仍由宿主执行。

复制插件到其他目录时，可用 `MODELATLAS_PYTHON` 指定安装了本包的 Python。
CLI 默认在当前目录的 `.modelatlas` 保存数据，MCP 默认使用用户目录下的 `.modelatlas`；
通过 `MODELATLAS_HOME` 或全局 `--workspace` 指定统一位置。

## 开发

```sh
python -m pip install -e '.[mcp,dev]'
python -m pytest -q
python -m build
```

[架构](architecture.md) · [变更记录](CHANGELOG.md)
