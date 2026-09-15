#!/usr/bin/env python3
"""Deterministic helper for the ats-resume-tailor skill.

The script intentionally avoids embeddings and local LLM calls. Codex supplies
semantic keyword expansion in --expanded-terms; this helper performs structured
matching, selection, LaTeX escaping, and report generation.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - clear runtime message is enough
    yaml = None


MONTHS = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}

AMBIGUOUS_SHORT_TERMS = {"go", "c", "r"}

GAP_STOPWORDS = {
    "AI",
    "API",
    "BSc",
    "CEO",
    "CRM",
    "CTO",
    "CV",
    "HR",
    "ID",
    "IT",
    "JD",
    "KPI",
    "ML",
    "PDF",
    "PM",
    "QA",
    "ROI",
    "SLA",
    "UI",
    "UX",
    "VP",
    "The",
    "This",
    "That",
    "These",
    "Those",
    "What",
    "When",
    "Where",
    "Which",
    "While",
    "Who",
    "How",
    "Why",
    "Our",
    "Your",
    "You",
    "We",
    "They",
    "Experience",
    "Requirements",
    "Responsibilities",
    "Skills",
    "Team",
    "Role",
    "Position",
    "Company",
    "Singapore",
    "Remote",
    "Hybrid",
    "Engineer",
    "Developer",
    "Analyst",
    "Intern",
    "Senior",
    "Junior",
    "Strong",
    "Good",
    "Great",
    "New",
    "Build",
    "Develop",
    "Design",
    "Manage",
    "Support",
    "Maintain",
    "Implement",
    "Deliver",
    "Collaborate",
    "Communicate",
}

GENERIC_MATCH_TERMS = {str(term).strip().lower() for term in GAP_STOPWORDS} | {
    "architecture",
    "driven",
    "engineering",
    "event",
    "language",
    "languages",
    "programming",
    "service",
    "services",
    "software",
}


def load_yaml(path: Path) -> Any:
    if yaml is None:
        raise SystemExit("PyYAML is required. Install it with: python -m pip install pyyaml")
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def normalize(text: Any) -> str:
    return re.sub(r"\s+", " ", str(text).strip().lower())


def dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        clean = str(item).strip()
        key = normalize(clean)
        if clean and key not in seen:
            seen.add(key)
            out.append(clean)
    return out


def keyword_in_text(keyword: str, text_lower: str, text_original: str = "") -> bool:
    keyword = str(keyword).strip()
    if not keyword:
        return False
    kw = normalize(keyword)
    compact = kw.replace(" ", "").replace("-", "")
    has_special = not compact.isalnum()
    if has_special:
        return kw in text_lower
    if kw in AMBIGUOUS_SHORT_TERMS or (len(kw) <= 2 and kw.isalpha()):
        target = text_original if text_original else text_lower
        needle = keyword if text_original else kw
        return bool(re.search(r"\b" + re.escape(needle) + r"\b", target))
    return bool(re.search(r"\b" + re.escape(kw) + r"\b", text_lower))


def parse_terms_file(path: Path | None) -> list[str]:
    if not path:
        return []
    raw = path.read_text(encoding="utf-8")
    terms: list[str] = []
    for line in raw.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        terms.extend(part.strip() for part in line.split(",") if part.strip())
    return dedupe(terms)


def tech_terms(tech_stack: dict[str, Any]) -> list[str]:
    terms: list[str] = []
    if not isinstance(tech_stack, dict):
        return terms
    for value in tech_stack.values():
        if isinstance(value, list):
            terms.extend(str(v) for v in value)
        elif value:
            terms.append(str(value))
    return terms


def project_terms(project: dict[str, Any]) -> list[str]:
    return dedupe(
        [project.get("name", "")]
        + list(project.get("ats_tags", []) or [])
        + tech_terms(project.get("tech_stack", {}) or {})
    )


def role_terms(role: dict[str, Any]) -> list[str]:
    return dedupe(list(role.get("skills_used", []) or []) + list(role.get("ats_tags", []) or []))


def skill_terms(skill: dict[str, Any]) -> list[str]:
    return dedupe([skill.get("name", "")] + list(skill.get("ats_keywords", []) or []))


def cert_terms(cert: dict[str, Any]) -> list[str]:
    return dedupe([cert.get("name", "")] + list(cert.get("ats_keywords", []) or []))


def build_project_text(project: dict[str, Any]) -> str:
    parts = [
        project.get("name", ""),
        project.get("summary", ""),
        " ".join(project.get("ats_tags", []) or []),
        " ".join(tech_terms(project.get("tech_stack", {}) or {})),
        " ".join(project.get("responsibilities", []) or []),
        " ".join(project.get("impact", []) or []),
    ]
    return " ".join(str(p) for p in parts if p)


def build_role_text(role: dict[str, Any]) -> str:
    parts = [
        role.get("title", ""),
        role.get("company", ""),
        " ".join(role.get("skills_used", []) or []),
        " ".join(role.get("ats_tags", []) or []),
        " ".join(role.get("bullets", []) or []),
    ]
    return " ".join(str(p) for p in parts if p)


def collect_known_terms(skills: dict[str, Any], projects: dict[str, Any], exp: dict[str, Any], certs: dict[str, Any]) -> list[str]:
    terms: list[str] = []
    for category in skills.get("categories", []) or []:
        for skill in category.get("skills", []) or []:
            terms.extend(skill_terms(skill))
    for project in projects.get("projects", []) or []:
        terms.extend(project_terms(project))
    for role in exp.get("roles", []) or []:
        terms.extend(role_terms(role))
    for cert in certs.get("certifications", []) or []:
        terms.extend(cert_terms(cert))
    return dedupe([term for term in terms if normalize(term) not in GENERIC_MATCH_TERMS])


def score_item(
    item_terms: list[str],
    item_text: str,
    target_terms: list[str],
    jd_lower: str,
    jd_text: str,
) -> tuple[float, list[str]]:
    item_term_keys = {normalize(t) for t in item_terms if normalize(t)}
    target_keys = {normalize(t) for t in target_terms if normalize(t)}
    item_lower = item_text.lower()
    hits: set[str] = set()

    for term in item_terms:
        key = normalize(term)
        if key in GENERIC_MATCH_TERMS:
            continue
        if key in target_keys or keyword_in_text(term, jd_lower, jd_text):
            hits.add(term)

    for term in target_terms:
        if normalize(term) in GENERIC_MATCH_TERMS:
            continue
        if normalize(term) in item_term_keys or keyword_in_text(term, item_lower, item_text):
            hits.add(term)

    hit_count = len({normalize(h) for h in hits})
    if hit_count == 0:
        return 0.0, []

    ratio = hit_count / max(len(item_term_keys), 1)
    coverage = min(hit_count / 6.0, 1.0)
    keyword_bonus = 0.08 * math.log2(1 + hit_count)
    overlap_bonus = (0.4 * ratio + 0.6 * coverage) * 0.35
    return keyword_bonus + overlap_bonus, sorted(hits, key=lambda s: normalize(s))


def parse_end_date(period: str) -> datetime:
    text = str(period)
    if "present" in text.lower():
        return datetime.now()
    matches = re.findall(r"([A-Za-z]{3,9})\s+(\d{4})", text)
    if matches:
        month_text, year_text = matches[-1]
        return datetime(int(year_text), MONTHS.get(month_text[:3].lower(), 6), 1)
    years = re.findall(r"(\d{4})", text)
    if years:
        return datetime(int(years[-1]), 6, 1)
    return datetime(1900, 1, 1)


def parse_start_date(period: str) -> datetime:
    text = str(period)
    matches = re.findall(r"([A-Za-z]{3,9})\s+(\d{4})", text)
    if matches:
        month_text, year_text = matches[0]
        return datetime(int(year_text), MONTHS.get(month_text[:3].lower(), 6), 1)
    years = re.findall(r"(\d{4})", text)
    if years:
        return datetime(int(years[0]), 6, 1)
    return datetime(1900, 1, 1)


def recency_multiplier(period: str) -> float:
    end_date = parse_end_date(period)
    now = datetime.now()
    months_ago = (now.year - end_date.year) * 12 + (now.month - end_date.month)
    if months_ago <= 0:
        return 1.10
    if months_ago <= 12:
        return 1.05
    if months_ago <= 24:
        return 1.02
    return 1.00


def latex_escape(text: Any) -> str:
    value = "" if text is None else str(text)
    replacements = [
        ("\\", r"\textbackslash{}"),
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("~", r"\textasciitilde{}"),
        ("^", r"\textasciicircum{}"),
    ]
    for old, new in replacements:
        value = value.replace(old, new)
    return value


def link_target(kind: str, value: str) -> tuple[str, str]:
    value = str(value).strip()
    if not value:
        return "", ""
    if value.startswith("http://") or value.startswith("https://"):
        display = value.replace("https://", "").replace("http://", "").rstrip("/")
        return value, display
    if kind == "linkedin":
        return f"https://linkedin.com/in/{value}", f"linkedin.com/in/{value}"
    if kind == "github":
        return f"https://github.com/{value}", f"github.com/{value}"
    return value, value


def tagline(summary: str, limit: int = 58) -> str:
    text = str(summary or "").strip()
    for marker in (" with ", " using ", " for ", " via ", " between "):
        if marker in text:
            text = text[: text.index(marker)]
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0]


def project_context(project: dict[str, Any], max_bullets: int, min_bullets: int) -> dict[str, Any]:
    bullets = list(project.get("responsibilities", []) or [])[:max_bullets]
    if len(bullets) < min_bullets:
        bullets.extend(list(project.get("impact", []) or [])[: min_bullets - len(bullets)])
    tech_line = ", ".join(tech_terms(project.get("tech_stack", {}) or {})[:8])
    return {
        "id": project.get("id", project.get("name", "")),
        "name": project.get("name", ""),
        "period": project.get("period", ""),
        "tagline": tagline(project.get("summary", project.get("name", ""))),
        "tech_line": tech_line,
        "bullets": bullets,
    }


def role_context(role: dict[str, Any], max_bullets: int) -> dict[str, Any]:
    return {
        "id": role.get("id", role.get("company", "")),
        "company": role.get("company", ""),
        "title": role.get("title", ""),
        "period": role.get("period", ""),
        "bullets": list(role.get("bullets", []) or [])[:max_bullets],
    }


def estimate_lines(experience: list[dict[str, Any]], projects: list[dict[str, Any]], skills: list[dict[str, str]], certs: list[dict[str, Any]], education: list[dict[str, Any]], summary: dict[str, Any] | None, chars_per_line: int) -> int:
    lines = 3
    if summary:
        lines += 1
        if summary.get("summary"):
            lines += math.ceil(len(str(summary.get("summary"))) / chars_per_line)
        lines += len(summary.get("highlights", []) or [])
    lines += max(1, len(education)) * 2
    lines += 1
    for role in experience:
        lines += 1 + sum(max(1, math.ceil(len(str(b)) / chars_per_line)) for b in role.get("bullets", []))
    lines += 1
    for project in projects:
        lines += 2 + sum(max(1, math.ceil(len(str(b)) / chars_per_line)) for b in project.get("bullets", []))
        if project.get("tech_line"):
            lines += math.ceil(len(str(project["tech_line"])) / chars_per_line)
    lines += 1 + len(skills)
    if certs:
        lines += 2
    return lines


def select_skills(categories: list[dict[str, Any]], target_terms: list[str], jd_lower: str, jd_text: str, max_lines: int) -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    prof_rank = {"advanced": 0, "intermediate": 1, "familiar": 2}
    language_line: dict[str, str] | None = None
    category_scores: list[tuple[dict[str, Any], list[tuple[dict[str, Any], float, list[str]]], float]] = []
    all_scores: list[dict[str, Any]] = []

    for category in categories:
        ranked: list[tuple[dict[str, Any], float, list[str]]] = []
        for skill in category.get("skills", []) or []:
            score, hits = score_item(skill_terms(skill), " ".join(skill_terms(skill)), target_terms, jd_lower, jd_text)
            ranked.append((skill, score, hits))
            all_scores.append(
                {
                    "skill": skill.get("name", ""),
                    "category": category.get("name", ""),
                    "score": round(score, 4),
                    "hits": hits,
                }
            )
        ranked.sort(key=lambda row: (prof_rank.get(row[0].get("proficiency", "familiar"), 2), -row[1], row[0].get("name", "")))
        top_scores = sorted([score for _, score, _ in ranked], reverse=True)[:5]
        avg_score = sum(top_scores) / len(top_scores) if top_scores else 0.0
        if category.get("name") == "Programming Languages":
            selected = [skill.get("name", "") for skill, score, _ in ranked[:12] if score > 0]
            if not selected:
                selected = [skill.get("name", "") for skill, _, _ in ranked[:6]]
            language_line = {"category": "Languages", "skills": ", ".join(dedupe(selected))}
        else:
            category_scores.append((category, ranked, avg_score))

    lines: list[dict[str, str]] = []
    if language_line:
        lines.append(language_line)

    category_scores.sort(key=lambda row: row[2], reverse=True)
    for category, ranked, _ in category_scores[: max(0, max_lines - len(lines))]:
        selected = [skill.get("name", "") for skill, score, _ in ranked[:10] if score > 0]
        if not selected:
            selected = [skill.get("name", "") for skill, _, _ in ranked[:3]]
        if selected:
            lines.append({"category": category.get("name", ""), "skills": ", ".join(dedupe(selected))})

    return lines[:max_lines], all_scores


def markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def detect_gaps(jd_text: str, known_terms: list[str]) -> list[str]:
    known = {normalize(t) for t in known_terms}
    candidates: set[str] = set()
    candidates.update(re.findall(r"\b([A-Z][A-Z0-9]{1,8})\b", jd_text))
    candidates.update(re.findall(r"\b([A-Z][a-z]+(?:[A-Z][a-z]+)+)\b", jd_text))
    candidates.update(re.findall(r"\b(C\+\+|C#|\.NET|F#)\b", jd_text))
    return sorted(c for c in candidates if normalize(c) not in known and c not in GAP_STOPWORDS)


def render_resume(
    profile: dict[str, Any],
    education: list[dict[str, Any]],
    experience: list[dict[str, Any]],
    projects: list[dict[str, Any]],
    skills: list[dict[str, str]],
    certs: list[dict[str, Any]],
    summary: dict[str, Any] | None,
    company: str,
    role: str,
) -> str:
    lines: list[str] = [
        f"% Resume tailored for: {latex_escape(company)} - {latex_escape(role)}",
        r"\documentclass[a4paper,10pt]{article}",
        r"\usepackage[left=0.5in,right=0.5in,top=0.4in,bottom=0.4in]{geometry}",
        r"\usepackage{enumitem,titlesec}",
        r"\usepackage[hidelinks]{hyperref}",
        r"\usepackage[T1]{fontenc}",
        r"\usepackage{lmodern}",
        "",
        r"\pagestyle{empty}",
        r"\setlength{\parindent}{0pt}",
        r"\titleformat{\section}{\large\bfseries}{}{0em}{}[\titlerule]",
        r"\titlespacing*{\section}{0pt}{6pt}{4pt}",
        r"\setlist[itemize]{nosep,left=0pt,label=\textbullet,topsep=1pt,itemsep=1pt}",
        "",
        r"\begin{document}",
        "",
        r"\begin{center}",
        r"{\LARGE\bfseries " + latex_escape(profile.get("name", "")) + r"}\\[3pt]",
    ]

    contact_parts = []
    email = str(profile.get("email", "")).strip()
    if email:
        contact_parts.append(r"\href{mailto:" + email + r"}{" + latex_escape(email) + r"}")
    if profile.get("phone"):
        contact_parts.append(latex_escape(profile.get("phone", "")))
    for kind in ("linkedin", "github"):
        url, display = link_target(kind, str(profile.get(kind, "")).strip())
        if url:
            contact_parts.append(r"\href{" + url + r"}{" + latex_escape(display) + r"}")
    lines.append(r" \enspace|\enspace ".join(contact_parts))
    lines.extend([r"\end{center}", ""])

    if summary:
        lines.extend([r"\section{Summary}"])
        summary_bits = [latex_escape(summary.get("summary", ""))]
        for highlight in summary.get("highlights", []) or []:
            summary_bits.append(r"\textbullet\enspace " + latex_escape(highlight))
        lines.extend([r" \enspace ".join(bit for bit in summary_bits if bit), ""])

    lines.extend([r"\section{Education}"])
    for idx, edu in enumerate(education):
        if idx:
            lines.append(r"\\[4pt]")
        lines.append(r"\textbf{" + latex_escape(edu.get("institution", "")) + r"} \hfill " + latex_escape(edu.get("period", "")) + r"\\")
        lines.append(latex_escape(edu.get("degree", "")) + r" $\cdot$ " + latex_escape(edu.get("field", "")))
    lines.append("")

    lines.extend([r"\section{Experience}"])
    for item in experience:
        lines.append(r"\textbf{" + latex_escape(item.get("company", "")) + r"}, " + latex_escape(item.get("title", "")) + r" \hfill " + latex_escape(item.get("period", "")))
        lines.append(r"\begin{itemize}")
        for bullet in item.get("bullets", []):
            lines.append(r"  \item " + latex_escape(bullet))
        lines.append(r"\end{itemize}")
    lines.append("")

    lines.extend([r"\section{Projects}"])
    for item in projects:
        lines.append(r"\textbf{" + latex_escape(item.get("name", "")) + r" -- " + latex_escape(item.get("tagline", "")) + r"} \hfill " + latex_escape(item.get("period", "")) + r"\\")
        if item.get("tech_line"):
            lines.append(r"\textit{" + latex_escape(item.get("tech_line", "")) + r"}")
        lines.append(r"\begin{itemize}")
        for bullet in item.get("bullets", []):
            lines.append(r"  \item " + latex_escape(bullet))
        lines.append(r"\end{itemize}")
    lines.append("")

    lines.extend([r"\section{Skills}"])
    for idx, item in enumerate(skills):
        suffix = r"\\" if idx < len(skills) - 1 else ""
        lines.append(r"\textbf{" + latex_escape(item.get("category", "")) + r":} " + latex_escape(item.get("skills", "")) + suffix)
    lines.append("")

    if certs:
        lines.extend([r"\section{Certifications}"])
        cert_line = []
        for cert in certs:
            cert_line.append(latex_escape(cert.get("name", "")) + " -- " + latex_escape(cert.get("issuer", "")))
        lines.append(r" \enspace|\enspace ".join(cert_line))
        lines.append("")

    lines.extend([r"\end{document}", ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="ATS resume tailoring helper for Codex.")
    parser.add_argument("--index", required=True, type=Path, help="Directory containing resume index YAML files.")
    parser.add_argument("--profile", type=Path, help="Path to profile.yaml. Defaults to profile.yaml next to index.")
    parser.add_argument("--jd", required=True, type=Path, help="Job description text file.")
    parser.add_argument("--company", required=True, help="Target company.")
    parser.add_argument("--role", required=True, help="Target role.")
    parser.add_argument("--expanded-terms", type=Path, help="Text file of Codex-inferred terms, one per line.")
    parser.add_argument("--output", type=Path, required=True, help="Output directory.")
    parser.add_argument("--max-experience", type=int, default=3)
    parser.add_argument("--max-projects", type=int, default=4)
    parser.add_argument("--max-skill-lines", type=int, default=4)
    parser.add_argument("--max-certifications", type=int, default=3)
    parser.add_argument("--max-project-bullets", type=int, default=3)
    parser.add_argument("--min-project-bullets", type=int, default=2)
    parser.add_argument("--max-exp-bullets", type=int, default=3)
    parser.add_argument("--min-projects", type=int, default=2)
    parser.add_argument("--min-experience", type=int, default=2)
    parser.add_argument("--max-page-lines", type=int, default=72)
    parser.add_argument("--chars-per-line", type=int, default=80)
    parser.add_argument("--section-priority", choices=["experience", "projects"], default="experience")
    args = parser.parse_args()

    index_dir = args.index
    profile_path = args.profile or index_dir.parent / "profile.yaml"
    out_dir = args.output
    out_dir.mkdir(parents=True, exist_ok=True)

    profile = load_yaml(profile_path)
    skills_data = load_yaml(index_dir / "skills.yaml")
    projects_data = load_yaml(index_dir / "projects.yaml")
    exp_data = load_yaml(index_dir / "experience.yaml")
    certs_data = load_yaml(index_dir / "certifications.yaml")
    summary_path = index_dir / "summary.yaml"
    summary_data = load_yaml(summary_path) if summary_path.exists() else None

    jd_text = args.jd.read_text(encoding="utf-8").strip()
    if not jd_text:
        raise SystemExit("Job description is empty.")
    jd_lower = jd_text.lower()

    known_terms = collect_known_terms(skills_data, projects_data, exp_data, certs_data)
    explicit_terms = [term for term in known_terms if keyword_in_text(term, jd_lower, jd_text)]
    expanded_terms = parse_terms_file(args.expanded_terms)
    target_terms = dedupe(explicit_terms + expanded_terms)
    gaps = detect_gaps(jd_text, known_terms + expanded_terms + [args.company, args.role])

    roles = list(exp_data.get("roles", []) or [])
    projects = list(projects_data.get("projects", []) or [])
    certs = list(certs_data.get("certifications", []) or [])
    education = list(exp_data.get("education", []) or [])[:2]

    role_ranked = []
    for role in roles:
        score, hits = score_item(role_terms(role), build_role_text(role), target_terms, jd_lower, jd_text)
        score *= recency_multiplier(role.get("period", ""))
        role_ranked.append({"item": role, "score": score, "hits": hits})
    role_ranked.sort(key=lambda row: row["score"], reverse=True)

    project_ranked = []
    for project in projects:
        score, hits = score_item(project_terms(project), build_project_text(project), target_terms, jd_lower, jd_text)
        score *= recency_multiplier(project.get("period", ""))
        project_ranked.append({"item": project, "score": score, "hits": hits})
    project_ranked.sort(key=lambda row: row["score"], reverse=True)

    cert_ranked = []
    for cert in certs:
        score, hits = score_item(cert_terms(cert), " ".join(cert_terms(cert)), target_terms, jd_lower, jd_text)
        cert_ranked.append({"item": cert, "score": score, "hits": hits})
    cert_ranked.sort(key=lambda row: row["score"], reverse=True)

    skill_lines, skill_scores = select_skills(skills_data.get("categories", []) or [], target_terms, jd_lower, jd_text, args.max_skill_lines)

    selected_roles = role_ranked[: args.max_experience]
    selected_projects = project_ranked[: args.max_projects]
    selected_certs = [row for row in cert_ranked if row["score"] > 0][: args.max_certifications]

    exp_ctx = [role_context(row["item"], args.max_exp_bullets) for row in selected_roles]
    proj_ctx = [project_context(row["item"], args.max_project_bullets, args.min_project_bullets) for row in selected_projects]
    cert_ctx = [row["item"] for row in selected_certs]

    line_est = estimate_lines(exp_ctx, proj_ctx, skill_lines, cert_ctx, education, summary_data, args.chars_per_line)
    trim_order = ["projects", "experience"] if args.section_priority == "experience" else ["experience", "projects"]
    for section in trim_order:
        if line_est <= args.max_page_lines:
            break
        if section == "projects":
            for project in proj_ctx:
                project["bullets"] = project.get("bullets", [])[: args.min_project_bullets]
        else:
            for role in exp_ctx:
                role["bullets"] = role.get("bullets", [])[:2]
        line_est = estimate_lines(exp_ctx, proj_ctx, skill_lines, cert_ctx, education, summary_data, args.chars_per_line)

    drop_order = ["projects", "experience"] if args.section_priority == "experience" else ["experience", "projects"]
    for section in drop_order:
        while line_est > args.max_page_lines:
            if section == "projects" and len(proj_ctx) > args.min_projects:
                proj_ctx.pop()
                selected_projects.pop()
            elif section == "experience" and len(exp_ctx) > args.min_experience:
                exp_ctx.pop()
                selected_roles.pop()
            else:
                break
            line_est = estimate_lines(exp_ctx, proj_ctx, skill_lines, cert_ctx, education, summary_data, args.chars_per_line)

    exp_order = sorted(range(len(exp_ctx)), key=lambda idx: parse_start_date(exp_ctx[idx].get("period", "")), reverse=True)
    proj_order = sorted(range(len(proj_ctx)), key=lambda idx: parse_start_date(proj_ctx[idx].get("period", "")), reverse=True)
    exp_ctx = [exp_ctx[idx] for idx in exp_order]
    proj_ctx = [proj_ctx[idx] for idx in proj_order]

    resume_tex = render_resume(profile, education, exp_ctx, proj_ctx, skill_lines, cert_ctx, summary_data, args.company, args.role)
    (out_dir / "resume.tex").write_text(resume_tex, encoding="utf-8")

    selected_role_ids = {row["item"].get("id", row["item"].get("company", "")) for row in selected_roles}
    selected_project_ids = {row["item"].get("id", row["item"].get("name", "")) for row in selected_projects}
    selected_cert_ids = {row["item"].get("id", row["item"].get("name", "")) for row in selected_certs}

    report_lines = [
        f"# Match Report: {args.company} - {args.role}",
        "",
        f"Estimated line count: {line_est} / {args.max_page_lines}",
        "",
        "## Explicit Matched Terms",
        "",
        ", ".join(explicit_terms) if explicit_terms else "_None detected from exact index terms._",
        "",
        "## Codex-Expanded Terms",
        "",
        ", ".join(expanded_terms) if expanded_terms else "_None provided._",
        "",
        "## Experience Rankings",
        "",
        "| Rank | Role | Company | Score | Selected | Hits |",
        "|---:|---|---|---:|:---:|---|",
    ]
    for idx, row in enumerate(role_ranked, 1):
        item = row["item"]
        selected = "Y" if item.get("id", item.get("company", "")) in selected_role_ids else ""
        report_lines.append(f"| {idx} | {markdown_cell(item.get('title', ''))} | {markdown_cell(item.get('company', ''))} | {row['score']:.3f} | {selected} | {markdown_cell(', '.join(row['hits']))} |")

    report_lines.extend(["", "## Project Rankings", "", "| Rank | Project | Score | Selected | Hits |", "|---:|---|---:|:---:|---|"])
    for idx, row in enumerate(project_ranked, 1):
        item = row["item"]
        selected = "Y" if item.get("id", item.get("name", "")) in selected_project_ids else ""
        report_lines.append(f"| {idx} | {markdown_cell(item.get('name', ''))} | {row['score']:.3f} | {selected} | {markdown_cell(', '.join(row['hits']))} |")

    report_lines.extend(["", "## Selected Skills", ""])
    for line in skill_lines:
        report_lines.append(f"- **{line['category']}:** {line['skills']}")

    if cert_ranked:
        report_lines.extend(["", "## Certification Rankings", "", "| Certification | Issuer | Score | Selected | Hits |", "|---|---|---:|:---:|---|"])
        for row in cert_ranked:
            item = row["item"]
            selected = "Y" if item.get("id", item.get("name", "")) in selected_cert_ids else ""
            report_lines.append(f"| {markdown_cell(item.get('name', ''))} | {markdown_cell(item.get('issuer', ''))} | {row['score']:.3f} | {selected} | {markdown_cell(', '.join(row['hits']))} |")

    if gaps:
        report_lines.extend(["", "## Coverage Gaps", ""])
        for gap in gaps:
            report_lines.append(f"- {gap}")

    (out_dir / "match_report.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    selection = {
        "company": args.company,
        "role": args.role,
        "line_estimate": line_est,
        "explicit_terms": explicit_terms,
        "expanded_terms": expanded_terms,
        "coverage_gaps": gaps,
        "selected_experience": [item.get("id", item.get("company", "")) for item in exp_ctx],
        "selected_projects": [item.get("id", item.get("name", "")) for item in proj_ctx],
        "selected_certifications": [item.get("id", item.get("name", "")) for item in cert_ctx],
        "skill_scores": skill_scores,
    }
    (out_dir / "selection.json").write_text(json.dumps(selection, indent=2), encoding="utf-8")

    print(f"Wrote {out_dir / 'resume.tex'}")
    print(f"Wrote {out_dir / 'match_report.md'}")
    print(f"Wrote {out_dir / 'selection.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
