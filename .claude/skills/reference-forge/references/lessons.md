# Lessons — real traps from building this skill (2026-09-26)

1. **The Met search wants `q` LAST.** With `q` before `departmentId`, the API
   silently returned `{"total":0}` (and once a truncated 4 hits for a query
   worth 800). Same query, q last: 28 cabassets. `ref_search.py` builds the
   URL in that order; never "tidy" it into alphabetical params.
2. **The search is keyword-loose.** "chapel de fer" returned late-Roman shield
   bosses; "kettle" returned a Japanese sword guard. Always pass `--must`
   class words (and a date window) — it is what makes the sheet relevant.
3. **Use period vocabulary.** "kettle hat" finds 1 object, "war hat" 0; the
   brimmed-helmet family is catalogued as morion (43), cabasset (28), sallet
   (47). sources.md keeps the term table — extend it when a search works.
4. **Museum titles carry HTML and typographic dashes** (`<i>Tsuba</i>`,
   "ca. 1575–80") — cleaned before captioning, or the sheet prints tags and
   tofu boxes.
5. **Measurements are structured.** `measurements[].elementMeasurements`
   gives numeric cm/kg — use those for ratios; the `dimensions` string is for
   humans and mixes inches and centimetres.
6. **Museum photos are 3/4-from-above on grey.** Compare at that angle, not at
   the diagonal card angle, or proportion errors hide.
