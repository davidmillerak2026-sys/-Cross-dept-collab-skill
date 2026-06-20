# Package Boundary

This repository keeps two different kinds of materials separate.

## SkillHub Upload Package

Use this folder or the matching ZIP for platform upload:

- `skillhub_upload_clean/industrial-cross-department-collaboration/`
- `release_zips/industrial-cross-department-collaboration-clean-20260620-v26.zip`

This package contains only product-facing Skill materials:

- `SKILL.md`
- `README.md`
- `VERSION.md`
- `submission_manifest.json`
- `templates/`
- `references/`

It intentionally excludes:

- local debugging logs
- manual GUI run records
- screenshots and visual upload evidence
- internal planning notes
- scoring or benchmark utilities
- helper scripts
- contest strategy documents
- example outputs and sample data

## Evidence Archive

Use this folder for traceability, internal review, and post-submission analysis:

- `evidence_archive/`

It contains the full development package snapshot, upload ZIP snapshot, platform screenshots, AstronClaw/SkillHub real run records, model run outputs, score reports, and submission materials.

These materials are useful for engineering traceability, but they should not be mixed into the SkillHub upload package.

## Official Submission Guide Alignment

The clean upload package was prepared against the official Skill development and submission guide:

- `SKILL.md` is present within one top-level directory.
- `name`, `description`, and `version` are declared in front matter.
- File count is below 500.
- Total package size is below 100 MB.
- Single file size is below 10 MB.
- No helper scripts, test outputs, screenshot evidence, or internal strategy notes are included in the upload package.
- The ZIP contains no nested ZIP files.

Official guide URL:

https://challenge.xfyun.cn/topic/info/md?md=https://openres.xfyun.cn/xfyundoc/2026-06-04/e8f94fb5-8626-45fe-91c3-f18130ec5348/1780542909612/Skill%E5%BC%80%E5%8F%91%E4%B8%8E%E6%8F%90%E4%BA%A4%E6%8C%87%E5%8D%97.md
