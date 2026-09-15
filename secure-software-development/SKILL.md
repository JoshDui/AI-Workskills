---
name: secure-software-development
description: Course-grounded secure software development guidance for measurable security requirements, misuse cases, DFD and STRIDE threat modeling, secure design and coding, DevSecOps, and verification with testing, SAST, SCA, DAST, and fuzzing. Use when studying the Secure Software Development module; drafting or reviewing SSDLC artifacts; mapping requirements, threats, controls, and tests; planning secure CI/CD; or interpreting its Docker, SecurityRAT, Threat Modeling Tool, Threat Dragon, GitHub Actions, Selenium, CodeQL, Dependency-Check, SonarQube, ZAP, and Burp labs.
---

# Secure Software Development

Apply secure software development as one traceable engineering loop: define what must be protected, model how it can fail, select and implement controls, then verify the promised behavior with evidence.

## Scope and source posture

This skill synthesizes the AY2025 Trimester 3 lecture and tutorial corpus from `C:\UniPain\SecureSWD\SSD`.

- Focus on reusable technical learning points.
- Ignore QR codes, attendance/access details, decorative media, repeated headers/footers, and other classroom-only logistics unless the user explicitly asks for them or they change a technical workflow.
- Separate classroom reproduction from production advice. Lab credentials, exposed ports, floating tags, old commands, and deliberately vulnerable targets are not production defaults.
- Verify current official standards, tool documentation, action versions, image tags, and cryptographic guidance before applying volatile details.
- Use active scanning, fuzzing, credential testing, or other intrusive techniques only against explicitly authorized targets.

## Core learning summary

### 1. Security belongs throughout the lifecycle

Secure software is not ordinary software plus a final penetration test. Integrate security into:

1. Feasibility and requirements
2. Architecture and detailed design
3. Implementation and code review
4. Build and CI/CD
5. Verification and release
6. Deployment, monitoring, maintenance, and incident response

Use quality gates, but do not turn security into a one-off sprint. Findings in a later phase must feed back into requirements, threat models, design, code, and regression tests.

### 2. Keep security terms distinct

| Item | Meaning |
|---|---|
| Asset | Something valuable that needs protection |
| Threat | A possible harmful event or attacker capability |
| Vulnerability | An exploitable weakness |
| Risk | Contextual likelihood and impact of harm |
| Requirement | A measurable security behavior or constraint |
| Control | A mechanism or process that treats risk |
| Test | A check of expected behavior under stated conditions |
| Finding | Evidence-backed observation requiring disposition |
| Residual risk | Risk remaining after controls and verification |

Use external knowledge sources correctly:

- CVE identifies public vulnerabilities.
- NVD enriches vulnerability records with affected products, references, and severity data.
- CVSS scores vulnerability severity; it is not complete business risk.
- CWE classifies weakness types.
- CAPEC describes reusable attack patterns.
- MITRE ATT&CK describes observed adversary tactics and techniques.
- STRIDE categorizes system-specific threats.
- Attack trees decompose an attacker goal into possible paths.
- ASVS catalogs verifiable application security controls.
- WSTG provides web security testing guidance.

Framework adoption or compliance does not prove that a product is secure. BSIMM measures observed security-program activities, SAMM supports maturity improvement, and Microsoft SDL prescribes lifecycle practices.

## End-to-end operating method

### Step 1: Scope the system

Identify:

- business purpose and critical workflows;
- stakeholders, users, administrators, operators, developers, suppliers, and service identities;
- assets and data classifications at rest, in transit, and during processing;
- deployment environments, topology, services, ports, protocols, stores, and external dependencies;
- attacker capabilities, including web, network, co-located, insider, supplier, automated, and recovery-path attackers;
- policies, contracts, regulations, privacy obligations, SLAs, and procurement constraints;
- assumptions, exclusions, and decision owners.

Treat every assumption as challengeable. An internal network, cloud account, container network, or third party is still a trust decision.

### Step 2: Write measurable security requirements

Use these categories deliberately:

- Secure functional requirements: security constraints integrated into ordinary behavior, including forbidden outcomes.
- Functional security requirements: explicit services such as authentication, authorization, backup, or audit.
- Nonfunctional security requirements: qualities such as resilience, recoverability, scalability, or robustness.
- Secure development requirements: required assurance activities such as review, scanning, test, or deployment gates.

