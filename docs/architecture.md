# Architecture

The parallel project keeps Sivia's source → figure claim → design → draw → review → correction → paired-case workflow, specialized for modeling papers and data figures. It has its own repository, plugin namespace and local library.

CLI and eight MCP tools call the same Python implementation. AnySearch discovers academic papers through its documented 3.1.1 REST endpoints. Local PDF/TXT/Markdown import stores source hashes and page text. Source-grounded cards are curated separately and retrieved with transparent token overlap ranking (not embeddings or an LLM reranker).

The renderer takes JSON, optionally binding CSV columns. It validates numeric shape, alignment, finite values, time ordering, interval meaning and optimization directions before plotting. Matplotlib creates PNG/SVG/PDF; SVG text remains text and PDF embeds TrueType fonts. A workflow spec is a lightweight editable node/edge layout, not a full general-purpose diagram editor. Actual model fitting, OCR, native PowerPoint and rich ImageGen scenes are separate host-agent capabilities.

Each run is immutable by convention and gets a unique directory. Data snapshot, normalized spec, full input claim, artifact hashes and mechanical audit travel together. The SQLite run index links the bundle to the card/source IDs. A local HTML gallery embeds only produced artifacts and supports filtering and downloads without a service.

Example numbers are synthetic fixture data. Tests verify rendering behavior, numerical semantics, source persistence, data rejection, bundle tamper detection and an actual MCP stdio round trip. These are engineering checks; they do not establish model performance or human approval.
