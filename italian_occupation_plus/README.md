# Italian Occupation Plus — v0.1.1 (Yugoslavia)

A Hearts of Iron 4 mod that gives **Italy** its own Reichskommissariat-style occupation system, inspired by *Reichskommissariats Plus*.

As Italy, occupy Yugoslav land → open the decisions tab (**Political Actions** list) → found military occupation governments as puppets → distribute individual states to them through events where **you pick the recipient**.

## What's in v0.1

### 3 new puppet nations

| Tag | Full name | Capital | Initial states (state IDs) |
|-----|-----------|---------|----------------------------|
| **ICR** | Governo Militare di Occupazione della Croazia | Croatia (109, Zagreb) | Dalmatia (103), Croatia (109), Bosnia (104), Herzegovina (804) |
| **ISE** | Governo Militare di Occupazione della Serbia | Serbia (107, Belgrade) | Serbia (107), Morava (108) |
| **IMT** | Governo Militare di Occupazione del Montenegro | Montenegro (105) | Montenegro (105) |

> **Why ISE and not ISR?** `ISR` is already used by vanilla HOI4 for **Israel** (releasable by the UK). Using it would overwrite Israel. `ISE` (Italian SErbia) keeps your `Ixx` pattern and is free in vanilla.

Puppet leaders (historical placeholders, all fascist):
- **ICR** — Mario Roatta (commander of the Italian 2nd Army in Yugoslavia)
- **ISE** — Vittorio Ambrosio (Italian Chief of Staff)
- **IMT** — Alessandro Pirzio Biroli (historical Italian governor of Montenegro)

### 20 decisions

**Founding (50 PP each, one-time):**
- Establish Military Occupation of Croatia — requires control of **Croatia (109)**
- Establish Military Occupation of Serbia — requires control of **Serbia (107)**
- Establish Military Occupation of Montenegro — requires control of **Montenegro (105)**

Founding only needs the **capital state**. Any other initial states you control transfer automatically. States you don't control yet can be assigned later with the distribution decisions.

**Distribution (10 PP each, repeatable):** one "Determine Fate of …" decision per state. Each fires an **event where you choose**: give to Croatia / Serbia / Montenegro, or keep under direct Italian rule.

| State ID | State | Event |
|----------|-------|-------|
| 102 | North Slovenia | choice of ICR / ISE / IMT / keep |
| 853 | Ljubljana | choice of ICR / ISE / IMT / keep |
| 103 | Dalmatia | choice of ICR / ISE / IMT / keep |
| 109 | Croatia | choice of ICR / ISE / IMT / keep |
| 104 | Bosnia | choice of ICR / ISE / IMT / keep |
| 804 | Herzegovina | choice of ICR / ISE / IMT / keep |
| 105 | Montenegro | choice of ICR / ISE / IMT / keep |
| 107 | Serbia | choice of ICR / ISE / IMT / keep |
| 108 | Morava | choice of ICR / ISE / IMT / keep |
| 45 | Vojvodina (Backa) | choice of ICR / ISE / IMT / keep |
| 764 | West Banat | choice of ICR / ISE / IMT / keep |
| 802 | Kosovo | choice of ICR / ISE / IMT / keep |
| 803 | Southern Serbia | choice of ICR / ISE / IMT / keep |
| 106 | Macedonia | choice of ICR / ISE / IMT / keep |
| 970 | Debar | choice of ICR / ISE / IMT / keep |
| **163** | **Zara (special)** | **cede to Croatia OR annex to Italy (+ Italian core)** |
| **852** | **Istria (special)** | **cede to Croatia OR annex to Italy (+ Italian core)** |

Zara and Istria start as Italian territory, so their decisions appear only **after** the Croatian occupation government exists.

## Installation