Cover:

- confidentiality;
- integrity and transaction invariants;
- availability, recovery, capacity, and dependency failure;
- authentication and recovery;
- authorization, ownership, tenant boundaries, and separation of duties;
- accountability, logging, alerting, retention, and privacy;
- session generation, transport, expiry, rotation, revocation, and replay;
- safe errors and exceptional conditions;
- configuration, secrets, dependencies, builds, updates, and deployment;
- timing, concurrency, atomicity, idempotency, and TOC/TOU;
- secure development and verification evidence.

Use this record:

```text
ID:
Type:
Protected asset or behavior:
Actor and condition:
Requirement: <component> shall <measurable behavior>
Failure behavior:
Rationale / source / threat:
Owner and priority:
Verification method and success criterion:
```

Replace vague words such as "secure," "strong," "fast," and "high availability" with observable thresholds or a pinned standard version.

### Step 3: Derive anti-requirements and misuse cases

1. Start from a valid use case and expected state/input.
2. List unacceptable outcomes: unauthorized action, disclosure, corruption, loss, delay, bypass, replay, or partial commit.
3. Explore malformed, boundary, oversized, repeated, reordered, concurrent, stale, and unauthorized inputs.
4. Add a misuse actor with explicit capability and goal.
5. Link the misuse case to the threatened use case or asset.
6. Add controls that mitigate the misuse.
7. Convert credible abuse paths into requirements and tests.

### Step 4: Build the threat model

Create a DFD containing:

- external entities;
- processes;
- data stores;
- directional data flows;
- data class, protocol, authentication, encryption, and purpose on important flows;
- entry/exit points and privileged functions;
- trust boundaries where identity, privilege, process, host, network, tenant, administration, or ownership changes;
- external services, CI runners, artifact stores, certificate/secret stores, logging, recovery, and update paths.

Then:

1. Apply STRIDE to the relevant DFD elements and flows.
2. Use misuse cases, attack trees, OWASP/CAPEC/ATT&CK, incident history, and domain knowledge to find omissions.
3. Prioritize using likelihood, impact, reachability, exploitability, data sensitivity, and existing controls.
4. Avoid, mitigate, transfer, or accept each threat with authority.
5. Link each mitigation to a requirement, design, implementation owner, and test.
6. Validate with architecture, development, operations, test, security, and business participants.
7. Maintain the model when data, trust, architecture, dependencies, deployment, or incidents change.

STRIDE mapping:

| STRIDE | Property | Core question |
|---|---|---|
| Spoofing | Authentication | Can an actor or service claim another identity? |
| Tampering | Integrity | Can data, code, configuration, or traffic be changed? |
| Repudiation | Accountability | Can an actor deny an action because evidence is weak? |
| Information disclosure | Confidentiality | Can unauthorized parties observe sensitive data or metadata? |
| Denial of service | Availability | Can resources, queues, locks, dependencies, or workflows be exhausted? |
| Elevation of privilege | Authorization | Can a principal gain a more privileged action or state? |

Automatic threat generation is a starting point, not exhaustive analysis. An incomplete DFD produces an incomplete threat list. Justify every `Not Applicable` or out-of-scope item.

Threat register template:

| ID | Element/flow | Threat/path | Asset | Preconditions | Likelihood | Impact | Control | Verification | Owner/status | Residual risk |
|---|---|---|---|---|---|---|---|---|---|---|

### Step 5: Apply secure design principles

Use the ten course principles:

