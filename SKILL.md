# CV Claw - Resume Tailoring

Tailor a CV to a specific job advertisement. Accepts any CV format as
input, converts to RenderCV YAML, tailors each section, validates, and
optionally renders to PDF.

## When to Use

- User asks to tailor/customise their resume for a job
- User pastes a job ad and wants their CV updated
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

Use Australian English spelling throughout the tailored CV (e.g., "colour"
not "color", "centre" not "center", "organisation" not "organization",
"optimise" not "optimize").

## Workflow

1. **Ingest** the user's CV (any format -- see Step 0 below)
2. **Analyse** the job advertisement the user provides
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
- **key_technologies** - Specific technologies, tools, frameworks mentioned
- **soft_skills** - Soft skills and personal qualities mentioned
- **role_focus** - Main responsibilities and focus areas
- **industry_domain** - The industry or business domain
- **company_culture** - Cultural aspects or values mentioned
- **experience_level** - Required years of experience
- **certifications_required** - Any certifications or professional qualifications mentioned
- **technical_expertise** - Technical skills and expertise areas mentioned
- **professional_qualifications** - Professional qualifications, licenses, or credentials mentioned

Pay special attention to:
- Any mention of "technical and professional expertise"
- Certification requirements or preferences
- Professional qualifications or licenses
- Partner enablement or training requirements

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
- **Emphasise key technologies** mentioned in the job requirements
- **Keep all existing skills** but prioritise the most relevant ones
- **Maintain the original skill categories/structure** if they exist

#### Summary Section:
- Analyse the candidate's actual background from their experience and education
- Match to job requirements by highlighting relevant experience and skills
- Be honest about experience level -- do not inflate or invent experience
- **Structure**: 50-60 words, 2-3 sentences with varied openings
- **CRITICAL**: Only mention skills that appear in the tailored skills section

#### Alignment Rules (CRITICAL):
- **Perfect sync**: Every technical skill mentioned in the summary MUST appear prominently in the tailored skills section
- **Priority matching**: Skills mentioned in summary should be in the top tier of the tailored skills section
- **No hallucination**: Never mention skills not present in the original skills list
- **Consistency**: Use the same terminology for skills in both sections
- **Validation**: Before finalising, cross-check every technical term in summary against skills list
- **Zero tolerance**: If a skill is mentioned in summary, it MUST be findable in the skills section

#### Summary Style Rules:
- AVOID generic phrases like "Technical professional", "Experienced professional", "Skilled professional"
- Use specific, varied language that reflects the candidate's actual background
- NEVER use vague headers like "Technical Professional." Use the exact role title from the job ad, or substitute "[industry] professional," e.g., "Data Professional"
- If mentioning education, always highlight the most recent and highest degree (e.g., MS over BS)

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

#### Role-Specific Guidelines:
- **Technical roles**: Emphasise technical skills, projects, and problem-solving
- **Management roles**: Emphasise leadership, team management, and strategic thinking
- **Service roles**: Emphasise customer service, communication, and problem resolution
- **Creative roles**: Emphasise creativity, innovation, and project outcomes

#### Content Restrictions:
- DO NOT ADD technical skills to non-technical roles unless they were actually used
- DO NOT ADD data engineering, SQL, Python, or machine learning content to hardware/testing roles
- DO NOT ADD software development claims to service/retail roles
- Hardware/testing roles should focus on testing, quality assurance, and production support
- Service roles should focus on customer service, communication, and operational tasks

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
- Emphasise technologies and skills relevant to the job
- Highlight quantifiable results and impact
- Focus on problem-solving and technical implementation
- Keep descriptions concise and impactful

#### Technology Accuracy:
- Only mention technologies that were actually used in the project
- Do NOT add technologies that weren't part of the original project
- If original project used only SQL, do NOT add Python, pandas, or other technologies
- Example: If original says "using SQL", do NOT change to "using SQL, Python, and pandas"

#### Project Type Guidelines:
- **Technical projects**: Emphasise technical skills, algorithms, and problem-solving
- **Data projects**: Emphasise data analysis, visualisation, and insights
- **Web projects**: Emphasise full-stack development, user experience, and deployment
- **Research projects**: Emphasise methodology, analysis, and findings

#### Critical Rules:
- Base everything on the candidate's ACTUAL projects
- Do NOT invent new projects or technologies
- Maintain factual accuracy about what was actually built
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
- **Technical roles**: Emphasise technical coursework, programming, algorithms
- **Business roles**: Emphasise business, management, and analytical courses
- **Creative roles**: Emphasise design, communication, and creative courses
- **Research roles**: Emphasise research methodology, analysis, and specialised courses

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

1. **ONLY mention programming languages, tools, or technologies that are EXPLICITLY listed in the source CV**
2. **NEVER mention skills like Java, C#, .NET, Angular, React, etc. unless they are actually in the original skills list**
3. **If the job requires skills the candidate doesn't have, focus on transferable skills they DO have**
4. **Cross-reference every technical skill against the source CV's skills section**
5. **When in doubt about a skill, omit it rather than risk hallucination**
6. **Focus on the candidate's genuine strengths rather than trying to match every job requirement**
7. **NEVER invent work experience, projects, education, or certifications**
8. **Do not inflate responsibilities or achievements beyond what the source CV states**
9. **Technology accuracy**: If a project used SQL, do not add Python/pandas. If a role was hardware testing, do not add software development
10. **FINAL CHECK**: Before writing the tailored YAML, verify every technical term exists in the source CV

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
