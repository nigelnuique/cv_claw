#!/usr/bin/env python3
"""
CV Claw - YAML validation and PDF rendering utility.

Usage:
    python render.py validate <yaml_file>
    python render.py render <yaml_file> [--output-dir DIR]
"""

import sys
import os
import json
import subprocess
import re
import yaml


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_professional_summary(summary_data):
    errors, warnings = [], []
    if not isinstance(summary_data, list):
        errors.append("Professional summary must be a list of strings")
    else:
        for i, item in enumerate(summary_data):
            if not isinstance(item, str):
                errors.append(f"Summary item {i} must be a string")
    return errors, warnings


def validate_experience(experience_data):
    errors, warnings = [], []
    if not isinstance(experience_data, list):
        errors.append("Experience must be a list of entries")
        return errors, warnings
    required = ["company", "position", "start_date"]
    for i, exp in enumerate(experience_data):
        if not isinstance(exp, dict):
            errors.append(f"Experience entry {i} must be a dictionary")
            continue
        for field in required:
            if field not in exp:
                errors.append(f"Experience entry {i} missing required field: {field}")
        if "highlights" in exp and not isinstance(exp["highlights"], list):
            errors.append(f"Experience entry {i} highlights must be a list")
    return errors, warnings


def validate_projects(projects_data):
    errors, warnings = [], []
    if not isinstance(projects_data, list):
        errors.append("Projects must be a list of entries")
        return errors, warnings
    for i, proj in enumerate(projects_data):
        if not isinstance(proj, dict):
            errors.append(f"Project entry {i} must be a dictionary")
            continue
        if "name" not in proj:
            errors.append(f"Project entry {i} missing required field: name")
        if "highlights" in proj and not isinstance(proj["highlights"], list):
            errors.append(f"Project entry {i} highlights must be a list")
    return errors, warnings


def validate_education(education_data):
    errors, warnings = [], []
    if not isinstance(education_data, list):
        errors.append("Education must be a list of entries")
        return errors, warnings
    required = ["institution", "degree", "area"]
    for i, edu in enumerate(education_data):
        if not isinstance(edu, dict):
            errors.append(f"Education entry {i} must be a dictionary")
            continue
        for field in required:
            if field not in edu:
                errors.append(f"Education entry {i} missing required field: {field}")
        if "highlights" in edu and not isinstance(edu["highlights"], list):
            errors.append(f"Education entry {i} highlights must be a list")
    return errors, warnings


def validate_skills(skills_data):
    errors, warnings = [], []
    if not isinstance(skills_data, list):
        errors.append("Skills must be a list of entries")
        return errors, warnings
    for i, skill in enumerate(skills_data):
        if not isinstance(skill, dict):
            errors.append(f"Skill entry {i} must be a dictionary")
            continue
        if "label" not in skill:
            errors.append(f"Skill entry {i} missing required field: label")
        if "details" not in skill:
            errors.append(f"Skill entry {i} missing required field: details")
    return errors, warnings


def check_date_formats(cv_data):
    errors, warnings = [], []
    date_fields = ["start_date", "end_date"]
    sections = cv_data.get("cv", {}).get("sections", {})
    if not isinstance(sections, dict):
        return errors, warnings
    for section_name, section_data in sections.items():
        if section_name in ("experience", "education", "projects") and isinstance(section_data, list):
            for i, entry in enumerate(section_data):
                if isinstance(entry, dict):
                    for df in date_fields:
                        if df in entry:
                            val = entry[df]
                            if not isinstance(val, (str, int)) and val != "present":
                                warnings.append(
                                    f"{section_name} entry {i}: {df} should be string, int, or 'present'"
                                )
    return errors, warnings


def check_highlight_strings(cv_data):
    errors, warnings = [], []
    sections = cv_data.get("cv", {}).get("sections", {})
    if not isinstance(sections, dict):
        return errors, warnings
    for section_name, section_data in sections.items():
        if isinstance(section_data, list):
            for i, entry in enumerate(section_data):
                if isinstance(entry, dict) and "highlights" in entry:
                    highlights = entry["highlights"]
                    if isinstance(highlights, list):
                        for j, h in enumerate(highlights):
                            if not isinstance(h, str):
                                errors.append(
                                    f"{section_name} entry {i} highlight {j} must be a string"
                                )
    return errors, warnings


def check_required_entry_fields(cv_data):
    errors, warnings = [], []
    reqs = {
        "experience": ["company", "position"],
        "education": ["institution", "degree", "area"],
        "projects": ["name"],
    }
    sections = cv_data.get("cv", {}).get("sections", {})
    if not isinstance(sections, dict):
        return errors, warnings
    for section_name, required in reqs.items():
        if section_name in sections:
            data = sections[section_name]
            if isinstance(data, list):
                for i, entry in enumerate(data):
                    if isinstance(entry, dict):
                        for field in required:
                            if field not in entry or not entry[field]:
                                errors.append(
                                    f"{section_name} entry {i} missing required field: {field}"
                                )
    return errors, warnings


