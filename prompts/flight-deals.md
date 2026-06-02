# Flight-Pricing Analyst Prompt Pack

A clean, de-duplicated set of prompts that turn Claude into a **skeptical flight-pricing analyst**. Paste any one into a fresh chat, fill in the `[BRACKETED]` inputs, and run.

These are built on three ground rules, carried into every prompt:

1. **No live fares are assumed.** Unless the model has web/search access, it must say so and use typical historical ranges — and **flag every number as an estimate to verify** on the day of booking.
2. **Real mechanisms, not folklore.** Confirmed pricing levers (revenue management, point-of-sale differences, fare buckets) are kept strictly separate from unproven claims (cookies inflating prices, device surcharges).
3. **Three honesty tiers for tactics:** *Legitimate optimisation* (always fine) → *Against airline terms but not illegal* (e.g. hidden-city/skiplagging — explain the risk) → *Off-limits* (fraud, misrepresentation — clearly labelled and never recommended).

> Estimates only. Verify final fares, fees, and fare rules on the airline/booking site before paying.

---

## 1. Hidden Route Scanner
**When to use:** You have a specific route and want every cheaper-routing alternative ranked by cost *and* risk.

```
Act as a professional flight-pricing analyst.

ROUTE: [Origin City] → [Destination City]
DATES: [Outbound date] / [Return date, or "one-way"]
PASSENGERS: [Number, cabin class]
FLEXIBILITY: [± days; willing to add stopovers? carry-on only?]

Break this route into the cheaper-alternative categories below and rank each by
estimated total cost, total door-to-door travel time, and risk level (low / medium / high):

1. Direct itinerary — baseline price for comparison.
2. Hidden-city / "skiplagging" — where my real destination is a layover on a longer ticket.
   Flag the known restrictions: no checked bags, one-way only, frequent-flyer-account risk,
   and that some carriers (e.g. Lufthansa, American) have pursued passengers. This is AGAINST
   airline terms but not illegal — say so. Do NOT recommend it if I have status with the carrier
   or any checked baggage.
3. Nearby-airport substitutions — airports within ~150 km of origin and destination, with
   realistic ground-transfer time and cost added in.
4. Multi-leg / self-transfer combinations — separate tickets stitched together. State the
   missed-connection risk (no through-protection) and a minimum recommended layover.
5. Open-jaw and stopover constructions where they apply.

For each option give: estimated price range, total door-to-door time, what could go wrong,
and whether it is legal vs. merely against airline terms.
End with a ranked shortlist of the top 3 for "risk tolerance = [low / medium / high]".

If you don't have live pricing, say so and use typical historical ranges for the route —
flag every number as an estimate I need to verify.
```

---

## 2. Pricing Reality Check
**When to use:** You want to understand how flight pricing *actually* works and separate real levers from myths before you start hunting.

```
Act as a flight-pricing analyst with a skeptical, evidence-based stance.

Give me an honest breakdown of how airline and OTA pricing works, sorted into three buckets:

A. CONFIRMED MECHANISMS — backed by airline documentation, regulator filings, or research.
   Address: revenue management / fare buckets, dynamic repricing on remaining inventory,
   day-of-week and time-to-departure demand curves, fare-class availability, A/B-tested promo
   fares, and currency / point-of-sale (POS) differences.

B. PLAUSIBLE BUT UNCONFIRMED — widely claimed online with weak evidence.
   Address: cookies causing price hikes on repeat searches, IP-based personalisation within the
   same POS, device-type (iOS vs Android) surcharges, browser fingerprinting. For each, cite what
   investigations actually found (e.g. Consumer Reports, DOT, academic studies) and rate the
   evidence strong / mixed / weak / debunked.

C. MYTHS — claims that have been tested and did not hold up.

Then give me a search method grounded ONLY in bucket A. For each step explain WHY it helps
(which real mechanism it exploits), not "do this because cookies." Example real levers: searching
from a different POS / currency, flexible-date matrices, fare-class availability tools (ExpertFlyer,
Google Flights / ITA Matrix), splitting one-way searches, timing around fare-bucket resets.

Flag any number, percentage, or "studies show…" claim I should verify before trusting it.
```

