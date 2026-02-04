# CV Claw

An [OpenClaw](https://github.com/user/openclaw) skill for AI-powered resume tailoring. The agent's own LLM handles all tailoring logic -- no separate API calls needed.

## How It Works

1. You provide a job advertisement
2. The agent reads your master CV (`master_CV.yaml`)
3. Following the rules in `SKILL.md`, the agent tailors each section:
   - Parses job requirements
   - Reorders/filters sections by relevance
   - Tailors summary + skills (aligned together)
   - Tailors experience, projects, education, certifications, extracurricular
4. Writes a new `tailored_CV.yaml`
5. Validates and optionally renders to PDF

## Installation

### As an OpenClaw skill

Copy to your OpenClaw workspace:

```bash
cp -r . ~/.openclaw/workspace/skills/cv-claw/
```

Then copy `master_CV_template.yaml` to `master_CV.yaml` and fill in your details:

```bash
cp master_CV_template.yaml master_CV.yaml
```

### Dependencies

```bash
pip install pyyaml "rendercv[full]"
```

That's it. Two packages.

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Complete tailoring workflow and rules for the agent |
| `render.py` | YAML validation + PDF rendering utility |
| `master_CV.yaml` | Your master CV (source of truth, gitignored) |
| `master_CV_template.yaml` | Template for creating your master CV |
| `markdown/` | RenderCV Jinja2 templates (11 files) |

## Usage

### With an OpenClaw agent

Just ask:

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
// validate
{"valid": true, "errors": [], "warnings": []}

// render
{"success": true, "pdf": "output/tailored_CV.pdf", "error": null}
```

## Architecture

`SKILL.md` contains all tailoring logic as structured instructions. The agent's own LLM does the reasoning. Python (`render.py`) only handles validation and PDF rendering.

## Anti-Hallucination Rules

The skill enforces strict anti-hallucination rules:

- Only mention skills/technologies that exist in the master CV
- Never invent work experience, projects, or certifications
- Technology accuracy: if a project used SQL, don't add Python/pandas
- Cross-reference every technical term against the master CV
- When in doubt, omit rather than risk hallucination

See `SKILL.md` for the complete set of rules.

## YAML Format

The CV uses [RenderCV](https://github.com/sinaatalay/rendercv) YAML format. See `master_CV_template.yaml` for the full structure reference.
