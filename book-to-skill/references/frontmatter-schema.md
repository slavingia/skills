# Frontmatter Schema for Claude Code Skills

Every `SKILL.md` starts with a YAML frontmatter block between two `---` markers. The fields below follow the Claude Code skill loader's expectations. Anything outside this list will be ignored.

## Required fields

### `name`

- Format: lowercase, hyphenated, ≤ 64 characters.
- Used as the skill's invocation handle (e.g. `/find-community`).
- Must be unique within the repo.
- Should match the folder name (`skills/<name>/SKILL.md`).

```
name: find-community
```

### `description`

- One paragraph, ≤ 1024 characters.
- The agent uses this to decide when to invoke the skill automatically.
- Include both the trigger phrase ("when the user asks about X") and sideways entry points ("when the user is starting a new project", "when the user feels stuck").
- Bad: vague ("Helps with business stuff").
- Bad: a single trigger ("Use when validating an idea").
- Good: 3-5 trigger phrases plus 1-2 sideways entries.

```
description: Find and evaluate communities to build a business around.
Use when looking for a business idea, evaluating which community to serve,
or deciding whether a community is underserved. Also relevant when a
product exists but the founder isn't sure who it actually serves.
```

## Optional but recommended

### `argument-hint`

- Free-text hint shown by some agents after the slash command.
- Helps the user know what to type.

```
argument-hint: describe your decision or situation
```

### `allowed-tools`

- If you want the skill to explicitly limit which tools it can use.
- Default: the agent's full toolset. Only restrict when necessary.

### `model`

- Override the default model for this skill.
- Rarely needed. Only set when the skill's tasks demand a different model.

## What NOT to put in frontmatter

- The skill's "core principle" or "output format." That goes in the body.
- Long trigger lists. The description is short; the body elaborates.
- Cross-references to other skills. Use natural prose in the body instead.
- Markdown headers. Frontmatter is YAML only.

## Validator checklist

Before saving a `SKILL.md`:

- [ ] First non-blank line after the opening `---` is `name:`
- [ ] `name` is lowercase, hyphenated, ≤ 64 chars
- [ ] `description` is one paragraph, ≤ 1024 chars
- [ ] `description` lists at least 3 trigger phrases plus 1 sideways entry
- [ ] If `argument-hint` is present, it is one short line
- [ ] No other top-level keys beyond `name`, `description`, `argument-hint`, `allowed-tools`, `model`

## Example minimal frontmatter

```yaml
---
name: where-next
description: Reclaim your time, align with ikigai, and decide what
comes after profitability. Use when the business is profitable but the
founder is burned out, when considering whether to scale, hold, hand
off, sell, or close.
---
```

## Example full frontmatter

```yaml
---
name: where-next
description: Reclaim your time, align with ikigai, and decide what
comes after profitability. Use when the business is profitable but the
founder is burned out, when considering whether to scale, hold, hand
off, sell, or close.
argument-hint: describe where you are and what you're stuck on
---
```

The second example is the default. Add `argument-hint` whenever the skill benefits from the user knowing what to type.