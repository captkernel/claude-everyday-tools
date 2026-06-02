"""Tiny CLI for the wardrobe / outfit-planner.

Usage (run from inside this folder):
    python cli.py add  --name "White Tee" --category top --color white --tags casual,summer
    python cli.py list [--category top]
    python cli.py remove --id <id>
    python cli.py suggest [--occasion formal] [--weather cold]
    python cli.py autotag --image path/to/photo.jpg

Data persists to ./wardrobe.json (next to this script) by default;
override with --db /path/to/file.json.
"""
from __future__ import annotations

import argparse
import os
import sys

from wardrobe import Garment, Wardrobe, suggest_outfit, autotag, NoOutfitError

DEFAULT_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wardrobe.json")


def _fmt(g: Garment) -> str:
    tags = ",".join(g.tags) if g.tags else "-"
    return f"  [{g.id}] {g.name}  ({g.category}/{g.color or '-'})  tags: {tags}"


def cmd_add(args, store: Wardrobe) -> int:
    tags = [t for t in (args.tags or "").split(",") if t.strip()]
    try:
        g = store.add(
            Garment(
                name=args.name,
                category=args.category,
                color=args.color or "",
                tags=tags,
            )
        )
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print("added:")
    print(_fmt(g))
    return 0


def cmd_list(args, store: Wardrobe) -> int:
    items = store.list(category=args.category)
    if not items:
        print("(wardrobe is empty)")
        return 0
    print(f"{len(items)} item(s):")
    for g in items:
        print(_fmt(g))
    return 0


def cmd_remove(args, store: Wardrobe) -> int:
    if store.remove(args.id):
        print(f"removed {args.id}")
        return 0
    print(f"no garment with id {args.id}", file=sys.stderr)
    return 1


def cmd_suggest(args, store: Wardrobe) -> int:
    try:
        outfit = suggest_outfit(store, occasion=args.occasion, weather=args.weather)
    except NoOutfitError as e:
        print(f"no outfit: {e}", file=sys.stderr)
        return 1
    bits = []
    if args.occasion:
        bits.append(f"occasion={args.occasion}")
    if args.weather:
        bits.append(f"weather={args.weather}")
    suffix = f"  ({', '.join(bits)})" if bits else ""
    print(f"suggested outfit{suffix}:")
    for g in outfit:
        print(_fmt(g))
    return 0


def cmd_autotag(args, store: Wardrobe) -> int:
    result = autotag(args.image)
    print("autotag (stub) result:")
    for k, v in result.items():
        print(f"  {k}: {v}")
    print("note: this is a stub. Plug a vision model into wardrobe.autotag().")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="cli.py", description="Wardrobe / outfit-planner")
    p.add_argument("--db", default=DEFAULT_DB, help="path to JSON data file")
    sub = p.add_subparsers(dest="command", required=True)

    a = sub.add_parser("add", help="add a garment")
    a.add_argument("--name", required=True)
    a.add_argument("--category", required=True,
                   help="top | bottom | dress | shoes | outerwear")
    a.add_argument("--color", default="")
    a.add_argument("--tags", default="", help="comma-separated, e.g. casual,summer")
    a.set_defaults(func=cmd_add)

    l = sub.add_parser("list", help="list garments")
    l.add_argument("--category", default=None)
    l.set_defaults(func=cmd_list)

    r = sub.add_parser("remove", help="remove a garment by id")
    r.add_argument("--id", required=True)
    r.set_defaults(func=cmd_remove)

    s = sub.add_parser("suggest", help="suggest an outfit")
    s.add_argument("--occasion", default=None)
    s.add_argument("--weather", default=None, help="cold | hot | (neutral)")
    s.set_defaults(func=cmd_suggest)

    t = sub.add_parser("autotag", help="auto-tag a garment photo (stub)")
    t.add_argument("--image", required=True)
    t.set_defaults(func=cmd_autotag)

    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    store = Wardrobe(path=args.db)
    return args.func(args, store)


if __name__ == "__main__":
    raise SystemExit(main())
