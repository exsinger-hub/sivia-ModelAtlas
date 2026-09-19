<h1 align="center">SIVIA · ModelAtlas</h1>
<h3 align="center">让美赛论文的方法与模型，一图读懂。</h3>

<p align="center">
  <a href="pyproject.toml"><img src="https://img.shields.io/badge/version-0.3.0-007C91?style=flat-square" alt="Version 0.3.0"></a>
  <a href="#showcase"><img src="https://img.shields.io/badge/Paper_%E2%86%92_Overview-MCM_%2F_ICM-355C7D?style=flat-square" alt="Paper to Overview for MCM and ICM"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-64748B?style=flat-square" alt="MIT license"></a>
</p>

<p align="center">
  <a href="#showcase"><b>看实际成图</b></a> &nbsp;·&nbsp;
  <a href="#library">逛插图知识库</a> &nbsp;·&nbsp;
  <a href="#quick-start">直接使用</a> &nbsp;·&nbsp;
  <a href="#setup">安装与运行</a>
</p>

**输入已有论文或草稿，输出忠于正文的 Overview，以及与图片配对的完整 prompt。**

ModelAtlas 是与 [SIVIA](https://github.com/exsinger-hub/Sivia) 并行的数学建模版本，主要面向美赛 MCM/ICM。
从论文中提炼模型关系、输入输出与验证逻辑，借鉴 O/F 论文的插图表达，形成适合 **Our Work / 方法总览** 的科学图示。
当前只做 **Paper → Overview**，不代替解题、论文写作或独立数据作图。

<a id="showcase"></a>

## 01 / 实际成图

<table>
  <tr>
    <td>
      <strong>From Forest to Farm</strong><br>
      <sub>2025 ICM E · 来源论文 Finalist · Team 2515324 ｜ ModelAtlas 新生成</sub>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="docs/examples/2025-e-paper2overview/overview.png">
        <img src="docs/examples/2025-e-paper2overview/overview.png" width="100%" alt="ModelAtlas 新生成的 Overview：森林氮循环、农田管理、七节点食物网、方案比较与可持续农业建议">
      </a>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="docs/examples/2025-e-paper2overview/overview.png"><b>查看高清成图</b></a> ·
      <a href="docs/examples/2025-e-paper2overview/full-prompt.md">完整 prompt</a> ·
      <a href="docs/examples/2025-e-paper2overview/README.md">案例与论文依据</a> ·
      <a href="docs/examples/2025-e-paper2overview/brief.json">审查记录</a>
    </td>
  </tr>
</table>

**这张图是本项目实际生成的测试结果，不是论文原图。**
读取完整 25 页论文，以“森林基线 → 农田管理 → 多物种食物网”为主线，再连接方案比较、敏感性分析与农业建议。

- **模型有层次**：三个模型如何继承与扩展，在主图中直接可见。
- **箭头有含义**：模型演进、营养传递与竞争关系分开编码。
- **建议有边界**：已模拟情景与文献支持的固氮、秸秆利用建议分开呈现。

<sub>实际交付：1536 × 1024 PNG + 两轮 prompt + 逐页证据。已完成生成、修正和内容自审；独立审查、印刷字号与用户验收仍待完成。来源论文的获奖身份不代表这张新图获奖或得到原作者认可。</sub>

<details>
<summary><b>展开看修订过程：初稿 → 修订稿</b></summary>

<table>
  <tr>
    <th width="50%">第一次生成</th>
    <th width="50%">修订后交付</th>
  </tr>
  <tr>
    <td width="50%" align="center" valign="middle">
      <a href="docs/examples/2025-e-paper2overview/overview-v1.png"><img src="docs/examples/2025-e-paper2overview/overview-v1.png" width="100%" alt="第一次生成：收获箭头位置和下排分析入口仍有歧义"></a>
    </td>
    <td width="50%" align="center" valign="middle">
      <a href="docs/examples/2025-e-paper2overview/overview.png"><img src="docs/examples/2025-e-paper2overview/overview.png" width="100%" alt="修订版本：收获从作物引出，模型到分析形成连续阅读路径"></a>
    </td>
  </tr>
  <tr>
    <td valign="top">收获箭头靠近杂草，分析入口与模型衔接不清；部分小标签需要放大。</td>
    <td valign="top">收获箭头从作物引出；主线按 a → b → c → d → e → f 连续阅读；放大关键标签。</td>
  </tr>
  <tr>
    <td align="center"><a href="docs/examples/2025-e-paper2overview/prompt.md">初次完整 prompt</a></td>
    <td align="center"><a href="docs/examples/2025-e-paper2overview/correction-prompt.md">本轮修正 prompt</a></td>
  </tr>
</table>

这是同一论文的一次实际执行与修订，不是两个独立风格，也不是未见样本盲测。没有重跑原论文模型或生成虚构结果曲线。
[完整执行链](docs/examples/2025-e-paper2overview/full-prompt.md) · [文件配对校验](docs/examples/2025-e-paper2overview/integrity-audit.json)

</details>

<a id="library"></a>

## 02 / 插图知识库

**看图学表达，用正文定内容。** 知识库按美赛题号和表达任务组织：既能检索同类题，也能借鉴跨题型的模型继承、并行分析、反馈与决策结构。

| 获奖论文参考 | 插图案例 | 科研延伸 |
| :---: | :---: | :---: |
| **8 篇 O/F 论文** | **18 个获奖图例** | **1 篇预印本 · 2 个图例** |

### 精选参考 · 模型继承与并行分析

下方展示**作者原图，不是 ModelAtlas 生成结果**。保留完整画面与原始比例；点击图片打开高清图。
模型与结论属于来源论文，这里借鉴的是视觉组织方式。

<table>
  <tr>
    <td width="50%" valign="top" align="center">
      <strong>E · 生态系统与可持续性</strong><br>
      <sub>2025 ICM E · Finalist · 2515324</sub><br>
      <b>从基础模型到扩展模型</b>
    </td>
    <td width="50%" valign="top" align="center">
      <strong>C · 数据洞察与规则设计</strong><br>
      <sub>2026 MCM C · Finalist · 2627351</sub><br>
      <b>共享推断、并行分析、决策合流</b>
    </td>
  </tr>
  <tr>
    <td width="50%" align="center" valign="middle">
      <a href="docs/assets/reference-overviews/2025-e-2515324-overview.jpg">
        <img src="docs/assets/reference-overviews/2025-e-2515324-overview.jpg" width="100%" alt="作者原图：2025 ICM E Finalist 的氮循环模型继承与绿色农业建议 overview">
      </a>
    </td>
    <td width="50%" align="center" valign="middle">
      <a href="docs/assets/reference-overviews/2026-c-2627351-overview.png">
        <img src="docs/assets/reference-overviews/2026-c-2627351-overview.png" width="100%" alt="作者原图：2026 MCM C Finalist 的投票推断、并行分析与规则再设计 overview">
      </a>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <b>借鉴什么</b><br>把模型继承画成依赖关系，把应用建议留在独立区域。<br>
      <sub>PDF p4 · Figure 2<br>e-model-inheritance-overview</sub>
    </td>
    <td width="50%" valign="top">
      <b>借鉴什么</b><br>共享估计结果分为分析支路，再汇入同一个决策出口。<br>
      <sub>PDF p5 · Figure 1<br>c-infer-compare-redesign</sub>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="docs/assets/reference-overviews/2025-e-2515324-overview.jpg">高清原图</a> ·
      <a href="https://github.com/LUKEQ420/MCM-ICM-2025-E-Nitrogen-Cycling-Model/blob/fb579acd7107706e055c8a10f921f9f56498a06a/paper/2515324.pdf">来源论文</a> ·
      <a href="knowledge-base/CATALOG.md#2025-e">案例说明</a>
    </td>
    <td align="center">
      <a href="docs/assets/reference-overviews/2026-c-2627351-overview.png">高清原图</a> ·
      <a href="https://github.com/alectimison-maker/2026MCM-ICM_C/blob/2fcf7bb344e6fa7c295ec771b5be79c3a9ebd361/2627351_submitted_paper.pdf">来源论文</a> ·
      <a href="knowledge-base/CATALOG.md#2026-c">案例说明</a>
    </td>
  </tr>
</table>

<sub>两张展示图来自作者 MIT 许可仓库，未裁切或重绘。[来源、版权与校验记录](docs/assets/reference-overviews/README.md)。作者原图没有本项目生成 prompt，不与上方生成案例混为一类。</sub>

### A–F 分类入口

| 原题类别 | 常见建模方向 | 已收录获奖论文 | 参考图例 |
| :---: | --- | --- | :---: |
| [**A**](knowledge-base/CATALOG.md#2024-a) | 连续变化、动力学 | 2024 O · 2400996 | 2 |
| [**B**](knowledge-base/CATALOG.md#2024-b) | 离散决策、优化 | 2024 O · 2419984 | 2 |
| [**C**](knowledge-base/CATALOG.md#2024-c) | 数据洞察、统计建模 | 2024 O · 2401919；2026 F · 2627351 | 6 |
| [**D**](knowledge-base/CATALOG.md#2024-d) | 网络系统、运筹控制 | 2024 O · 2417831 | 2 |
| [**E**](knowledge-base/CATALOG.md#2024-e) | 环境、生态、可持续性 | 2024 O · 2413552；2025 F · 2515324 | 4 |
| [**F**](knowledge-base/CATALOG.md#2024-f) | 政策、社会决策 | 2024 O · 2422054 | 2 |

类别是检索入口，不是永久题型定义；**题号 F ≠ 奖项 F（Finalist）**。科研论文用于补充表达方法，单列为扩展参考，不冒充美赛获奖论文。

[完整逐图目录](knowledge-base/CATALOG.md) · [入库标准](knowledge-base/README.md) · [科研延伸](knowledge-base/CATALOG.md#research) · [结构化索引](src/modelatlas/knowledge/corpus.json)

<details>
<summary><b>参考库如何保持可追溯？</b></summary>

每个图例记录年份、题号、论文版本与 SHA-256、物理 PDF 页码、图号、官方 O/F 证据、构图分析及不应迁移的内容。
检索默认 Overview；已收录机制图、算法图与数据图继续作为局部表达参考，不代表新增独立绘图功能。

这仍是种子库，不是全历年论文全集。除上面两张保留作者许可的展示图外，仓库保存元数据与原创分析，
第三方 PDF/页面缓存在本地，不自动公开。新生成的测试案例与作者参考库分开管理。

</details>

<a id="quick-start"></a>

## 03 / 直接使用

上传已有论文或草稿，复制下面的需求。**你不需要自己编写绘图 prompt。**

```text
使用 SIVIA ModelAtlas，为这篇美赛论文生成一张 Our Work / Overview。

阅读全文，以正文和公式为依据，提炼本图的核心信息，
梳理模型继承、输入输出、并行分析、验证与决策之间的关系。
从知识库选择表达任务相近的插图，只借鉴构图，不复制别人的模型或结果。

先说明图意和分区，再编写逐区域的完整 ImageGen prompt，实际生成图片。
检查箭头、术语、布局与缩小后的可读性；发现问题后修正并保留前一版。

交付：实际图片、完整 prompt、论文依据、图注与放置建议。
只做 Paper → Overview，不解题、不写论文、不制作 PPT。
```

### 从论文到图，保留中间依据

**读全文 → 查阅参考图 → 设计图意与布局 → ImageGen 生成 → 审查修正 → 图片与 prompt 配对**

| 输入 | 工作方式 | 交付 |
| --- | --- | --- |
| PDF / Markdown / TXT / TeX 论文或草稿 | 唯一主 skill：`paper2overview`；参考库辅助构图，论文约束内容 | Overview 图片、完整 prompt、页码依据、图注、审查记录 |

需要调整时，指出区域与目标，例如：“放大核心模型区，保留其他布局；把模型继承与数据流的箭头区分开。”
每次修订保留对应图片和 prompt，方便回看。

<a id="setup"></a>

## 04 / 安装与运行

需要 **Python 3.10+**；查看参考 PDF 图页需 Poppler 的 `pdftoppm`。
实际成图还需要宿主会话提供 ImageGen；项目不内置模型或 API 凭据。

```sh
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
python -m pip install -e '.[mcp,dev]'

modelatlas coverage
modelatlas styles --problem E
modelatlas paper2overview path/to/paper.pdf --problem E
```

Windows 可使用 [bootstrap.ps1](scripts/bootstrap.ps1)。
**CLI 的 `paper2overview` 只准备论文快照、提取正文并推荐参考，不会单独生成图片**；
实际阅读、设计、生成和审查由宿主按 skill 执行。没有生图能力时，只交付设计/prompt 并明确说明未成图。

<details>
<summary><b>展开：参考检索、成图归档与 AnySearch</b></summary>

```sh
modelatlas reference e-model-inheritance-overview
modelatlas styles --role all --collection all

modelatlas literature "COMAP 2025 2515324 Finalist" --mode web
modelatlas literature "mathematical modeling overview" --mode academic

modelatlas pair-overview SESSION_DIR --image overview.png --prompt prompt.md --brief brief.json
modelatlas audit-overview BUNDLE_DIR
```

AnySearch 用于公开来源检索；结果不自动进入已审阅知识库。
可选 `ANYSEARCH_API_KEY`，不要把私人论文或凭据作为检索内容。
全局 `--workspace` 放在子命令前，或设置 `MODELATLAS_HOME`：
CLI 默认当前目录 `.modelatlas`，MCP 默认用户目录 `.modelatlas`；相同配置可共享缓存。

[制作契约](plugins/sivia-modelatlas/skills/paper2overview/references/production-contract.md)定义完整 prompt、论文证据和审查记录。
文件校验只证明文件完整性，不等于科学内容、图片质量或用户验收通过。

</details>

<details>
<summary><b>展开：MCP 接入与插件位置</b></summary>

插件源码：[plugins/sivia-modelatlas](plugins/sivia-modelatlas)。
只提供一个主 skill：`paper2overview`，七个底层工具服务同一条工作流：
准备论文、检索插图、查看覆盖、获取参考页、找论文、图片/prompt 配对和文件完整性校验。

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

替换为本机绝对路径。复制插件后可设置 `MODELATLAS_PYTHON` 指向已安装本包的 Python。
源码更新不代表宿主已重新安装；扫描 PDF 需先 OCR。

</details>

<details>
<summary><b>展开：开发、版本范围与历史</b></summary>

```sh
python -m pytest -q
python -m build
```

0.3.0 将产品聚焦于 Paper → Overview，移除了独立数值绘图后端、配方/demo、通用 HTML 图库、
旧 SQLite 卡片接口及旁支 skills，并去掉 NumPy/Matplotlib 依赖。
已有参考 PDF、本地数据库和生成文件未删除，旧代码可从 Git 历史恢复。

[架构](docs/architecture.md) · [变更记录](docs/CHANGELOG.md)

</details>

---

<p align="center">
  工作流源自 <a href="https://github.com/exsinger-hub/Sivia">SIVIA</a> · 专注数学建模论文的 Paper → Overview<br>
  <sub>README 借鉴 SIVIA 的分类图片卡片与图文配对导航。新增代码与原创分析采用 MIT；来源论文、作者插图与用户稿件保留各自权利。</sub>
</p>
