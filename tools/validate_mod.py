#!/usr/bin/env python3
"""
Italian Occupation Plus - pre-release validation.

Checks the things that break silently in HOI4 (bad paths, missing loc keys,
orphaned events, asset gaps, brace imbalance) without needing to boot the game.

Usage:
    python3 tools/validate_mod.py            # from the repo root
    python3 tools/validate_mod.py --strict   # warnings become errors

Exit code 0 = clean, 1 = errors found.
"""

from __future__ import annotations

import argparse
import math
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MOD = ROOT / "italian_occupation_plus"

# Tags this mod adds. IBL ships ideology variants only (fascist puppets), so the
# base <TAG>.tga is optional - see REQUIRED_FLAG_VARIANTS below.
TAGS = ["ICR", "ISE", "IMT", "IAL", "IBL"]
# Puppets are always fascist, so the fascist variant is the only hard requirement.
REQUIRED_FLAG_VARIANTS = ["fascism"]
FLAG_SIZES = ["gfx/flags", "gfx/flags/medium", "gfx/flags/small"]

# Deliberate mirrors: IOP_countries_l_english.yml repeats the autonomy name so it
# still resolves if IOP_autonomy_l_english.yml ever fails to load. Identical text
# is fine (and enforced); only a divergence is an error.
ALLOWED_LOC_MIRRORS = {"autonomy_military_occupation", "autonomy_military_occupation_desc"}

# Vanilla state IDs the mod is allowed to touch (verified against 1.19).
KNOWN_STATES = {
    44, 45, 48, 102, 103, 104, 105, 106, 107, 108, 109, 163, 211, 212,
    764, 801, 802, 803, 804, 805, 852, 853, 934, 970,
}

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def strip_comments(text: str) -> str:
    return re.sub(r"#[^\n]*", "", text)


# --------------------------------------------------------------------------- #
# checks
# --------------------------------------------------------------------------- #
def check_descriptors() -> None:
    outer = ROOT / "italian_occupation_plus.mod"
    inner = MOD / "descriptor.mod"
    if not outer.exists():
        err("missing root italian_occupation_plus.mod")
        return
    if not inner.exists():
        err("missing descriptor.mod inside the mod folder")
        return
    a, b = read(outer), read(inner)

    # The outer .mod is the launcher entry and must carry path=; descriptor.mod
    # lives inside the mod folder and must NOT (its path is implicit).
    if 'path="mod/italian_occupation_plus"' not in a:
        err('italian_occupation_plus.mod: path= must be "mod/italian_occupation_plus"')
    if re.search(r"(?m)^path=", b):
        err("descriptor.mod: must not contain a path= key")

    def fields(text: str) -> dict[str, str]:
        out = {}
        for m in re.finditer(r'(?m)^(\w+)=(?:"([^"]*)"|\{([^}]*)\})', text):
            out[m.group(1)] = (m.group(2) if m.group(2) is not None else m.group(3)).strip()
        return out

    fa, fb = fields(a), fields(b)
    for key in ("version", "name", "supported_version", "tags"):
        if key not in fa or key not in fb:
            err(f"{key}= missing from a descriptor")
        elif fa[key] != fb[key]:
            err(f"{key}= differs between the two descriptors: {fa[key]!r} vs {fb[key]!r}")
    for text, name in ((a, outer.name), (b, inner.name)):
        if not re.search(r'supported_version="[^"]+"', text):
            err(f"{name}: no supported_version")


def check_syntax() -> None:
    """Brace balance, tabs-not-spaces, and the `}<tab>option = {` glitch."""
    scripts = [
        *MOD.glob("common/**/*.txt"),
        *MOD.glob("events/*.txt"),
        *MOD.glob("history/**/*.txt"),
        *MOD.glob("interface/*.gfx"),
    ]
    for f in scripts:
        raw = f.read_bytes()
        text = read(f)
        rel = f.relative_to(ROOT)

        bal = strip_comments(text).count("{") - strip_comments(text).count("}")
        if bal:
            err(f"{rel}: unbalanced braces ({bal:+d})")
        if b"\r\n" in raw:
            err(f"{rel}: CRLF line endings (HOI4 wants LF)")
        if re.search(r"(?m)^ +\S", text):
            warn(f"{rel}: space-indented lines (project style is tabs)")
        for i, line in enumerate(text.splitlines(), 1):
            if re.search(r"\}[^\S\n]+option = \{", line):
                err(f"{rel}:{i}: `}}` and `option = {{` on one line")
        if not raw.endswith(b"\n"):
            warn(f"{rel}: no trailing newline")


