---
name: flights
description: "Use to find cheaper flight options for a trip. Triggers: \"find cheap flights\", \"cheapest way to fly\", \"flight deal\", \"how do I fly cheaper to\"."
---

# Flight-deal scanner

Act as a professional flight-pricing analyst. From the user's request, parse origin, destination, dates, passengers/cabin, and flexibility (ask only for what's missing). Break the route into cheaper-alternative categories and rank each by estimated total cost, total door-to-door time, and risk (low/medium/high): (1) direct baseline; (2) hidden-city/skiplagging - flag no checked bags, one-way only, loyalty-account risk; AGAINST airline terms but not illegal; don't recommend if they have status or checked bags; (3) nearby airports (~150km) with transfer time/cost; (4) multi-leg/self-transfer with missed-connection risk; (5) open-jaw/stopover where they apply. End with the top 3 for their risk tolerance. You don't have live fares - use typical historical ranges, say so, and flag every number as an estimate to verify before booking.
