#!/usr/bin/env python3
"""
Italian Occupation Plus - static validator.

The HOI4 engine is not available in the development sandbox, so this script is
the check that gets run before a commit. It parses the real shipped files under
italian_occupation_plus/ (no re-implementation of game logic) and fails on the
classes of mistake that show up in logs/error.log or as raw loc keys in-game.

Usage:
    python3 Additional_Data/tools/validate_iop.py [path-to-mod-folder]

Exit code 0 = clean, 1 = problems found (they are printed as ERROR lines).
"""

import glob
import os
import re
import sys

# ---------------------------------------------------------------- utilities

MOD_TAGS = []  # filled from common/country_tags/iop_tags.txt


def read(path):
    with open(path, "rb") as fh:
        raw = fh.read()
    return raw.decode("utf-8-sig", errors="replace")


def strip_comments(text):
    """Remove '#' comments that are not inside a quoted string."""
    out = []
    for line in text.split("\n"):
        in_str = False
        for i, ch in enumerate(line):
            if ch == '"':
                in_str = not in_str
            elif ch == "#" and not in_str:
                line = line[:i]
                break
        out.append(line)
    return "\n".join(out)


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def err(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)

    def dump(self):
        for m in self.errors:
            print("ERROR   " + m)
        for m in self.warnings:
            print("WARNING " + m)
        print(
            "\n%d error(s), %d warning(s)" % (len(self.errors), len(self.warnings))
        )
        return 1 if self.errors else 0


# ---------------------------------------------------------------- checks


def check_braces(mod, rep):
    """Brace balance + balanced quotes on every scripted .txt file."""
    patterns = ["common/**/*.txt", "events/*.txt", "history/**/*.txt", "interface/*.gfx"]
    files = []
    for p in patterns:
        files += glob.glob(os.path.join(mod, p), recursive=True)
    for f in sorted(files):
        text = strip_comments(read(f))
        depth = 0
        for line in text.split("\n"):
            depth += line.count("{") - line.count("}")
            if depth < 0:
                rep.err("%s: '}' without a matching '{'" % os.path.relpath(f, mod))
                depth = 0
        if depth != 0:
            rep.err(
                "%s: %d unclosed '{' at end of file" % (os.path.relpath(f, mod), depth)
            )
        if text.count('"') % 2 != 0:
            rep.err("%s: odd number of '\"' characters" % os.path.relpath(f, mod))
    return files


def check_localisation(mod, rep):
    """BOM, header, duplicate keys, and a key -> value map."""
    loc_keys = {}
    files = sorted(glob.glob(os.path.join(mod, "localisation/english/*.yml")))
    for f in files:
        raw = open(f, "rb").read()
        rel = os.path.relpath(f, mod)
        if not raw.startswith(b"\xef\xbb\xbf"):
            rep.err("%s: missing UTF-8 BOM (HOI4 will not read the file)" % rel)
        text = raw.decode("utf-8-sig", errors="replace")
        lines = text.split("\n")
        if not lines or lines[0].strip() != "l_english:":
            rep.err("%s: first line must be 'l_english:'" % rel)
        for n, line in enumerate(lines[1:], start=2):
            if not line.strip() or line.lstrip().startswith("#"):
                continue  # blank line / comment (both legal in HOI4 loc files)
            m = re.match(r"^\s+([A-Za-z0-9_\.]+):\d+\s+\"(.*)\"\s*$", line)
            if not m:
                rep.warn("%s:%d unparsed localisation line" % (rel, n))
                continue
            key, value = m.group(1), m.group(2)
            if key in loc_keys:
                prev_file, prev_line, prev_value = loc_keys[key]
                if prev_value == value:
                    rep.warn(
                        "%s:%d duplicate loc key '%s' with identical text "
                        "(also in %s) - last file loaded wins"
                        % (rel, n, key, prev_file)
                    )
                else:
                    rep.err(
                        "%s:%d duplicate loc key '%s' with DIFFERENT text "
                        "(also in %s:%d)" % (rel, n, key, prev_file, prev_line)
                    )
                continue
            loc_keys[key] = (rel, n, value)
    return loc_keys