def collect_loc_keys() -> dict[str, str]:
    """Returns {key: "file:line"}; also flags duplicates whose text differs."""
    keys: dict[str, str] = {}
    values: dict[str, str] = {}
    loc_dir = MOD / "localisation"
    if not loc_dir.exists():
        err("no localisation/ folder")
        return keys
    for f in sorted(loc_dir.rglob("*.yml")):
        raw = f.read_bytes()
        if raw[:3] != b"\xef\xbb\xbf":
            err(f"{f.relative_to(ROOT)}: missing UTF-8 BOM (HOI4 will not load it)")
        lines = read(f).splitlines()
        if not lines or lines[0].strip() != "l_english:":
            err(f"{f.relative_to(ROOT)}: first line must be `l_english:`")
        for i, line in enumerate(lines, 1):
            m = re.match(r"\s([A-Za-z0-9_.]+):(\d?)\s*(.*)$", line)
            if not m:
                if line.strip() and not line.lstrip().startswith("#") and i != 1:
                    warn(f"{f.relative_to(ROOT)}:{i}: not a valid loc entry: {line[:50]!r}")
                continue
            key, value = m.group(1), m.group(3).strip()
            where = f"{f.relative_to(ROOT)}:{i}"
            if key in keys:
                # Deliberate mirrors are fine as long as the text matches; a
                # mismatch means one file silently wins and the UI lies.
                if values[key] != value:
                    err(f"duplicate loc key `{key}` with DIFFERENT text: "
                        f"{keys[key]} vs {where}")
                elif key not in ALLOWED_LOC_MIRRORS:
                    warn(f"duplicate loc key `{key}` ({keys[key]} and {where}) - identical "
                         f"mirror, later file wins")
                continue
            keys[key] = where
            values[key] = value
    return keys


def check_loc_coverage(loc: dict[str, str]) -> None:
    scripts = [*MOD.glob("common/**/*.txt"), *MOD.glob("events/*.txt"),
               *MOD.glob("history/**/*.txt")]
    referenced: dict[str, str] = {}
    for f in scripts:
        rel = f.relative_to(ROOT)
        for i, line in enumerate(read(f).splitlines(), 1):
            for m in re.finditer(
                r"\b(?:name|title|desc|custom_effect_tooltip)\s*=\s*\"?([A-Za-z0-9_.]+)", line
            ):
                key = m.group(1)
                if key.startswith(("iop_", "PODCAT_", "autonomy_", "RULE_DESC_")):
                    referenced.setdefault(key, f"{rel}:{i}")

    for key, where in sorted(referenced.items()):
        # RULE_DESC_* are vanilla keys, provided by the game.
        if key.startswith("RULE_DESC_"):
            continue
        if key not in loc:
            err(f"missing loc key `{key}` (referenced at {where})")

    # Implicit keys: the engine resolves these by id/name, never via `name = ...`.
    implicit: set[str] = set()
    decisions = read(MOD / "common/decisions/IOP_yugoslavia.txt")
    for m in re.finditer(r"\n\t(iop_[a-z0-9_]+) = \{", decisions):
        key = m.group(1)
        implicit |= {key, f"{key}_desc"}
        if key not in loc:
            err(f"decision `{key}` has no loc key of the same name")
        if f"{key}_desc" not in loc:
            err(f"decision `{key}` has no `{key}_desc` loc key")
    for m in re.finditer(r"(?m)^(\w+) = \{", read(MOD / "common/decisions/categories/iop_categories.txt")):
        implicit |= {m.group(1), f"{m.group(1)}_desc"}
    for m in re.finditer(r"id = (\w+)", read(MOD / "common/autonomous_states/iop_autonomy.txt")):
        implicit |= {m.group(1), f"{m.group(1)}_desc"}
    for tag in TAGS:
        implicit |= {tag, f"{tag}_DEF", f"{tag}_ADJ"}
        implicit |= {f"{tag}_{ideo}{suffix}" for ideo in
                     ("fascism", "neutrality", "democratic", "communism")
                     for suffix in ("_party", "_party_long")}
    # leader descriptions are referenced from history files, already covered above.

    for key, where in sorted(loc.items()):
        if key in referenced or key in implicit:
            continue
        if key.startswith("PODCAT_") or key.startswith("iop_"):
            warn(f"loc key `{key}` ({where}) is never referenced")