1. **Minimize attack surface.** Remove unused features, methods, ports, privileges, data, dependencies, and public reachability.
2. **Establish secure defaults.** Default to deny, minimal data, restricted exposure, safe permissions, and explicit opt-in for risky behavior.
3. **Apply least privilege.** Scope users, services, administrators, CI tokens, containers, databases, filesystems, networks, and resources.
4. **Use defense in depth.** Combine independently useful controls across identity, authorization, validation, transactions, data protection, audit, and detection.
5. **Fail securely.** Initialize to deny, handle errors/timeouts/partial failure, roll back atomic work, and never preserve privilege after exceptions.
6. **Do not trust services.** Treat suppliers, APIs, identity providers, packages, actions, images, and update channels as external trust relationships.
7. **Separate duties.** Separate requesting, approving, executing, receiving, auditing, deploying, and granting exceptions.
8. **Avoid dependence on obscurity.** Correctness must survive disclosure of source, architecture, identifiers, and algorithms.
9. **Keep security simple.** Prefer centralized, understandable, tested framework mechanisms over custom special cases.
10. **Fix issues correctly.** Reproduce, find root cause, locate related uses, repair generally, add regression tests, and retest affected systems.

Distinguish design flaws from implementation bugs. Correct code can faithfully implement an unsafe workflow.

### Step 6: Implement secure controls

#### Authentication and recovery

- Design enrollment, login, step-up, recovery, credential change, lockout/rate limits, revocation, deletion, administration, and incident response.
- Combine different factor categories for MFA; two passwords are not two factors.
- Rate-limit by account and other context, not IP alone.
- Return generic client errors while preserving useful restricted server evidence.
- Treat recovery and unlock as separate high-value authentication paths.
- For one-time codes, accept only valid recent state, limit attempts, expire promptly, and prevent replay.
- Passkeys use service/account-specific asymmetric credentials and signed challenges; review origin binding, synced/device-bound behavior, lost-device recovery, fallback, and usability.
- SMS/email passwordless flows inherit mailbox, SIM-swap, forwarding, interception, and recovery risks.

#### Sessions

Document token/cookie structure, cryptographic generation, server-side or self-contained state, transport/storage, cookie flags, fixation prevention, rotation, idle/absolute expiry, revocation, logout, concurrent sessions, CSRF, replay, cluster consistency, key rotation, and audit evidence.

#### Authorization and accountability

- Define principal, resource, operation, tenant/owner, state, and conditions.
- Enforce server-side object ownership and state transitions; hiding UI controls is not authorization.
- Test horizontal, vertical, cross-tenant, stale-role, forced-browsing, alternate endpoint, and workflow-order bypass.
- Administrator must not automatically mean universal customer access or impersonation.
- Log stable actor identity, action, target, time, source/context, outcome, and correlation while excluding passwords, keys, and session tokens.
- Protect log integrity/access, centralize where appropriate, monitor, alert, rotate, retain, and dispose.

#### Input, output, database, and files

- Validate at each trust boundary using types, schemas, ranges, lengths, fixed values, normalization, and bounded full-string regexes.
- Prefer allowlists for constrained fields; blocklists are bypass-prone.
- Bound regex complexity and input length to prevent ReDoS.
- Use context-aware output encoding for XSS prevention.
- Use prepared statements/parameterized queries for SQL; allowlist unavoidable dynamic identifiers.
- Apply least database privilege and encrypted connections.
- Validate upload size, type, and content; generate storage names; prevent traversal; store outside executable roots; scan/quarantine where appropriate.

Input validation is not the primary defense against SQL injection or XSS.

#### Cryptography, TLS, passwords, and secrets

- Use established libraries and current approved algorithms/protocols; do not invent cryptography.
- Distinguish encryption, signatures, MACs, hashing, and password KDFs.
- Use a current password-specific KDF with unique salts and managed parameters; fast hashes alone are unsuitable.
- Store algorithm/parameter metadata to support migration.
- Verify certificate hostname, chain, expiry, protocol/cipher policy, key storage, renewal, revocation, redirect, and reload failure.
- Prefer modern forward-secret TLS configurations.
- Remember that TLS protects a channel; it does not fix phishing, authorization, injection, unsafe recovery, or endpoint compromise.
- Manage secret creation, distribution, scope, storage, rotation, revocation, logging, and incident response. Prevent leaks into source, logs, caches, images, test artifacts, and PR output.

#### Dependencies, containers, and supply chain

1. Inventory direct/transitive packages, images, tools, actions, generated code, and update channels.
2. Commit lockfiles and build deterministically.
3. Select trusted sources and verify integrity/provenance.
4. Scan continuously, then triage reachability, exploitability, configuration, and false matches.
5. Patch, upgrade, replace, isolate, or accept with owner and expiry.
6. Preserve SBOM, artifact digest, provenance, report, and suppression rationale.

