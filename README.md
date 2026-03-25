# The Minimalist Entrepreneur — Codex Skills

Codex skills based on [The Minimalist Entrepreneur](https://www.minimalistentrepreneur.com/) by Sahil Lavingia.

## Install For Codex

Clone the repo locally:

```bash
git clone https://github.com/slavingia/skills.git ~/src/minimalist-entrepreneur-skills
```

Install one or more skills into `~/.codex/skills`:

```bash
mkdir -p ~/.codex/skills
cp -R ~/src/minimalist-entrepreneur-skills/skills/* ~/.codex/skills/
```

If you want the repo to stay live-linked while you edit it locally, symlink individual skills instead of copying them:

```bash
mkdir -p ~/.codex/skills
ln -sfn ~/src/minimalist-entrepreneur-skills/skills/find-community ~/.codex/skills/find-community
```

Restart Codex after installing or updating skills.

## Using The Skills

Codex can pick these skills implicitly from natural-language requests, or you can invoke them explicitly with `$skill-name`.

## Skills

| Skill | Explicit invocation | When to use |
|-------|---------------------|-------------|
| **Find Community** | `$find-community` | Looking for a business idea or deciding which community to serve |
| **Validate Idea** | `$validate-idea` | Testing whether a business idea is worth pursuing before building |
| **MVP** | `$mvp` | Scoping the smallest product or service you can ship quickly |
| **First Customers** | `$first-customers` | Getting early customers through direct outreach and feedback |
| **Pricing** | `$pricing` | Setting an initial price, pricing model, or future tiers |
| **Marketing Plan** | `$marketing-plan` | Building a content-first marketing plan after early traction |
| **Grow Sustainably** | `$grow-sustainably` | Making spending, hiring, fundraising, or scaling decisions |
| **Company Values** | `$company-values` | Defining culture, values, and hiring signals |
| **Minimalist Review** | `$minimalist-review` | Gut-checking a business decision and simplifying the plan |

## The Minimalist Entrepreneur Journey

The skills follow the book's progression:

1. **Community** — Start by finding your people
2. **Validate** — Make sure the problem is worth solving
3. **Build** — Ship a manual process, then productize it
4. **Sell** — Get to 100 customers one by one
5. **Price** — Charge something from day one
6. **Market** — Build an audience through content
7. **Grow** — Stay profitable, grow sustainably
8. **Culture** — Build the house you want to live in
9. **Review** — Apply minimalist principles to every decision
