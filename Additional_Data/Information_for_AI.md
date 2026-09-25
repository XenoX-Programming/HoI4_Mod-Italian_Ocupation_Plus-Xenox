# Information for AI (and human) successors

**Project:** `XenoX-Programming/HoI4_Mod-Italian_Ocupation_Plus-Xenox`
**Mod:** Italian Occupation Plus — a Hearts of Iron 4 mod that gives Italy a
Reichskommissariat-style occupation system.
**Last updated:** v0.0.37 (Roman law discipline) — the version that introduced
the content described in §5.

Read this before touching anything. It is the accumulated, verified state of the
project: what is true, what is fragile, what has already been tried, and which
commands prove your change did not break the mod.

---

## 0. Two-minute orientation

```
repo root/
├── italian_occupation_plus.mod      # launcher descriptor (version!)
├── italian_occupation_plus/         # THE MOD - everything here ships to the game
│   ├── descriptor.mod               # second descriptor (version must match!)
│   ├── README.md                    # long-form docs, changelog, file map
│   ├── common/  events/  gfx/  history/  interface/  localisation/
└── Additional_Data/                 # DEVELOPMENT MATERIAL - never ships
    ├── Graphics/                    # source PNGs for the leader portraits/flags
    ├── Information_for_AI.md        # this file
    └── tools/validate_iop.py        # static validator - run it before committing
```

- Only `italian_occupation_plus/` + `italian_occupation_plus.mod` are the mod.
  Anything in `Additional_Data/` is development material and must **never** be
  copied into a player's `…/Hearts of Iron IV/mod/` folder.
- `README.md` is the user/modder-facing document and is kept in sync by
  convention: **every version bump gets a "What's in v0.0.x" section *and* a
  changelog bullet.** The validator enforces that both exist.

## 1. The engine rules that have already bitten this project

These are hard-won; violating one produces either `logs/error.log` spam or a
silently broken feature (worse — it looks fine in the editor).

1. **Localisation files must be UTF-8 *with BOM*.** Without the BOM the game
   reads nothing and shows raw keys. `IOP_flavour_l_english.yml` shipped for
   several versions without one (fixed in v0.0.37). The validator checks every
   `.yml` for `EF BB BF`.
2. **Leader portraits must live in `gfx/leaders/<TAG>/`.** The engine only looks
   inside the tag subfolder; a flat file in `gfx/leaders/` is never found (this
   is why Bastianini was invisible in v0.0.9).
3. **Map colours need the documented form** `color = rgb { 25 100 14 }`.
   Plain `color = { 25 100 14 }` is silently ignored.
4. **Decision categories belong in `common/decisions/categories/`.**
   The old `common/decision_category/` path is never read and hid the whole tab
   (v0.0.4 hotfix).
5. **No vanilla file overrides.** This mod overrides *nothing* from the base
   game — no `history/states`, no `common/ideas/_manpower.txt` /
   `_economic.txt` / `_political.txt`, no `.gfx` interface files. That is a
   deliberate compatibility policy (survives map mods and vanilla patches) and
   it constrains several designs — most visibly the law lock (§5).
6. **Tags that clash with vanilla are unusable.** `ISR` is Israel (→ `ISE`),
   `IMO` ignored the per-file colour and rendered tan (→ `IOM`), vanilla
   releasable Georgia is `GEO` (→ `IGE`). Check vanilla before inventing a tag.
7. **Undocumented keys do nothing but pollute `error.log`.** Examples already
   removed from this mod: `capitulate_factor` (replaced by the real
   `surrender_limit`), `show_as_unavailable` in events (unknown key). If you
   invent a key, assume it is wrong until the wiki confirms it.
8. **`ai_will_do = { factor = 0 }` on every decision.** Without it the Italian
   AI takes founding/distribution decisions and destroys its own game.
9. **One-shot content must be flag-guarded.** A decision whose `visible`
   depends on state ownership can reappear after the transfer (v0.0.33 bug:
   "Transfer Poitou" came back). Use `fire_only_once` *and* a
   `has_country_flag` guard for terminal decisions.
