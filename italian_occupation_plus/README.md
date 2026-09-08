# Italian Occupation Plus — v0.0.6 (Yugoslavia + Albania)

A Hearts of Iron 4 mod that gives **Italy** its own Reichskommissariat-style occupation system, inspired by *Reichskommissariats Plus*.

As Italy, occupy Yugoslav land → open the decisions tab **"Italian Occupation"** → found military occupation governments as puppets → distribute individual states to them through events where **you pick the recipient (must border the state)**.

> **Version scheme:** `0.0.x` — future updates increment only the last number (0.0.4, 0.0.5, …).

## What's in v0.0.3

### 4 new puppet nations

| Tag | Full name | Capital | Initial states (state IDs) |
|-----|-----------|---------|----------------------------|
| **ICR** | Governo Militare di Occupazione della Croazia | Croatia (109, Zagreb) | Dalmatia (103), Croatia (109), Bosnia (104), Herzegovina (804) |
| **ISE** | Governo Militare di Occupazione della Serbia | Serbia (107, Belgrade) | Serbia (107), Morava (108) |
| **IMT** | Governo Militare di Occupazione del Montenegro | Montenegro (105) | Montenegro (105) |
| **IAL** | Governo Militare di Occupazione dell'Albania | Albania (44, Tirana) | Albania (44), Northern Epirus (805), Shkoder (934) |

> **Why ISE and not ISR?** `ISR` is already used by vanilla HOI4 for **Israel** (releasable by the UK). Using it would overwrite Israel. `ISE` (Italian SErbia) keeps the `Ixx` pattern and is free in vanilla.

Puppet leaders (historical placeholders, all fascist):
- **ICR** — Giuseppe Bastianini (historical Governor of Dalmatia, custom portrait included)
- **ISE** — Vittorio Ambrosio (Italian Chief of Staff)
- **IMT** — Alessandro Pirzio Biroli (historical Italian governor of Montenegro)
- **IAL** — Francesco Jacomoni (historical Lieutenant of the King in Albania)

### New autonomy level: Military Occupation

Between **annexation** and **Reichskommissariat** on the freedom scale (`min_freedom_level = 0.1`). Stats modelled on the Reichskommissariat, except industry:

| Stat | Value |
|------|-------|
| Civilian industry to overlord | **100%** |
| Military industry to overlord | **100%** |
| Manpower to overlord | 100% |
| Trade to overlord / overlord trade cost | 100% / −90% |
| Overlord can build in subject | Yes |
| Subject rules | Cannot declare war, cannot decline call to war, deployed units go to overlord, no spymaster/operatives/collab governments |

- Assigned **automatically** when a puppet is founded (`set_autonomy` in the founding decision).
- Restricted to **Italian subjects only** (`allowed` block), so it never pollutes other nations' UI, peace deals, or subject interactions.
- Has its own 35×35 icon (`gfx/interface/autonomy/` + `interface/iop_autonomy.gfx`).

### 24 decisions — all free, all with map highlighting

Own tab: **"Italian Occupation"**. Hovering any decision outlines the state(s) it needs/changes.

**Founding (one per puppet, repeatable if the puppet is destroyed):**
- Establish Military Occupation of Croatia — requires control of **Croatia (109)**, highlights all 4 initial states
- Establish Military Occupation of Serbia — requires control of **Serbia (107)**, highlights both initial states
- Establish Military Occupation of Albania — requires control of **Albania (44)**, highlights all 3 initial states

Founding only needs the **capital state**. Any other initial states you control transfer automatically.

**Fall of Montenegro (special):** Montenegro is no longer founded directly. The **"Fall of Montenegro"** decision (requires control of **105** plus at least one of ICR / ISE / IAL already existing) fires an event with 4 options: **Integrate into Croatia / Serbia / Albania** (each must border Montenegro; transfers + cores the state) or **Create a new occupational government** (releases IMT as before).

**Distribution (repeatable):** one "Determine Fate of …" decision per state. Each fires an **event where you choose the recipient — but only occupation governments that BORDER the state are eligible.** This forces natural, contiguous expansion (e.g. assign Macedonia before Debar).

