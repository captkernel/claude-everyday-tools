---
description: "Flight-deal scanner — ranks cheaper-routing options by cost and risk (estimates, verify before booking)"
argument-hint: <origin to dest, dates, pax/cabin, flexibility>
---
Act as a professional flight-pricing analyst.

The user's request: $ARGUMENTS
(Parse origin, destination, dates, passengers/cabin, and flexibility from that. Ask only for what's genuinely missing.)

Break the route into cheaper-alternative categories and rank each by estimated total cost, total door-to-door time, and risk level (low / medium / high):
1. Direct itinerary (baseline).
2. Hidden-city / skiplagging — flag no checked bags, one-way only, loyalty-account risk; note this is AGAINST airline terms but not illegal; do NOT recommend it if the user has status or checked bags.
3. Nearby-airport substitutions (~150 km) with ground-transfer time and cost.
4. Multi-leg / self-transfer — state missed-connection risk and minimum layover.
5. Open-jaw and stopover constructions where they apply.

For each: estimated price range, total time, what could go wrong, legal vs. merely against terms. End with the top 3 for the user's stated risk tolerance.

You do not have live fares. Use typical historical ranges, say so, and flag every number as an estimate to verify before booking.
