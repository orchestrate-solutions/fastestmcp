## Repo Reorganization Proposal — 2025-09-03

Purpose: Propose a clean, minimal reorganization of the `fastmcp-templates` repository to improve discoverability, template reusability, and maintenance while preserving backwards compatibility for existing users.

Immediate next step: this document records the proposed new layout, rationale, exact migration commands, packaging notes, CI and quality gates, and a small PR checklist to execute the change incrementally.

Plan
- Inventory current layout and concerns
- Propose a target layout (high-level and tree view)
- Provide step-by-step migration commands and import/packaging notes
- Recommend CI, linting, tests, and pre-commit hooks
- Provide a small incremental migration checklist and PR guidance

Goals and constraints
- Goals:
  - Make the repository easier to approach for newcomers
  - Make it simple to extract or reuse parts (client, server, examples) as templates
  - Keep packaging and installation straightforward (pip/pyproject/setup.py)
  - Preserve existing public APIs where possible to avoid breaking users
- Constraints:
  - Avoid large refactors in a single PR
  - Preserve existing top-level files used by packaging (`pyproject.toml`, `setup.py`, `requirements.txt`)
  - Keep changes transparent and reversible via git

Key observations from current layout
- Top-level mixes source, examples, docs, and server/client in multiple folders.
- `client/`, `server/`, `fastestmcp/`, and `examples/` contain useful code and demos but are not organized under a single `src/` or `packages/` convention.
- `DOCS/` already exists — a good place to hold repository-level guides like this one.

High-level recommendation
- Adopt a clearer top-level separation with the following intents:
  - `src/` (or `packages/`) contain installable Python packages
  - `examples/` keep runnable demo scripts and minimal configs
  - `docs/` (lowercase) for detailed docs and guides; keep `DOCS/` as source if desired but normalize to `docs/`
  - `templates/` (optional) to hold small copies or cookiecutter-friendly templates exposeable to other projects
  - `tests/` remains for unit/integration tests
  - Keep packaging and CI artifacts at repo root

Proposed target tree (condensed)

```
fastmcp-templates/                     # repo root (unchanged)
├── pyproject.toml
├── setup.py
├── requirements.txt
├── README.md
├── docs/                              # normalized docs (move content from DOCS/ and document/)
│   ├── repo-reorganization-2025-09-03.md
│   └── ...
├── src/
│   ├── fastmcp/                       # existing package moved here
│   ├── client/                        # client package
│   └── server/                        # server implementations moved here
├── examples/                          # runnable demos, small configs
│   ├── component_demo.py
│   └── ...
├── templates/                         # optional: minimal templates for reuse
├── tests/                             # tests remain at root for CI
└── .github/workflows/                 # CI workflows
```

Mapping from current paths (quick reference)
- `fastestmcp/` → `src/fastestmcp/` (standalone package; note: `fastestmcp` depends on `fastmcp` and should remain an independent distribution)
- `client/` (top-level) → `src/client/` or merge into `src/fastmcp/client` depending on package boundaries
- `server/` → `src/server/` (moved to consolidate primary server implementations)
- `DOCS/` + `document/` → `docs/` (consolidate and normalize filenames)
- `examples/` (already present) → keep under `examples/` but remove duplicates
- `tests/` → keep at root level for standard CI access

Migration steps (incremental, reversible)
1) Create `src/` and `docs/` directories locally and prepare a migration branch

   git checkout -b reorg/2025-09-repo-layout
   mkdir -p src docs

2) Move packages into `src/` and docs into `docs/` using `git mv` so history is preserved

   # move package folders
   git mv fastestmcp src/fastmcp
   git mv client src/client

   # move docs
   git mv DOCS docs/archive_DOCS
   git mv document docs/archive_document

   # move README and other top-level docs into docs/ as index or references
   git mv MCP-Client-Guide.md docs/ || true

3) Run a quick test that imports work locally (use PYTHONPATH or install editable)

   # Option A: temporary PYTHONPATH
   PYTHONPATH=$(pwd)/src python3 -c "import fastestmcp; print(fastestmcp.__name__)"

   # Option B: install editable (recommended for test)
   pip install -e .

