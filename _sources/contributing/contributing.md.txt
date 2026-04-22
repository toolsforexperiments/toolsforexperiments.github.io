# Contributing

A guide to contributing code to any of the Tools for Experiments repositories.

---

## Workflow overview

### 1. Fork the repository

Go to the GitHub page of the repository you want to contribute to and click **Fork** in the top-right corner. This creates a personal copy of the repo under your GitHub account.

### 2. Clone your fork locally

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

### 3. Create a new branch

Never commit directly to `main`. Create a dedicated branch for your changes:

```bash
git checkout -b my-feature-branch
```

Use a short, descriptive name (e.g. `fix-calibration-bug`, `add-sweep-tool`).

### 4. Make your changes

Edit the code, add new files, or fix bugs. Once you're happy with the changes, stage and commit them:

```bash
git add <files>
git commit -m "Short description of what you changed"
```

### 5. Set up the environment with uv

Each repository uses uv to manage its environment. From the root of the cloned repo, run:

```bash
uv sync
```

This installs all dependencies (including dev tools like `ruff`, `mypy`, and `pytest`) into a local `.venv`. You don't need to activate it — prefix every command with `uv run` and uv will use the right environment automatically.

### 6. Run the checks locally

Before pushing, run the three checks below to catch issues early. **The CI pipeline runs the same checks automatically and will block your pull request from merging if any of them fail.**

Run all commands from the root of the repository (where `pyproject.toml` lives).

#### Linting — ruff

[ruff](https://docs.astral.sh/ruff/) checks code style and common errors:

```bash
uv run ruff check
```

The `.` (current directory) is implied when no path is given, so running `uv run ruff check` from the repo root checks all files in the project. To auto-fix issues where possible:

```bash
uv run ruff check --fix
```

#### Type checking — mypy

[mypy](https://mypy.readthedocs.io/) checks for type errors:

```bash
uv run mypy
```

Again, run this from the repo root — mypy reads the project configuration from `pyproject.toml` and knows which files to check.

Fix any reported type errors before submitting.

#### Tests — pytest

[pytest](https://docs.pytest.org/) runs the test suite:

```bash
uv run pytest
```

All tests must pass. If you added new functionality, add tests for it too.

### 7. Push and open a pull request

```bash
git push origin my-feature-branch
```

Then go to your fork on GitHub and click **Compare & pull request**. Fill in a description of what your changes do and why, then submit.

The CI pipeline will run `ruff`, `mypy`, and `pytest` automatically. You can follow the results in the **Checks** tab of your pull request. All checks must pass before the PR can be merged.

---

## Contributing to the documentation

The docs are written in Markdown using [MyST](https://myst-parser.readthedocs.io/) and built with [Sphinx](https://www.sphinx-doc.org/). Every page is a `.md` file inside the `docs/` directory.

### How the docs are organized

```
docs/
├── conf.py          # Sphinx configuration
├── index.md         # Top-level table of contents
├── guides/
│   ├── index.md     # Section table of contents
│   └── *.md         # Individual guide pages
├── contributing/
│   └── *.md
└── examples/
    └── *.md
```

Each `index.md` contains a `{toctree}` directive that lists the pages in that section. When you add a new page, register it there.

### Adding a new page

1. Create a new `.md` file in the appropriate section folder.
2. Add its filename (without extension) to the `{toctree}` in that folder's `index.md`:

   ````markdown
   ```{toctree}
   :maxdepth: 2

   existing-page
   your-new-page
   ```
   ````

### Editing an existing page

Just edit the `.md` file directly — it is plain Markdown with optional MyST directives.

### Building the docs locally

The docs repo has its own `pyproject.toml` at the root of `toolsforexperiments/` that includes Sphinx and its dependencies. First sync the environment:

```bash
uv sync
```

Then build the HTML from the `docs/` directory:

```bash
cd docs
uv run make html
```

The output is written to `docs/build/html/`. Open `docs/build/html/index.html` in your browser to preview the result:

```bash
open docs/build/html/index.html   # macOS
xdg-open docs/build/html/index.html  # Linux
```

To do a clean rebuild from scratch (useful if pages aren't updating):

```bash
cd docs
uv run make clean html
```