For containers, use minimal/pinned images, non-root users, scoped capabilities and mounts, private networks, explicit published ports, resources, health checks, managed secrets, and deliberate backup/restore. Startup order is not readiness; persistence is not backup or confidentiality.

### Step 7: Integrate DevSecOps and CI/CD

DevSecOps puts security/compliance inside frequent delivery work. Continuous delivery keeps a deployment decision; continuous deployment releases successful changes automatically.

Design the pipeline to:

1. Build once from reviewed source and deterministic inputs.
2. Run unit, integration, UI, lint/SAST, SCA, secret/container, and other relevant checks.
3. Propagate failures and preserve structured evidence.
4. Minimize token permissions and isolate untrusted PR code from secrets.
5. Pin and govern actions, images, tools, and dependencies.
6. Create a bounded artifact with digest, SBOM/provenance, retention, and promotion history.
7. Apply explicit gates, suppressions, approvals, protected environments, and required checks.
8. Deploy the same artifact with safe secret access, health checks, rollback, monitoring, and response.

An uploaded artifact is CI evidence, not deployment. A report-only scan is not a gate. A green workflow is meaningful only if tests can fail and policy requires the checks.

### Step 8: Verify with complementary techniques

Use a portfolio:

| Method | Stronger at | Typical blind spots |
|---|---|---|
| Unit/integration tests | Known invariants and component behavior | Unimagined cases and production configuration |
| API/UI tests | Workflow and integration behavior | Deep code paths and internal state |
| Manual design/code review | Intent, authorization, state, business logic | Cost, consistency, scale |
| Lint/pattern SAST | Fast known patterns and conventions | Interprocedural semantics and runtime behavior |
| Semantic SAST | Data/control flow and repeatable queries | Build gaps, false positives, business intent |
| SCA/SBOM | Known vulnerable components and inventory | Reachability, unknown flaws, configuration |
| DAST | Deployed behavior and configuration | Paths/endpoints not discovered |
| Fuzzing | Parser/input/state robustness | Oracle quality, payload and coverage limits |
| Operational checks | Monitoring, recovery, deployment controls | Source/design defects outside observed operations |

Derive positive, negative, boundary, bypass, abuse, concurrency, replay, alternate-endpoint, and failure/degradation tests from requirements and threats. Use ASVS for what to verify and WSTG for how to test web controls, while pinning the versions used.

Static analysis examines code without execution. Understand false positives, false negatives, control/data-flow analysis, source-to-sink reasoning, abstract interpretation, model checking, and formal verification. Finding one good path does not prove an all-path invariant.

### Step 9: Triage, remediate, and retest

1. Record authorization/scope, commit/build, environment, tool/version, rule profile, exact command, and time.
2. Preserve raw reports and relevant request/response/trace evidence.
3. Normalize and deduplicate findings.
4. Reproduce safely and separate observed fact from inference.
5. Evaluate reachability, exploitability, data sensitivity, likelihood, impact, and existing controls.
6. Assign disposition, owner, SLA, severity rationale, and accepted-risk expiry.
7. Repair the root cause and related occurrences.
8. Add a regression test and rerun the same configuration.
9. Record before/after evidence and residual risk.

Finding template:

```text
ID and title:
Requirement / threat / ASVS / WSTG / CWE mapping:
Affected asset and location/endpoint:
Preconditions and attacker capability:
Observed evidence and reproduction:
Data/control-flow or workflow trace:
Tool, rule/query, version, configuration, and commit:
Likelihood, impact, exploitability, and severity rationale:
Disposition and confidence:
Root cause and related occurrences:
Remediation and regression test:
Retest evidence and status:
Residual risk / accepted-risk owner and expiry:
```

## Course lab workflows and lessons

### Docker and Compose

The lab runs Nginx, MySQL, a local Git HTTP server, and Selenium Grid to teach services, networks, published ports, volumes, builds, environment variables, and service discovery.

Production translation:

