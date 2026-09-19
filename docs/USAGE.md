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
