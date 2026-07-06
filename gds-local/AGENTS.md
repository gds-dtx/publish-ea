# AGENTS.md

This file provides guidance to OpenCode and Claude Code when working with code in this repository.

## Scope

Work in this session is scoped to the `gds-local/` folder only. The parent `publish-ea` repository contains other architecture resources — ignore them unless explicitly asked.

## What This Is

GDS Local is the **Local Government Architecture Model (LGAM)** — a 5-layer reference architecture for UK local government digital services. It is part of the wider PublishEA enterprise architecture resource library maintained by the GOV.UK Digital Backbone team.

The upstream repository is `https://github.com/govuk-digital-backbone/publish-ea`. Deployment is via **GitHub Pages** (auto-deploys on merge to main). Live at `architecture.cddo.cabinetoffice.gov.uk/gds-local/`.

## Development

This project uses the official `govuk-frontend` NPM package for styling and JavaScript.

**Prerequisites:**
- Node.js (for `npm`)
- Python 3 (for the build script)
- Dart Sass (installed globally via `npm install -g sass`)

**Workflow:**
1. Install dependencies: `npm install` (within `gds-local/`)
2. Edit custom styles in `src/scss/`
3. Edit page content in `_build/_pages/`
4. Run the build script: `python3 _build/build.py`

### Customisation Approach

To ensure updates to GOV.UK Frontend do not break LGAM customizations, we use an override-first approach:
- **Never modify `govuk-frontend` files directly.**
- We define our custom variables (e.g. `$govuk-brand-colour`) in `src/scss/_settings.scss`.
- We import GOV.UK Frontend (`@import "govuk-frontend/dist/govuk/all"`) in `src/scss/application.scss`.
- Component-specific overrides (like `_lgam-accordion.scss` and `_lgam-tags.scss`) are imported *after* the GOV.UK dependencies.
- Use `@extend` targeting vanilla classes (e.g. `@extend .govuk-tag`) or custom variables (`%lgam-tag-base`) whenever possible rather than duplicating CSS blocks.

### Build system for subpages

Subpages (everything except `index.html` and `gds-local-alt.html`) are **generated** by a Python build script from shared partials + per-page source files:

```bash
python3 _build/build.py
```

This script:
1. Compiles `src/scss/application.scss` to `css/application.css` using Dart Sass.
2. Copies the UMD JavaScript bundle (`all.bundle.js`) from `node_modules` to `js/govuk-frontend.min.js`.
3. Assembles the output HTML files from `_build/_partials/` (header, footer) and `_build/_pages/` (content).

**Do not edit generated HTML files directly** — edit the source in `_build/_pages/` instead, then re-run `build.py`. Generated files are committed to git for legacy GitHub Pages deploy-from-branch.

The build script also generates a local preview index at `preview/directory.html`, grouping pages by folder hierarchy.

### Page source format

Each `_build/_pages/*.html` file has front matter and tagged content blocks:

```html
---
title: Page Title
caption: LGAM Capabilities    # or "LGAM Business Areas"
status: published              # or "draft"
description: "Summary outlining the purpose and content design concept of the page" # Optional, used in preview directory
redirect_from:                 
  - "old-path.html"            # Optional temporary shim. Do not use for new pages; intended to be removed once pages graduate to live.
---
<style>/* page-specific CSS */</style>
<nav-contents><!-- sidebar Contents li items --></nav-contents>
<main-content><!-- main page content --></main-content>
<page-script>/* optional page-specific JS */</page-script>
```

- `status: published` — build.py adds a "View X detail →" link in the matching index.html item
- `status: draft` — HTML is built (for preview) but no link appears in index.html

## Architecture: The 5-Layer Model

The LGAM describes local government services as a stack of five layers (top to bottom):

1. **Public Channels** — how citizens reach the council (Online, Phone, In Person, etc.)
2. **Council Agents** — interfaces that handle interactions (Website, API Gateway, App, Human, etc.)
3. **Capabilities** — reusable functional tools (Payments, Forms, Identity, Booking, Workflow, etc.)
4. **Business Areas / Functions** — service domains (Planning, Housing, Adult Social Care, etc.) with optional granular Functions beneath them
5. **IT Systems** — underlying technology (CRM, ERP, domain-specific systems)

Relationships flow downward: channels route to agents, agents use capabilities, capabilities support business areas, business areas are served by IT systems.

## Key Files

| File | Purpose |
|---|---|
| `index.html` | Main LGAM page — hand-authored, sidebar nav, coloured capability blocks |
| `gds-local-alt.html` | Interactive graph view using **Vis.js Network** — hand-authored |
| `_build/build.py` | Build script — assembles subpages from partials + page sources |
| `_build/_partials/` | Shared HTML fragments (header, footer, layout CSS, CDN fixes) |
| `_build/_pages/` | Page source files (edit these to change subpage content) |
| `preview/directory.html` | **Generated** — Local preview index grouping drafts and modifications |
| `business-area/adult-social-care/index.html` | **Generated** — Example hierarchical taxonomy-aligned page |
| `payments.html` | **Generated** — Example root-level page |
| `resources/lgam-data.json` | Graph data (nodes + edges) without Function-level detail |
| `resources/lgam-data-lgaFunctions.json` | Extended graph data including Function nodes |