4) Adjust `pyproject.toml` / `setup.py` package/module settings if necessary

   - If using `setuptools.find_packages()`, set `package_dir={'': 'src'}` and use `find_packages('src')`.
   - Example in `setup.py`:

     from setuptools import setup, find_packages
     setup(
         ...,
         package_dir={'': 'src'},
         packages=find_packages('src'),
     )

5) Update import paths and references only when tests show breakage (do minimal changes)

6) Create a small CI workflow to run lint and tests on the reorganized branch before merging

7) Merge in small, discrete PRs rather than one large change. Keep migration reversible by frequently running `git status` and `git diff`.

Example `git mv` commands (safe history-preserving moves)

```
git checkout -b reorg/repackage
git mv fastestmcp src/fastmcp
git mv client src/client
git mv DOCS docs/archive_DOCS
git mv document docs/archive_document
git commit -m "Reorganize repo: move packages into src/ and consolidate docs into docs/."
```

Packaging & import notes
- If `setup.py` or `pyproject.toml` currently rely on packages at repo root, set `package_dir={'': 'src'}` and ensure `MANIFEST.in` includes any data files now under `src/` or `docs/`.
- Tests and tools that import modules during CI should either install the package in editable mode (`pip install -e .`) or set `PYTHONPATH` to include `src/`.
- For backward compatibility, retain small top-level shim modules for a transition period (e.g., keep `client/__init__.py` at repo root that imports from `src.client` and warns about relocation).

CI, linting, and tests (recommended minimal setup)
- GitHub Actions workflow triggers: `push` to main, PRs to main, and optionally `pull_request_target` for protected branches.
- Steps:
  1. Checkout
  2. Set up Python
  3. Install dependencies (`pip install -r requirements.txt`) and editable install (`pip install -e .`)
  4. Run lint (flake8/ruff) and type check (mypy if used)
  5. Run tests (pytest) with coverage

Sample lightweight `ci.yml` (high-level; add file under `.github/workflows/ci.yml`)

```
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: python -m pip install --upgrade pip
      - run: pip install -r requirements.txt
      - run: pip install -e .
      - run: pip install ruff pytest
      - run: ruff check .
      - run: pytest -q

```

Pre-commit
- Add `pre-commit` to `requirements.txt` and a `.pre-commit-config.yaml` using `ruff`, `black` (if desired), and `isort` to keep style consistent.

Quality gates (brief mapping)
- Build: `pip install -e .` (PASS/FAIL) — ensure installable from `src/` structure
- Lint/Typecheck: `ruff` / `mypy` — ensure zero or minimal acceptable warnings
- Tests: `pytest` — cover happy path for templates/examples and at least one import smoke test
- Smoke test: run a small example script under `examples/` and assert it completes without exceptions

Contract for migration (short)
- Inputs: repository files on branch `reorg/*`
- Outputs: same codebase, relocated to `src/` + `docs/`, CI workflow added
- Success: repository installs (`pip install -e .`), tests pass on CI, and examples run locally
- Error modes: broken imports (fix with top-level shims or update imports), packaging metadata missing files

Edge cases and notes
- If some modules use namespace packages or rely on relative file paths, test them explicitly after moving.
- Keep `MANIFEST.in` in sync with moved documentation and packaging data files.
- If either `client/` or `fastestmcp/` are intended to be separate PyPI packages in the future, consider splitting them into separate repositories and making this repo a monorepo with clear package boundaries.

Small incremental migration plan (PR checklist)
1. Create branch `reorg/phase-1` and move `fastestmcp/` → `src/fastestmcp` and `DOCS/` → `docs/` using `git mv` (commit)
2. Run `pip install -e .` and fix packaging errors (commit small fixes)
3. Add CI workflow `ci.yml` that runs a smoke test and linter (commit)
4. Move `client/` to `src/client/` in a separate PR and add a small shim at the old location if needed
5. Consolidate `document/` and other docs into `docs/` and tidy docs structure
6. Final PR: remove shims and finalize `README.md`/CONTRIBUTING

Detailed actionable PR: move `fastestmcp` into `src/` (minimal, reviewable)

Goal: produce a small PR that only moves `fastestmcp/` into `src/fastestmcp`, updates packaging metadata, and verifies install and tests pass. This keeps risk minimal, preserves history, and allows CI to validate the change.

