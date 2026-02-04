# CV Claw - Resume Tailoring

Tailor a CV to a specific job advertisement. Accepts any CV format as
input, converts to RenderCV YAML, tailors each section, validates, and
optionally renders to PDF.

## When to Use

- User asks to tailor/customise their resume for a job
- User pastes or references a job ad and wants their CV updated
- Agent finds a job listing (e.g. via web search or file) and needs to tailor a CV to it
- User asks to optimise their resume for a specific role
- User wants to convert their CV to a clean PDF

## Accepted CV Inputs

The user can provide their CV in **any** of these ways:

- **RenderCV YAML file** (e.g. `master_CV.yaml`) -- used directly
- **Any YAML/JSON file** -- converted to RenderCV format
- **PDF file** -- read and converted to RenderCV YAML
- **Word document** (.docx) -- read and converted to RenderCV YAML
- **Plain text / Markdown** -- pasted into chat or provided as a file
- **No CV provided** -- ask the user for their CV before proceeding

If a `master_CV.yaml` exists in this skill's directory, use it as the
default when the user doesn't specify a CV file.

## Files

- `master_CV_template.yaml` - Reference template for RenderCV YAML format
- `render.py` - Validation and PDF rendering utility
- `markdown/` - RenderCV Jinja2 templates (11 files)

## Dependencies

Only `pyyaml` and `rendercv[full]` are required.

## Language

Match the spelling conventions used in the source CV. If the source CV uses
British/Australian English (e.g., "colour", "organisation", "optimise"),
keep that throughout. If it uses American English (e.g., "color",
"organization", "optimize"), keep that instead. When unclear, default to
the conventions of the country where the job is located.

## Job Advertisement Input

The job ad can come from anywhere:

- **Pasted by the user** in chat
- **A file** (text, PDF, Word, HTML) provided by the user or found by the agent
- **A URL** the agent fetches
- **Already in context** from an earlier part of the conversation

If the job ad hasn't been provided yet, ask for it or fetch it before proceeding.

## Workflow

1. **Ingest** the CV (any format -- see Step 0 below)
2. **Obtain** the job advertisement (from user, file, URL, or context)
3. **Tailor** each section following Steps 1-7 below
4. **Write** the tailored CV to a new YAML file (e.g. `tailored_CV.yaml`)
5. **Validate**: `python render.py validate tailored_CV.yaml`
6. **Render** (if user wants PDF): `python render.py render tailored_CV.yaml`

---

## Step-by-Step Tailoring Process

### Step 0: Ingest the CV

Convert the user's CV into RenderCV YAML format. Use `master_CV_template.yaml`
as the structural reference.

#### If the CV is already RenderCV YAML:
- Read it directly. No conversion needed.

#### If the CV is any other format (PDF, Word, plain text, pasted text, JSON, etc.):
1. Read/extract all content from the source
2. Map it to the RenderCV YAML structure (see YAML Format Reference below)
3. Preserve **all** information -- do not drop any content during conversion
4. Write the converted CV to a YAML file (e.g. `source_CV.yaml`)
5. Run `python render.py validate source_CV.yaml` to confirm the structure is correct

#### Mapping rules:
- **Name, contact info, links** go under `cv:` top-level fields
- **Summary/objective/profile** goes into `sections.professional_summary` (as a list with one string)
- **Work history** goes into `sections.experience` (each role is a dict with company, position, start_date, end_date, location, highlights)
- **Projects/portfolio** goes into `sections.projects`
- **Education** goes into `sections.education` (institution, degree, area, dates, highlights)
- **Skills** goes into `sections.skills` (each category is a dict with label + details string)
- **Certifications/licenses** goes into `sections.certifications` (list of strings)
- **Activities/volunteering** goes into `sections.extracurricular` (each is a dict with label + details)
- Any section that doesn't fit the above can be added as a custom section name

#### Important:
- This step is about **faithful conversion**, not tailoring. Keep everything.
- The tailoring happens in Steps 1-7.
- The converted YAML becomes the source of truth for the rest of the workflow.
  **Never modify** the source file after this point -- all tailoring writes to
  a new file.

### Step 1: Parse the Job Advertisement

Extract the following from the job ad:

- **essential_requirements** - Must-have skills/qualifications
- **preferred_requirements** - Nice-to-have skills/qualifications
- **key_skills_and_tools** - Specific skills, tools, methods, or technologies mentioned
- **soft_skills** - Soft skills and personal qualities mentioned
- **role_focus** - Main responsibilities and focus areas
- **industry_domain** - The industry or business domain
- **company_culture** - Cultural aspects or values mentioned
- **experience_level** - Required years of experience
- **certifications_required** - Any certifications or professional qualifications mentioned
- **domain_expertise** - Specialist knowledge areas mentioned
- **professional_qualifications** - Professional qualifications, licenses, or credentials mentioned

