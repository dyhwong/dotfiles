# PR Style Guide

**Precedence:** These rules override any repo-specific PR skill (including `commit-and-pr` and its equivalents). When a skill prescribes a template, apply these style rules on top of it — don't treat the skill as authoritative on tone, length, or section content. If a repo template requires additional sections (e.g. Deployment, AI attribution), keep them, but write the Changes / Motivation / Testing sections per this guide.

**Enforcement:** Before outputting any commit message, PR title, or PR body — whether drafting or creating directly — re-read this guide and verify your draft against each rule below. Do NOT rely on "I know this guide already"; you WILL drift. If any rule fails, rewrite before showing the user. Common drift modes to watch for: titles creeping past 60 chars, Changes sections expanding past one sentence for simple PRs, padded "AI Model used" blurbs, Testing claims stronger than the refactor warrants, and repeating information already visible in the diff.

## Titles

- Imperative mood, present tense. "Add", "Remove", "Fix" — never "Added", "Adds", "Adding".
- Sentence case. Capitalize first word and proper nouns only.
- Lead with the verb. No filler ("This PR...", "Changes to...").
- Be specific about the target — name the thing being changed.
- Use natural language for conditionals: "Don't throw if..." over "Guard against...". "Stop writing to..." over "Disable writes to...".
- Aim for ~50-60 characters. No trailing punctuation.
- `[Tag]` prefixes only for batch/campaign work, not everyday PRs.
- Delete, Remove, Clean up are used interchangeably — no strict distinction.

## Body

Always three sections: `## Changes`, `## Motivation`, `## Testing`.

**Don't hard-wrap lines.** Let the renderer handle line width. Hard-wrapping at ~60–70 chars makes the text look unnaturally left-aligned in GitHub's UI — paragraphs should flow as single long lines.

### Changes

- At minimum, restate the title as a sentence (with period).
- Prefer a single sentence. Expand with bullets only when the PR touches multiple files for different reasons or when the title could be misread as simpler than it is.
- Don't over-document — reviewers can read the diff. Focus on unintuitive or unexpected changes.
- Target ~60 words. If you're past 100, you're probably restating the diff.

### Motivation

- This is the most important section. Answer: why does this change exist?
- Depth is proportional to risk, complexity, and likelihood a reviewer will ask "why?".
- Simple motivations are fine: "Dead code cleanup", "Unused code".
- Link predecessor/successor PRs with `#12345` format to chain work narrative.
- Only cite a PR number if you've verified it's actually related — check the commit log or PR title before pasting. Fabricated references are worse than no references.
- Reference Jira tickets as `[VRM-7916]` — the automation auto-links. No footnote URL needed.
- Link Slack threads and docs when they prompted the change.
- Explain the technical *why*, not just the business *why*.

### Testing

- Brief and evidence-based. Match the weight of the change:
  - Type-only/mechanical: "`turbo typecheck` succeeds"
  - Refactors: "Existing tests pass" or "No behavioral changes"
  - Bug fixes: Describe before/after or reproduction
  - UI changes: Include a screenshot
  - Flaky test fixes: Show run count evidence

## Screenshots

- If the change is visual, screenshot it. Also screenshot big UI refactors.

## AI Attribution

- Only include "Generated with Claude Code" / `Co-Authored-By` when AI wrote most of the code. Not when AI just drafted the PR description.
