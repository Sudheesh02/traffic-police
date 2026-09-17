# Quick Reference Note: Antigravity Skills

> Keep this note handy. You can use these skills anytime across all your projects.

---

## ⚡ Slash Commands Cheat Sheet

| Command | What it does | Example prompt |
| :--- | :--- | :--- |
| `/ppt-pitch-crafter` | Writes slides from code without buzzwords or hyphens | `/ppt-pitch-crafter build 6 slides for our project` |
| `/ppt-multi-reviewer` | 3-judge panel audits your slides for clarity, facts, and anti-AI voice | `/ppt-multi-reviewer review our intro slide` |
| `/git-commit-formatter` | Formats commit messages in Conventional Commits style | `/git-commit-formatter commit the auth bugfix` |
| `/json-to-pydantic` | Converts JSON payloads into typed Python Pydantic models | `/json-to-pydantic convert api response to models` |
| `/license-header-adder` | Adds Apache 2.0 license headers from template | `/license-header-adder add headers to src/` |
| `/database-schema-validator` | Runs deterministic checks on SQL schema definitions | `/database-schema-validator validate schema.sql` |
| `/always-verify-gcp` | Verifies Google Cloud commands before running | `/always-verify-gcp deploy to Cloud Run` |

---

## 💡 Quick Tips for Winning PPT Presentations

1. **The 5-Second Scan Rule**:
   * If a judge glances at your slide for 5 seconds, they must understand:
     1. What broke?
     2. How did you fix it?
     3. What is the real number?

2. **The 3 Never-Do's**:
   * **Never** write walls of dashed bullet lists (`- - -`). Use bold title cards or metric boxes instead.
   * **Never** use AI filler: *seamlessly, tapestry, testament, empowers, delve, multifaceted*.
   * **Never** make unverified claims. Put exact latency (e.g. 1.6 ms), exact test pass rates, or exact chemistry limits.

---

## 📂 Where Everything Lives on Your System

* **Desktop Master Library**:
  `C:\Users\Asus\Desktop\agy-skills\`
* **Active Project Workspace**:
  `C:\Users\Asus\Desktop\JSL\.agents\skills\`
* **Global Antigravity System Paths (Runs in ANY folder)**:
  * `C:\Users\Asus\.gemini\config\skills\`
  * `C:\Users\Asus\.gemini\antigravity-cli\skills\`
  * `C:\Users\Asus\.gemini\skills\`

---

## 🚀 One-Liner to Add All Skills to a New Project

In any future project directory in PowerShell:
```powershell
New-Item -ItemType Directory -Path .\.agents\skills -Force
Get-ChildItem -Path "C:\Users\Asus\Desktop\agy-skills\*\*" -Directory | ForEach-Object { Copy-Item $_.FullName -Destination .\.agents\skills -Recurse -Force }
```