10. **Mods may use `*_laws_cost_factor` / `economy_cost_factor`.** These used to
    error in mods because the law slots were unknown until the vanilla law files
    loaded; vanilla law files start with `_` so they load first, and the
    modifiers are now safe. (See §5.)
11. **`add_namespace = <prefix>` is mandatory** in an event file before using
    `<prefix>.<number>` ids. The validator cross-checks every id and every
    `country_event = { id = … }` reference.

## 2. Verified inventory (as of v0.0.37)

From `python3 Additional_Data/tools/validate_iop.py`:

- **20 country tags** — ICR, ISE, IMT, IAL, IBL, IGR, ITR, INA, IEG, ISP, IPG,
  IOC, ILV, IIQ, IAR, IAM, IIR, IMR, IOM, IGE. Each has a
  `common/countries/Italy_*.txt`, a `history/countries/*.txt`, 5 flag variants
  in 3 sizes, and a leader for **all four** ideologies.
- **16 custom portraits** (`gfx/leaders/<TAG>/…dds`); 4 puppets use vanilla
  portraits: IPG (Salazar), ILV (Amin al-Husseini), IIQ (Rashid Ali al-Gaylani),
  IIR (Reza Shah Pahlavi).
- **91 decisions** in 14 files under `common/decisions/` (+ 1 category file).
- **61 events** in 14 files under `events/`.
- **20 occupation zones** — consistent in all four places that must agree:
  `common/dynamic_modifiers/iop_zones.txt` (the modifier),
  `common/scripted_effects/iop_zones.txt` (`iop_grant_zone_*`),
  `common/scripted_localisation/iop_zones.txt` (20 `defined_text` tokens) and
  `localisation/english/IOP_zones_l_english.yml` (`iop_zone_list_*`).
- **~1130 localisation keys** in 9 `.yml` files, all with BOM.
- **2 autonomy levels**: `autonomy_military_occupation` (default) and
  `iop_province` / `autonomy_province` (after the Roman Empire is restored).
- **1 shared focus tree** (`iop_puppet_focus`), gated on the `iop_puppet`
  country flag that every history file sets.

## 3. How the mod is wired (the flows you will touch)

### Founding a puppet
`common/decisions/IOP_<region>.txt` → `iop_establish_*`:
```
visible  = at least half of the initial states held by Italy or its subjects
available= the capital state is held (iop_med_controlled)
complete_effect = {
    hidden_effect = { iop_grant_zone_<region> = yes }        # Italy-side bonus
    hidden_effect = {
        set_country_flag = iop_<region>_established
        <state> = { add_core_of = TAG }                       # per initial state
        release_puppet = TAG
        TAG = { iop_on_puppet_founded = yes }                 # v0.0.37 law hook
        set_autonomy = { target = TAG autonomous_state = autonomy_military_occupation }
        TAG = { transfer_state = <state> }                    # per controlled state
    }
}
```
`release_puppet` runs the tag's `history/countries/*.txt`, which is where the
leaders, tech, `iop_puppet` flag and the `iop_locked_laws` spirit come from.
IMT (Montenegro) and IOM (Oman) are the two exceptions: they are released from
an **event option** (`events/IOP_yugoslavia.txt` → `iop_yugo.1000`,
`events/IOP_arabia.txt`) instead of a decision — the same hook line applies
there.

### Distributing a state
`iop_decide_<stateID>` (visibility + border requirement) → `country_event`
(`iop_yugo.*`, `iop_greece.*`, …) → option per eligible recipient, each gated by
`any_neighbor_state = { is_owned_by = TAG }` → `add_core_of` + `transfer_state`.
Islands cannot be border-checked, so they use existence checks instead.

### Zones and the Roman Empire
Every founding grants Italy the `iop_occupation_directorate` hub spirit plus
that zone's dynamic modifier, once ever (country flag `iop_zone_<region>`).
`common/decisions/IOP_roman.txt` restores the Roman Empire: cosmetic tags
(`ICR_roman`, `ITA_roman`, `ISP_iberia`, `IGT_transcaucasus`, …), the
`iop_roman_empire` flag, the `autonomy_province` level, and a monthly
`on_monthly_pulse` that converts subjects created *after* the restoration.

## 4. Adding a new puppet — checklist