- Replace `pass` and other lab credentials.
- Do not expose unauthenticated Git HTTP, Selenium, databases, or dashboards broadly.
- Pin images/digests, add health checks, scope mounts/capabilities, and use managed secrets.
- The supplied Git Dockerfile serves `/home/git`, while Compose mounts persistence at `/var/www/git`; that mount does not persist the generated repository.

### SecurityRAT

Use it to select a profile, generate candidate requirements, decide handling, and preserve status/ticket evidence. `admin/admin` and `user/user` are lab-only. Generated requirements still need system-specific assets, threats, conditions, owners, verification, and standard versions.

### Microsoft Threat Modeling Tool and Threat Dragon

Draw the DFD, generate/review STRIDE threats, record priority/status/justification/mitigation, and preserve both editable model and report. Automatic output is not exhaustive. Marking an item out of scope suppresses threat generation and therefore requires a reason.

### Nginx, TLS, and Certbot

The intended flow is static Nginx, ACME challenge, certificate storage, HTTPS, HTTP redirect, renewal, safe reload, and verification.

Known supplied issues:

- TLS Compose mounts `nginx.conf`, not `nginx-tls.conf`.
- Certbot has no issuance/renewal command.
- TLS config does not clearly serve the mounted HTML.
- The CI content assertion is weak and cleanup is not guaranteed on earlier failure.

### GitHub Actions, Node, and Selenium

The sample separates build and test jobs, transfers an artifact, runs unit tests, starts the Node service, starts Selenium, and runs a browser check.

Critical issues:

- The Selenium test catches errors without rethrowing, so failures can appear green.
- It waits for element existence rather than final text, creating a race.
- The archive has dependency changes and a deleted lockfile.
- `npm install` plus cached `node_modules` is non-deterministic.
- Archived checkout/artifact actions and floating images are outdated.
- The artifact omits the lockfile and the test job reinstalls dependencies.
- `npm test` runs `tests/*.js`; it does not run the `.mjs` Selenium test.

Harden by committing a lockfile, using deterministic install, building once, pinning reviewed actions/images, using bounded readiness polling, propagating failures, and publishing structured test/failure artifacts.

### ESLint, SARIF, Dependency-Check, and CodeQL

- ESLint provides fast lint/pattern checks; SARIF is a report format, not a scanner.
- The supplied ESLint workflow uses `|| true`, so findings do not gate the build.
- Dependency-Check produces an HTML SCA report, but its mutable `@main` action receives an NVD secret and has no fail threshold.
- CodeQL provides query-based semantic analysis with code-scanning permissions; select languages, builds, queries, and exclusions deliberately.
- Fork PRs and secrets require explicit trust-boundary handling.

### SonarQube

Run SonarQube/PostgreSQL locally, change initial credentials, create a project/token, scan, review issues/hotspots/quality gate, and connect CI only through a securely reachable server.

Remaining supplied gaps include hard-coded DB credentials, broad port 9000 exposure, no health checks/TLS/backups/resource controls, no reproducible project arguments, and no explicit quality-gate enforcement. A passed gate means configured thresholds passed, not that the product is secure.

### ZAP

Configure authorized scope, authentication, users, include/exclude paths, APIs, and rate limits. Browse/import traffic, run passive analysis, use traditional/AJAX discovery, review coverage, then run approved active checks. Preserve session/report and request/response evidence. Active scanning sends attack payloads and can harm or change the target.

### Burp Intruder

Capture a baseline request, choose payload positions, bound payload/rate/concurrency, define response oracles, inspect anomalies, and verify authenticated state or protected-resource access. The course username/password Cluster-bomb example is credential guessing with response-differential analysis, not general-purpose fuzzing. A redirect difference alone is not proof.

## Common misconceptions to correct

- Firewalls and TLS do not compensate for application authorization, validation, session, or design flaws.
- Encryption at rest does not stop an authorized application query or SQL injection from returning plaintext.
- Authentication, authorization, and accountability are different controls.
- Two passwords are not two-factor authentication.
- Logging alone is not accountability; logs need useful content, integrity, access control, monitoring, retention, and escalation.
- Replication is not backup; container persistence is not confidentiality or integrity.
- Client-side validation is usability support, not a security boundary.
- Input validation alone does not prevent XSS or SQL injection.
- A scanner warning is not proof of exploitability; no warning is not proof of safety.
- False positives and false negatives are opposites.
- SAST, SCA, DAST, fuzzing, and manual review are complementary, not interchangeable.
- A screenshot, dashboard, or green workflow is not reproducibility, completeness, authorization, or remediation evidence.
- Warning suppression without evidence and periodic review creates blind spots.
- LLM review is nondeterministic; repository text can contain prompt injection, and proprietary code/secrets need approved handling and human verification.

