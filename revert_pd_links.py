import os
import subprocess

FILES_TO_COPY = {
    "gds-local/_build/_pages/business-areas/planning-and-development/building-control.html": "gds-local/_build/_pages/ba-pd-building-control.html",
    "gds-local/_build/_pages/business-areas/planning-and-development/planning-policy.html": "gds-local/_build/_pages/ba-pd-planning-policy.html",
    "gds-local/_build/_pages/business-areas/planning-and-development/development-control.html": "gds-local/_build/_pages/ba-pd-development-control.html",
    "gds-local/_build/_pages/business-areas/planning-and-development/index.html": "gds-local/_build/_pages/ba-planning-hub.html"
}

LINK_REPLACEMENTS = {
    "building-control.html": "ba-pd-building-control.html",
    "planning-policy.html": "ba-pd-planning-policy.html",
    "development-control.html": "ba-pd-development-control.html",
    "index.html": "ba-planning-hub.html",
}

for src, dest in FILES_TO_COPY.items():
    subprocess.run(["git", "show", f"feature/folder-restructure:{src}"], stdout=open(dest, "w"))
    
    with open(dest, "r") as f:
        content = f.read()
    
    for old, new in LINK_REPLACEMENTS.items():
        content = content.replace(f'href="{old}"', f'href="{new}"')
        content = content.replace(f'parent: {old}', f'parent: {new}')
    
    with open(dest, "w") as f:
        f.write(content)

print("Files checked out and links reverted.")
