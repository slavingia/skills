# The Minimalist Entrepreneur — Claude Code Skills

Claude Code skills based on [The Minimalist Entrepreneur](https://www.minimalistentrepreneur.com/) by Sahil Lavingia.

## Architecture

**Book-grounded advice.** The full book (159 pages) is indexed as markdown in `data/book/` and searchable at runtime via [qmd](https://github.com/tobi/qmd) semantic search. Skills query relevant passages before giving advice, grounding responses in specific quotes and page references.

**Progressive disclosure.** Each skill is a folder, not a monolith. `SKILL.md` is a routing document (~100-150 lines) that points to sub-files loaded on demand:

- `gotchas.md` — common failure modes (every skill has one)
- `references/` — detailed frameworks, templates, evaluation criteria

**Shared conventions.** `skills/_shared/conventions.md` defines the advisor persona, output standards, tool integration patterns, and skill progression logic. Read once, applied everywhere.

**Graceful tool degradation.** Skills use Exa, Perplexity, and Firecrawl when available for live research. If any tool is missing or fails, the skill continues in advisory-only mode. Nothing breaks.

## Skills

| Skill | Command | Tools Used | When to use |
|-------|---------|------------|-------------|
| **Find Community** | `/find-community` | Exa, Perplexity | Looking for a business idea, trying to find your community |
| **Validate Idea** | `/validate-idea` | Exa, Perplexity | Testing if a business idea is worth pursuing |
| **MVP** | `/mvp` | Firecrawl, Perplexity | Ready to build your first product, struggling with scope |
| **First Customers** | `/first-customers` | Exa | Have a product, need to find your first 100 customers |
| **Pricing** | `/pricing` | Firecrawl, Exa | Setting prices, considering price changes |
| **Marketing Plan** | `/marketing-plan` | Exa, Perplexity, Firecrawl | Have product-market fit, ready to scale with content |
| **Grow Sustainably** | `/grow-sustainably` | qmd only | Making decisions about spending, hiring, or scaling |
| **Company Values** | `/company-values` | qmd only | Defining culture, preparing to hire |
| **Minimalist Review** | `/minimalist-review` | qmd only | Gut-checking any business decision |

All skills also use **qmd** for book search when the collection is indexed.

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

## Installation

Clone and install as a Claude Code plugin:

```bash
git clone https://github.com/slavingia/skills.git ~/.claude/plugins/skills
```

Then in Claude Code:

```
/plugin install ~/.claude/plugins/skills
```

**Optional: enable book search.** Index the book content for semantic search during skill execution:

```bash
bash scripts/setup-qmd.sh
```

Requires [qmd](https://github.com/tobi/qmd) installed locally. If skipped, skills work normally but without book passage citations.

## Tool Requirements

All tools are **optional**. Skills work as advisory without any of them.

| MCP Server | Tools | Enhances | Purpose |
|------------|-------|----------|---------|
| Exa | `web_search_exa`, `company_research_exa` | find-community, validate-idea, first-customers, pricing, marketing-plan | Semantic search for companies, communities, competitors |
| Perplexity | `perplexity_search`, `perplexity_ask` | find-community, validate-idea, mvp, marketing-plan | Web-grounded research, market sizing |
| Firecrawl | CLI: `firecrawl scrape`, `firecrawl search` | mvp, pricing, marketing-plan | Competitor pricing pages, product analysis |
| Instant Domain Search | `search_domains`, `check_domain_availability` | validate-idea | Domain availability checks |
| qmd | `qmd query` | all skills | Book passage search with semantic ranking |

## Folder Structure

```
skills/
  _shared/
    conventions.md          # Advisor persona, tool patterns, output standards
    scripts/
      search-book.sh        # qmd wrapper for book queries
  find-community/
    SKILL.md                # Core instructions + pointers to sub-files
    gotchas.md              # Common failure modes
    references/             # Evaluation criteria, frameworks
  validate-idea/
  mvp/
  first-customers/
  pricing/
  marketing-plan/
  grow-sustainably/
  company-values/
  minimalist-review/
data/
  book/                     # 159 pages of book content (markdown)
    ch01-the-minimalist-entrepreneur/
    ch02-community-first/
    ...
scripts/
  setup-qmd.sh             # Index book content for semantic search
  convert-book-csv.py       # Book CSV to markdown converter
```