| State ID | State | Recipients |
|----------|-------|-----------|
| 102 | North Slovenia | bordering puppets only |
| 853 | Ljubljana | bordering puppets only |
| 103 | Dalmatia | bordering puppets only |
| 109 | Croatia | bordering puppets only |
| 104 | Bosnia | bordering puppets only |
| 804 | Herzegovina | bordering puppets only |
| 105 | Montenegro | bordering puppets only |
| 107 | Serbia | bordering puppets only |
| 108 | Morava | bordering puppets only |
| 45 | Vojvodina (Backa) | bordering puppets only |
| 764 | West Banat | bordering puppets only |
| 802 | Kosovo | bordering puppets only |
| 803 | Southern Serbia | bordering puppets only |
| 106 | Macedonia | bordering puppets only |
| 970 | Debar | bordering puppets only |
| 44 | Albania (capital — reassignable only after IAL exists) | bordering puppets only |
| 805 | Northern Epirus | bordering puppets only |
| 934 | Shkoder | bordering puppets only |
| **163** | **Zara (special)** | **Croatia (must border) OR annex to Italy (+ Italian core)** |
| **852** | **Istria (special)** | **Croatia (must border) OR annex to Italy (+ Italian core)** |

Only **Zara and Istria** keep an annex-to-Italy option (core gain is intentionally not shown) — all other transfers must go to a bordering puppet. A distribution decision stays unavailable (greyed) until at least one puppet borders its state, so the event can never fire without a valid recipient. Capital states (Croatia 109, Serbia 107, Montenegro 105, Albania 44) have no redistribution decision at all while their puppet can still be created — found (or settle) the puppet first.

## Installation

