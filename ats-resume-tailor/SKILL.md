---
name: ats-resume-tailor
description: Tailor structured resume indexes to job descriptions for ATS-focused resumes. Use when asked to create, revise, score, or render a targeted resume from YAML/JSON/Markdown resume data; generate match reports; infer job-description keywords with Codex instead of Ollama/local LLMs; or reproduce ats-tailor-style resume selection workflows.
---

# ATS Resume Tailor

## Principle

Use Codex for semantic judgment and conservative writing. Use the bundled script for deterministic parsing, keyword scoring, section selection, LaTeX escaping, and report generation.

Never invent qualifications, employers, dates, technologies, metrics, awards, or credentials. If a JD requests something missing from the index, surface it as a coverage gap instead of fabricating evidence.

## Workflow

1. Locate the inputs: job description, target company, target role, resume profile, and resume index.
   - Prefer an index directory containing `skills.yaml`, `projects.yaml`, `experience.yaml`, and `certifications.yaml`.
   - If the schema is unfamiliar, read `references/index-schema.md`.
2. Read the JD and extract:
   - explicit requirements and technologies;
   - implied concrete technologies, platforms, protocols, libraries, and domains;
   - missing terms that the resume index does not cover.
3. Write inferred terms to an output-side text file, one term per line, such as `expanded_terms.txt`.
   - Include only concrete technical terms.
   - Exclude soft skills, job titles, generic verbs, and claims not grounded in the JD.
4. Run the deterministic helper:

```powershell
python C:\Users\urnot\.codex\skills\ats-resume-tailor\scripts\tailor_resume.py `
  --index path\to\index `
  --profile path\to\profile.yaml `
  --jd path\to\job-description.txt `
  --company "Company" `
  --role "Role" `
  --expanded-terms path\to\expanded_terms.txt `
  --output path\to\output
```

5. Review `selection.json` and `match_report.md` against the JD.
   - If the deterministic score misses an obviously stronger item, use Codex judgment and explain the override in the report.
   - Keep the resume one page unless the user asks otherwise.
6. Optionally compile `resume.tex` with `pdflatex` and verify the page count when the user needs a submission-ready PDF.

## Codex Keyword Expansion

Before running the helper, create expanded terms from the JD yourself. Prefer terms that bridge JD wording to resume tags, for example:

- "distributed systems" from "scale high-traffic services";
- "REST APIs" from "backend service interfaces";
- "feature engineering" from "model input pipelines";
- "CI/CD" from "automated deployment workflows".

Do not add trendy adjacent terms unless the JD or the resume evidence supports them.

## Selection Rules

Read `references/selection-rubric.md` when selections are close, the JD is vague, or the output needs justification.

Default priority:

1. Direct evidence for required technologies and responsibilities.
2. Recent experience or projects with credible impact.
3. Role-relevant depth over breadth.
4. Skills backed by projects or work history.
5. Certifications only when relevant or requested.

## Resources

- `scripts/tailor_resume.py`: deterministic resume selection and rendering helper. Requires Python and PyYAML.
- `assets/resume_template.tex`: LaTeX structure to mirror when custom rendering is needed.
- `references/index-schema.md`: expected resume index fields.
- `references/selection-rubric.md`: judgment rules for Codex overrides and bullet rewriting.