def check_decision_event_graph() -> None:
    dfile = MOD / "common/decisions/IOP_yugoslavia.txt"
    efile = MOD / "events/IOP_yugoslavia.txt"
    if not dfile.exists() or not efile.exists():
        err("decisions or events file missing")
        return
    decisions, events = read(dfile), read(efile)

    defined_events = set(re.findall(r"id = (iop_yugo\.\d+)", events))
    fired = re.findall(r"country_event = \{ id = (iop_yugo\.\d+)", decisions)
    for ev in fired:
        if ev not in defined_events:
            err(f"decision fires `{ev}` but that event does not exist")
    for ev in sorted(defined_events):
        if ev not in fired:
            warn(f"event `{ev}` is never fired by any decision (orphaned)")

    # Every decision block must have the keys the engine/UI expects.
    required = ["icon =", "allowed =", "visible =", "available =",
                "complete_effect =", "ai_will_do ="]
    for block in re.split(r"\n\t(?=iop_[a-z0-9_]+ = \{)", decisions)[1:]:
        name = block.split("=")[0].strip()
        missing = [r for r in required if r not in block]
        if missing:
            err(f"decision `{name}` is missing: {', '.join(missing)}")
        if "factor = 0" not in block:
            warn(f"decision `{name}`: ai_will_do is not 0 (AI may take it)")

    # Event options: each must have a loc name and either a trigger or be unconditional.
    for block in re.split(r"(?m)^country_event = \{", events)[1:]:
        eid = re.search(r"id = (iop_yugo\.\d+)", block)
        eid = eid.group(1) if eid else "?"
        if "is_triggered_only = yes" not in block:
            err(f"event {eid}: missing `is_triggered_only = yes`")
        if "picture = " not in block:
            err(f"event {eid}: missing `picture =`")
        options = re.findall(r"\toption = \{(.*?)\n\t\}", block, re.S)
        if not options:
            err(f"event {eid}: no options")
        for opt in options:
            if "name = " not in opt:
                err(f"event {eid}: option without a `name =` loc key")
            if "trigger = {" not in opt and "ai_chance" not in opt:
                warn(f"event {eid}: option has neither trigger nor ai_chance")

    # Softlock check: a decision becomes available when ANY tag in its border gate
    # owns a neighbour, so every gating tag MUST also be offered by the event.
    # (The reverse is fine - an event may offer tags the gate never requires,
    # e.g. North Slovenia gates on Croatia but any bordering puppet may receive.)
    for block in re.split(r"(?m)^country_event = \{", events)[1:]:
        eid = re.search(r"id = iop_yugo\.(\d+)", block).group(1)
        offered = set(re.findall(r"any_neighbor_state = \{ is_owned_by = (\w{3}) \}", block))
        dname = {
            "163": "iop_decide_163_zara", "852": "iop_decide_852_istria",
            "1000": "iop_fall_of_montenegro",
        }.get(eid, f"iop_decide_{eid}")
        m = re.search(r"\n\t" + re.escape(dname) + r" = \{(.*?)\n\t\}", decisions, re.S)
        if not m:
            err(f"event iop_yugo.{eid} has no matching decision `{dname}`")
            continue
        avail = m.group(1).split("available = {", 1)[-1]
        gating = set(re.findall(r"is_owned_by = (\w{3})", avail))
        unconditional = any("trigger = {" not in o for o in
                            re.findall(r"\toption = \{(.*?)\n\t\}", block, re.S))
        if gating and not gating.issubset(offered):
            err(f"{dname}: border gate can be satisfied by {sorted(gating - offered)} "
                f"but the event offers no option for them -> decision fires with "
                f"no valid recipient")
        if not offered and not unconditional:
            err(f"{dname}: every event option is gated but the decision has no border gate")