---

## 3. Geo-Pricing (Point-of-Sale) Comparison
**When to use:** Same ticket, different country site/currency — find where it's cheapest and how to book it legally.

```
Act as a professional flight-pricing analyst.

ROUTE: [Origin] → [Destination], [dates], [cabin]
MY CURRENCY: [e.g. USD]

Compare how this same itinerary is typically priced when booked from different points of sale (POS)
— different country versions of the airline's site and different currencies. Cover at least:

- Carrier's home-country POS
- Origin-country POS
- Destination-country POS
- 2–3 third-country POS historically cheap for this region (e.g. India, Turkey, Brazil, Thailand —
  pick whichever are plausible for this route)

For each POS give: estimated price in local currency and converted to [my currency], why the price
differs (taxes, local competition, regulated fares, carrier strategy), and the typical gap on this route.

Then list the LEGAL ways to actually book a foreign POS fare, with each method's catches:
- Multi-currency credit cards and FX fees
- Travel agents / OTAs based in the cheaper market
- VPN + foreign payment method — note this can violate airline terms even when not illegal;
  explain the difference
- Award tickets via a foreign frequent-flyer programme

Do NOT suggest anything involving identity misrepresentation or fraudulent payment details.
Flag every price figure as an estimate to verify on the day of booking.
```

---

## 4. Timing Sweet-Spot Finder
**When to use:** You're flexible on when to book or fly and want the best booking window, day, and season for your route.

```
Act as a professional flight-pricing analyst.

ROUTE: [Origin] → [Destination]
TRIP TYPE: [leisure / business / holiday]
TRAVEL MONTH: [target month or "flexible"]

Using typical historical pricing patterns for this route (not live data), tell me:

1. The booking window that historically yields the lowest fares — separately for short-haul domestic,
   regional, and long-haul; state which category this route is.
2. The cheapest day-of-week to depart and to return, and roughly how much that saves vs. peak days.
3. The cheapest weeks of the calendar year for this route (shoulder seasons, post-holiday troughs).
4. Typical "fare reset" / sale patterns (e.g. Tuesday-afternoon US lore, end-of-quarter sales,
   Black Friday) — and which are evidence-backed vs. anecdotal.
5. Events that reliably spike prices on this route (holidays, school breaks, major local events).

Explain the underlying drivers: revenue-management curves, advance-purchase rules, capacity changes,
competitor entry/exit. Then give a concrete plan: "start watching by [date], book by [date],
avoid [windows]."

Be explicit about confidence — which recommendations are well-established vs. rules of thumb.
Don't cite specific studies unless you're sure of them. Flag every number as an estimate.
```

---

## 5. Fare-Rules Decoder
**When to use:** You want fare classes, stay rules, and fare codes explained in plain English so you can spot legitimate savings.

```
Act as a professional flight-pricing analyst and explain airline fare rules in plain English.

ROUTE: [Origin] → [Destination], [dates], [carrier(s) if known]

Cover each of these in concrete, non-jargon terms, with one example of how it could legitimately
save money:

1. Fare basis codes and fare classes (Y, B, M, H, Q, etc.) — how to read them and what they reveal
   about price and restrictions.
2. Advance-purchase, minimum-stay, and Saturday-night-stay rules — and when a longer trip is
   paradoxically cheaper than a short one.
3. Round-trip vs. two one-ways — when each is cheaper and why.
4. Open-jaw, stopover, and "married segment" logic — how breaking the routing can lower or raise fare.
5. Refundability, change fees, and "basic economy" stripped fares — what's given up and what it's worth.
6. Codeshares vs. operating carrier — when buying from the "right" airline on the same metal is cheaper.
7. Promotional and corporate fare codes — what's publicly accessible (AAA, student, youth, senior,
   military) vs. what isn't.

For each, sort tactics into three clearly labelled tiers:
- LEGITIMATE OPTIMISATION (always fine to use)
- AGAINST AIRLINE TERMS BUT NOT ILLEGAL (e.g. hidden-city) — explain the risk
- OFF-LIMITS (fraud, misrepresentation) — label this explicitly and don't recommend it

Finish with a checklist of fare-rule questions I should ask before booking.
```