1. `common/country_tags/iop_tags.txt`: `IXX = "countries/Italy_<Region>.txt"`.
2. `common/countries/Italy_<Region>.txt`: `color = rgb { … }` + graphical culture.
3. `history/countries/IXX - <full Italian name>.txt`: capital, `oob = "IOP_empty"`,
   tech, `set_politics`/`set_popularities`, **four** `create_country_leader`
   blocks (`fascism_ideology`, `despotism`, `liberalism`, `marxism`) with a trait
   from `common/country_leader/iop_traits.txt`, stability/war support,
   `set_country_flag = iop_puppet`, `set_country_flag = iop_<region>`, and
   `add_ideas = { iop_locked_laws }`.
4. Flags: `gfx/flags/IXX*.tga` + `medium/` + `small/` (5 variants each).
5. Founding decision + `iop_grant_zone_<region>` + `iop_zone_<region>` modifier +
   its `defined_text` token + `iop_zone_list_<region>` loc line.
6. `release_puppet = IXX` **must** be followed by `IXX = { iop_on_puppet_founded = yes }`.
7. Distribution decisions + events for the neighbouring states.
8. Localisation keys (with BOM), then run the validator.

## 5. v0.0.37 — Roman law discipline (the newest subsystem)

**Goal:** no occupation government may change its conscription, trade or economy
law; on formation the puppet is told (by an event of its own) that it is on
Service by Requirement and Total Mobilization.

**Files**

| File | What it holds |
|------|---------------|
| `common/ideas/IOP_ideas.txt` | the `iop_locked_laws` national spirit |
| `common/scripted_effects/iop_laws.txt` | `iop_on_puppet_founded`, `iop_lock_current_trade_law`, `iop_enforce_roman_laws` |
| `events/IOP_laws.txt` | `iop_laws.1` "A Decree from Rome" |
| `common/on_actions/iop_on_actions.txt` | `on_weekly` watchdog + catch-all |
| `history/countries/*.txt` (×20) | `add_ideas = { iop_locked_laws }` |
| `localisation/english/IOP_laws_l_english.yml` | the 5 new keys |
| 20 `release_puppet` sites | `TAG = { iop_on_puppet_founded = yes }` |

**Runtime chain**

1. History file → the spirit exists from the moment the tag exists, on *any*
   creation path (founding decision, peace conference, console `release`).
2. `iop_on_puppet_founded` (run in the **puppet's** scope right after
   `release_puppet`) re-applies the spirit defensively and queues `iop_laws.1`
   with `hours = 6 random_hours = 6`, flag-guarded by `iop_laws_decree_fired`
   so re-founding a destroyed puppet does not spam it.
3. The event fires **for the puppet, never for Italy**. Its single option
   (`ai_chance = 100`, so AI-run puppets answer it immediately) applies
   `service_by_requirement` + `tot_economic_mobilisation`, sets
   `iop_laws_decree_accepted`, and records the trade law in force
   (`iop_trade_law_free_trade` / `_export_focus` / `_limited_exports` /
   `_closed_economy`).
4. `on_weekly` → `iop_enforce_roman_laws` puts any of the three laws back if it
   moved. The second `on_weekly` block is a catch-all: any Italian subject
   carrying the `iop_puppet` flag without `iop_laws_decree_fired` gets the
   spirit and the decree.

**Why the lock is not a greyed-out law slot.** HOI4 has no engine flag that
locks a law slot from a national spirit. Paradox does it the other way round —
the *laws* check `NOT = { has_idea = … }` in their `available` block — which
requires overriding vanilla `common/ideas/_manpower.txt`, `_economic.txt` and
`_political.txt`. This mod refuses to override vanilla files (policy §1.5), so
the lock is two layers instead:

- the spirit sets `mobilization_laws_cost_factor`, `trade_laws_cost_factor` and
  `economy_cost_factor` to `10` → **+1000%** (a 150 PP law change costs 1650 PP);
- the weekly watchdog reverts anything that still gets through, including
  vanilla "demobilise the economy/army" decisions and console changes.