def check_progression_rules() -> None:
    """Design rules for how decisions unlock and retire.

    1. Founding decisions appear only once >=50% of the puppet's required states
       are controlled, and that list must match the decision's own highlight
       block (so the map outline and the gate can never disagree).
    2. Founding decisions stay repeatable, so a destroyed puppet can be re-founded.
    3. Integration decisions ("Determine Fate of ..." + Fall of Montenegro) are
       one-shot: fire_only_once = yes and no days_re_enable cooldown.
    """
    f = MOD / "common/decisions/IOP_yugoslavia.txt"
    if not f.exists():
        return
    text = read(f)
    blocks = re.split(r"\n\t(?=iop_[a-z0-9_]+ = \{)", text)[1:]
    by_name = {b.split("=")[0].strip(): b for b in blocks}

    for name, block in by_name.items():
        integration = name.startswith("iop_decide_") or name == "iop_fall_of_montenegro"
        founding = name.startswith("iop_establish_")

        if integration:
            if "fire_only_once = yes" not in block:
                err(f"{name}: integration decision must be `fire_only_once = yes` "
                    f"(otherwise it reappears the day after being taken)")
            if "days_re_enable" in block:
                warn(f"{name}: `days_re_enable` is redundant with fire_only_once")

        if founding:
            if re.search(r"fire_only_once = yes", block):
                err(f"{name}: founding decisions must stay repeatable - a destroyed "
                    f"puppet has to be re-foundable")
            highlighted = re.findall(r"state = (\d+)",
                                     block.split("allowed")[0])
            m = re.search(r"visible = \{(.*?)\n\t\t\}", block, re.S)
            if not m or "count_triggers" not in m.group(1):
                err(f"{name}: `visible` has no count_triggers gate - the decision "
                    f"shows up before half the required states are controlled")
                continue
            ct = m.group(1).split("count_triggers = {", 1)[1]
            amount = re.search(r"amount = (\d+)", ct)
            counted = re.findall(r"controls_state = (\d+)", ct)
            if not amount:
                err(f"{name}: count_triggers has no `amount`")
                continue
            want = math.ceil(len(highlighted) / 2)
            if int(amount.group(1)) != want:
                err(f"{name}: count_triggers amount={amount.group(1)} but 50% of "
                    f"{len(highlighted)} required states is {want}")
            if sorted(counted) != sorted(highlighted):
                err(f"{name}: count_triggers states {sorted(counted)} do not match the "
                    f"highlighted required states {sorted(highlighted)}")
            if "available = {" in block:
                avail = block.split("available = {", 1)[1]
                cap = re.search(r"controls_state = (\d+)", avail)
                if cap and cap.group(1) not in counted:
                    err(f"{name}: `available` requires state {cap.group(1)}, which is "
                        f"not one of the required states")


def check_tags_and_states() -> None:
    tagfile = MOD / "common/country_tags/iop_tags.txt"
    if not tagfile.exists():
        err("common/country_tags/iop_tags.txt missing")
        return
    defined = dict(re.findall(r'^(\w{3}) = "([^"]+)"', read(tagfile), re.M))
    for tag in TAGS:
        if tag not in defined:
            err(f"tag {tag} not defined in country_tags")
    for tag, path in defined.items():
        if not (MOD / "common" / path).exists():
            err(f"tag {tag} points to missing common/{path}")
        hist = list((MOD / "history/countries").glob(f"{tag} - *.txt"))
        if not hist:
            err(f"tag {tag} has no history/countries/{tag} - *.txt file")

    used = set()
    for f in [*MOD.glob("common/**/*.txt"), *MOD.glob("events/*.txt")]:
        text = read(f)
        used |= {int(s) for s in re.findall(r"\b(\d{2,3}) = \{ (?:add_core_of|any_neighbor_state)", text)}
        used |= {int(s) for s in re.findall(r"\b(?:controls_state|owns_state|transfer_state|state) = (\d{2,3})", text)}
    unknown = {s for s in used if s not in KNOWN_STATES}
    if unknown:
        warn(f"state IDs not in the verified vanilla list: {sorted(unknown)} "
             f"(check they still exist in the supported patch)")

    # every tag mentioned in scripts must be defined somewhere (comments ignored -
    # they mention vanilla ISR, and "IOP" is this mod's own id prefix)
    scripts_text = strip_comments("".join(
        read(f) for f in [*MOD.glob("common/**/*.txt"),
                          *MOD.glob("events/*.txt"),
                          *MOD.glob("history/**/*.txt")]))
    known_vanilla = {"ITA"}
    for tag in set(re.findall(r"\b(I[A-Z]{2})\b", scripts_text)) - {"IOP"}:
        if tag not in defined and tag not in known_vanilla:
            err(f"tag {tag} used in scripts but not defined in country_tags")

    # set_autonomy must reference a defined autonomy level
    autonomy_ids = set(re.findall(r"id = (\w+)", read(MOD / "common/autonomous_states/iop_autonomy.txt")))
    for lvl in set(re.findall(r"autonomous_state = (\w+)", scripts_text)):
        if lvl not in autonomy_ids:
            err(f"set_autonomy references undefined level `{lvl}`")


