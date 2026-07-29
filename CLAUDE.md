# Project Rules

- Public contents are limited to project documentation, rules, the distributable Skill, reusable templates, scripts, references, and fictional examples.
- Never commit local fonts, employer source projects, private prompts, client assets, or local review renders.
- `SKILL.md`, `assets/templates/`, `references/`, and `scripts/` are package source. After changing them, rebuild `dist/video-asset-generator.skill`, update `checksums.txt`, and update the README checksum.
- Keep generated and disposable files in ignored `work/`.
- Use `npx hyperframes` for documented HyperFrames commands.
- Run relevant script checks, package inspection, checksum verification, and privacy scans before publishing.
- Commit and push completed repository changes to `main` unless the user explicitly requests an experiment branch.