1. Copy the `italian_occupation_plus` folder **and** the `italian_occupation_plus.mod` file into your HOI4 mod folder:
   - **Windows:** `Documents\Paradox Interactive\Hearts of Iron IV\mod\`
   - **Linux:** `~/.local/share/Paradox Interactive/Hearts of Iron IV/mod/`
2. Open the Paradox launcher → *Mods* → enable **Italian Occupation Plus**.
3. Launch the game. Supported version: `1.18.*` (if your game is newer and the launcher shows it as outdated, you can still try enabling it — the mod uses stable scripting features).

## How to play / test

1. Start as **Italy**, justify on Yugoslavia (or wait for the historical war).
2. Capitulate Yugoslavia and make sure **you** control the land (not Germany — decisions check `controls_state` for Italy).
3. Open the **Decisions tab** → find them in the **Political Actions** list (search "Occupation" or "Fate").
4. Click **Establish Military Occupation of Croatia / Serbia / Montenegro** (50 PP each).
5. New puppets appear as your subjects. Then use the **"Determine Fate of …"** decisions (10 PP) — an event pops up letting you pick which puppet gets the state.
6. For Zara/Istria, the event offers **cede to Croatia** vs **annex to Italy** (annexing adds an Italian core).

**Quick console test:** `tag ITA`, `annex YUG`, then open decisions. (Annexing via console gives you control of everything, so all founding decisions light up.)

## How it works (for modding)

- **No `history/states` overrides.** Cores are added at release time via `add_state_core`, so the mod is compatible with map mods and future vanilla state changes (as long as IDs stay the same).
- Founding effect: `add_state_core` → `release_puppet = TAG` → `transfer_state` for each controlled initial state (guarded by `if` + `controls_state`, so it never steals land from Germany).
- Distribution: decision → `country_event` → event option does `add_state_core` + `transfer_state` to the chosen puppet.
- AI never touches it (`ai_will_do = { factor = 0 }`), so Italy AI won't break itself.
- Localisation files are UTF-8 **with BOM** (required by HOI4).
- Flags are v1 placeholders: local colors + Italian tricolor canton, in all 3 sizes × 5 ideologies.

## File map

```
italian_occupation_plus/
├── descriptor.mod
├── README.md
├── common/
│   ├── country_tags/iop_tags.txt        # ICR / ISE / IMT
│   ├── countries/Italy_*.txt            # gfx culture + map color
│   └── decisions/IOP_yugoslavia.txt     # 3 founding + 17 distribution decisions
├── history/
│   ├── countries/ICR|ISE|IMT*.txt       # capitals, leaders, tech
│   └── units/IOP_empty.txt              # empty puppet OOB
├── events/IOP_yugoslavia.txt            # 17 events (iop_yugo.102, .103, ...)
├── localisation/english/IOP_*_l_english.yml  # countries / decisions / events (BOM!)
└── gfx/flags/ (+ medium/, small/)       # 45 placeholder .tga flags
```

## Extending to v0.2 (Greece, Albania, France…)

The pattern per new region is:

1. **New tags** in `common/country_tags/iop_tags.txt` + `common/countries/` + `history/countries/` + flags (copy an existing one, rename, change capital/colors/leader).
2. **Founding decision** in a new `common/decisions/IOP_greece.txt` (copy `iop_establish_croatia`, change state IDs + tag + flag name).
3. **Distribution decisions + events** per state (copy a `iop_decide_*` block and its event, change the state ID).
4. **Localisation**: add decision/event/country keys to the three `.yml` files (keep the BOM!).

Suggested next regions: Greece (Epirus, Thessaly, Athens…), Albania protectorate, Corsica/Savoy, Egypt/Libya, Ethiopia/East Africa.

## Troubleshooting

- **Decisions don't show:** you must be playing the country with `original_tag = ITA`, and founding decisions need control of the capital state (109 / 107 / 105). Distribution decisions need at least one puppet to exist first.
- **Mod shows as outdated:** edit `supported_version` in both `.mod` files to match your game (e.g. `1.19.*`).
- **Check errors:** after running the game, look at `Documents\Paradox Interactive\Hearts of Iron IV\logs\error.log` and search for `iop`.
- **Missing portraits:** if a leader shows a silhouette, the portrait `.dds` name doesn't exist in your game version — replace `picture = ...` in the history file with another vanilla portrait. It never crashes, it's cosmetic.

## Changelog

- **0.1.1** — Hotfix: decisions moved to vanilla `political_actions` category (custom category could hide them), `visible` triggers fixed to use `country_exists` (old `TAG = { NOT = { exists } }` never evaluated true for non-existent tags, so founding decisions never appeared), cores now added via state-scope `add_core_of` (works before the tag exists), founding is repeatable if a puppet is destroyed, `supported_version` bumped to `1.18.*`.
- **0.1.0** — First version: ICR / ISE / IMT, Yugoslavia founding + distribution, Zara/Istria special annexation, placeholder flags, English localisation.