def check_assets() -> None:
    gfx = MOD / "gfx"
    for size in FLAG_SIZES:
        d = MOD / size
        if not d.exists():
            err(f"missing flag folder {size}")
            continue
        for tag in TAGS:
            for variant in REQUIRED_FLAG_VARIANTS:
                name = f"{tag}_{variant}.tga"
                if not (d / name).exists():
                    err(f"missing required flag {size}/{name}")
    for f in sorted(gfx.rglob("*.tga")):
        raw = f.read_bytes()
        if len(raw) < 18 or raw[2] not in (2, 10) or raw[16] not in (24, 32):
            err(f"{f.relative_to(ROOT)}: not a valid uncompressed/RLE truecolor TGA")

    for f in sorted(gfx.rglob("*.dds")):
        raw = f.read_bytes()
        if raw[:4] != b"DDS ":
            err(f"{f.relative_to(ROOT)}: not a DDS file")
            continue
        h, w = struct.unpack("<II", raw[12:20])
        if raw[84:88] != b"DXT5":
            warn(f"{f.relative_to(ROOT)}: fourcc {raw[84:88]!r} (project standard is DXT5)")
        if f.parent.name in TAGS and f.stem.split("_")[0] != f.parent.name:
            err(f"{f.relative_to(ROOT)}: leader portrait must live in gfx/leaders/<TAG>/ "
                f"and be named <TAG>_*.dds")

    for f in sorted((MOD / "interface").glob("*.gfx")):
        for tex in re.findall(r'texturefile = "([^"]+)"', read(f)):
            if not (MOD / tex).exists():
                err(f"{f.relative_to(ROOT)}: sprite points to missing {tex}")

    # leader portraits referenced by history files must exist
    for f in sorted((MOD / "history/countries").glob("*.txt")):
        tag = f.name.split(" - ")[0]
        for pic in set(re.findall(r'picture = "([^"]+)"', read(f))):
            if not (MOD / "gfx/leaders" / tag / pic).exists():
                err(f"{f.relative_to(ROOT)}: picture `{pic}` not found in gfx/leaders/{tag}/")


def check_autonomy() -> None:
    f = MOD / "common/autonomous_states/iop_autonomy.txt"
    if not f.exists():
        return
    text = read(f)
    m = re.search(r"min_freedom_level = ([\d.]+)", text)
    if not m:
        err("autonomy level has no min_freedom_level")
    else:
        vanilla = {0.0, 0.2, 0.4, 0.5, 0.6, 0.75, 0.8}
        if float(m.group(1)) in vanilla:
            err(f"min_freedom_level {m.group(1)} collides with a vanilla autonomy level")
    for key in ('desc = "RULE_DESC_IS_A_SUBJECT"', "autonomy_gain_global_factor",
                "ai_subject_wants_higher", "ai_overlord_wants_lower", "allowed = {"):
        if key not in text:
            warn(f"autonomy level is missing `{key}`")
    for factor in re.findall(r"ai_(?:subject_wants_higher|overlord_wants_lower) = \{\s*factor = ([\d.]+)", text):
        if float(factor) != 0.0:
            warn(f"AI autonomy factor {factor} != 0.0 - puppets will drift between levels")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = ap.parse_args()

    if not MOD.exists():
        print(f"mod folder not found: {MOD}", file=sys.stderr)
        return 1

    check_descriptors()
    check_syntax()
    loc = collect_loc_keys()
    check_loc_coverage(loc)
    check_decision_event_graph()
    check_progression_rules()
    check_tags_and_states()
    check_assets()
    check_autonomy()

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")

    fatal = errors or (warnings if args.strict else [])
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
    if fatal:
        print("FAILED" + (" (--strict)" if args.strict and not errors else ""))
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