def check_events(mod, rep, loc_keys):
    """Namespaces, unique ids, referenced ids, title/desc/option loc keys."""
    ids = {}
    namespaces = set()
    referenced = []
    files = sorted(glob.glob(os.path.join(mod, "events/*.txt")))
    for f in files:
        rel = os.path.relpath(f, mod)
        text = strip_comments(read(f))
        for m in re.finditer(r"add_namespace\s*=\s*([A-Za-z0-9_]+)", text):
            namespaces.add(m.group(1))
        for m in re.finditer(r"\bid\s*=\s*([A-Za-z0-9_]+\.[A-Za-z0-9_]+)", text):
            ids.setdefault(m.group(1), []).append(rel)
    for eid, where in ids.items():
        if len(where) > 1:
            rep.err("event id '%s' defined in more than one file: %s" % (eid, where))
        if eid.split(".")[0] not in namespaces:
            rep.err(
                "event id '%s' has no 'add_namespace = %s' (%s)"
                % (eid, eid.split(".")[0], where[0])
            )
    # every country_event/news_event reference must resolve
    for f in sorted(
        glob.glob(os.path.join(mod, "common/**/*.txt"), recursive=True)
        + files
        + glob.glob(os.path.join(mod, "history/**/*.txt"), recursive=True)
    ):
        rel = os.path.relpath(f, mod)
        text = strip_comments(read(f))
        for m in re.finditer(
            r"(?:country_event|news_event|state_event|unit_leader_event)\s*=\s*\{[^}]*?\bid\s*=\s*([A-Za-z0-9_]+\.[A-Za-z0-9_]+)",
            text,
            flags=re.S,
        ):
            referenced.append((m.group(1), rel))
        for m in re.finditer(
            r"(?:country_event|news_event)\s*=\s*([A-Za-z0-9_]+\.[A-Za-z0-9_]+)", text
        ):
            referenced.append((m.group(1), rel))
    for eid, rel in referenced:
        if eid not in ids:
            rep.err("%s: fires undefined event '%s'" % (rel, eid))
    # title / desc / option names of every event need loc keys
    for f in files:
        rel = os.path.relpath(f, mod)
        text = strip_comments(read(f))
        for block in re.finditer(
            r"country_event\s*=\s*\{(.*?)\n\}", text, flags=re.S
        ):
            body = block.group(1)
            eid = re.search(r"\bid\s*=\s*([A-Za-z0-9_\.]+)", body)
            eid = eid.group(1) if eid else "?"
            for key_name in ("title", "desc"):
                m = re.search(r"\b%s\s*=\s*([A-Za-z0-9_\.]+)" % key_name, body)
                if not m:
                    rep.err("%s: event %s has no '%s'" % (rel, eid, key_name))
                elif m.group(1) not in loc_keys:
                    rep.err(
                        "%s: event %s %s key '%s' has no localisation"
                        % (rel, eid, key_name, m.group(1))
                    )
            options = re.findall(r"option\s*=\s*\{", body)
            if not options:
                rep.err("%s: event %s has no option" % (rel, eid))
            for m in re.finditer(r"\bname\s*=\s*([A-Za-z0-9_\.]+)", body):
                if m.group(1) not in loc_keys:
                    rep.err(
                        "%s: event %s option name '%s' has no localisation"
                        % (rel, eid, m.group(1))
                    )
    return ids


def check_ideas(mod, rep, loc_keys):
    """Every idea defined in the mod: loc keys + a resolvable picture sprite."""
    sprites = set()
    for f in glob.glob(os.path.join(mod, "interface/*.gfx")):
        for m in re.finditer(r'name\s*=\s*"(GFX_[A-Za-z0-9_]+)"', read(f)):
            sprites.add(m.group(1))
    ideas = {}
    for f in sorted(glob.glob(os.path.join(mod, "common/ideas/*.txt"))):
        rel = os.path.relpath(f, mod)
        text = strip_comments(read(f))
        for m in re.finditer(r"^\t\t([A-Za-z0-9_]+)\s*=\s*\{", text, flags=re.M):
            name = m.group(1)
            ideas[name] = rel
            if name not in loc_keys:
                rep.err("%s: idea '%s' has no name localisation" % (rel, name))
            if name + "_desc" not in loc_keys:
                rep.err("%s: idea '%s' has no _desc localisation" % (rel, name))
        for m in re.finditer(r"picture\s*=\s*([A-Za-z0-9_]+)", text):
            if "GFX_idea_" + m.group(1) not in sprites:
                rep.err(
                    "%s: picture '%s' has no GFX_idea_%s sprite in interface/*.gfx"
                    % (rel, m.group(1), m.group(1))
                )
    # iop_* ideas referenced anywhere must exist
    for f in sorted(
        glob.glob(os.path.join(mod, "common/**/*.txt"), recursive=True)
        + glob.glob(os.path.join(mod, "events/*.txt"))
        + glob.glob(os.path.join(mod, "history/**/*.txt"), recursive=True)
    ):
        rel = os.path.relpath(f, mod)
        text = strip_comments(read(f))
        for m in re.finditer(
            r"\b(?:add_ideas|remove_ideas|has_idea|swap_ideas|add_timed_idea)\b[^\n]*?\b(iop_[a-z0-9_]+)",
            text,
        ):
            if m.group(1) not in ideas:
                rep.err("%s: references undefined iop idea '%s'" % (rel, m.group(1)))
    return ideas