---

## 6. Extra-Fees Breakdown
**When to use:** You've found a fare and want every add-on fee itemised, plus legitimate ways to avoid each.

```
Act as a professional flight-pricing analyst.

FLIGHT / FARE: [airline, route, dates, fare type e.g. basic economy]

Detail ALL additional fees beyond the base fare for this flight, including:
- Checked and carry-on baggage
- Seat selection (and which seats are genuinely free)
- Priority / early boarding
- Payment-method surcharges and currency-conversion markups
- Change / cancellation fees
- Any "service" or booking fees from the channel

For each fee, suggest LEGITIMATE strategies to avoid or minimise it based on current fare rules
(e.g. loyalty-status waivers, co-brand card baggage perks, choosing a fare bundle, packing to
carry-on limits). Do NOT suggest anything that misrepresents bag size, identity, or eligibility.

Give me the realistic all-in total (base fare + likely fees) so I can compare it fairly against
other options. Flag each fee figure as an estimate to confirm at checkout.
```

---

## 7. Airline vs OTA — Where to Actually Book
**When to use:** You know the fare and need to decide between booking direct vs. through an online travel agency.

```
Act as a professional flight-pricing analyst.

ROUTE: [Origin] → [Destination], [dates], [cabin]

Compare where to actually book this ticket across these channel types:
- The operating airline's direct website (home-country POS)
- The operating airline's site on other POS (see the geo-pricing prompt)
- Major global OTAs (Expedia, Booking.com Flights, plus Kayak / Google Flights as meta-search,
  not bookers)
- Aggressive-pricing OTAs (Kiwi.com, Trip.com, Mytrip, Gotogate, etc.)
- Regional / lesser-known platforms relevant to this route
- Traditional travel agents and consolidators

For each, address:
1. Typical price position vs. airline direct (often cheaper / similar / often more expensive).
2. Hidden fees: service fees, payment surcharges, "premium support," seat upcharges, FX markups.
3. What you give up: voucher-only refunds, slow support, no airline-side recognition of the booking,
   weak protection on schedule changes and irregular operations.
4. Documented patterns of misleading practices (chargeable "free" cancellation windows, fake urgency
   timers, drip pricing) — name platforms only where this is well-documented; flag where you're unsure.

End with a decision rule: "Book direct with the airline if [conditions]; consider an OTA only if
[conditions]." Be explicit that the cheapest sticker price is often not the cheapest total cost
once a schedule change or refund is needed.
```

---

## 8. Risk & Flexibility Analyzer
**When to use:** You're comparing 2–3 specific fares and want the one with the lowest financial risk if plans change.

```
Act as a professional flight-pricing analyst.

CANDIDATE FARES: [paste 2–3 options: airline, fare type, price, channel for each]
HOW LIKELY ARE MY PLANS TO CHANGE: [low / medium / high]

For each candidate, analyse:
1. Change policy — fee, fare-difference rules, and how easy changes actually are.
2. Cancellation policy — refundable, voucher-only, or non-refundable; any 24-hour free-cancel window.
3. Refund mechanics — cash vs. credit, processing time, and who I deal with (airline vs. OTA).
4. Hidden or easily-missed clauses — no-show rules, married-segment cancellation traps,
   basic-economy restrictions, third-party booking limitations.

Then rank the options by lowest financial risk for my stated likelihood of change, and state the
"insurance premium": how much extra (if any) the more flexible option costs and whether it's worth it.
Flag any figure as an estimate to confirm in the fare rules before booking.
```

---

## 9. Promo & Deal Verifier
**When to use:** You've seen a "deal," sale, or promo code and want it checked before you trust it.
*(Best with web/search access enabled; otherwise it will tell you what to verify manually.)*