def fix_cpp_in_skills(cv_data):
    """Replace bare C++ with `C++` in skills details for Markdown safety."""
    warnings = []
    sections = cv_data.get("cv", {}).get("sections", {})
    skills = sections.get("skills", []) if isinstance(sections, dict) else []
    for i, skill in enumerate(skills):
        if isinstance(skill, dict) and "details" in skill and isinstance(skill["details"], str):
            original = skill["details"]
            # Don't double-escape already backtick-wrapped C++
            fixed = re.sub(r'(?<!`)C\+\+(?!`)', '`C++`', original)
            if fixed != original:
                skill["details"] = fixed
                warnings.append(
                    f"skills: Entry {i} - Replaced 'C++' with '`C++`' for Markdown safety."
                )
    return warnings


def validate_yaml_file(filepath):
    """Validate a YAML file for RenderCV compatibility.

    Returns dict: {"valid": bool, "errors": [...], "warnings": [...]}
    """
    errors = []
    warnings = []

    # Load YAML
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            cv_data = yaml.safe_load(f)
    except Exception as e:
        return {"valid": False, "errors": [f"Cannot read YAML: {e}"], "warnings": []}

    if not isinstance(cv_data, dict):
        return {"valid": False, "errors": ["YAML root must be a mapping"], "warnings": []}

    # Top-level structure
    if "cv" not in cv_data:
        return {"valid": False, "errors": ["Missing 'cv' top-level key"], "warnings": []}

    cv = cv_data["cv"]
    for field in ("name", "sections"):
        if field not in cv:
            errors.append(f"Missing required CV field: {field}")

    # Section validators
    section_validators = {
        "professional_summary": validate_professional_summary,
        "experience": validate_experience,
        "projects": validate_projects,
        "education": validate_education,
        "skills": validate_skills,
    }

    sections = cv.get("sections", {})
    if not isinstance(sections, dict):
        errors.append("Sections must be a dictionary, not a list")
    else:
        for name, data in sections.items():
            if name in section_validators:
                sec_errs, sec_warns = section_validators[name](data)
                errors.extend(f"{name}: {e}" for e in sec_errs)
                warnings.extend(f"{name}: {w}" for w in sec_warns)

    # Cross-section checks
    for check_fn in (check_date_formats, check_highlight_strings, check_required_entry_fields):
        errs, warns = check_fn(cv_data)
        errors.extend(errs)
        warnings.extend(warns)

    # Fix C++ in skills
    cpp_warnings = fix_cpp_in_skills(cv_data)
    warnings.extend(cpp_warnings)

    # If we fixed C++, write back
    if cpp_warnings:
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                yaml.dump(cv_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        except Exception as e:
            warnings.append(f"Could not write C++ fix back to file: {e}")

    # Round-trip serialization test
    try:
        yaml_str = yaml.dump(cv_data, default_flow_style=False, sort_keys=False, allow_unicode=True)
        yaml.safe_load(yaml_str)
    except Exception as e:
        errors.append(f"YAML serialization round-trip error: {e}")

    return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def render_cv(filepath, output_dir=None):
    """Render a YAML CV to PDF using RenderCV.

    Returns dict: {"success": bool, "pdf": str | None, "error": str | None}
    """
    if not os.path.exists(filepath):
        return {"success": False, "pdf": None, "error": f"File not found: {filepath}"}

    cmd = ["python", "-m", "rendercv", "render", filepath]
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        cmd.extend(["--output-folder-name", output_dir])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        return {"success": False, "pdf": None, "error": "RenderCV timed out after 60 seconds"}
    except Exception as e:
        return {"success": False, "pdf": None, "error": str(e)}

    if result.returncode != 0:
        err_msg = result.stderr.strip() if result.stderr else f"Return code {result.returncode}"
        return {"success": False, "pdf": None, "error": err_msg}

    # Find the PDF in the output
    search_dir = output_dir if output_dir else "rendercv_output"
    pdf_path = None
    if os.path.isdir(search_dir):
        for fname in os.listdir(search_dir):
            if fname.endswith(".pdf"):
                pdf_path = os.path.join(search_dir, fname)
                break

    # Also check stdout for path hints
    if pdf_path is None and result.stdout:
        for line in result.stdout.splitlines():
            if ".pdf" in line:
                # Try to extract a path
                match = re.search(r'[\w/\\:.-]+\.pdf', line)
                if match:
                    candidate = match.group()
                    if os.path.exists(candidate):
                        pdf_path = candidate
                        break

    return {"success": True, "pdf": pdf_path, "error": None}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python render.py validate <yaml_file>")
        print("  python render.py render <yaml_file> [--output-dir DIR]")
        sys.exit(1)

    command = sys.argv[1]
    filepath = sys.argv[2]

    if command == "validate":
        result = validate_yaml_file(filepath)
        print(json.dumps(result, indent=2))
        sys.exit(0 if result["valid"] else 1)

    elif command == "render":
        output_dir = None
        if "--output-dir" in sys.argv:
            idx = sys.argv.index("--output-dir")
            if idx + 1 < len(sys.argv):
                output_dir = sys.argv[idx + 1]
        result = render_cv(filepath, output_dir)
        print(json.dumps(result, indent=2))
        sys.exit(0 if result["success"] else 1)

    else:
        print(f"Unknown command: {command}")
        print("Use 'validate' or 'render'")
        sys.exit(1)


if __name__ == "__main__":
    main()
