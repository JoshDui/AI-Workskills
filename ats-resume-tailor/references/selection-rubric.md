# Selection Rubric

Use deterministic scores as a baseline, then apply Codex judgment when the JD or index wording is too indirect for exact matching.

## Strong Match

Prefer an item when it shows at least two of:

- required technology appears in tags, tech stack, skills used, or bullets;
- responsibilities closely match the JD's day-to-day work;
- impact is quantified or clearly outcome-oriented;
- item is recent or ongoing;
- the candidate can defend the claim from the stored evidence.

## Weak Match

Downgrade an item when:

- it shares only generic terms such as "software", "team", "design", or "support";
- the technology is listed only as a familiar skill with no evidence;
- the project domain is attractive but the implementation work is unrelated;
- a stronger recent item demonstrates the same capability.

## Coverage Gaps

Report missing requirements explicitly. Do not rewrite bullets to imply missing experience.

Examples:

- JD asks for Kubernetes but the index only has Docker: report Kubernetes as a gap.
- JD asks for React Native but the index only has React web: report React Native as a gap unless mobile evidence exists.
- JD asks for Spark and the index has pandas pipelines: describe data-pipeline relevance but do not claim Spark.

## Bullet Rewriting

Rewrite bullets only from existing evidence.

Good rewrite pattern:

```text
Built FastAPI service endpoints for X workflow, reducing Y manual step by Z through validation and async processing.
```

Avoid:

- adding metrics not in the index;
- changing a coursework project into production experience;
- swapping technologies to match the JD;
- stuffing keyword lists into one bullet.

## Override Notes

When overriding the script's selection, record a short note in `match_report.md`:

```text
Override: selected Project A over Project B because the JD emphasizes payment workflow reliability, and Project A has stronger integration-test evidence despite a lower exact keyword score.
```