Step-by-step (commands to run locally and commit):

```
# create branch
git checkout -b reorg/phase-1-move-fastestmcp

# create src/ if missing and move fastestmcp preserving history
mkdir -p src
git mv fastestmcp src/fastestmcp

# move docs as part of this PR if desired (optional)
git mv DOCS docs/archive_DOCS || true

git commit -m "chore(reorg): move fastestmcp into src/fastestmcp (preserve history)"
```

Packaging changes
- If `setup.py` is used, update `setup.py` to use `package_dir` and `find_packages('src')`. Example diff to apply:

```
from setuptools import setup, find_packages

setup(
    name='fastmcp-templates',
    # ... other metadata ...
    package_dir={'': 'src'},
    packages=find_packages('src'),
)
```

- If `pyproject.toml` with `setuptools` backend is used, ensure the `[tool.setuptools.packages]` section points to `src` or use `find` with `where = ["src"]`.

fastestmcp as a standalone distribution
- Because `fastestmcp` is a separate distribution that depends on `fastmcp`, ensure `fastestmcp`'s packaging metadata declares that dependency. If the repository packages multiple distributions from `src/`, consider using a monorepo approach with separate `setup.cfg`/`pyproject.toml` per package or keep a single packaging entry that exposes both packages with distinct names.

Example `pyproject.toml` snippet for `fastestmcp` declaring `fastmcp` as a dependency (if you publish `fastestmcp` separately):

```
[project]
name = "fastestmcp"
version = "0.0.0"
dependencies = [
  "fastmcp>=0.0.0",
]

[tool.setuptools.packages.find]
where = ["src"]
include = ["fastestmcp*"]
```

Verification steps in PR
1. Add CI job or workflow entry to run `pip install -e .` and `pytest` (or run locally with editable install) to ensure imports work with packages under `src/`.
2. Run a quick smoke import in CI or a test such as:

```
PYTHONPATH=$(pwd)/src python3 -c "import fastestmcp; print(fastestmcp.__name__)"
```

3. If `fastestmcp` is going to be published independently, validate that `fastestmcp`'s packaging declares `fastmcp` as a dependency and that wheel builds succeed.

PR body template (copy into pull request for reviewers)

```
Summary

- Move `fastestmcp/` into `src/fastestmcp` to adopt the `src/` layout and avoid accidental imports from repo root.

Why

- Keeps package layout conventional and makes editable installs predictable.
- Preserves git history via `git mv`.

What changed

- `fastestmcp/` → `src/fastestmcp/` (moved)
- `setup.py` / `pyproject.toml` updated to find packages under `src/`

How to review

- Confirm `git mv` moved files (history preserved)
- Confirm CI runs `pip install -e .` and `pytest` successfully
- Optionally run `PYTHONPATH=$(pwd)/src python -c "import fastestmcp"` locally

Notes

- `fastestmcp` is a standalone distribution and depends on `fastmcp`. The packaging for `fastestmcp` declares `fastmcp` as a dependency.

```

After this PR merges, continue with the next PR that moves `client/` and consolidates documentation.


PR checklist before merging
- All tests pass in CI
- Linting & type checks pass
- `pip install -e .` succeeds on the workflow and locally
- No breaking changes to public APIs without a deprecation notice

Next steps (recommended)
1. Run the incremental plan starting with a small branch that moves `fastestmcp/` to `src/fastestmcp` and consolidates `DOCS/` into `docs/`.
2. Add the `ci.yml` and a `.pre-commit-config.yaml` for immediate feedback.
3. Consider adding a `templates/` folder and small example templates that consumers can copy or `git clone`.

Appendix: quick commands

```
# create branch
git checkout -b reorg/2025-09-03

# move packages and docs preserving history
git mv fastestmcp src/fastmcp
git mv client src/client
git mv DOCS docs/archive_DOCS
git mv document docs/archive_document
git commit -m "Move packages into src/ and consolidate docs into docs/."

# test install
pip install -e .

# run tests
pytest -q
```

If you'd like, I can open the first small PR on your behalf that only moves `fastestmcp/` into `src/` and adds a minimal CI workflow; that reduces risk and makes the migration easier to review.

-- End of proposal --
