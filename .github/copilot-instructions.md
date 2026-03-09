# Copilot Instructions for Smart Study Hub

This project is a small Python-backed educational site. The codebase is mostly scaffolding and static
assets at the moment; application logic lives in three top-level Python modules which are currently
empty (`app.py`, `config.py`, `database.py`). The HTML layout and user flows are expressed in the
`templetes/` directory (note the misspelling) with subfolders for `admin` and `Student` panels.

## Architecture Overview

1. **Entry point files**
   - `app.py` is intended to initialize the web framework (Flask or similar) and register routes.
   - `config.py` should hold configuration constants (database URI, secret keys, etc.).
   - `database.py` is supposed to define database connection logic/models.
   Currently these are placeholders; look for future additions or follow existing naming if you add
   new modules.

2. **Templates**
   - All frontend HTML is under `templetes/` using Jinja-style templating (e.g. `base.html` extends
     to other pages). Keep the same directory structure when adding pages for new roles or
     features.
   - `templetes/index.html` is the public landing page. Admin and Student views use
     `templetes/admin/` and `templetes/Student/` respectively.
   - Paths referenced in the Python code should match this folder exactly; pay attention to the
     typo in the folder name—it is intentional at the moment and changing it will break any
     hardcoded references.

3. **Static assets**
   - The `Static/` directory holds `css/`, `js/`, `images/`, and `uploads/` (with separate `notes/`
     and `pyqs/` subfolders).
   - Use `url_for('static', filename='...')` (or equivalent) in templates to reference these files.
   - Uploaded files are stored under `Static/uploads`; ensure any file-handling code matches that
     path.

4. **User roles & flows**
   - The HTML structure hints at two primary roles: *admin* and *student*.
   - Admin template pages include `dashboard.html`, `manage_sub.html`, `upload.html`, implying
     subject management and content upload features.
   - Student pages include `dashboard.html`, `quiz.html`, `resources.html`.
   - When writing backend routes or APIs, mirror these logical divisions.

5. **Dependencies & environment**
   - `requirements.txt` is currently empty but will list Python packages (Flask, SQLAlchemy, etc.).
   - Standard workflow is `python -m venv venv` then `pip install -r requirements.txt`.
   - No build or test commands are present; add `pytest` or linter commands here later as needed.

## Conventions & Patterns

- Use snake_case for Python module and function names.
- Templates use Bootstrap-esque structure; keep CSS classes consistent when adding new elements.
- The project currently avoids any JavaScript frameworks; keep client code lightweight and place it
  under `Static/js`.
- When referring to template or static paths in code, treat the case sensitivity as it appears on
  disk (Windows is case-insensitive but production may not be).

## Adding Features

1. **New routes**: define in `app.py` (or a new blueprint module) and render templates from
   `templetes/`. Example:
   ```python
   @app.route('/student/quiz')
   def student_quiz():
       return render_template('Student/quiz.html')
   ```
2. **Database changes**: update `database.py` with models or helper functions and import in
   `app.py` or other modules. Follow PEP 8 style.
3. **Static files**: add CSS/JS under `Static/` and reference via `url_for('static', filename='css/foo.css')`.
4. **Uploads**: saved under `Static/uploads/notes` or `pyqs`; ensure path logic uses `os.path.join`
   and checks for directories.

## Developer Workflows

- **Running the app**: currently no run script; typical command is
  `python -m flask run` or `python app.py` once `app.py` is implemented.
- **Testing / linting**: none defined. Add tests under a `tests/` folder and adjust
  `requirements.txt` accordingly.
- **Version control**: normal Git workflow. Keep the `.github` folder for future issue templates.

> ⚠️ There is no existing `.github/copilot-instructions.md`. This file is the initial guidance. If
> the structure evolves, update this document and ask for feedback.

Let me know if there are any areas you think need more detail or explanations! Adjustments can be
made to ensure AI agents understand the project's specifics.