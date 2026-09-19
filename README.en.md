<h1 align="center">SIVIA ModelAtlas</h1>

<p align="center">Turn MCM/ICM papers into overview figures</p>

<p align="center">
  <a href="README.md">中文</a> · English<br>
  <a href="#showcase">Figure comparisons</a> ·
  <a href="#quick-start">Quick Start</a> ·
  <a href="#library">Reference library</a> ·
  <a href="docs/USAGE.md">Documentation (中文)</a>
</p>

Start with a paper or draft. Generate an Our Work / method overview, with the full prompt and caption.
After approving the image, optionally use [Sivia](https://github.com/exsinger-hub/Sivia) to rebuild it as an editable PowerPoint figure.

<a id="showcase"></a>

## Figure comparisons

Organized by problem, year, paper and generation round. Click any image for full resolution.

[E · Ecology & environment](#category-e) · 2025 · 1 paper · 2 rounds

<a id="category-e"></a>

### E · Ecology & environment / 2025

<a id="2025-e-forest-to-farm"></a>

**From Forest to Farm** · 2025 ICM E · Source paper: Finalist · Team 2515324

<table>
  <tr>
    <th width="50%">Original paper figure</th>
    <th width="50%">ModelAtlas · Round 2 / current</th>
  </tr>
  <tr>
    <td width="50%" align="center" valign="middle">
      <a href="docs/assets/reference-overviews/2025-e-2515324-overview.jpg"><img src="docs/assets/reference-overviews/2025-e-2515324-overview.jpg" width="100%" alt="Original Figure 2 from a 2025 ICM E Finalist paper: progression through three nitrogen-cycle models"></a>
    </td>
    <td width="50%" align="center" valign="middle">
      <a href="docs/examples/2025-e-paper2overview/overview.png"><img src="docs/examples/2025-e-paper2overview/overview.png" width="100%" alt="ModelAtlas round 2: forest, farmland, food web and scenario evaluation, continuing right to left along the bottom"></a>
    </td>
  </tr>
  <tr>
    <td align="center"><sub>Figure 2 · PDF p4 · Authors’ original</sub></td>
    <td align="center"><sub>Redesigned from the full paper · PNG 1536 × 1024</sub></td>
  </tr>
</table>

#### Generation rounds

<table>
  <tr>
    <th width="50%">Round 1 · Initial draft</th>
    <th width="50%">Round 2 · Revision</th>
  </tr>
  <tr>
    <td width="50%" align="center" valign="middle">
      <a href="docs/examples/2025-e-paper2overview/overview-v1.png"><img src="docs/examples/2025-e-paper2overview/overview-v1.png" width="100%" alt="ModelAtlas round 1: initial model scenes and analysis layout"></a>
    </td>
    <td width="50%" align="center" valign="middle">
      <a href="docs/examples/2025-e-paper2overview/overview.png"><img src="docs/examples/2025-e-paper2overview/overview.png" width="100%" alt="ModelAtlas round 2: revised harvest arrow, reading order and forest decoration"></a>
    </td>
  </tr>
  <tr>
    <td align="center"><sub>Forest → farmland → food web</sub><br><a href="docs/examples/2025-e-paper2overview/prompt.md">Round 1 prompt</a></td>
    <td align="center"><sub>Harvest originates at crops; analysis follows the food web</sub><br><a href="docs/examples/2025-e-paper2overview/correction-prompt.md">Round 2 prompt</a></td>
  </tr>
</table>

[Current image, full resolution](docs/examples/2025-e-paper2overview/overview.png) ·
[Full prompt](docs/examples/2025-e-paper2overview/full-prompt.md) ·
[Paper & production notes](docs/examples/2025-e-paper2overview/README.en.md) ·
[Original image & license](docs/assets/reference-overviews/README.md)

The award belongs to the source paper. Generated figures are redesign examples; print-size checks and user approval remain pending.

<a id="quick-start"></a>
<a id="setup"></a>

## Quick Start

Requires Python 3.10+ and a host that can read local files and call ImageGen. Viewing reference PDF pages also requires [Poppler](docs/USAGE.md).

**1. Clone and install**

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

**2. Open the project in your host, attach a paper, and send:**

```text
Follow plugins/sivia-modelatlas/skills/paper2overview/SKILL.md
to create an English overview figure for this MCM/ICM paper.
Use relevant library figures for composition, and verify model relationships and arrows against the paper.
Deliver the image, full prompt and caption.
```

**3. Review and revise.** For example: “Enlarge the core model, reduce the text, and keep the current reading order.”

**4. Rebuild as an editable PowerPoint figure (optional)**

After approving the image, continue with [Sivia](https://github.com/exsinger-hub/Sivia).
Install Sivia separately; this step requires Node.js and an available PowerPoint / WPS backend.
Installing ModelAtlas alone does not provide this capability. Attach the approved image and send:

```text
Use Sivia to faithfully rebuild this approved overview as an editable PPTX.
Target: PowerPoint. Create overview-editable.pptx, preserving the image’s aspect ratio and layout.
Use native editable objects for text, equations, shapes and arrows.
Keep complex artwork as separate images, with editable labels.
Work in the background without changing other presentations. Check editability, text overflow and connectors.
Deliver the PPTX and an exported preview; identify any elements that remain raster images.
```

For WPS, change the target to “WPS Presentation.” This step rebuilds individual objects, rather than embedding the entire PNG as a slide.
[Dependencies & delivery checks (中文)](docs/USAGE.md#editable-ppt)

Image generation runs in the host. The CLI only prepares the paper and references.
[MCP configuration & commands (中文)](docs/USAGE.md)

<a id="library"></a>

## Reference library

Search by problem A–F and year: 26 O/F papers with 36 figure cases, plus 3 research papers with 4 additional cases.
[Figure catalog](knowledge-base/CATALOG.md) · [Sources & year coverage](knowledge-base/SOURCES.md) · [Search & inclusion criteria (中文)](knowledge-base/README.md)

---

[Documentation (中文)](docs/USAGE.md) · [Figure guidelines](plugins/sivia-modelatlas/skills/paper2overview/references/production-contract.md) ·
[Showcase index](docs/examples/showcase.json) · [Changelog](docs/CHANGELOG.md) · [MIT License](LICENSE)

Based on [Sivia](https://github.com/exsinger-hub/Sivia). Third-party papers and figures retain their respective copyrights.