## Evidence checklist

Prefer:

- measurable requirements with acceptance criteria;
- editable DFD/threat-model source plus report;
- STRIDE/threat register with priority, status, owner, mitigation, test, and residual risk;
- role/resource/action matrix;
- authentication, recovery, passkey, and session diagrams;
- exact TLS, password KDF, key/secret, access-control, logging, database, and upload configuration;
- repository commit, lockfile, dependency/SBOM inventory, artifact digest, and provenance;
- pipeline triggers, permissions, gates, deliberately failing tests, passing runs, and structured results;
- raw SARIF/SCA/Sonar/ZAP/Burp evidence with tool/config/version and sanitized sensitive data;
- remediation commit, regression test, same-configuration retest, and residual risk.

Use this traceability chain:

```text
requirement -> asset/DFD element -> threat -> control
            -> implementation file/config -> test/tool result
            -> remediation/regression -> residual risk
```

## Source coverage audit

The synthesis reviewed every instructional source in the directory:

- 24 unencrypted PDFs: 728 physical pages.
- 14 lecture PDFs: 643 pages.
- 10 tutorial/lab PDFs: 85 pages.
- 3 ZIP archives: all entries inventoried; all substantive instructional files read.
- 6 standalone YAML workflow/configuration files read fully.
- The Debian VS Code installer and local `.claude` settings were classified as non-instructional artifacts.

PDF sources and page counts:

| Source | Pages |
|---|---:|
| Lecture 1-P1 Module Overview | 24 |
| Lecture 1-P2 Secure Software Concepts x01 | 44 |
| Lecture 2-P1 Secure Software Concepts x02 | 32 |
| Lecture 2-P2 Secure Software Requirements x01 | 44 |
| Lecture 3-P1 Secure Software Requirements x02 | 44 |
| Lecture 3-P2 Threat Modeling | 48 |
| Lecture 4 Secure Software Design x01 | 39 |
| Lecture 5 Secure Software Design x02 | 59 |
| Lecture 5.5 Second Half Intro | 10 |
| Lecture 6 Secure Implementation | 63 |
| Lecture 7 Secure Implementation/Coding | 54 |
| Lecture 8 Secure Implementation/Testing | 53 |
| Lecture 9 Static Code Analysis x01 | 72 |
| Lecture 10 Static Code Analysis x02 | 57 |
| Lab01 Docker Compose | 11 |
| Lab02 Secure Software Requirement | 5 |
| X03 Microsoft Threat Modeling Tool | 8 |
| X04 OWASP Threat Dragon | 5 |
| X05 GitHub Actions | 9 |
| X07 GitHub Actions with Automated Testing | 11 |
| X08 Static Code Analysis | 12 |
| X09 SonarQube | 10 |
| X11a OWASP ZAP | 6 |
| X11b Burp Suite | 8 |

Archive/config coverage:

- `Lab01-requiredfiles.zip`: `compose.yaml`, `compose-selenium.yaml`, and `gitserver.Dockerfile`; macOS metadata ignored.
- `Lab05-files.zip`: HTML, HTTP/TLS Nginx Compose/config, Certbot volumes, and CI test.
- `github-actions-nodejs-test.zip`: README, package manifest, server, unit test, Selenium test, workflow, and relevant Git provenance; routine object/hook bytes ignored.
- `cda-eslint.yml`, `codeql.yml`, `dependency-check.yml`, `selenium-tests.yml`, `sonarqube.yml`, and `sonarqube-compose.yml` read fully.

No PDF page was wholly unreadable. Minor typographic encoding errors, inconsistent printed page numbers, small screenshot text, and time-sensitive UI/version details were handled through text extraction, page-count checks, targeted visual review, artifact inspection, and cross-source comparison.
