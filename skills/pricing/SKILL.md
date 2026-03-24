---
name: pricing
description: "Use when setting prices, considering price changes, or figuring out what to charge for a product or service. Triggers: 'what should I charge', 'pricing strategy', 'how to price this'."
---

# Pricing

Applies minimalist entrepreneur pricing philosophy. Read `_shared/conventions.md` for cross-skill rules.

## Gotchas

Read `gotchas.md` before any pricing recommendation — common failure modes live there.

## Core Principle

**Charge something. Always.** The zero price effect (Dan Ariely) means there is a massive difference between free and $1. If you don't charge, you can't learn what customers actually value.

## Two Pricing Models

### Cost-Based Pricing
- Calculate costs (hosting, time, materials, payment processing fees)
- Add margin (20-50% typical)
- Best for: physical products, services with clear cost structure
- Example: retail buy wholesale, double the price (50% margin)

### Value-Based Pricing
- Price based on value to customer, not your costs
- A feature costing you nothing extra can be worth a premium to the customer
- Best for: software, digital products, high perceived value services
- Example: Netflix multi-screen costs them nothing but commands a premium

## Key Principles

1. **Start low, raise over time** — prices go up as products improve
2. **Pricing is iterative** — not permanent, just another thing to test
3. **Tiered pricing is the goal** — economy/business/first class for different segments
4. **Free trials, not free products** — trials are table stakes, but always with a clear path to paid
5. **Don't confuse marketing with giving away product** — ad-driven models make charging harder later

## Tool Integration

When the user needs competitive context:
- **Firecrawl**: `firecrawl scrape "<competitor>/pricing"` for direct pricing page extraction
- **Firecrawl search**: `firecrawl search "<product category> pricing" --scrape --limit 5`
- **Exa**: `web_search_exa` or `company_research_exa` for market comps and positioning

## Financial Independence Math

See `references/financial-independence-calculator.md` for the full step-by-step framework: monthly needs, price point, customers needed, timeline projections, and the Slack IPO concentration example.

## Discovery Questions

Ask the user:
1. What are your variable costs per unit/customer?
2. What are competing/alternative solutions charging?
3. What would make this a "no-brainer" purchase for your ideal customer?
4. What price lets you be profitable from customer #1?

## Output

Deliver:
1. Recommended pricing model (cost-based, value-based, or hybrid) with rationale
2. Initial price point with supporting logic
3. Potential tier structure for the future
4. Customers needed for financial independence (using the calculator)
5. When and how to revisit pricing