def check_scripted(mod, rep):
    """iop_* scripted effects/triggers used must be defined."""
    defined = set()
    for folder in ("scripted_effects", "scripted_triggers"):
        for f in glob.glob(os.path.join(mod, "common", folder, "*.txt")):
            for m in re.finditer(
                r"^([A-Za-z0-9_]+)\s*=\s*\{", strip_comments(read(f)), flags=re.M
            ):
                defined.add(m.group(1))
    for f in sorted(
        glob.glob(os.path.join(mod, "common/**/*.txt"), recursive=True)
        + glob.glob(os.path.join(mod, "events/*.txt"))
        + glob.glob(os.path.join(mod, "history/**/*.txt"), recursive=True)
    ):
        rel = os.path.relpath(f, mod)
        text = strip_comments(read(f))
        for m in re.finditer(r"^\s*([A-Za-z0-9_]+)\s*=\s*(?:yes|no)\s*$", text, flags=re.M):
            name = m.group(1)
            if name.startswith("iop_") and name not in defined:
                rep.err("%s: calls undefined scripted effect/trigger '%s'" % (rel, name))
    return defined


def check_tags(mod, rep):
    """Every tag: history file, gfx file, law-lock spirit."""
    tags = []
    tagfile = os.path.join(mod, "common/country_tags/iop_tags.txt")
    for m in re.finditer(
        r'^([A-Z]{3})\s*=\s*"countries/([A-Za-z0-9_]+)\.txt"',
        read(tagfile),
        flags=re.M,
    ):
        tags.append((m.group(1), m.group(2)))
    for tag, gfxname in tags:
        gfx = os.path.join(mod, "common/countries", gfxname + ".txt")
        if not os.path.exists(gfx):
            rep.err("tag %s points at missing %s" % (tag, gfx))
        hist = glob.glob(os.path.join(mod, "history/countries", tag + " *.txt"))
        if not hist:
            rep.err("tag %s has no history/countries file" % tag)
            continue
        text = read(hist[0])
        if "iop_puppet" not in text:
            rep.err("%s: history file does not set the iop_puppet flag" % tag)
        if "iop_locked_laws" not in text:
            rep.err("%s: history file does not grant iop_locked_laws" % tag)
    return [t for t, _ in tags]


def check_founding_hooks(mod, rep):
    """Every release_puppet must queue the founding decree for that tag."""
    sites = 0
    for f in sorted(
        glob.glob(os.path.join(mod, "common/decisions/*.txt"))
        + glob.glob(os.path.join(mod, "events/*.txt"))
    ):
        rel = os.path.relpath(f, mod)
        lines = read(f).split("\n")
        for i, line in enumerate(lines):
            m = re.match(r"^[ \t]*release_puppet = ([A-Z]{3})[ \t]*$", line)
            if not m:
                continue
            sites += 1
            tag = m.group(1)
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if "%s = { iop_on_puppet_founded = yes }" % tag not in nxt:
                rep.err(
                    "%s:%d release_puppet = %s is not followed by the "
                    "iop_on_puppet_founded call" % (rel, i + 1, tag)
                )
    return sites


def check_version(repo, mod, rep):
    """Both .mod files and the README header must agree."""
    versions = {}
    for f in (
        os.path.join(repo, "italian_occupation_plus.mod"),
        os.path.join(mod, "descriptor.mod"),
    ):
        m = re.search(r'^version="([^"]+)"', read(f), flags=re.M)
        if not m:
            rep.err("%s: no version= line" % f)
        else:
            versions[os.path.basename(f)] = m.group(1)
    readme = read(os.path.join(mod, "README.md"))
    m = re.search(r"v(0\.0\.\d+)", readme.split("\n")[0])
    if not m:
        rep.err("README.md: title has no version")
    else:
        versions["README.md"] = m.group(1)
    if len(set(versions.values())) != 1:
        rep.err("version mismatch: %s" % versions)
    if "- **%s** —" % versions.get("README.md") not in readme:
        rep.err(
            "README.md changelog has no entry for %s" % versions.get("README.md")
        )
    return versions


