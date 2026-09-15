---
name: session-handoff
description: Use when the user asks for a session handoff, continuity summary, end-of-session summary, or compact next-session context after a long or multi-feature work session.
---

# Session Handoff Summary

Use this skill at the end of a long or multi-feature session to create a continuity summary.

## Output Format

Generate a summary with these sections:

### Session Summary â€” [Date]

**What was accomplished:**
- [List completed work items]

**What's still pending:**
- [List unfinished items or known TODOs]

**Known issues / blockers:**
- [List any bugs, failures, or blockers encountered]

**Current state:**
- Branch: `[branch name]`
- Last commit: `[hash] â€” [message]`
- Working directory status: [clean / uncommitted changes in X files]

**Next steps:**
- [Suggested actions for the next session]

---

Paste this at the start of your next session for instant context.
