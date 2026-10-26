# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

PublishEA: a static website of enterprise architecture resources for the UK public sector. It is served by GitHub Pages at `architecture.cddo.cabinetoffice.gov.uk` (see `CNAME`). Merging to `main` deploys automatically. Jekyll passes the HTML through unchanged. The upstream repo is `gds-dtx/publish-ea`. The project is at proof-of-concept stage.

The repo has no root-level build, lint or test tooling. How you work depends on which section you are editing.

## Two kinds of section

### 1. Hand-authored static pages (most of the repo)

`index.html` (landing page), `psai-tech/`, `digital-capability-model/`, `guidance/`, `Tools/` and `citizen-architecture/` are plain, self-contained HTML files. Edit them directly. To preview, open them in a browser. There is no build step.

- Each page loads **GOV.UK Frontend 5.13.0 from the jsDelivr CDN** (CSS plus a `type="module"` JS init) and has its own inline `<style>` block. No CSS is shared between pages. When you change a layout or pattern, copy the change by hand into the sibling pages that use it.
- Header, service nav (Documentation / Contact `mailto:`) and footer markup is duplicated in every page. Update every copy together.
- Images go in `images/` (or a section's own `images/`). Downloadable artefacts (e.g. `.xlsx` playbooks) go in `downloads/`.
- When you add a page, add links to it from `index.html` and/or the section's `index.html`.
- The README lists `AI-Technology-Enablement/`, but that directory does not exist. The AI content lives in `psai-tech/`.

### 2. `gds-local/`: the Local Government Architecture Model (LGAM), which has a build

This sub-project has its own npm dependencies and a Python build. **Read [gds-local/AGENTS.md](gds-local/AGENTS.md) before working in it.** It is the authoritative guide: it covers the page source format, front matter, statuses, SCSS approach, taxonomy colours and content rules. Its "scope to gds-local only" instruction applies to sessions working on LGAM, not to the whole repo. Also see `gds-local/_build/WORKFLOW.md` and `gds-local/resources/README.md`.

```bash
cd gds-local && npm install         # govuk-frontend 6.x, sass, MoJ frontend
python3 gds-local/_build/build.py   # compile SCSS, copy GOV.UK JS bundle, assemble pages
```

Rules that are easy to break:
- **Generated files are committed.** Any `gds-local/` page that has a source in `_build/_pages/`, plus everything under `preview/` and `css/application.css`, is build output. Edit the sources in `_build/_pages/`, `_build/_partials/` or `src/scss/`, rebuild, and commit both the sources and the output. `index.html` and `gds-local-alt.html` are hand-authored. Changes you haven't published yet go in `_build/_hand/`, which is copied to `preview/` only.
- The `status:` front matter decides where a page is written. `published` goes to root and `preview/`, and `build.py` injects a "View X detail →" link into `index.html`. `draft` goes to `preview/` only. `modified` goes to `preview/` only and leaves the root copy at its last-published version.
- `gds-local` uses **GOV.UK Frontend v6, compiled locally**, while the rest of the site uses v5 from the CDN. Don't mix the two approaches. Never edit `node_modules/govuk-frontend`. Override it in `src/scss/components/`.
- Keep the v5-style inline header (service name inside `govuk-header`). Don't switch to `govuk-service-navigation`.
- LGAM content must use exact taxonomy naming (from `resources/lgam-data.json`), use British English, and follow `resources/lgam_architectural_principles.md`.

## Conventions across the site

- Follow GOV.UK Design System patterns and accessibility practice: skip links, semantic HTML, contrast. The primary colour is `#1d70b8`, and the font is GDS Transport with an Arial fallback.
- Use British English throughout.
- Contributions arrive as PRs from forks against `gds-dtx/publish-ea` `main`.
