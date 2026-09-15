# Resume Index Schema

Prefer this directory layout:

```text
profile.yaml
index/
  skills.yaml
  projects.yaml
  experience.yaml
  certifications.yaml
  summary.yaml       # optional
```

## profile.yaml

```yaml
name: "Jane Doe"
email: "jane@example.com"
phone: "+65 0000 0000"
linkedin: "janedoe"
github: "janedoe"
```

`linkedin` and `github` may be handles or full URLs.

## skills.yaml

```yaml
categories:
  - name: "Programming Languages"
    skills:
      - name: "Python"
        ats_keywords: ["Python", "python3"]
        proficiency: advanced
        evidence:
          - ref: "project-or-role-id"
```

`proficiency` should be `advanced`, `intermediate`, or `familiar`.

## projects.yaml

```yaml
projects:
  - id: "project-id"
    name: "Project Name"
    period: "Jan 2025 - Present"
    summary: "Short project description"
    tech_stack:
      languages: [Python]
      frameworks: [FastAPI]
      infrastructure: [Docker, PostgreSQL]
      patterns: [REST]
      tools: [pytest]
    responsibilities:
      - "Built ..."
    impact:
      - "Reduced ..."
    ats_tags: ["Python", "FastAPI", "REST"]
```

## experience.yaml

```yaml
roles:
  - id: "role-id"
    company: "Company"
    title: "Software Engineer Intern"
    period: "Jun 2024 - Dec 2024"
    skills_used: ["Python", "Docker"]
    bullets:
      - "Developed ..."
    ats_tags: ["Python", "Docker"]

education:
  - institution: "University"
    degree: "BSc"
    field: "Computer Science"
    period: "2022 - 2026"
```

## certifications.yaml

```yaml
certifications:
  - id: "cert-id"
    name: "Certification"
    issuer: "Issuer"
    ats_keywords: ["Cloud", "AWS"]
```

## summary.yaml

```yaml
summary: "One-sentence professional summary."
highlights:
  - "Backend systems"
  - "Cloud deployment"
```

Only use `summary.yaml` if the user's resume format needs a summary.