Pay special attention to:
- Specific expertise or domain knowledge requirements
- Certification requirements or preferences
- Professional qualifications or licenses
- Industry-specific terminology or standards

### Step 2: Reorder and Filter Sections

Analyse the resume sections against the job requirements:

1. **Remove** sections not relevant to the role
2. **Reorder** remaining sections by importance to the job
3. For the extracurricular section, check first if any items are relevant -- if not, remove the section entirely
4. Keep sections that demonstrate relevant skills and experience
5. Be specific about why each section is kept, removed, or reordered

### Step 3: Tailor Summary and Skills (Together)

These two sections must be done **simultaneously** to ensure perfect alignment.

#### Skills Section:
- **Reorder skills** to put the most job-relevant ones first
- **Group related skills** together for better readability
- **Emphasise key skills and tools** mentioned in the job requirements
- **Keep all existing skills** but prioritise the most relevant ones
- **Maintain the original skill categories/structure** if they exist

#### Summary Section:
- Analyse the candidate's actual background from their experience and education
- Match to job requirements by highlighting relevant experience and skills
- Be honest about experience level -- do not inflate or invent experience
- **Structure**: 50-60 words, 2-3 sentences with varied openings
- **CRITICAL**: Only mention skills that appear in the tailored skills section

#### Alignment Rules (CRITICAL):
- **Perfect sync**: Every specific skill mentioned in the summary MUST appear prominently in the tailored skills section
- **Priority matching**: Skills mentioned in summary should be in the top tier of the tailored skills section
- **No hallucination**: Never mention skills not present in the original skills list
- **Consistency**: Use the same terminology for skills in both sections
- **Validation**: Before finalising, cross-check every skill claim in summary against skills list
- **Zero tolerance**: If a skill is mentioned in summary, it MUST be findable in the skills section

#### Summary Style Rules:
- AVOID generic phrases like "Experienced professional", "Skilled professional", "Dedicated worker"
- Use specific, varied language that reflects the candidate's actual background
- Use the exact role title from the job ad when possible, or a relevant industry-specific title
- If mentioning education, always highlight the most recent and highest qualification

### Step 4: Tailor Experience

#### Relevance Assessment:
- **Keep**: Roles directly related to the job requirements
- **Modify**: Roles with transferable skills that can be emphasised
- **Remove**: Clearly irrelevant roles that don't add value

#### Content Optimisation:
- Emphasise achievements and skills relevant to the target role
- Highlight transferable skills (leadership, problem-solving, etc.)
- Quantify results where possible
- Focus on impact and outcomes

#### Content Restrictions:
- DO NOT ADD skills or responsibilities to a role unless they were actually performed
- Each role should reflect what the candidate genuinely did -- not what the target job wants to hear
- Emphasise the aspects of each role that are most relevant to the target job, but do not fabricate

#### Critical Rules:
- Base everything on the candidate's ACTUAL experience
- Do NOT invent or inflate responsibilities
- Be honest about the nature of each role
- Focus on transferable skills and genuine achievements
- Maintain chronological order unless reordering improves relevance

### Step 5: Tailor Projects

#### Project Selection:
- Select the most relevant projects (max 4-5)
- Prioritise projects that demonstrate skills required for the job
- Remove projects that don't align with the role requirements

#### Content Optimisation:
- Emphasise skills, methods, and outcomes relevant to the job
- Highlight quantifiable results and impact
- Focus on problem-solving and implementation
- Keep descriptions concise and impactful

#### Accuracy:
- Only mention tools, methods, or skills that were actually used in the project
- Do NOT add skills or tools that weren't part of the original project

#### Critical Rules:
- Base everything on the candidate's ACTUAL projects
- Do NOT invent new projects or capabilities
- Maintain factual accuracy about what was actually done
- Keep project links and names intact

### Step 6: Tailor Education

#### Coursework Selection:
- Select the most relevant coursework (max 5 courses per institution)
- Prioritise courses that align with job requirements
- Remove irrelevant courses that don't add value
- If no courses are relevant, omit the coursework highlight entirely

#### Content Optimisation:
- Keep all factual information (institution, degree, dates, GPA, etc.)
- Optimise coursework highlights to emphasise relevant skills
- Maintain academic achievements and honours
- Keep thesis/capstone project descriptions intact

#### Relevance Guidelines:
- Prioritise coursework and achievements that align with the target role's requirements
- Emphasise any specialisations, honours, or research relevant to the job

