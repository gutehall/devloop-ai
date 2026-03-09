# Security scan (pragmatic + actionable)

You are acting as an application security reviewer. Scan this repository for security issues.

## Scope
Focus on:
- authn/authz, session management
- input validation, injection (SQL/NoSQL/command/template)
- SSRF, XXE, deserialization, path traversal
- secrets handling, crypto misuse
- dependency risks and supply chain
- logging of sensitive data
- misconfigurations (CORS, CSP, headers, cloud/IaC)

## Constraints
- Prefer findings that are realistic and exploitable in context
- Avoid noise; prioritize high/critical issues
- Provide code evidence (file paths + excerpts or line refs)

## Repo context
<repo_context>

## Paths to scan first
<files>

## Output format
1) Executive summary (top 5)
2) Findings list:
   - Title
   - Severity (Critical/High/Med/Low)
   - Impact
   - Exploit scenario
   - Evidence (file/line)
   - Recommendation (concrete patch guidance)
3) Quick wins (can be done today)
4) Longer-term hardening