## Tech Stack & Asset Dependencies

- **GOV.UK Frontend 6.x** (CSS + JS) compiled locally via npm/Sass — provides Design System components (accordions, details, header, footer, phase banner)
- **Vis.js Network** via unpkg — interactive graph rendering in `gds-local-alt.html`
- **Tailwind CSS** via CDN — used only in `gds-local-alt.html`
- **GDS Transport** web font with Arial fallback

All pages initialise GOV.UK Frontend JS using local paths. `build.py` handles the prefixing to ensure relative paths resolve correctly from subdirectories:
```html
<script src="{{ prefix }}js/govuk-frontend.min.js"></script>
<script>
  window.GOVUKFrontend.initAll();
</script>
```

## Customising the Frontend (Sass / CSS)

All styling is managed in `src/scss/`. **Do not** edit `css/application.css` directly, as it will be overwritten by `build.py`.

1. **Overriding GOV.UK Variables**: To override default GOV.UK Frontend Sass variables (e.g. `$govuk-brand-colour`), pass them into the `with (...)` configuration block in `src/scss/application.scss`:
   ```scss
   @use "node_modules/govuk-frontend/dist/govuk/index" as * with (
     $govuk-assets-path: "/assets/"
     // Add overrides here
   );
   ```
2. **Adding Custom CSS Classes**: Add any custom utility classes, component overrides, or new styling to the partials in `src/scss/components/` (e.g. `_index.scss` or `_shared-components.scss`). 
3. **Recompiling**: Run `python3 _build/build.py` from the `gds-local` directory. This script uses `libsass` to compile the SCSS into `css/application.css` before assembling the HTML pages.

## GOV.UK Frontend v6 Header Layout Note

In GOV.UK Frontend v6, the standard `govuk-header` component was split, removing the inline service name and moving it to a new `govuk-service-navigation` band. To preserve vertical space, we have manually recreated the v5 inline layout classes (`.govuk-header__content`, `.govuk-header__service-name`) in `src/scss/components/_index.scss`. 
**Do not** replace the header layout with `govuk-service-navigation` unless explicitly requested. Keep the service name inline inside the `govuk-header`.

## Graph Data Model

Nodes have: `id`, `label`, `type`, `description`
Edges have: `source`, `target`, `relationship` (one of `ROUTES_TO`, `USES`, `SUPPORTS`)

Node types: `PublicChannel`, `CouncilAgent`, `Capability`, `ITSystem`, `FunctionGroup`, `Function`

The same data model is used in both the JSON resource files and the inline data in `gds-local-alt.html`. When updating the model, keep both in sync.

## Design Conventions

- Follow **GOV.UK Design System** patterns: https://design-system.service.gov.uk/
- Use the GOV.UK colour palette — each layer has a distinct colour (blue, purple, teal, orange, red)
- All pages carry a **Beta phase banner**
- New subpages: create a file in the appropriate taxonomy-aligned folder (e.g., `_build/_pages/business-area/`) or a specific `topics/` folder (e.g. for cross-cutting concepts like the data sharing hub). Set `status: draft`, run `build.py`, iterate, then flip to `status: published` when ready
- Ensure accessibility: skip links, semantic HTML, sufficient contrast, ARIA attributes where needed

## Content Development Rules

- **Taxonomy Alignment:** Always check capabilities and business areas against the official taxonomy before adding them to pages. Do not deviate from the exact naming. Use `resources/lgam-data.json` or `_hand/lgam-content-tracker.csv` as the source of truth for LGAM nodes.
- **British English:** Always use British English spellings (e.g., categorise, centre, colour, cancelling).
- **Architectural Principles:** Ensure all domain and capability designs are consistent with the principles defined in `resources/lgam_architectural_principles.md`. If there is a compelling domain-specific reason to deviate, this must be discussed between you and the user and potentially recorded in the principles document. **Do not** include these internal debates or justifications in the public-facing HTML pages.

## LGAM Taxonomy Colours

When adding or styling elements for each LGAM layer, use the following hex codes for consistency:

- **Public Channels:** `#CC00CC`
- **Council Interfaces:** `#800080`
- **Capabilities:** `#000080`
- **Business Areas:** `#0000FF`
- **Corporate Areas:** `#696969`
- **Foundational Technology:** `#008080`
  - Artificial Intelligence: `#006400`
  - Developer and Operations Tooling: `#008000`
  - End User and Productivity: `#228B22`
  - Service Management: `#2E8B57`
  - Infrastructure & Hosting: `#556B2F`
- **Integration:** `#6B6B00`
- **Security:** `#CC0000`
- **Data and Information:** `#800000`
