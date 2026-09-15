---
name: verify-source-links
description: Verify source links before including them in answers. Use when Codex plans to cite sources, list references, include URLs, add footnotes, link to local files, or provide source-backed claims in a final response; especially use after web browsing, research, document review, news/current-info lookups, product comparisons, academic references, legal/medical/financial citations, or any task where broken, stale, mismatched, or unsupported links would undermine the answer.
---

# Verify Source Links

## Overview

Ensure every source link included in the response has been checked and actually supports the nearby claim. Replace, repair, or omit links that cannot be verified.

## Workflow

1. Build the source list only from material actually inspected during the task. Do not cite memory-only URLs, search-result snippets, guessed URLs, or links copied from another page without opening or otherwise validating them.

2. Verify each candidate link before finalizing:
   - Open the exact URL, DOI landing page, PDF, documentation page, local file, or cited resource with the best available tool.
   - Confirm the destination loads, is not a 404/error page, and is not merely a search result, homepage redirect, login wall, or unrelated landing page.
   - Confirm the page title, publisher/domain, date when relevant, and visible content match the source being cited.
   - Confirm the linked source supports the specific claim attached to it.
   - Prefer canonical, official, or primary-source URLs. Strip obvious tracking parameters when doing so preserves the destination.

3. Repair bad links:
   - If a link redirects unexpectedly, cite the final canonical page if it is correct.
   - If a link is broken, stale, gated, or mismatched, look for an official replacement or a more direct source.
   - If no replacement can be verified, omit the link. If the missing verification affects the answer materially, say so briefly.

4. Treat local file links as sources too:
   - Verify the file exists before linking it.
   - Use absolute clickable file links with a line number when relevant.
   - Do not link to generated or temporary files unless the user needs that artifact.

5. Final response checklist:
   - Every included link was opened or otherwise validated in this turn, unless the user explicitly supplied source contents and asked not to browse.
   - Every cited source supports the adjacent claim.
   - Dates are checked for time-sensitive claims.
   - No broken links, bare search URLs, tracking-only URLs, irrelevant redirects, or unsupported source lists remain.