1. Copy the `italian_occupation_plus` folder **and** the `italian_occupation_plus.mod` file into your HOI4 mod folder:
   - **Windows:** `Documents\Paradox Interactive\Hearts of Iron IV\mod\`
   - **Linux:** `~/.local/share/Paradox Interactive/Hearts of Iron IV/mod/`
2. Open the Paradox launcher → *Mods* → enable **Italian Occupation Plus**.
3. Launch the game. Supported version: `1.18.*` (if your game is newer and the launcher shows it as outdated, you can still try enabling it — the mod uses stable scripting features).

## How to play / test

1. Start as **Italy**, justify on Yugoslavia (or wait for the historical war).
2. Capitulate Yugoslavia and make sure **you** control the land (not Germany — decisions check `controls_state` for Italy).
3. Open the **Decisions tab** → category **"Italian Occupation"**.
4. Click **Establish Military Occupation of Croatia / Serbia / Albania** (free), and use **Fall of Montenegro** for Montenegro. Puppets appear as your subjects with the **Military Occupation** autonomy level.
5. Use the **"Determine Fate of …"** decisions (free) — an event pops up letting you pick which **bordering** puppet gets the state. Assign in contiguous order (e.g. Macedonia before Debar).
6. For Zara/Istria, the event offers **cede to Croatia** (must border) vs **annex to Italy** (adds an Italian core).

**Quick console test:** `tag ITA`, `annex YUG`, then open decisions. (Annexing via console gives you control of everything, so all founding decisions light up.)

## How it works (for modding)

- **No `history/states` overrides.** Cores are added at release time via state-scope `add_core_of`, so the mod is compatible with map mods and future vanilla state changes (as long as IDs stay the same).
- Founding effect: `add_core_of` → `release_puppet = TAG` → `set_autonomy` (Military Occupation) → `transfer_state` for each controlled initial state (guarded by `if` + `controls_state`, so it never steals land from Germany).
- Distribution: decision (`available` requires ≥1 bordering puppet) → `country_event` → event option does `add_core_of` + `transfer_state` to the chosen puppet. Option triggers use `any_neighbor_state = { is_owned_by = TAG }`.
- AI never touches it (`ai_will_do = { factor = 0 }`), so Italy AI won't break itself.
- Localisation files are UTF-8 **with BOM** (required by HOI4).
- Flags are placeholders: local colors + Italian tricolor canton, in all 3 sizes × 5 ideologies.

## File map

```
italian_occupation_plus/
├── descriptor.mod
├── README.md
├── common/
│   ├── autonomous_states/iop_autonomy.txt   # Military Occupation level
│   ├── country_tags/iop_tags.txt            # ICR / ISE / IMT
│   ├── countries/Italy_*.txt                # gfx culture + map color
│   ├── decisions/categories/iop_categories.txt # "Italian Occupation" tab (note: categories/ subfolder!)
│   └── decisions/IOP_yugoslavia.txt         # 3 founding + 17 distribution decisions
├── history/
│   ├── countries/ICR|ISE|IMT*.txt           # capitals, leaders, tech
│   └── units/IOP_empty.txt                  # empty puppet OOB
├── gfx/leaders/Portrait_Giuseppe_Bastianini.dds # custom ICR leader portrait
├── events/IOP_yugoslavia.txt                # 17 events (iop_yugo.102, .103, ...)
├── interface/iop_autonomy.gfx               # autonomy icon sprite
├── interface/iop_decisions.gfx               # category icon sprite
├── gfx/
│   ├── flags/ (+ medium/, small/)           # 45 placeholder .tga flags
│   └── interface/autonomy/                  # Military Occupation .dds icon
└── localisation/english/IOP_*_l_english.yml # countries / decisions / events / autonomy (BOM!)
```

## Extending (Greece, Albania, France…)

The pattern per new region is:

1. **New tags** in `common/country_tags/iop_tags.txt` + `common/countries/` + `history/countries/` + flags (copy an existing one, rename, change capital/colors/leader).
2. **Founding decision** in a new `common/decisions/IOP_greece.txt` (copy `iop_establish_croatia`, change state IDs + tag + flag name; keep the `set_autonomy` block to use Military Occupation).
3. **Distribution decisions + events** per state (copy a `iop_decide_*` block and its event, change the state ID — border logic works automatically).
4. **Localisation**: add decision/event/country keys to the `.yml` files (keep the BOM!).

Suggested next regions: Greece (Epirus, Thessaly, Athens…), Albania protectorate, Corsica/Savoy, Egypt/Libya, Ethiopia/East Africa.

## Troubleshooting

- **Decisions don't show:** you must be playing the country with `original_tag = ITA`. Founding needs control of the capital state (109 / 107 / 105). Distribution needs ≥1 puppet to exist AND at least one puppet bordering the state.
- **Mod shows as outdated:** edit `supported_version` in both `.mod` files to match your game (e.g. `1.19.*`).
- **"Military Occupation" level missing/wrong:** check `error.log` for `autonomy_military_occupation` — most likely the `.gfx` sprite or `.dds` path. The icon falling back to `?` is cosmetic only.
- **Check errors:** after running the game, look at `Documents\Paradox Interactive\Hearts of Iron IV\logs\error.log` and search for `iop`.
- **Missing portraits:** if a leader shows a silhouette, the portrait `.dds` name doesn't exist in your game version — replace `picture = ...` in the history file with another vanilla portrait. It never crashes, it's cosmetic.

## Changelog

- **0.0.6** — Fall of Montenegro requires ICR/ISE/IAL to exist; all puppets use Italy's map color { 67 127 63 }; portraits/icons re-encoded as proper DXT5 DDS (fixes Bastianini not showing); leader desc localisation keys; autonomy name mirrored into countries loc as redundancy.
- **0.0.5** — New IAL (Albania: 44/805/934) with full founding + redistribution parity and 4th recipient option in every fate event; Montenegro moved to 'Fall of Montenegro' event (integrate into Croatia/Serbia/Albania or create IMT); capitals can't be redistributed while their puppet is still creatable; Zara/Istria annex no longer mentions cores; Giuseppe Bastianini (custom portrait) leads ICR.
- **0.0.4** — Hotfix: decision category moved to the correct `common/decisions/categories/` path (the old `common/decision_category/` folder is never read by the game, which hid the whole tab); custom Italian-roundel category icon + registered sprite.
- **0.0.3** — Military Occupation autonomy level (0.1, RK-like, 100% civ+mil industry, Italy-only, custom icon); new "Italian Occupation" decision category; map highlighting on all 20 decisions; all decisions free; transfers restricted to bordering puppets (Zara/Istria keep annex-to-Italy); version scheme reset to 0.0.x.
- **0.1.1** — Hotfix: vanilla category, `country_exists` triggers, state-scope cores, repeatable founding, `supported_version` 1.18.*.
- **0.1.0** — First version: ICR / ISE / IMT, Yugoslavia founding + distribution, Zara/Istria special annexation, placeholder flags, English localisation.