def check_law_discipline(mod, rep):
    """The v0.0.37 law-lock chain must be complete and self-consistent.

    event option laws  ⊆  watchdog laws  ⊆  event laws + the 4 trade laws
    (the watchdog may only ever restore a law the decree set or recorded),
    and the watchdog itself must actually be wired into on_actions.
    """
    trade_laws = {"free_trade", "export_focus", "limited_exports", "closed_economy"}

    ev = os.path.join(mod, "events/IOP_laws.txt")
    se = os.path.join(mod, "common/scripted_effects/iop_laws.txt")
    oa = os.path.join(mod, "common/on_actions/iop_on_actions.txt")
    for f in (ev, se, oa):
        if not os.path.exists(f):
            rep.err("law discipline: missing %s" % os.path.relpath(f, mod))
            return

    ev_text = strip_comments(read(ev))
    se_text = strip_comments(read(se))
    oa_text = strip_comments(read(oa))

    option = re.search(r"option\s*=\s*\{(.*?)\n\t\}", ev_text, flags=re.S)
    if not option:
        rep.err("events/IOP_laws.txt: iop_laws.1 has no option block")
        return
    decree_laws = set(re.findall(r"add_ideas\s*=\s*([a-z_]+)", option.group(1)))
    if not decree_laws:
        rep.err("events/IOP_laws.txt: the decree option sets no laws at all")
    if "iop_laws_decree_accepted" not in option.group(1):
        rep.err(
            "events/IOP_laws.txt: the decree option must set the "
            "iop_laws_decree_accepted flag (the watchdog keys on it)"
        )

    watchdog = re.search(
        r"^iop_enforce_roman_laws\s*=\s*\{(.*)^\}", se_text, flags=re.S | re.M
    )
    if not watchdog:
        rep.err("scripted_effects/iop_laws.txt: iop_enforce_roman_laws not defined")
        return
    restored = set(re.findall(r"add_ideas\s*=\s*([a-z_]+)", watchdog.group(1)))

    missing = decree_laws - restored
    if missing:
        rep.err(
            "law discipline: the decree sets %s but iop_enforce_roman_laws never "
            "restores it" % sorted(missing)
        )
    extra = restored - decree_laws - trade_laws
    if extra:
        rep.err(
            "law discipline: iop_enforce_roman_laws restores %s, which the decree "
            "never sets or records" % sorted(extra)
        )

    if "iop_enforce_roman_laws = yes" not in oa_text:
        rep.err("on_actions: iop_enforce_roman_laws is never called (watchdog dead)")
    if "iop_on_puppet_founded = yes" not in oa_text:
        rep.err("on_actions: the catch-all iop_on_puppet_founded call is missing")
    if "on_weekly" not in oa_text:
        rep.err("on_actions: no on_weekly block - the watchdog would never run")

    founding = re.search(
        r"^iop_on_puppet_founded\s*=\s*\{(.*)^\}", se_text, flags=re.S | re.M
    )
    if not founding:
        rep.err("scripted_effects/iop_laws.txt: iop_on_puppet_founded not defined")
    else:
        body = founding.group(1)
        if "add_ideas = iop_locked_laws" not in body:
            rep.err("iop_on_puppet_founded does not grant iop_locked_laws")
        if "id = iop_laws.1" not in body:
            rep.err("iop_on_puppet_founded does not fire iop_laws.1")

    idea = strip_comments(read(os.path.join(mod, "common/ideas/IOP_ideas.txt")))
    block = re.search(r"^\t\tiop_locked_laws\s*=\s*\{(.*?)^\t\t\}", idea, flags=re.S | re.M)
    if not block:
        rep.err("ideas/IOP_ideas.txt: iop_locked_laws spirit not defined")
    else:
        body = block.group(1)
        for key in (
            "mobilization_laws_cost_factor",
            "trade_laws_cost_factor",
            "economy_cost_factor",
        ):
            if key not in body:
                rep.err("iop_locked_laws does not lock %s" % key)
        if "removal_cost = -1" not in body:
            rep.err("iop_locked_laws is removable (removal_cost must be -1)")
    print(
        "law discipline: decree sets %s | watchdog restores %d law(s)"
        % (sorted(decree_laws), len(restored))
    )


# ---------------------------------------------------------------- main


def main():
    repo = os.path.abspath(
        sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "..")
    )
    mod = os.path.join(repo, "italian_occupation_plus")
    if not os.path.isdir(mod):
        print("mod folder not found: %s" % mod)
        return 2
    rep = Report()

    check_braces(mod, rep)
    loc_keys = check_localisation(mod, rep)
    ids = check_events(mod, rep, loc_keys)
    ideas = check_ideas(mod, rep, loc_keys)
    scripted = check_scripted(mod, rep)
    tags = check_tags(mod, rep)
    sites = check_founding_hooks(mod, rep)
    check_law_discipline(mod, rep)
    versions = check_version(repo, mod, rep)

    print("tags: %d | events: %d | iop ideas: %d | scripted iop_*: %d"
          % (len(tags), len(ids), len(ideas), len(scripted)))
    print("founding sites hooked: %d | version: %s"
          % (sites, versions.get("README.md")))
    print("localisation keys: %d" % len(loc_keys))
    return rep.dump()


if __name__ == "__main__":
    sys.exit(main())