```
Act as a flight-pricing analyst with a skeptical, fact-checking stance.

DEAL / CODE / CLAIM: [paste the promo code, sale, or "deal" you saw, and where you saw it]
ROUTE & DATES (if relevant): [Origin → Destination, dates]
AIRLINE(S): [if specified]

Assess this deal honestly:
1. Is the promotion / code real and currently active? Identify the official source.
2. Expiration, route/date restrictions, and exclusions.
3. Whether the "discount" is genuine vs. an inflated-then-reduced sticker price or fake urgency.
4. Any catches: limited inventory, basic-economy-only, hidden fees that erase the saving.

Discard anything expired or that you cannot verify, and SAY when you can't verify it rather than
guessing. If you don't have live access, list the exact checks I should run myself and where.
Treat every "% off" and "lowest in X years" claim as unverified until confirmed at the source.
```

---

## 10. Fare-Tracking Strategy
**When to use:** You're not ready to book and want a sane plan to watch the fare and pull the trigger at the right time.

```
Act as a professional flight-pricing analyst.

ROUTE: [Origin] → [Destination], [dates], [cabin], [budget ceiling]
TIME UNTIL DEPARTURE: [X weeks / months]

Design a fare-tracking strategy for the time before departure. Cover:

1. TOOLS — which fare-alert services to use (Google Flights tracking, Hopper, Kayak alerts,
   Going / Scott's Cheap Flights, airline native alerts). One honest line each: what it's good at,
   what it isn't.
2. SEARCH HYGIENE — there is LIMITED solid evidence that cookies / IP / repeat searches inflate
   prices for individuals. Treat incognito, clearing cookies, and varying device as low-cost
   precautions, NOT proven necessities. Be clear what's evidence-backed (POS / currency matter;
   cookies probably don't) vs. folklore.
3. CADENCE — how often to check without burning out (e.g. 2×/week early, daily in the final 2 weeks,
   plus a calendar trigger before known fare-reset days).
4. DECISION RULES — concrete heuristics: "if price drops X% below the rolling 30-day median, book";
   "stop watching at T-14 for long-haul, T-7 for short-haul."
5. BACKSTOPS — 24-hour-hold / free-cancel rules, fare locks, refundable fares as insurance, so a
   tracked-then-missed drop isn't catastrophic.
6. WORKED EXAMPLE — walk through one month of monitoring on this route, showing what I'd do each week.

Flag every rule of thumb ("book 6 weeks out", "Tuesday is cheapest") as a heuristic, not a law,
and say which are actually backed by data vs. just commonly repeated.
```

---

## 11. Price-Match / Discount Email Draft
**When to use:** You want a professional email asking an airline or agency for a price match or discount.

```
Act as a professional travel-fares correspondent.

SITUATION: [who I'm writing to — airline / OTA / travel agent]
MY FARE FOUND: [route, dates, price, source/screenshot details]
COMPETING PRICE: [the lower price and where it's offered]
MY LEVERAGE: [loyalty programme & tier, repeat customer, corporate account, flexibility — if any]

Draft a concise, professional, persuasive email that:
- States the specific competing price and source clearly.
- References the recipient's own price-match or best-fare policy IF one plausibly exists — and tells
  me to verify that policy first rather than asserting it as fact.
- Cites my genuine loyalty / relationship leverage where it applies.
- Offers a clear, reasonable ask and an easy way to say yes.

Keep it honest: do not fabricate policies, competitor quotes, or loyalty status. If price-matching is
unlikely for this type of fare/airline, tell me that up front so I don't waste the effort.
```

---

### Notes on responsible use
- **Skiplagging / hidden-city** ticketing is *against airline terms of service*, not a crime — but it carries real consequences (forfeited return legs, no checked bags, loyalty-account closure, occasional carrier pushback). It's included so you understand it, with its risks; use your own judgement.
- **Geo-pricing via VPN / foreign POS** can breach airline terms even where it isn't illegal. Never combine it with false identity or payment details.
- Anything involving **misrepresentation or fraudulent payment** is off-limits and these prompts are written to refuse it.
- The model does not have your live fares unless it can search the web. Treat every figure it gives as an **estimate to verify at the source** before you pay.
