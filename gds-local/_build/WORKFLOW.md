# Build & Publishing Workflow

## What build.py does

`build.py` is a zero-dependency Python script that assembles full HTML pages from:
- **Shared partials** (`_build/_partials/`) — the GOV.UK header, footer, layout CSS, CDN asset fixes, and sidebar navigation that every subpage needs. Change once, applies everywhere.
- **Page sources** (`_build/_pages/`) — one file per page containing only the page-specific content, with a front matter block declaring its title, caption, and publication status.

It reads each page source, wraps the content in the shared partials, and writes the assembled HTML. It also:
- Generates all pages to `preview/` regardless of status (for sharing/feedback)
- Only writes to root (the live location) for `status: published` pages
- Copies hand-authored files (`_build/_hand/index.html`) to `preview/` without touching the root published version
- Generates `preview/directory.html` — a link index listing all preview pages with their status
- Manages "View X detail →" links in index.html for published/modified pages

## Branch and PR workflow

1. **Create a branch** from main on your fork for the changes you're making
2. **Edit** source files in `_build/_pages/` or `_build/_hand/`
3. **Run** `python3 gds-local/_build/build.py` locally to generate output
4. **Commit** both source files and generated output to your branch
5. **Push** to your fork and open a PR against `govuk-digital-backbone/publish-ea` main
6. **Review** — reviewers can check the generated `preview/` pages in the PR diff, or merge to their own fork to see them rendered
7. **Merge** — once approved, the PR merges to upstream main. GitHub Pages serves the committed HTML via Jekyll (pass-through, no transformation happens since our files aren't Jekyll templates)

## Publication status controls

| Status in front matter | Root (live site) | Preview | Index link |
|---|---|---|---|
| `published` | Written/updated | Written | Yes |
| `modified` | Untouched (keeps last-approved version) | Written with latest changes | Yes (points to old root) |
| `draft` | Not written | Written | No |

## What requires Python locally

Running `build.py` is the only step that needs Python 3 (pre-installed on macOS and Linux; available via Microsoft Store on Windows). Without it, you can still edit source files and commit them — but the generated output won't update until someone with Python runs the build.
