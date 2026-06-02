"""Tests for the wardrobe core logic (written TDD-first).

Run from the repo root:
    .venv\\Scripts\\python.exe -m pytest projects\\wardrobe-outfit-planner
"""
import json
import os

import pytest

from wardrobe import (
    Garment,
    Wardrobe,
    suggest_outfit,
    NoOutfitError,
    autotag,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def store(tmp_path):
    """A fresh, empty wardrobe backed by a temp JSON file."""
    return Wardrobe(path=str(tmp_path / "wardrobe.json"))


@pytest.fixture
def stocked(store):
    """A wardrobe with at least one valid top+bottom+shoes combo and a dress."""
    store.add(Garment(name="White Tee", category="top", color="white",
                       tags=["casual", "summer"]))
    store.add(Garment(name="Navy Halter Top", category="top", color="navy",
                       tags=["formal", "evening"]))
    store.add(Garment(name="Blue Jeans", category="bottom", color="blue",
                      tags=["casual"]))
    store.add(Garment(name="Black Trousers", category="bottom", color="black",
                      tags=["formal"]))
    store.add(Garment(name="White Sneakers", category="shoes", color="white",
                      tags=["casual"]))
    store.add(Garment(name="Black Heels", category="shoes", color="black",
                      tags=["formal", "evening"]))
    store.add(Garment(name="Pink Slip Dress", category="dress", color="pink",
                      tags=["formal", "evening"]))
    return store


# ---------------------------------------------------------------------------
# Garment data model
# ---------------------------------------------------------------------------
def test_garment_gets_id_and_normalizes(store):
    g = store.add(Garment(name="Tee", category="TOP", color="White"))
    assert g.id  # auto-assigned, non-empty
    assert g.category == "top"   # normalized to lowercase
    assert g.color == "white"


def test_garment_rejects_unknown_category():
    with pytest.raises(ValueError):
        Garment(name="Thing", category="hat", color="red")


def test_garment_roundtrips_to_dict():
    g = Garment(name="Tee", category="top", color="white", tags=["casual"])
    g2 = Garment.from_dict(g.to_dict())
    assert g2.name == g.name
    assert g2.category == g.category
    assert g2.tags == g.tags


# ---------------------------------------------------------------------------
# Wardrobe store: add / list / remove / persist
# ---------------------------------------------------------------------------
def test_add_and_list(store):
    store.add(Garment(name="Tee", category="top", color="white"))
    store.add(Garment(name="Jeans", category="bottom", color="blue"))
    items = store.list()
    assert len(items) == 2


def test_list_filter_by_category(stocked):
    tops = stocked.list(category="top")
    assert len(tops) == 2
    assert all(g.category == "top" for g in tops)


def test_remove(store):
    g = store.add(Garment(name="Tee", category="top", color="white"))
    assert store.remove(g.id) is True
    assert store.list() == []
    assert store.remove(g.id) is False  # already gone


def test_persistence_roundtrip(tmp_path):
    path = str(tmp_path / "wardrobe.json")
    w1 = Wardrobe(path=path)
    w1.add(Garment(name="Tee", category="top", color="white", tags=["casual"]))
    w1.add(Garment(name="Jeans", category="bottom", color="blue"))

    # A brand new store pointed at the same file sees the data.
    w2 = Wardrobe(path=path)
    assert len(w2.list()) == 2
    names = {g.name for g in w2.list()}
    assert names == {"Tee", "Jeans"}


def test_persistence_file_is_valid_json(tmp_path):
    path = str(tmp_path / "wardrobe.json")
    w = Wardrobe(path=path)
    w.add(Garment(name="Tee", category="top", color="white"))
    assert os.path.exists(path)
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    assert isinstance(data, list)
    assert data[0]["name"] == "Tee"


# ---------------------------------------------------------------------------
# Outfit suggester rules
# ---------------------------------------------------------------------------
def test_suggest_returns_valid_combo(stocked):
    outfit = suggest_outfit(stocked)
    cats = [g.category for g in outfit]
    # Either top+bottom+shoes OR dress+shoes
    assert "shoes" in cats
    if "dress" in cats:
        assert cats.count("dress") == 1
        assert "top" not in cats and "bottom" not in cats
    else:
        assert "top" in cats and "bottom" in cats


def test_suggest_never_returns_two_tops(stocked):
    # Run several times since suggestion may be randomized.
    for _ in range(30):
        outfit = suggest_outfit(stocked)
        cats = [g.category for g in outfit]
        assert cats.count("top") <= 1
        assert cats.count("bottom") <= 1
        assert cats.count("shoes") == 1


def test_suggest_always_includes_shoes(stocked):
    for _ in range(20):
        outfit = suggest_outfit(stocked)
        assert any(g.category == "shoes" for g in outfit)


def test_suggest_respects_occasion(stocked):
    for _ in range(20):
        outfit = suggest_outfit(stocked, occasion="formal")
        for g in outfit:
            assert "formal" in g.tags


def test_suggest_raises_when_empty(store):
    with pytest.raises(NoOutfitError):
        suggest_outfit(store)


def test_suggest_raises_when_no_shoes(store):
    store.add(Garment(name="Tee", category="top", color="white"))
    store.add(Garment(name="Jeans", category="bottom", color="blue"))
    with pytest.raises(NoOutfitError):
        suggest_outfit(store)


def test_suggest_weather_cold_adds_outerwear(store):
    store.add(Garment(name="Tee", category="top", color="white", tags=["casual"]))
    store.add(Garment(name="Jeans", category="bottom", color="blue", tags=["casual"]))
    store.add(Garment(name="Sneakers", category="shoes", color="white", tags=["casual"]))
    store.add(Garment(name="Wool Coat", category="outerwear", color="grey",
                      tags=["casual"]))
    found_outerwear = False
    for _ in range(20):
        outfit = suggest_outfit(store, weather="cold")
        if any(g.category == "outerwear" for g in outfit):
            found_outerwear = True
    assert found_outerwear, "cold weather should be able to add outerwear"


def test_suggest_color_sense_no_clash(store):
    # A clashing pair (red + pink) plus a safe neutral. The suggester should
    # prefer combos that don't clash when an alternative exists.
    store.add(Garment(name="Red Top", category="top", color="red", tags=["casual"]))
    store.add(Garment(name="Pink Jeans", category="bottom", color="pink",
                      tags=["casual"]))
    store.add(Garment(name="Black Jeans", category="bottom", color="black",
                      tags=["casual"]))
    store.add(Garment(name="White Sneakers", category="shoes", color="white",
                      tags=["casual"]))
    for _ in range(30):
        outfit = suggest_outfit(store)
        colors = {g.color for g in outfit}
        # red + pink is the only defined clash; it must never be chosen
        assert not ({"red", "pink"} <= colors)


# ---------------------------------------------------------------------------
# Optional vision auto-tagging stub
# ---------------------------------------------------------------------------
def test_autotag_returns_dict_stub():
    result = autotag("some/photo.jpg")
    assert isinstance(result, dict)
    # Stub returns the expected shape without requiring any model.
    assert "category" in result
    assert "color" in result
    assert "tags" in result
