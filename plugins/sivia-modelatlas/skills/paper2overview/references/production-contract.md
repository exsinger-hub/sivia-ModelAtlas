# Paper-to-overview production contract

## Complete prompt

Fill these sections with actual content; never send placeholders to ImageGen.

1. **Purpose and authority.** One figure claim, intended section, language, print width and aspect ratio.
   The draft controls all scientific content. Mark pending results as pending.
2. **Composition.** Reading path, dominant region and secondary branches/feedback/validation zones.
   Specify relative locations and proportions without unnecessary pixel micromanagement.
3. **Regions.** Exact titles/short labels, meaningful objects, operations, inputs/outputs and grouping.
   Clearly separate drawn text from instructions.
4. **Connections.** Enumerate source → target and meaning; name signals/data products. Distinguish
   feedback and evaluation. No extra automatic connecting arrows.
5. **Visual grammar.** Consistent role colors, object scale, line weight and calm background. Source
   style governs composition only; never copy its scientific content.
6. **Typography.** Short readable labels, correct notation, no miniature paragraphs. At final print
   width normally aim around 8–10 pt equivalent; adapt to venue and inspect actual output. Shorten
   text rather than shrinking everything.
7. **Evidence policy.** Identify conceptual panels and real plots that must be inserted separately.
   No invented metrics, copied award results, absent algorithm names or bogus units.
8. **Reference adaptation/exclusions.** Name chosen visual principles and defects to avoid. No team
   numbers, institutional branding, award badges, screenshots or watermarks.
9. **Final checks.** Clear main path; all supported dependencies; exact text; no decorative numbers
   or unnecessary duplicated models.

## Brief JSON

Replace all example strings; this is a schema example, not a paper.

```json
{
  "claim": "What this draft's reader should understand",
  "manuscript_evidence": [
    {"locator": "Section 3.2 / PDF page 7", "supports": "The actual model and relationship drawn"}
  ],
  "model_relationships": [
    {"source": "Component name", "target": "Component name", "meaning": "Actual signal", "locator": "Section/page"}
  ],
  "references": [
    {"case_id": "c-infer-compare-redesign", "borrowed": "Shared input and branch/merge organization", "not_borrowed": "Voting models, numeric results and long labels"}
  ],
  "caption": "A caption grounded in the draft",
  "placement": "End of Introduction, before model definitions",
  "generation": {"backend": "Actual host image tool", "artifact_id": "Actual returned ID or local path", "status": "generated"},
  "review": {"status": "pending", "checks": [], "issues": []}
}
```

References can be empty only with a nonempty `reference_note` explaining why no reference was used.
Do not write review `passed` until viewing the final image. Record concrete checks of content, arrow
semantics, text and print-size readability, plus unresolved issues. User approval is not inferred.

Pairing checks required fields, image format, draft snapshot and file hashes. It cannot establish
scientific fidelity, prove a generation backend, or prove that a visual review occurred. The host is
responsible for truthful generation/review records. Keep the full prompt with the actual image.
