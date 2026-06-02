"""Wardrobe / outfit-planner core logic.

A 'Clueless'-style digital closet: catalog garments and compose outfits.
Dependency-light: Python standard library only, persisted to a local JSON file.

Public API:
    Garment        -- a single item of clothing (id, name, category, color, tags)
    Wardrobe       -- the store: add / list / remove, persisted to JSON
    suggest_outfit -- compose a valid outfit honoring simple rules
    autotag        -- OPTIONAL vision auto-tagging stub (plug a model here)
"""
from __future__ import annotations

import json
import os
import random
import uuid
from dataclasses import dataclass, field
from typing import List, Optional


# Recognized garment categories. Keep this small and explicit.
CATEGORIES = {"top", "bottom", "dress", "shoes", "outerwear"}


class NoOutfitError(Exception):
    """Raised when no valid outfit can be composed from the wardrobe."""


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------
@dataclass
class Garment:
    """A single item of clothing.

    Category is validated against CATEGORIES. Category and color are
    normalized to lowercase so filtering and color rules are case-insensitive.
    An ``id`` is auto-assigned if not supplied.
    """

    name: str
    category: str
    color: str = ""
    tags: List[str] = field(default_factory=list)
    id: str = ""

    def __post_init__(self) -> None:
        self.category = (self.category or "").strip().lower()
        if self.category not in CATEGORIES:
            raise ValueError(
                f"unknown category {self.category!r}; "
                f"expected one of {sorted(CATEGORIES)}"
            )
        self.color = (self.color or "").strip().lower()
        self.name = self.name.strip()
        # normalize tags to lowercase, drop blanks
        self.tags = [t.strip().lower() for t in self.tags if t and t.strip()]
        if not self.id:
            self.id = uuid.uuid4().hex[:8]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "color": self.color,
            "tags": list(self.tags),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Garment":
        return cls(
            id=d.get("id", ""),
            name=d.get("name", ""),
            category=d.get("category", ""),
            color=d.get("color", ""),
            tags=list(d.get("tags", [])),
        )


# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------
class Wardrobe:
    """A persisted collection of garments.

    Data is stored as a JSON array in ``path``. The file is loaded on
    construction and rewritten on every mutation, so a new Wardrobe pointed
    at the same path always reflects the latest state.
    """

    def __init__(self, path: str = "wardrobe.json") -> None:
        self.path = path
        self._items: List[Garment] = []
        self._load()

    # -- persistence -------------------------------------------------------
    def _load(self) -> None:
        if not os.path.exists(self.path):
            self._items = []
            return
        with open(self.path, encoding="utf-8") as fh:
            try:
                raw = json.load(fh)
            except json.JSONDecodeError:
                raw = []
        self._items = [Garment.from_dict(d) for d in raw]

    def _save(self) -> None:
        parent = os.path.dirname(os.path.abspath(self.path))
        os.makedirs(parent, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as fh:
            json.dump([g.to_dict() for g in self._items], fh, indent=2)

    # -- CRUD --------------------------------------------------------------
    def add(self, garment: Garment) -> Garment:
        """Add a garment and persist. Returns the stored garment."""
        self._items.append(garment)
        self._save()
        return garment

    def list(self, category: Optional[str] = None) -> List[Garment]:
        """Return garments, optionally filtered by category."""
        if category is None:
            return list(self._items)
        category = category.strip().lower()
        return [g for g in self._items if g.category == category]

    def remove(self, garment_id: str) -> bool:
        """Remove a garment by id. Returns True if something was removed."""
        before = len(self._items)
        self._items = [g for g in self._items if g.id != garment_id]
        removed = len(self._items) < before
        if removed:
            self._save()
        return removed


# ---------------------------------------------------------------------------
# Outfit suggester
# ---------------------------------------------------------------------------
#
# Rules (deliberately simple and documented):
#
#  1. A valid outfit is EITHER  top + bottom + shoes  OR  dress + shoes.
#     -> Never two tops, never two bottoms, never a top paired with a dress.
#  2. Shoes are always required.
#  3. occasion filter: every garment must carry the occasion as a tag.
#  4. weather:
#       - "cold": add one outerwear item if available (optional otherwise).
#       - "hot":  prefer the dress+shoes combo, and never add outerwear.
#  5. Basic color sense: reject combos containing a known clashing color pair
#     (see CLASHES) whenever a non-clashing alternative exists.
#
# The suggester randomizes among valid candidates so repeated calls give
# variety, but every returned outfit still satisfies the rules above.

# Known clashing color pairs (unordered). Kept intentionally tiny.
CLASHES = {
    frozenset({"red", "pink"}),
    frozenset({"red", "orange"}),
    frozenset({"green", "red"}),
    frozenset({"purple", "brown"}),
}


def _clashes(garments: List[Garment]) -> bool:
    """True if any pair of garment colors is a known clash."""
    colors = [g.color for g in garments if g.color]
    for i in range(len(colors)):
        for j in range(i + 1, len(colors)):
            if frozenset({colors[i], colors[j]}) in CLASHES:
                return True
    return False


def _matches_occasion(g: Garment, occasion: Optional[str]) -> bool:
    if occasion is None:
        return True
    return occasion.strip().lower() in g.tags


def suggest_outfit(
    wardrobe: Wardrobe,
    occasion: Optional[str] = None,
    weather: Optional[str] = None,
    rng: Optional[random.Random] = None,
) -> List[Garment]:
    """Compose a valid outfit from ``wardrobe``.

    Args:
        wardrobe: the store to draw from.
        occasion: if set, only garments tagged with it are eligible.
        weather:  "cold" may add outerwear; "hot" prefers a dress and skips
                  outerwear. Any other / None value is treated as neutral.
        rng:      optional random.Random for deterministic tests.

    Returns:
        A list of Garment objects forming a valid outfit.

    Raises:
        NoOutfitError: if no valid outfit can be composed.
    """
    rng = rng or random
    weather = (weather or "").strip().lower() or None

    def pool(category: str) -> List[Garment]:
        items = [
            g
            for g in wardrobe.list(category=category)
            if _matches_occasion(g, occasion)
        ]
        rng.shuffle(items)
        return items

    tops = pool("top")
    bottoms = pool("bottom")
    dresses = pool("dress")
    shoes = pool("shoes")
    outerwear = pool("outerwear")

    if not shoes:
        raise NoOutfitError("no shoes available for the given filters")

    # Build candidate base outfits (without outerwear yet).
    candidates: List[List[Garment]] = []
    for sh in shoes:
        for dr in dresses:
            candidates.append([dr, sh])
        for tp in tops:
            for bo in bottoms:
                candidates.append([tp, bo, sh])

    if not candidates:
        raise NoOutfitError("no valid top+bottom+shoes or dress+shoes combo")

    # Hot weather: prefer dress-based outfits when any exist.
    if weather == "hot":
        dress_based = [c for c in candidates if any(g.category == "dress" for g in c)]
        if dress_based:
            candidates = dress_based

    rng.shuffle(candidates)

    # Color sense: prefer a non-clashing candidate, but fall back to any
    # valid candidate rather than failing outright.
    non_clashing = [c for c in candidates if not _clashes(c)]
    chosen = non_clashing[0] if non_clashing else candidates[0]
    outfit = list(chosen)

    # Cold weather: layer on outerwear if we have a non-clashing option.
    if weather == "cold" and outerwear:
        for ow in outerwear:
            if not _clashes(outfit + [ow]):
                outfit.append(ow)
                break
        else:
            outfit.append(outerwear[0])

    return outfit


# ---------------------------------------------------------------------------
# OPTIONAL: vision auto-tagging stub
# ---------------------------------------------------------------------------
def autotag(image_path: str) -> dict:
    """Stub for vision-based garment auto-tagging.

    Returns the SHAPE a real tagger would produce::

        {"category": "top", "color": "white", "tags": ["casual"]}

    >>> PLUG A VISION MODEL HERE <<<
    Replace the body below with a call to your vision model (e.g. an
    Anthropic/OpenAI multimodal API or a local classifier). Send
    ``image_path`` to the model and map its response onto this dict. The
    rest of the app needs no changes -- it only relies on this return shape.

    This stub intentionally requires no model, key, or network so the app
    runs out of the box.
    """
    return {
        "category": "",   # one of CATEGORIES, filled by the model
        "color": "",      # dominant color, filled by the model
        "tags": [],       # e.g. ["casual", "summer"], filled by the model
        "_note": "stub - plug a vision model into autotag()",
        "_image": image_path,
    }
