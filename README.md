# CV Claw

An OpenClaw skill for AI-powered resume tailoring. The agent's own LLM handles all tailoring logic -- no separate API calls needed.

## How It Works

1. You provide your CV (any format) and a job advertisement
2. The agent converts your CV to RenderCV YAML (if not already)
3. Following the rules in `SKILL.md`, the agent tailors each section:
   - Parses job requirements
   - Reorders/filters sections by relevance
   - Tailors summary + skills (aligned together)
   - Tailors experience, projects, education, certifications, extracurricular
4. Writes a new `tailored_CV.yaml`
5. Validates and optionally renders to PDF

## Accepted CV Formats

- RenderCV YAML (used directly)
- PDF, Word (.docx), plain text, Markdown
- Pasted text in chat
- Any structured format (JSON, other YAML)

## Installation

### From ClawhHub

```bash
clawhub install cv-claw
```

### Manual

Copy to your OpenClaw workspace:

```bash
cp -r . ~/.openclaw/workspace/skills/cv-claw/
```

### Dependencies

```bash
pip install pyyaml "rendercv[full]"
```

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Complete tailoring workflow and rules for the agent |
| `render.py` | YAML validation + PDF rendering utility |
| `master_CV_template.yaml` | Reference template for RenderCV YAML format |
| `markdown/` | RenderCV Jinja2 templates (11 files) |

## Usage

Just ask your agent:

> "Tailor my resume for this job: [paste job ad]"

The agent reads `SKILL.md`, follows the workflow, and produces a tailored CV.

### Manual validation and rendering

```bash
# Validate YAML structure
python render.py validate tailored_CV.yaml

# Render to PDF
python render.py render tailored_CV.yaml --output-dir output
```

Both commands output JSON:

```json
{"valid": true, "errors": [], "warnings": []}
{"success": true, "pdf": "output/tailored_CV.pdf", "error": null}
```

## Architecture

`SKILL.md` contains all tailoring logic as structured instructions. The agent's own LLM does the reasoning. Python (`render.py`) only handles validation and PDF rendering. No external API keys required.

## Security

`render.py` makes **no network calls**. It only reads and writes local YAML files and shells out to `rendercv` for PDF generation. You can audit the entire script -- it's a single file under 350 lines.

## Anti-Hallucination Rules

The skill enforces strict anti-hallucination rules:

- Only mention skills that exist in the source CV
- Never invent work experience, projects, or certifications
- Do not add skills or tools to a role that weren't originally there
- Cross-reference every claim against the source CV
- When in doubt, omit rather than risk hallucination

See `SKILL.md` for the complete set of rules.

## YAML Format

The CV uses [RenderCV](https://github.com/sinaatalay/rendercv) YAML format. See `master_CV_template.yaml` for the full structure reference.

## License

MIT
