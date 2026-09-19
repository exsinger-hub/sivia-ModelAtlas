<h1 align="center">SIVIA ModelAtlas</h1>

<p align="center">为美赛论文生成 Overview</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> ·
  <a href="#showcase">示例</a> ·
  <a href="#library">插图知识库</a> ·
  <a href="docs/USAGE.md">使用文档</a>
</p>

ModelAtlas 是 [SIVIA](https://github.com/exsinger-hub/Sivia) 的数学建模版本。
输入已有论文或草稿，生成 Our Work / 方法总览图，同时保存完整绘图 prompt、图注和论文依据。

<a id="quick-start"></a>
<a id="setup"></a>

## Quick Start

需要 Python 3.10+，以及能读取本地文件、调用 ImageGen 的宿主。参考图页的读取另需 [Poppler](docs/USAGE.md)。

**1. 下载并安装**

```powershell
git clone https://github.com/exsinger-hub/sivia-ModelAtlas.git
cd sivia-ModelAtlas
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[mcp]"
```

<details>
<summary>macOS / Linux</summary>

```sh
git clone https://github.com/exsinger-hub/sivia-ModelAtlas.git
cd sivia-ModelAtlas
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[mcp]'
```

</details>

**2. 在宿主中打开项目，附上论文，发送：**

```text
请按 plugins/sivia-modelatlas/skills/paper2overview/SKILL.md 的流程，
为这篇美赛论文生成一张英文 Overview。
参考同类题的知识库插图，核对模型关系和箭头。
交付图片、完整 prompt 和图注。
```

**3. 查看成图，提出修改意见。** 例如：“放大核心模型，减少文字，保留目前的阅读顺序。”

这条流程由宿主完成生图；单独运行 CLI 只会准备论文与参考资料。[MCP 配置与命令说明](docs/USAGE.md)

<a id="showcase"></a>

## 示例

**From Forest to Farm** · 2025 ICM E · 来源论文 Finalist

<a href="docs/examples/2025-e-paper2overview/overview.png">
  <img src="docs/examples/2025-e-paper2overview/overview.png" width="100%" alt="ModelAtlas 生成示例：森林氮循环、农田管理、食物网与方案评价">
</a>

[高清图片](docs/examples/2025-e-paper2overview/overview.png) ·
[完整 prompt](docs/examples/2025-e-paper2overview/full-prompt.md) ·
[论文与制作记录](docs/examples/2025-e-paper2overview/README.md)

这张图由 ModelAtlas 阅读论文后生成。当前为 PNG 候选稿，出版尺寸审查尚未完成；修订前后对照及具体检查见制作记录。

<a id="library"></a>

## 插图知识库

按 A–F 题号整理 O/F 论文中的 Overview 和相关插图，另收录科研论文参考。
目前有 **8 篇获奖论文、18 个图例**，以及 **1 篇科研论文、2 个扩展图例**。

下面是作者原图，不是 ModelAtlas 生成结果。点击图片查看高清版本。

<table>
  <tr>
    <th width="50%">E · 生态建模</th>
    <th width="50%">C · 数据建模</th>
  </tr>
  <tr>
    <td width="50%" align="center" valign="middle">
      <a href="docs/assets/reference-overviews/2025-e-2515324-overview.jpg"><img src="docs/assets/reference-overviews/2025-e-2515324-overview.jpg" width="100%" alt="作者原图：2025 ICM E Finalist，氮循环模型的逐步扩展"></a>
    </td>
    <td width="50%" align="center" valign="middle">
      <a href="docs/assets/reference-overviews/2026-c-2627351-overview.png"><img src="docs/assets/reference-overviews/2026-c-2627351-overview.png" width="100%" alt="作者原图：2026 MCM C Finalist，投票推断与规则比较"></a>
    </td>
  </tr>
  <tr>
    <td align="center">2025 ICM E · Finalist<br><sub>模型继承与农业建议</sub></td>
    <td align="center">2026 MCM C · Finalist<br><sub>共享推断与并行分析</sub></td>
  </tr>
  <tr>
    <td align="center"><a href="knowledge-base/CATALOG.md#2025-e">论文与图例</a></td>
    <td align="center"><a href="knowledge-base/CATALOG.md#2026-c">论文与图例</a></td>
  </tr>
</table>

| 类别 | 常见方向 | 获奖论文 | 图例 |
| :---: | --- | :---: | :---: |
| [A](knowledge-base/CATALOG.md#2024-a) | 连续变化、动力学 | 1 | 2 |
| [B](knowledge-base/CATALOG.md#2024-b) | 离散决策、优化 | 1 | 2 |
| [C](knowledge-base/CATALOG.md#2024-c) | 数据洞察、统计建模 | 2 | 6 |
| [D](knowledge-base/CATALOG.md#2024-d) | 网络系统、运筹控制 | 1 | 2 |
| [E](knowledge-base/CATALOG.md#2024-e) | 环境、生态、可持续性 | 2 | 4 |
| [F](knowledge-base/CATALOG.md#2024-f) | 政策、社会决策 | 1 | 2 |

[全部图例](knowledge-base/CATALOG.md) · [科研参考](knowledge-base/CATALOG.md#research) ·
[入库标准](knowledge-base/README.md) · [结构化索引](src/modelatlas/knowledge/corpus.json) ·
[展示图片许可](docs/assets/reference-overviews/README.md)

---

[使用文档](docs/USAGE.md) ·
[绘图规范](plugins/sivia-modelatlas/skills/paper2overview/references/production-contract.md) ·
[架构](docs/architecture.md) · [变更记录](docs/CHANGELOG.md) · [MIT License](LICENSE)

基于 [SIVIA](https://github.com/exsinger-hub/Sivia)。第三方论文与插图保留各自版权。
