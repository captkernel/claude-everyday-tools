# Register as Claude Code slash commands

Two of the prompts in `prompts.md` are the most reusable as on-demand commands:
the **Hidden Route Scanner** (the all-in-one route hunt) and the **Pricing Reality Check**
(the skeptical "how does this actually work" explainer). Below is how to wire them up.

Claude Code reads slash commands from Markdown files in a `.claude/commands/` directory.
- **Project-scoped:** `.claude/commands/` in the repo root → command appears as `/flights` for anyone in this project.
- **Personal (all projects):** `~/.claude/commands/` → available everywhere for you.

The filename becomes the command name (`flights.md` → `/flights`). `$ARGUMENTS` is replaced
with whatever you type after the command.

---

## 1. `/flights` — Hidden Route Scanner

Create `.claude/commands/flights.md`:

```markdown
---
description: Skeptical flight-pricing analyst — ranks cheaper-routing options by cost and risk
---
Act as a professional flight-pricing analyst.

The user's request: $ARGUMENTS
(Parse origin, destination, dates, passengers/cabin, and flexibility from that. Ask only for
what's genuinely missing.)

Break the route into cheaper-alternative categories and rank each by estimated total cost,
total door-to-door time, and risk level (low / medium / high):
1. Direct itinerary (baseline).
2. Hidden-city / skiplagging — flag no checked bags, one-way only, loyalty-account risk; note this
   is AGAINST airline terms but not illegal; do NOT recommend it if the user has status or checked bags.
3. Nearby-airport substitutions (~150 km) with ground-transfer time and cost.
4. Multi-leg / self-transfer — state missed-connection risk and minimum layover.
5. Open-jaw and stopover constructions where they apply.

For each: estimated price range, total time, what could go wrong, legal vs. merely against terms.
End with the top 3 for the user's stated risk tolerance.

You do not have live fares. Use typical historical ranges, say so, and flag every number as an
estimate to verify before booking.
```

Use it like:
```
/flights NYC to Lisbon, Jun 12 outbound / Jun 20 return, 2 adults economy, ±3 days, carry-on only
```

---

## 2. `/farecheck` — Pricing Reality Check

Create `.claude/commands/farecheck.md`:

```markdown
---
description: Separates real airline pricing mechanisms from myths, then gives an evidence-based method
---
Act as a flight-pricing analyst with a skeptical, evidence-based stance.

Context from the user (optional): $ARGUMENTS

Break down how airline/OTA pricing works in three buckets:
A. CONFIRMED MECHANISMS (airline docs, regulator filings, research) — revenue management / fare
   buckets, dynamic repricing, demand curves, fare-class availability, POS / currency differences.
B. PLAUSIBLE BUT UNCONFIRMED (weak evidence) — cookies inflating prices, IP personalisation, device
   surcharges, fingerprinting; cite what investigations actually found and rate strong/mixed/weak/debunked.
C. MYTHS — claims tested and not held up.

Then give a search method grounded ONLY in bucket A, explaining WHY each step helps (which real
mechanism it exploits). Flag any number or "studies show…" claim to verify.
```

Use it like:
```
/farecheck I keep hearing flights get pricier if you search twice — is that real?
```

---

### Quick setup (project-scoped, from the repo root)

```bash
mkdir -p .claude/commands
# then create .claude/commands/flights.md and .claude/commands/farecheck.md
# with the bodies above. Restart / reload Claude Code and type /flights or /farecheck.
```

All other prompts in `prompts.md` work fine pasted directly into a chat — only the two highest-reuse
ones are worth promoting to commands.
