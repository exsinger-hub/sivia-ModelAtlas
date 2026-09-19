# SIVIA ModelAtlas · Paper → Overview

**输入已有论文，输出一张忠于论文内容的 overview。**

面向美赛 MCM/ICM，沿用 SIVIA 的论文理解与科学绘图流程。
当前只做 **Paper → Overview**：读论文 → 查阅参考插图 → 设计构图 → 生成图像 → 审查修正。

交付是**实际 overview 图片 + 完整绘图 prompt + 论文依据与图注建议**。
不扩展到解题、写论文、独立数据作图或通用图表平台。

## 使用

在支持图像生成的宿主中调用唯一主 skill **`paper2overview`**：

> 用 SIVIA ModelAtlas 阅读这篇论文，参考知识库里的同类 O/F 插图，生成一张 overview。
> 保留完整 prompt，检查模型关系和箭头，不改写论文内容。

输入可以是完整论文或已有草稿。参考图用于学习构图，模型、关系与结论必须来自输入论文。
概念 overview 由宿主 ImageGen 生成；没有图像生成能力时，会明确标为设计/prompt 未成图。

## 插图知识库

**知识库保留，不随功能精简删除。** 已核验并逐图阅读的种子库包括：
**8 篇 O/F 论文、18 个获奖图例；1 篇科研预印本、2 个扩展图例。**

| 类别入口（常见方向，非永久题型定义） | 获奖论文 | 原题所属图例 |
| --- | --- | --- |
| A：连续变化、动力学 | 2024 O · 2400996 | 2 |
| B：离散决策、优化 | 2024 O · 2419984 | 2 |
| C：数据洞察、统计建模 | 2024 O · 2401919；2026 F · 2627351 | 6 |
| D：网络系统、运筹控制 | 2024 O · 2417831 | 2 |
| E：环境、生态、可持续性 | 2024 O · 2413552；2025 F · 2515324 | 4 |
| F：政策、社会决策 | 2024 O · 2422054 | 2 |

每个图例保留来源链接、固定 PDF 版本/哈希、物理页码、图号、构图分析、可借鉴内容与局限。
O/F 对照官方结果核验，科研扩展独立标记；题目 F 不等于奖项 F（Finalist）。

检索默认 overview。已有机制图、算法图、数据图等读图资料继续保留，供 overview 的局部表达参考，
**不代表项目还提供这些图种的独立绘制功能**。跨类适用性不会改写原论文的题号和年份。

[逐图目录与来源](knowledge-base/CATALOG.md) · [知识库组织与入库标准](knowledge-base/README.md)
· [结构化知识库](src/modelatlas/knowledge/corpus.json)

这仍是种子库，不是全历年获奖论文全集。仓库保存元数据和原创分析；第三方 PDF/页面图像只在本地
缓存，不把参考图冒充项目新成图，也不默认再分发第三方插图。

## 安装与运行

Python 3.10+；查看参考 PDF 图页另需 Poppler 的 `pdftoppm`。

```sh
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
python -m pip install -e '.[mcp,dev]'
modelatlas coverage
modelatlas styles --problem C
modelatlas reference c-infer-compare-redesign
modelatlas paper2overview path/to/paper.pdf --problem C
```

Windows 也可运行 `scripts/bootstrap.ps1`。
**CLI 的 paper2overview 负责保存论文快照、提取正文和选择参考候选，不会独立调用模型生成图片。**
宿主按 skill 完成阅读、设计、实际生成与视觉检查。支持 PDF/Markdown/TXT/TeX；扫描 PDF 需先 OCR。

实际成图后归档：

```sh
modelatlas pair-overview SESSION_DIR --image overview.png --prompt prompt.md --brief brief.json
modelatlas audit-overview BUNDLE_DIR
```

[制作契约](plugins/sivia-modelatlas/skills/paper2overview/references/production-contract.md)
说明完整 prompt、论文证据和审查记录的要求。文件校验通过不等于视觉或科学审查通过。

全局 `--workspace` 放在子命令前，或设置 `MODELATLAS_HOME`。CLI 默认当前目录 .modelatlas，
MCP 默认用户目录 .modelatlas；配置相同路径可共享论文与参考缓存。旧本地数据不会自动清理。

## 插件与工具

插件源码在 `plugins/sivia-modelatlas`，与原 SIVIA 独立。只提供一个 skill：`paper2overview`。
七个底层 MCP 工具服务于同一条流程：准备论文、检索插图、查看覆盖、取回参考页、找论文、
图像/prompt 配对、归档校验。

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

替换为本机路径。复制插件后可设置 `MODELATLAS_PYTHON` 指向已安装本包的 Python。
源码更新不代表所有宿主已重新安装；项目不内置模型密钥。

AnySearch 保留为论文/插图来源检索工具：

```sh
modelatlas literature "COMAP 2025 2515324 Finalist" --mode web
modelatlas literature "mathematical modeling overview" --mode academic
```

检索结果不自动进入已审阅知识库。可选 `ANYSEARCH_API_KEY`，不复制其他项目凭据或保存返回密钥。
需要查看其他已保留插图时使用 `modelatlas styles --role all --collection all`。

## 开发与范围

```sh
python -m pytest -q
python -m build
```

0.3.0 移除了独立数值绘图后端、八种配方/demo、通用 HTML 图库、旧 SQLite 卡片接口及旁支 skills，
并去掉 NumPy/Matplotlib 依赖。旧入口统一为 paper2overview / atlas_prepare_paper。
已有参考 PDF、本地数据库及生成文件未删除，旧功能代码可从 Git 历史恢复。

[架构](docs/architecture.md) · [变更记录](docs/CHANGELOG.md)

工作流源自 [SIVIA](https://github.com/exsinger-hub/Sivia)。新增代码与原创分析遵循 MIT，
第三方论文/插图和用户论文保留自身权利。
