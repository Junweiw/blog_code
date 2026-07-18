# Content-infra sync pack

Canonical destination (your machine + GitHub):

`~/.../context-infrastructure/rules/skills/`

## Install locally

```bash
cd /path/to/context-infrastructure
cp /path/to/this/content-infra/rules/skills/workflow_infographic_to_editable_ppt.md rules/skills/
# then add the bullet from INDEX-ENTRY.md into rules/skills/INDEX.md
git add rules/skills/
git commit -m "Add workflow skill: infographic to editable PPT"
git push
```

This Cloud Agent cannot push to `Junweiw/context-infrastructure` (403). Push from your local clone.