#### Critical Rules:
- Do NOT invent courses or institutions
- Maintain factual accuracy about degrees, dates, and achievements
- Keep all academic honours, GPA, and scholarships
- Preserve thesis and capstone project descriptions -- NEVER truncate existing descriptions

### Step 7: Tailor Certifications and Extracurricular Activities

Handle both sections together -- they are both simple filtering/reordering tasks
that share the same job requirements context.

#### Certifications:

**Approach: Be INCLUSIVE** -- if there is any reasonable connection, keep it.

1. Include any certification that relates to any skill, technology, or area of expertise mentioned in the job requirements
2. Prioritise certifications that demonstrate proficiency in the job's key technical or professional areas
3. Order certifications by relevance to the job requirements (most relevant first)
4. Remove only certifications that are completely unrelated to the role's requirements
5. When in doubt, keep the certification

**Priority Order:**
1. Certifications for skills, technologies, or areas of expertise mentioned in the job requirements
2. Industry-specific certifications relevant to the role
3. Professional certifications that demonstrate relevant expertise
4. General certifications that show professional development

**Critical Rules:**
- Use ONLY the actual certifications from the source CV
- DO NOT create, invent, or generate new certification names
- If no certifications are relevant, remove the section entirely

#### Extracurricular Activities:

**Approach: Be SELECTIVE** -- only keep activities that add clear professional value.

1. Select ONLY extracurricular activities that demonstrate relevant skills or qualities
2. Order them by relevance to the target role
3. Remove activities that are:
   - Completely unrelated to professional skills
   - Too personal or not professionally relevant
   - Outdated or from too long ago
4. Keep activities that demonstrate:
   - Leadership skills
   - Teamwork and collaboration
   - Skills mentioned in job requirements
   - Qualities that align with company culture
   - Community involvement (if valued by company)

If none are relevant, remove the section entirely.

---

## Critical Anti-Hallucination Rules

These rules apply across ALL tailoring steps:

1. **ONLY mention skills, tools, or qualifications that are EXPLICITLY present in the source CV**
2. **NEVER add skills the candidate doesn't have** -- no matter how relevant they are to the job
3. **If the job requires skills the candidate doesn't have, focus on transferable skills they DO have**
4. **Cross-reference every skill claim against the source CV**
5. **When in doubt about a skill, omit it rather than risk hallucination**
6. **Focus on the candidate's genuine strengths rather than trying to match every job requirement**
7. **NEVER invent work experience, projects, education, or certifications**
8. **Do not inflate responsibilities or achievements beyond what the source CV states**
9. **Do not add skills or tools to a role/project that weren't originally listed there**
10. **FINAL CHECK**: Before writing the tailored YAML, verify every claim traces back to the source CV

---

## YAML Format Reference

The YAML file follows the RenderCV format:

```yaml
cv:
  name: "Full Name"
  location: "City, State"
  email: "email@example.com"
  phone: "+1234567890"
  website: "https://example.com"
  social_networks:
    - network: LinkedIn
      username: username
    - network: GitHub
      username: username
  sections:
    professional_summary:
      - "A single paragraph string (50-60 words)."

    skills:
      - label: "Category Name"
        details: "Skill1, Skill2, Skill3"

    experience:
      - company: "Company Name"
        position: "Job Title"
        location: "City, State"
        start_date: "2022-01"
        end_date: "present"
        highlights:
          - "Achievement or responsibility"

    projects:
      - name: "Project Name"
        date: "2023"
        highlights:
          - "What you built and the impact"
        link: "https://github.com/..."

    education:
      - institution: "University Name"
        area: "Field of Study"
        degree: "BS/MS/PhD"
        location: "City, State"
        start_date: "2018"
        end_date: "2022"
        highlights:
          - "Relevant coursework or achievements"

    certifications:
      - "Certification Name (Issuer, Year)"

    extracurricular:
      - label: "Activity Name"
        details: "Description of the activity"
```

### Date Formats
- `"2022-01"` (year-month)
- `"2022"` (year only)
- `"present"` (for current positions)
- Integers are also accepted (e.g. `2022`)

### Special Characters
- `C++` must be wrapped in backticks: `` `C++` `` (for Markdown safety)
- The `render.py validate` command will auto-fix this

---

## Validation and Rendering

### Validate
```bash
python render.py validate tailored_CV.yaml
```
Returns JSON: `{"valid": true/false, "errors": [...], "warnings": [...]}`

### Render to PDF
```bash
python render.py render tailored_CV.yaml --output-dir output
```
Returns JSON: `{"success": true/false, "pdf": "/path/to/file.pdf", "error": null}`