**Known consequences** (deliberate, but be aware before "fixing" them):
- The mandated laws may exceed what the puppet's war support would normally
  allow (history files set `set_war_support = 0.60`, Total Mobilization normally
  wants more). The engine does **not** auto-revert a scripted law change; it
  offers the vanilla demobilise decision instead, and the watchdog overrides it.
- The revert window is up to 7 days (`on_weekly`). `on_daily` would tighten it
  but runs for every country every day — not worth it.
- The spirit is permanent: it is never removed, not even if the puppet is
  liberated. `removal_cost = -1` and `allowed = { always = no }`.
- To change the mandated laws, edit `events/IOP_laws.txt` (option) *and*
  `iop_enforce_roman_laws` (watchdog) — they must stay in sync.

## 6. Verification — what to run, and what it does *not* prove

```bash
python3 Additional_Data/tools/validate_iop.py        # from the repo root
```

It parses the real shipped files (no re-implementation of game logic) and fails
on: unbalanced braces or quotes in any `.txt`; missing BOM or bad header in any
`.yml`; duplicate localisation keys (warning if the text is identical, error if
it differs); missing loc keys for event titles/descriptions/option names and for
idea names + `_desc`; event ids without a namespace, defined twice, or fired
without being defined; events with no option; `iop_*` ideas / scripted effects /
scripted triggers referenced but never defined; idea pictures with no matching
`GFX_idea_*` sprite; a tag missing its history file, gfx file, `iop_puppet` flag
or `iop_locked_laws` spirit; a `release_puppet` not followed by its
`iop_on_puppet_founded` hook; the v0.0.37 law chain being incomplete or out of
sync (decree vs. watchdog, watchdog not wired into `on_weekly`, spirit missing a
lock modifier or removable); and any version disagreement between the two
`.mod` files, the README title and the README changelog.

**It cannot prove the mod works in-game.** The HOI4 engine is not available in
this sandbox — there is no way to run the game, so nothing here verifies
runtime behaviour (whether an effect is accepted, whether a modifier name is
valid in the target patch, whether a sprite renders). After an in-game test,
check `Documents/Paradox Interactive/Hearts of Iron IV/logs/error.log` and
search for `iop`. If you claim a feature works, say explicitly whether it was
verified statically (validator) or in-game (error.log + observed behaviour).

Quick manual test of the v0.0.37 system in a live game:
`tag ITA` → `annex YUG` → take "Establish Military Occupation of Croatia" →
switch to ICR (`tag ICR`) and confirm: the "Rome Sets the Laws" spirit is
present, the decree event fires for ICR, conscription reads Service by
Requirement, economy reads Total Mobilization, and any law change costs 1650 PP
and is reverted within a week.

## 7. Conventions and housekeeping

- **Version scheme `0.0.x`** — bump the last number only, in *both*
  `italian_occupation_plus.mod` and `italian_occupation_plus/descriptor.mod`,
  plus the README title, a "What's in v0.0.x" section and a changelog bullet.
  The validator fails on a mismatch.
- **`supported_version` is `1.19.2`** in both `.mod` files.
- Commit messages in this repo are descriptive and mention the version.
- `.gitignore` excludes `*.zip`, `uploads/`, OS junk. Releases are distributed as
  GitHub Releases, not committed zips.
- Players must **clean-reinstall** (delete the old mod folder first); HOI4 never
  cleans up removed files, so stale files masquerade as bugs.
- Source art (`Additional_Data/Graphics/*.png`) is *not* what the game loads —
  the game loads the converted `.dds`/`.tga` inside the mod folder. One filename
  contains a space (`IGR_ Pietro_Parini.png`); quote it in shell commands.

## 8. Known rough edges (candidate work)

- `autonomy_military_occupation` / `_desc` are defined twice on purpose
  (`IOP_autonomy_l_english.yml` + `IOP_countries_l_english.yml`) as redundancy;
  identical text, so last-loaded wins. The validator reports it as a warning.
- README sections are ordered by when they were written, not chronologically
  ("What's in v0.0.3" before "v0.0.29" …). The newest section is always
  directly under the version-scheme note.
- The "76 decisions" heading and some per-file decision counts in the old README
  sections are stale; the current total is 91 (validator output).
- No automated in-game test exists; the validator is the only gate.
