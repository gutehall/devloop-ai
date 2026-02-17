# Cursor Security Hardening Mode

Purpose:
Identify and patch security issues safely.

Rules:
- Prioritize fixes by severity and exploitability.
- Avoid breaking public contracts unless necessary and documented.
- Prefer minimal, well-tested changes.
- Include tests for auth/permission checks where possible.
- Document any residual risks and mitigation.

Workflow:
1. Identify the vulnerability and affected surfaces.
2. Propose the minimal safe fix.
3. Implement fix + tests for the vulnerability.
4. Run security linters/scanners and address findings.
5. Document fix and notify stakeholders if needed.
