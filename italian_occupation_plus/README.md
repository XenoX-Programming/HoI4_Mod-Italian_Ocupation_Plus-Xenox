# Italian Occupation Plus — v0.0.37 (Yugoslavia + Albania + Bulgaria + Greece + Turkey + North Africa + Egypt + Morocco + Spain + Portugal + Occitania + Levant + Iraq + Arabia + Armenia + Iran + Georgia)

A Hearts of Iron 4 mod that gives **Italy** its own Reichskommissariat-style occupation system, inspired by *Reichskommissariats Plus*.

As Italy, occupy Yugoslav land → open the decisions tab **"Italian Occupation"** → found military occupation governments as puppets → distribute individual states to them through events where **you pick the recipient (must border the state)**.

> **Version scheme:** `0.0.x` — future updates increment only the last number (0.0.4, 0.0.5, …).

## What's in v0.0.37 (Roman law discipline)

Every occupation government is administered from Rome, so its three law slots are no longer its own business:

- **New national spirit `iop_locked_laws` — "Rome Sets the Laws"** on **all 20** occupation governments (ICR, ISE, IMT, IAL, IBL, IGR, ITR, INA, IEG, ISP, IPG, IOC, ILV, IIQ, IAR, IAM, IIR, IMR, IOM, IGE). It is granted in every `history/countries/*.txt`, so it is present no matter how the country comes into existence (founding decision, peace conference, console `release`), and it is re-applied defensively by the founding scripted effect. `removal_cost = -1`, so the player cannot strip it off.
- **Conscription, trade and economy law are closed.** HOI4 has no engine flag that greys out a law slot from a national spirit — a real grey-out would mean overriding vanilla `common/ideas/_manpower.txt`, `_economic.txt` and `_political.txt`, which this mod deliberately never does (it would pin the mod to one vanilla version). The lock is therefore two layers deep:
  1. the spirit sets `mobilization_laws_cost_factor`, `trade_laws_cost_factor` and `economy_cost_factor` to `+1000%`, so a 150 PP law change costs 1650 PP;
  2. a **weekly watchdog** (`on_weekly` in `common/on_actions/iop_on_actions.txt` → `iop_enforce_roman_laws`) puts the mandated laws straight back, so even a console/decision-driven change (e.g. vanilla "demobilise the economy") cannot be kept.
- **New founding decree event `iop_laws.1` — "A Decree from Rome"** (`events/IOP_laws.txt`). It fires **for the puppet itself, never for Italy**, 6–12 hours after that puppet is founded (queued by the `iop_on_puppet_founded` scripted effect, which every one of the 20 `release_puppet` sites now calls). Its single option sets **Conscription law → Service by Requirement** (`service_by_requirement`) and **Economy law → Total Mobilization** (`tot_economic_mobilisation`), and records whichever **trade law** the government holds at that moment as the fixed one.
- A **catch-all** in the same `on_weekly` hands the spirit and the decree to any occupation government that appeared outside the founding decisions, so nothing can slip through unregulated.
- **Fix:** `localisation/english/IOP_flavour_l_english.yml` was missing its UTF-8 BOM, so every string in it (the Occupation Directorate spirit and the flavour events) rendered as a raw key in-game. BOM added.
- **Repo housekeeping:** the source PNGs moved to `Additional_Data/Graphics/`, and `Additional_Data/Information_for_AI.md` documents the project for the next maintainer (human or AI). `python3 Additional_Data/tools/validate_iop.py` is the static check that runs over the shipped files (braces, loc BOM/keys/duplicates, event ids and references, idea sprites, tag coverage, founding hooks, version agreement).

## What's in v0.0.3

### 20 new puppet nations

| Tag | Full name | Capital | Initial states (state IDs) |
|-----|-----------|---------|----------------------------|
| **ICR** | Governo Militare di Occupazione della Croazia | Croatia (109, Zagreb) | Croatia (109), Bosnia (104), Herzegovina (804) — Dalmatia (103) via its own fate decision |
| **ISE** | Governo Militare di Occupazione della Serbia | Serbia (107, Belgrade) | Serbia (107), Morava (108) |
| **IMT** | Governatorato del Montenegro | Montenegro (105) | Montenegro (105) |
| **IAL** | Governo Militare di Occupazione dell'Albania | Albania (44, Tirana) | Albania (44), Shkoder (934) |
| **IBL** | Governatorato di occupazione militare della Bulgaria | Sofia (48) | Sofia (48), Moesia (801), Plovdiv (212), Burgas (211) |
| **IGR** | Governatorato militare di occupazione della Grecia | Attica (47, Athens) | Attica (47), Peloponnese (186), Epirus (185), Aegean Islands (187) |
| **ITR** | Governo militare di occupazione della Turchia | Ankara (49) | Ankara (49), Izmit (347), Izmir (339), Antalya (342), Afyon (343), Kastamonu (356), Samsun (355), Amasya (798), Sivas (349), Tunceli (353), Hakkari (352), Diyarbakir (350), Malatya (344), Kayseri (348), Mersin (345), Konya (346) |
| **INA** | Governatorato di occupazione militare del Nord Africa | Tripoli (448) | Tripoli (448), Tripolitania (661), El Agheila (449), Sirte (662), Benghasi (450), Derna (451), Cyrenaica (663), Libyan Desert (273) |
| **IEG** | Governo militare di occupazione dell'Egitto | Cairo (907) | Matrouh (452), Alexandria (447), Cairo (907), Western Desert (552), Aswan (456), Eastern Desert (457) |
| **ISP** | Governatorato militare di occupazione della Spagna | Madrid (41) | Galicia (171), Asturias (790), León (174), País Vasco (792), Navarra (172), Western Aragón (166), Eastern Aragón (794), Cataluña (165), Valladolid (791), Burgos (176), Salamanca (788), Madrid (41), Guadalajara (793), Valencia (167), Extremadura (170), Ciudad Real (175), Murcia (168), Córdoba (789), Sevilla (169), Granada (173) |
| **IPG** | Governo militare di occupazione del Portogallo | Lisbon (112) | Porto (180), Guarda (181), Lisbon (112), Santarém (795), Beja (179) |
| **IOC** | Governo militare di occupazione dell'Occitania | Aquitaine (19, Bordeaux) | Centre-Sud (33), Limousin (25), Aquitaine (19), Pyrénées-Atlantiques (806), Midi-Pyrénées (31), Auvergne (26), Rhône (20), Languedoc (22) |
| **ILV** | Governatorato di occupazione militare del Levante | Palestine (454) | Palestine (454), Jordan (455), Lebanon (553), Damascus (554), Aleppo (677), Deir-az-Zur (680) |
| **IIQ** | Governatorato di occupazione militare dell'Irak | Baghdad (291) | Mosul (676), Al Anbar (1010), Baghdad (291), Al Hajara (675), Al Basrah (1011) |
| **IAR** | Governatorato di occupazione militare dell'Arabia | Nejd (292, Riyadh) | Jawf (854), Tabuk (855), Al-Qassim (857), Madinah (679), Dammam (859), Nejd (292), Asir-Makkah (856), Rub al Khali (678), Najiran (858) |
| **IAM** | Governatorato di occupazione militare dell'Armenia | Armenia (230, Yerevan) | Armenia (230) |
| **IIR** | Governatorato di occupazione militare dell'Iran | Tehran (266) | West Azerbaijan (419), East Azerbaijan (1000), Gilan (420), Kurdistan (1001), Ilam (421), Hamadan (417), Khuzestan (413), Tehran (266), North Khorasan (1004), Khorasan (416), Semnan (418), Isfahan (411), Yazd (1002), South Khorasan (1003), Fars (412), Kerman (414), Sistan (410) |
| **IMR** | Governo Militare di Occupazione del Marocco | Casablanca (461) | Casablanca (461), Marrakech (462) — expands into Spanish Africa (290), Sidi Ifni (783), Rio de Oro (699) |
| **IGE** | Governo militare di occupazione della Georgia | Georgia (231, Tbilisi) | Georgia (231), Abkhazia (826) — expands into Armenia (230) and Azerbaijan (229) via the Transcaucasus unification decision |

> **Why ISE and not ISR?** `ISR` is already used by vanilla HOI4 for **Israel** (releasable by the UK). Using it would overwrite Israel. `ISE` (Italian SErbia) keeps the `Ixx` pattern and is free in vanilla.

Puppet leaders (historical placeholders, all fascist):
- **ICR** — Giuseppe Bastianini (Governor of Croatia, custom portrait included)
- **ISE** — Tito Agosti (Governor of Serbia, custom portrait included)
- **IMT** — Alessandro Pirzio Biroli (Governor of Montenegro, custom portrait included)
- **IAL** — Alfredo Guzzoni (Governor of Albania, custom portrait included)
- **IBL** — Attilio Biseo (Governor of Bulgaria, custom portrait included)
- **IGR** — Pietro Parini (Governor of Greece, custom portrait included)
- **ITR** — Rodolfo Graziani (Governor of Turkey, custom portrait included)
- **INA** — Ettore Bastico (Governor of North Africa, custom portrait included)
- **IEG** — Italo Gariboldi (Governor of Egypt, custom portrait included)
- **ISP** — Mario Roatta (Governor of Spain, custom portrait included)
- **IPG** — António de Oliveira Salazar (Portuguese authoritarian ruler/client, vanilla CL-U portrait)
- **IOC** — Enea Navarini (Governor of Occitania, custom portrait included)
- **ILV** — Amin al-Husseini (Palestinian Arab-nationalist client, vanilla CL-U portrait)
- **IIQ** — Rashid Ali al-Gaylani (Iraqi Arab-nationalist client-ruler, vanilla CL-U portrait)
- **IAR** — Gianrico Tedeschi (Governor of Arabia, custom portrait included)
- **IAM** — Drastamat "Dro" Kanayan (Governor of Armenia, custom portrait included)
- **IIR** — Reza Shah Pahlavi (Iranian sovereign/client, vanilla CL-U portrait)
- **IMR** — Shakib Arslan, "Amir al-Bayan" (Governor of Morocco, custom portrait included)
- **IGE** — Jakov Dzhugashvili (Governor of Georgia, custom portrait included; becomes Viceroy of the Transcaucasus after unification)
- **IOM** — Said bin Taimur (Sultan of Muscat and Oman — created from the Oman fate event, no custom portrait)

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

### 76 decisions — all free, all with map highlighting

Own tab: **"Italian Occupation"**. Hovering any decision outlines the state(s) it needs/changes.

**Founding (one per puppet, repeatable if the puppet is destroyed):**
- Establish Military Occupation of Croatia — requires control of **Croatia (109)**, highlights all 4 initial states
- Establish Military Occupation of Serbia — requires control of **Serbia (107)**, highlights both initial states
- Establish Military Occupation of Albania — requires control of **Albania (44)**, highlights Albania and Shkoder (Northern Epirus stays Italian until you assign it via its fate decision)
- Establish Military Occupation of Bulgaria — requires control of **Sofia (48)**, highlights all 4 initial states
- Establish Military Occupation of Greece — requires control of **Attica (47, Athens)**, highlights all 4 initial states (Central Macedonia, Thrace, Crete and Dodecanese stay Italian until you assign them via their fate decisions)
- Establish Military Occupation of Turkey — requires control of **Ankara (49)**, highlights all 18 initial Anatolian states (Edirne, Bursa and Istanbul stay Italian until you assign them via their fate decisions; Alexandretta has no fate decision)
- Establish Military Occupation of North Africa — requires control of **Tripoli (448)** (starts Italian, so INA can be founded on day one), highlights all 8 Libyan states
- Establish Military Occupation of Egypt — requires control of **Cairo (907)**, highlights all 6 initial states (Suez stays Italian until the Fall of Suez Canal; Sinai comes in a later update)

Each founding decision only **appears** once **Italy or its subjects (the occupation governments) control at least half of that puppet's initial states** (rounded up — e.g. 2 of 3 for Croatia, 10 of 20 for Spain), and still needs the **capital state** controlled by Italy or a subject to click. Any other initial states controlled by Italy or its subjects transfer automatically — so territory under puppet occupation counts toward founding, and occupied states are pooled into the new occupation government.

**Fall of Montenegro (special):** Montenegro is no longer founded directly. The **"Fall of Montenegro"** decision (requires control of **105** plus at least one of ICR / ISE / IAL already existing) fires an event with 4 options: **Integrate into Croatia / Serbia / Albania** (each must border Montenegro; transfers + cores the state) or **Create a new occupational government** (releases IMT as before).

**Distribution (repeatable):** one "Determine Fate of …" decision per state. Each fires an **event where you choose the recipient — but only occupation governments that BORDER the state are eligible.** This forces natural, contiguous expansion (e.g. assign Macedonia before Debar).

| State ID | State | Recipients |
|----------|-------|-----------|
| 102 | North Slovenia | bordering puppets (with cores) + Germany/Austria (plain handover, no cores; decision needs ICR/GER/AUS border) |
| 853 | Ljubljana | Croatia (needs ICR to own a neighbor) OR integrate into Italy |
| 103 | Dalmatia | Croatia (needs ICR to own a neighbor) OR integrate into Italy |
| 109 | Croatia | bordering puppets only |
| 104 | Bosnia | bordering puppets only |
| 804 | Herzegovina | bordering puppets only |
| 105 | Montenegro | bordering puppets only |
| 107 | Serbia | bordering puppets only |
| 45 | Vojvodina (Backa) | ICR or ISE only (must border) |
| 764 | West Banat | ICR or ISE only (must border) |
| 802 | Kosovo | bordering puppets only |
| 803 | Southern Serbia | any bordering puppet (decision needs ISE or IBL border) |
| 106 | Macedonia | any bordering puppet (decision needs ISE or IBL border) |
| 970 | Debar | bordering puppets only |
| 44 | Albania (capital — reassignable only after IAL exists) | bordering puppets only |
| 805 | Northern Epirus | IAL or IGR only (must border) |
| **163** | **Zara (special)** | **Decision needs ICR border; then Croatia OR annex to Italy** |
| **852** | **Istria (special)** | **Decision needs ICR border; then Croatia OR annex to Italy** |
| 731 | Central Macedonia | IGR or IBL only (must border) |
| 184 | Thrace | IGR or IBL only (must border) |
| **182** | **Crete (special, island — no border check)** | **Needs IGR to exist; then Greece OR annex to Italy** |
| **164** | **Dodecanese (special, island — no border check)** | **Needs IGR or ITR to exist; then Greece, Turkey OR annex to Italy** |
| **341** | **Edirne (special)** | **Needs IBL or IGR to border; then Bulgaria, Greece OR annex to Italy** |
| **340** | **Bursa (special)** | **Needs ITR or IGR border; then Turkey, Greece OR annex to Italy** |
| **797** | **Istanbul (special)** | **Needs ITR or IGR border; then Turkey, Greece OR annex to Italy — or restore Constantinople to Greece itself (GRE existence check, plain handover)** |
| **347** | **Izmit (special)** | **Needs ITR or IGR border; then Turkey, Greece OR annex to Italy** |
| 339 | Izmir | Turkey or Greece (must border) OR annex to Italy |
| 342 | Antalya | annex to Italy OR Turkey/Greece (must border) |
| 665 + 458 | Tunisia: Gabès + Tunisia (grouped) | INA only — direct transfer, no event |
| 459 + 460 + 513 + 514 | Algeria: Algiers + Constantine + Tlemcen + Algerian Desert (grouped) | INA only — direct transfer, no event |
| 461 + 462 | Morocco: Casablanca + Marrakech | **Establish Military Occupation of Morocco (IMR)** — or the old INA-only direct transfer |
| **290** | **Spanish Africa (special)** | **Needs INA or IMR to exist; then North Africa, Morocco OR annex to Italy** |
| **699** | **Rio de Oro (special)** | **Needs INA or IMR to exist; then North Africa, Morocco OR annex to Italy** |
| **783** | **Sidi Ifni (special)** | **Needs INA to exist; then North Africa OR integrate into Italy** |
| 767 + 551 + 883 + 886 + 549 + 887 + 884 + 885 | Sudan (grouped) | IEG only — direct transfer, no event |
| **446** | **Suez / Fall of Suez Canal (special)** | **Needs IEG to control a neighboring state; then Egypt OR integrate into Italy** |
| **118** | **Gibraltar / Fall of Gibraltar (special)** | **Needs ISP to own a neighboring state; then Spain OR integrate into Italy** |
| **177** | **Islas Baleares (special, island)** | **Needs ISP to exist; then Spain OR integrate into Italy** |
| **178** | **Islas Canarias (special, island)** | **Needs ISP to exist; then Spain OR integrate into Italy** |
| **698 + 697** | **Azores + Madeira (special, islands, grouped)** | **Needs IPG or ISP to exist; then Portugal, Spain OR integrate into Italy** |
| **32 + 21** | **Provence: Alpes + Bouches-du-Rhône (special, grouped)** | **Needs IOC to own a bordering state; then Occitania OR integrate into Italy** |
| **735 + 851** | **Savoy + Var (special, grouped)** | **Needs IOC to own a bordering state; then Occitania OR integrate into Italy** |
| **1** | **Corsica (special, island)** | **Needs IOC to exist; then Occitania OR integrate into Italy** |
| **799** | **Hatay (special)** | **Turkey OR Levant — each must own a bordering state; no Italian option** |
| **453** | **Sinai (special)** | **Levant OR Egypt (each must own a bordering state) OR integrate into Italy** |
| **183** | **Cyprus (special, island)** | **Turkey, Levant OR Greece (exist) OR integrate into Italy** |
| **656** | **Kuwait (special)** | **Iraq OR Arabia (each must own a bordering state) OR integrate into Italy** |
| 293 + 659 + 992 | Yemen: North Yemen + South Yemen + Aden (grouped) | IAR only — direct transfer, no event |
| **1016 + 1015 + 294** | **Oman: Dhofar + Oman + Muscat (grouped, special)** | **IAR, OR restore the Sultanate of Oman (IOM — separate Military Occupation under Sultan Said bin Taimur); afterwards cede further coast to IOM** |
| **658** | **Abu Dhabi (special)** | **Arabia (IAR) OR Sultanate of Oman (IOM) OR integrate into Italy** |
| 765 | Qatar | IAR only — direct transfer, no event |
| **77** | **Dobrudja (special)** | **Needs IBL to own a bordering state; then Bulgaria OR integrate into Italy** |
| **971** | **Northern Dobruja (special)** | **Needs IBL to own a bordering state; then Bulgaria OR integrate into Italy** |
| **354 + 800** | **Trabzon + Van (special, grouped)** | **Turkey OR Armenia — each must own a bordering state; no Italian option** |
| 23 | Poitou | IOC only — direct transfer, no event (owned/controlled by Italy or a subject; one-shot — flag-guarded so it can never reappear) |
| 19 + 806 | Aquitaine + Pyrénées-Atlantiques (grouped) | IOC only — direct transfer, no event |
| — | **Unite the Iberian Peninsula** | **Visible once IPG founded and ISP exists; ISP annexes IPG, gains cores on all Portuguese states and becomes the Governatorato di occupazione militare della penisola Iberica (cosmetic tag `ISP_iberia`); afterwards all "cede to Spain" options read "cede to Iberia"** |

Only **Dalmatia, Ljubljana, Zara, Istria, Crete, Dodecanese, Edirne, Bursa, Istanbul, Sidi Ifni, Suez, Gibraltar, the Balearics, the Canaries, Azores/Madeira, Provence, Savoy/Var, Corsica, Sinai, Cyprus, Kuwait and Dobrudja** keep an annex-to-Italy option (core gain is intentionally not shown) — all other transfers must go to a bordering puppet, except North Slovenia which can also be handed to a bordering Germany or Austria (no cores), and the North African and Sudanese group transfers which go straight to INA/IEG (existence check only). Bačka (45) and West Banat (764) can only go to Croatia or Serbia; Central Macedonia (731) and Thrace (184) can only go to Greece or Bulgaria; Northern Epirus (805) can only go to Albania or Greece; Edirne (341) can only go to Bulgaria or Greece (or Italy). Zara and Istria decisions need Croatia to border the state (or the Dalmatia decision to have been taken); Bursa and Istanbul need Turkey to border; Edirne needs Bulgaria or Greece to border; Suez needs Egypt to control a neighboring state; Gibraltar needs Spain to own a neighboring state; the Balearics (island) only need ISP to exist. Crete and Dodecanese are islands, so no border check is possible — Crete needs IGR to exist, Dodecanese needs IGR or ITR to exist (Dodecanese starts Italian, so its decision appears right after founding either). North Slovenia (102) needs Croatia, Germany or Austria to border — occupation governments receive it with cores, Germany/Austria as a plain handover. Dalmatia (103) and Ljubljana (853) need Croatia to own a bordering state and go to Croatia or Italy only. Southern Serbia (803) and Macedonia (106) decisions need Serbia or Bulgaria to border, but any bordering puppet (including Bulgaria) can receive. The Tunisian, Algerian, Moroccan and Spanish-African groups transfer directly to INA with no event and no border checks — and none of those states has any other fate decision. The Sudan group works the same for IEG. Sinai (453) goes to the Levant, Egypt or Italy; Hatay (799) to Turkey or the Levant only. A distribution decision stays unavailable (greyed) until a valid recipient exists, so the event can never fire without one. Capital states (Croatia 109, Serbia 107, Montenegro 105, Albania 44) have no redistribution decision at all while their puppet can still be created — found (or settle) the puppet first.

## What's in v0.0.29 (flavour)

- **The "Military Government" spirit no longer fakes "cannot capitulate".** The undocumented `capitulate_factor` key was replaced by the real `surrender_limit = 1.0` modifier (+100% surrender limit), so a puppet now genuinely holds out until it loses essentially every victory point. `−25% PP` and `−50% recruitable population` are unchanged.
- **Six regional occupation spirits**, one per theatre, added to each puppet at founding alongside "Military Government": `iop_flavour_balkans` (ICR/ISE/IMT/IAL), `iop_flavour_aegean` (IGR/IBL), `iop_flavour_anatolia` (ITR/IAM/IIR), `iop_flavour_north_africa` (INA/IEG), `iop_flavour_iberia` (ISP/IPG/IOC), `iop_flavour_levant` (ILV/IIQ/IAR). Each is a deliberately **mixed** trade-off (e.g. Anatolia: +15% resources / +20% oil, but +10% attrition and +10% supply use).
- **`iop_occupation_directorate` on Italy**: added the first time you found any puppet. `−25%` required garrisons, +15% compliance growth, −10% resistance growth in your occupied states, subjects gain autonomy 50% slower, at the cost of −10% political power.
- **17 governor traits**: every `create_country_leader` now carries a historically-flavoured trait (Bastianini "Diplomat Governor", Graziani "Colonial Repressor", Kanayan "Mountain Defender", …) defined in `common/country_leader/iop_traits.txt`.
- **10 flavour events** (`events/IOP_flavour.txt`): partisan ambushes, requisition crises, oil concessions, the governors quarrel, etc. They fire for Italy with `mean_time_to_happen` and a 300-day shared cooldown, and hand out timed `iop_spirit_*` ideas (180–240 days).
- **7 new idea icons**: `gfx/interface/ideas/*.dds` (DXT1, 60×68) generated by `tools/gen_flavour_icons.py` and registered in `interface/iop_flavour.gfx`.

All new modifiers were checked against the HOI4 wiki modifier list; all new localisation lives in `IOP_flavour_l_english.yml` (UTF-8 BOM).

## What's in v0.0.30 (Anatolian fates + Roman Empire)

- **New Anatolian fate decisions**: Izmit (347) and Izmir (339) leave Turkey's initial set and get "Determine Fate" decisions (Greece / Turkey / annex Italy). Bursa (340) and Istanbul/Constantinople (797) gain a **Greece** option alongside Turkey/annex. **Antalya (342)** gets its own decision to annex it to Italy (or cede to Turkey/Greece).
- **Dobruja (77)**: the existing "Fate of Dobrudja" decision gives it to Bulgaria (IBL) or integrates it into Italy - confirmed working.
- **Restore the Roman Empire**: once every listed Mediterranean coastal state is owned by Italy or an Italian subject, a one-time decision appears. Completing it renames Italy to **Imperivm Romanvm** (cosmetic tag `ITA_roman` with imperial flags and map color `#A84232`), changes the names of all occupation governments (and vanilla Italian East Africa **AOI** $\rightarrow$ **Aethiopia**) to their historical Roman province counterparts with U replaced with V (e.g. `Illyricvm`, `Aegyptvs`, `Lvsitania`, `Hispania`, `Mavretania Tingitana`, `Africa Proconsvlaris`, `Aethiopia`, `Moesia Svperior`, `Epirvs Nova`, `Gallia Narbonensis`, `Asia Minor`, `Syria Palaestina`, `Mesopotamia`, `Arabia Felix`, `Armenia Maior`, `Parthia`, `Thracia`, `Achaea`, `Praevalitana`, `Omana`), sets their map color to a distinct darker red (`#702318`), and switches every occupation government to the **Province** autonomy level (`autonomy_province`, min_freedom 0.05): full industry/manpower/trade to Rome plus construction & stability bonuses, at the cost of −35% PP, −60% recruitable population and −10% research.
- **Dynamic Post-Restoration Integration**: any puppet released after the Roman Empire is proclaimed automatically receives the Province autonomy level, darker red color, and Roman province cosmetic tag.
- All new modifiers verified against the HOI4 wiki modifier list; new localisation in `IOP_roman_l_english.yml` (UTF-8 BOM).

## What's in v0.0.34 (zone bonuses replace puppet spirits + Oman rework)

- **Puppet national spirits removed.** With Military Occupation funnelling all industry, manpower and trade to Italy, puppet-side modifiers were dead weight: `iop_military_government`, all six `iop_flavour_*` regionals and the four puppet-side timed spirits are gone (governor traits and the shared focus tree stay — the tree is now gated on the `iop_puppet` country flag instead).
- **Occupation Zone bonuses on Italy.** Each founding now grants the **Occupation Directorate** hub spirit (slimmed to −10% garrisons, +5% compliance growth, −25% subject autonomy gain) **plus that zone's own stacking bonus** — 19 dynamic modifiers, each different: Croatia cuts attrition, Serbia cuts garrisons, Iraq/Iran/Arabia pump oil, Portugal trims consumer goods, Oman tributes political power, and so on (see `common/dynamic_modifiers/iop_zones.txt`). One-shot per zone: re-founding a destroyed puppet grants nothing new. Montenegro and Oman foundings now grant the Directorate too (they previously didn't).
- **Flavour events retargeted.** The 10 events still fire for Italy, but their options now pay out Italian bonuses (stability, war support, PP, army XP, manpower) instead of puppet spirits.
- **Oman rework.** The Sultanate's tag changed **IMO → IOM** (IMO ignored the per-file map colour and showed tan in-game; IOM renders occupation green like the rest), and Sultan Said bin Taimur now uses the **vanilla HOI4 leader portrait** (`gfx/leaders/IOM/`).

## What's in v0.0.31 (puppet national focuses)

- Every occupation government now gets a **small shared focus tree** (`common/national_focus/iop_puppet.txt`, id `iop_puppet_focus`). It applies to any country carrying the `iop_puppet` country flag, so all current and future puppets pick it up automatically.
- 10 focuses, 5 rows: *Consolidate the Occupation* → *Local Police / Census* → *Carabinieri Reforms / Repair the Railways* → *Garrison Drills / Labour Levies / Resource Extraction* → capstones *The Model Province / Tribute to Rome*.
- All completion rewards are one-off, documented effects (PP, stability, war support, army XP, manpower, instant construction) and use vanilla `GFX_goal_generic_*` icons - no new art, no new spirits. Cost 5 each; localisation in `IOP_focus_l_english.yml` (UTF-8 BOM).

## Installation

1. Copy the `italian_occupation_plus` folder **and** the `italian_occupation_plus.mod` file into your HOI4 mod folder:
   - **Windows:** `Documents\Paradox Interactive\Hearts of Iron IV\mod\`
   - **Linux:** `~/.local/share/Paradox Interactive/Hearts of Iron IV/mod/`
2. Open the Paradox launcher → *Mods* → enable **Italian Occupation Plus**.
3. Launch the game. Supported version: `1.19.2` (if your game is newer and the launcher shows it as outdated, you can still try enabling it — the mod uses stable scripting features).

## How to play / test

1. Start as **Italy**, justify on Yugoslavia (or wait for the historical war).
2. Capitulate Yugoslavia and make sure **you** control the land (not Germany — decisions check `controls_state` for Italy).
3. Open the **Decisions tab** → category **"Italian Occupation"**.
4. Click **Establish Military Occupation of Croatia / Serbia / Albania / Bulgaria / Greece / Turkey / North Africa / Egypt** (free), and use **Fall of Montenegro** for Montenegro. Puppets appear as your subjects with the **Military Occupation** autonomy level.
5. Use the **"Determine Fate of …"** decisions (free) — an event pops up letting you pick which **bordering** puppet gets the state. Assign in contiguous order (e.g. Macedonia before Debar, Central Macedonia before Thrace, Thrace or Plovdiv before Edirne). The North African **"Transfer …"** decisions instead hand whole regions straight to INA with no event, and "Transfer Sudan to Egypt" does the same for IEG.
6. For Zara/Istria, the event offers **cede to Croatia** (must border) vs **annex to Italy** (adds an Italian core). For Crete, the event offers **cede to Greece** (needs IGR to exist, no border check — islands) vs **annex to Italy**; Dodecanese additionally offers **cede to Turkey** (needs IGR or ITR). Bursa/Istanbul work the same with Turkey (must border), Edirne offers Bulgaria, Greece or annexation, Sidi Ifni offers North Africa or integration into Italy proper, and the Fall of Suez Canal offers Egypt or integration.

**Quick console test:** `tag ITA`, `annex YUG`, then open decisions. (Annexing via console gives you control of everything, so all founding decisions light up.)

## How it works (for modding)

- **No `history/states` overrides.** Cores are added at release time via state-scope `add_core_of`, so the mod is compatible with map mods and future vanilla state changes (as long as IDs stay the same). For the same reason the mod **never overrides vanilla `common/ideas/_manpower.txt` / `_economic.txt` / `_political.txt`** — which is why the law lock is implemented with cost modifiers + a watchdog instead of greying the law slots out (see v0.0.37).
- Founding effect: `add_core_of` → `release_puppet = TAG` → `TAG = { iop_on_puppet_founded = yes }` (law-lock spirit + founding decree event for the puppet) → `set_autonomy` (Military Occupation) → `transfer_state` for each controlled initial state (guarded by `if` + `iop_med_controlled`, so it never steals land from Germany).
- Distribution: decision (`available` requires ≥1 bordering puppet) → `country_event` → event option does `add_core_of` + `transfer_state` to the chosen puppet. Option triggers use `any_neighbor_state = { is_owned_by = TAG }`.
- AI never touches the decisions (`ai_will_do = { factor = 0 }`), so Italy AI won't break itself. The founding decree event *is* answered by the AI (`ai_chance = { factor = 100 }`), because occupation governments are AI-run by default.
- Localisation files are UTF-8 **with BOM** (required by HOI4).
- Flags are placeholders: local colors + Italian tricolor canton, in all 3 sizes × 5 ideologies.
- **Static check:** `python3 Additional_Data/tools/validate_iop.py` (from the repository root) parses every shipped file — brace balance, loc BOM/keys/duplicates, event ids and every `country_event` reference, idea loc keys and picture sprites, tag coverage (history file + `iop_locked_laws`), and that each `release_puppet` is followed by its founding hook. Exit code 0 = clean.

## File map

```
italian_occupation_plus/
├── descriptor.mod                             # version must match ../italian_occupation_plus.mod
├── README.md
├── common/
│   ├── autonomous_states/
│   │   ├── iop_autonomy.txt                   # Military Occupation level (autonomy_military_occupation)
│   │   └── iop_province.txt                   # Province level (after the Roman Empire is restored)
│   ├── countries/Italy_*.txt                  # one per tag: graphical culture + rgb map colour
│   ├── country_tags/iop_tags.txt              # the 20 tags (ISE not ISR, IOM not IMO, IGE not GEO)
│   ├── country_leader/iop_traits.txt          # governor traits
│   ├── decisions/categories/iop_categories.txt # "Italian Occupation" tab (categories/ subfolder is mandatory!)
│   ├── decisions/IOP_*.txt                    # 91 decisions: foundings, "Determine Fate of …", Roman Empire
│   ├── dynamic_modifiers/iop_zones.txt        # 20 per-zone bonuses granted to Italy
│   ├── ideas/IOP_ideas.txt                    # Italy-side spirits + iop_locked_laws (puppet law lock)
│   ├── national_focus/iop_puppet.txt          # shared focus tree for every occupation government
│   ├── on_actions/iop_on_actions.txt          # Roman-integration pulse + weekly law watchdog (v0.0.37)
│   ├── scripted_effects/iop_zones.txt         # iop_grant_zone_* (one-shot per zone)
│   ├── scripted_effects/iop_laws.txt          # iop_on_puppet_founded / iop_lock_current_trade_law / iop_enforce_roman_laws
│   ├── scripted_localisation/iop_zones.txt    # zone list inside the Directorate tooltip
│   ├── scripted_localisation/iop_decision_names.txt
│   └── scripted_triggers/iop_triggers.txt     # iop_med_owned / iop_med_controlled
├── events/IOP_*.txt                           # 61 events (fate pickers, flavour, Roman Empire, iop_laws.1)
├── gfx/
│   ├── flags/ (+ medium/, small/)             # 114 .tga per size: base + 4 ideologies per tag/cosmetic tag
│   ├── leaders/<TAG>/<TAG>_Name.dds           # custom portraits - the tag subfolder is REQUIRED
│   └── interface/{autonomy,decision_category,ideas}/   # .dds icons
├── history/
│   ├── countries/*.txt                        # 20 files: capital, leaders, tech, iop_puppet flag, iop_locked_laws
│   └── units/IOP_empty.txt                    # empty puppet OOB
├── interface/iop_{autonomy,decisions,directorate}.gfx  # sprite definitions for the .dds above
└── localisation/english/IOP_*_l_english.yml   # 9 files, ~1130 keys - UTF-8 WITH BOM (required!)
```

Everything outside `italian_occupation_plus/` in this repository — the `Additional_Data/` folder with the source PNGs (`Additional_Data/Graphics/`), `Additional_Data/Information_for_AI.md` and `Additional_Data/tools/validate_iop.py` — is **development material, not part of the mod**. Never copy it into the game's mod folder.

## Extending (a new region)

The pattern per new region is:

1. **Tag**: add `IXX = "countries/Italy_<Region>.txt"` to `common/country_tags/iop_tags.txt`, write `common/countries/Italy_<Region>.txt` (colour + gfx culture) and `history/countries/IXX - <full name>.txt` (capital, leaders for all 4 ideologies, tech, `set_country_flag = iop_puppet`, `add_ideas = { iop_locked_laws }`).
2. **Flags**: `gfx/flags/IXX*.tga` in all three sizes × 5 variants (base + 4 ideologies).
3. **Founding decision** in `common/decisions/IOP_<region>.txt` (copy an `iop_establish_*` block): highlight the states, `count_triggers` for "at least half controlled", capital check in `available`, then `add_core_of` → `release_puppet` → **`IXX = { iop_on_puppet_founded = yes }`** → `set_autonomy` → `transfer_state` per state (each guarded by `iop_med_controlled`).
4. **Zone bonus**: add `iop_zone_<region>` to `common/dynamic_modifiers/iop_zones.txt`, a matching `iop_grant_zone_<region>` scripted effect, and its scripted-localisation line in the Directorate tooltip.
5. **Distribution decisions + events** per state (copy an `iop_decide_*` block and its event, change the state ID — the border logic works automatically).
6. **Localisation**: add country/decision/event keys to the `.yml` files (keep the BOM!).
7. **Check it**: `python3 Additional_Data/tools/validate_iop.py` fails if the new tag has no `iop_locked_laws` spirit, if a `release_puppet` is missing its `iop_on_puppet_founded` hook, if an event fires an id that does not exist, or if any loc key is missing.

## IMPORTANT: always clean-reinstall

HOI4 does not clean up removed/renamed mod files on update. If puppets show **wrong colors, wrong leaders, or old decisions**, you are almost certainly running **stale files mixed with the new version**. Fix: **delete** `Documents\Paradox Interactive\Hearts of Iron IV\mod\italian_occupation_plus` **and** `italian_occupation_plus.mod` completely, then extract the new zip. Never extract over the old folder.

## Troubleshooting

- **Decisions don't show:** you must be playing the country with `original_tag = ITA`. Founding needs control of the capital state (109 / 107 / 105). Distribution needs ≥1 puppet to exist AND at least one puppet bordering the state.
- **Mod shows as outdated:** edit `supported_version` in both `.mod` files to match your game (e.g. `1.20.*`).
- **"Military Occupation" level missing/wrong:** check `error.log` for `autonomy_military_occupation` — most likely the `.gfx` sprite or `.dds` path. The icon falling back to `?` is cosmetic only.
- **Check errors:** after running the game, look at `Documents\Paradox Interactive\Hearts of Iron IV\logs\error.log` and search for `iop`.
- **Missing portraits:** if a leader shows a silhouette, the referenced vanilla portrait GFX name or portrait `.dds` path does not exist in your game version — replace `picture = ...` in the history file with another vanilla portrait. It never crashes, it's cosmetic.

## Changelog

- **0.0.37** — Roman law discipline: new `iop_locked_laws` national spirit ("Rome Sets the Laws") on all 20 occupation governments, closing their conscription, trade and economy law (+1000% law-change cost, `removal_cost = -1`, granted from every history file); new founding decree event `iop_laws.1` fired **for the puppet itself** 6–12 h after its formation, setting Service by Requirement + Total Mobilization and fixing the trade law in force at that moment; weekly `on_weekly` watchdog (`iop_enforce_roman_laws`) restores the mandated laws so no change can be kept, plus a catch-all that regulates occupation governments created outside the founding decisions; `IOP_flavour_l_english.yml` regained its missing UTF-8 BOM; repository housekeeping (`Additional_Data/` for source art, `Information_for_AI.md`, `tools/validate_iop.py`).
- **0.0.36** — New 20th puppet: IGE (Governo militare di occupazione della Georgia, Tbilisi (231) + Abkhazia (826)), led by Jakov Dzhugashvili (portrait from the PNG added on main, converted to DXT5 DDS); Georgian Occupation Zone (Chiatura manganese: resource-shortage penalties reduced); generated Georgian five-cross flags with the Italian canton (base/medium/small × 5 variants) plus the same set for the new IGT_transcaucasus cosmetic tag; "Form the Transcaucasus Vicerealm" decision using the vanilla Transcaucasian formable condition (Armenia 230 + Georgia 231 + Abkhazia 826 + Azerbaijan 229 all controlled by Italy or its subjects, IGE founded): IGE annexes IAM if it exists and is our subject, absorbs the Caucasian states, takes the IGT_transcaucasus tag and Jakov re-emerges as Viceroy; Roman integration names the provinces Iberia (IGE) and Lazica et Iberia (IGT).
- **0.0.35** — Occupation Directorate is now a container spirit: its description dynamically lists exactly the zones founded (19 scripted-localisation tokens + `iop_zone_list_*` loc keys, empty fallback for the rest); zone modifiers themselves unchanged.
- **0.0.34** — Puppet national spirits removed (Military Government, six regionals, four puppet-side timed spirits — dead weight under 100% extraction); Italy's Occupation Directorate is now a slim hub (−10% garrisons, +5% compliance, −25% subject autonomy gain) with 19 different stacking per-zone bonuses (dynamic modifiers, one-shot per zone via `iop_grant_zone_*` scripted effects); flavour events pay Italian bonuses instead; shared focus tree and Roman-Empire filter re-gated on the `iop_puppet` flag; Oman retagged IMO → IOM (IMO ignored the map colour) with the vanilla Said bin Taimur portrait; regional flavour icons deleted.
- **0.0.33** — "Transfer Poitou to Occitania" can no longer reappear after being taken (one-shot `fire_only_once` + `iop_poitou_given` country-flag guard; its "owner is a subject" trigger stayed true after the transfer — every other decision was audited and already self-hides, terminal one-shots are flag-guarded). Founding checks reworked: the "at least half of the initial states" count and the capital check now accept states controlled by Italy **or its subjects**, and founding pulls in every initial state controlled by Italy or a subject (puppet occupation zones count and are pooled into the new government; scripted trigger `iop_med_controlled`). New "Transfer Aquitaine and the Pyrénées-Atlantiques to Occitania" direct decision (19 + 806 → IOC). Istanbul/Constantinople can now also be restored to Greece itself (GRE existence check, plain handover — no cores). Rebuilt the Bursa and Istanbul events: the v0.0.32 nested-option repair had mis-fired and shipped malformed blocks (now rebuilt cleanly and covered by a parser-based validator).
- **0.0.32** — Greece can now receive Constantinople (Istanbul), Bursa, Cyprus and Izmit: their fate events/decisions gained Greek occupation-government options (and the malformed nested-option blocks in the Bursa and Istanbul events were repaired). New 18th puppet: IMR (Governo Militare di Occupazione del Marocco, Casablanca + Marrakech, Shakib Arslan "Amir al-Bayan" with custom portrait, trait and tricolour-canton Moroccan flag) — its expansion events cover Spanish Africa, Sidi Ifni and Rio de Oro (INA, IMR or annex-to-Italy). "Transfer Oman to Arabia" became "Determine Fate of Oman": hand the coast to IAR, or restore the Sultanate of Oman (IOM) under Sultan Said bin Taimur as a separate Military Occupation (own tag, history, flag and sultan trait; repeatable to expand it). Spanish Africa lost its direct INA-only transfer and gained a full fate decision (INA / IMR / Italy). New "Determine Fate of Northern Dobruja" (971): Bulgarian occupation government (must border) or annex to Italy. Removed three leftover empty `if = {}` blocks from the Turkish founding decision.
- **0.0.31** — Small shared national focus tree for all occupation puppets (`iop_puppet_focus`), 10 focuses with one-off rewards.
- **0.0.30** — Anatolian fate decisions (Izmit/Izmir/Antalya, Greece options on Bursa/Istanbul), Dobruja-to-Bulgaria confirmed, and the Restore-the-Roman-Empire decision with the Imperium Romanum cosmetic tag and the Province autonomy level.
- **0.0.29** — Flavour update: `surrender_limit = 1.0` replaces the invalid `capitulate_factor` in the Military Government spirit; six regional occupation spirits; the Italy-side Occupation Directorate spirit; 17 governor traits; 10 flavour events; 7 new idea icons.
- **0.0.28** — Founding decisions ("Establish Military Occupation of …") now only **appear** once Italy controls **at least half of the required territory** (rounded up, via `count_triggers`: 2 of 3 Croatia, 1 of 2 Serbia/Albania, 2 of 4 Bulgaria/Greece, 8 of 16 Turkey, 4 of 8 North Africa/Occitania, 3 of 6 Egypt/Levant, 10 of 20 Spain, 3 of 5 Portugal/Iraq, 5 of 9 Arabia, 1 of 1 Armenia, 9 of 17 Iran). Clicking still needs the capital state. Montenegro unchanged (its Fall decision already needs control of 105).
- **0.0.27** — Fixed annex-to-Italy fate decisions reappearing after integration (e.g. Dalmatia): every decision with an integrate option now hides once the state is an Italian core (`is_core_of = ITA` check in `visible`; grouped Provence, Savoy/Var and Azores/Madeira decisions stay visible until all their states are decided). Zara, Istria and Dodecanese start as Italian cores, so they use a decided-flag instead (`iop_zara_decided`, `iop_istria_decided`, `iop_dodecanese_decided`) — a core check there would have hidden them from the start and made ceding them to a puppet impossible.
- **0.0.26** — Every occupation government now starts with the **Military Government** national spirit: −100% capitulation factor (cannot capitulate), −25% political power, −50% recruitable population factor.
- **0.0.25** — Two new puppets: IAM (Governatorato di occupazione militare dell'Armenia, Yerevan, Drastamat "Dro" Kanayan) and IIR (Governatorato di occupazione militare dell'Iran, Tehran + 16 states, Giuseppe Pièche); Turkey no longer spawns with Trabzon/Van — new "Fate of Trabzon and Van" (Turkey or Armenia, bordering owner); "Fate of Dobrudja" (Bulgaria or Italy); ITR crescent centred right of the canton; ILV and IIQ flags now carry a full-height Italian tricolour.
- **0.0.24** — Two new puppets: IIQ (Governatorato di occupazione militare dell'Irak, Baghdad + Mosul/Al Anbar/Al Hajara/Al Basrah, Nino Sozzani) and IAR (Governatorato di occupazione militare dell'Arabia, Riyadh/Nejd + 8 Saudi states, Gianrico Tedeschi); "Determine Fate of Kuwait" (Iraq, Arabia or Italy); grouped direct transfers to IAR: Yemen (North/South Yemen + Aden), Oman (Dhofar/Oman/Muscat), Abu Dhabi, Qatar.
- **0.0.23** — "Determine Fate of Cyprus" (island: Turkey, Levant or Italy — existence checks only).
- **0.0.22** — New 13th puppet: ILV (Governatorato di occupazione militare del Levante), founded from Palestine with Jordan/Lebanon/Damascus/Aleppo/Deir-az-Zur, led by Niccolò Nicchiarelli (Governor of Levant); "Determine Fate of Hatay" (Turkey or Levant, bordering owner); "Determine Fate of Sinai" (Levant, Egypt or Italy); Zara/Istria now also unlock once the Dalmatia decision has been taken.
- **0.0.21** — IOC capital moved to Aquitaine (Bordeaux); "Transfer Poitou to Occitania" direct decision (owned/controlled by Italy or a subject); Roatta's description becomes "Governor of Spain and Portugal" after Iberian unification; Croatia no longer spawns with Dalmatia — Dalmatia (103) and Ljubljana (853) are now Croatia-or-Italy fate events requiring ICR to own a neighboring state.
- **0.0.20** — New 12th puppet: IOC (Governo militare di occupazione dell'Occitania), founded from Midi-Pyrénées with Centre-Sud/Limousin/Aquitaine/Pyrénées-Atlantiques/Auvergne/Rhône/Languedoc, led by Enea Navarini (Governor of Occitania); "Determine Fate of Provence" (Alpes + Bouches-du-Rhône) and "Savoy and Var" events (Occitania — needs IOC to own a bordering state — or Italy); "Determine Fate of Corsica" (island: IOC only needs to exist); Unite Iberia highlight now covers the whole peninsula.
- **0.0.19** — New 11th puppet: IPG (Governo militare di occupazione del Portogallo), founded from Lisbon with Porto/Guarda/Santarém/Beja, led by Giuseppe Lombrassa (Governor of Portugal); "Determine Fate of the Canary Islands" (Spain or Italy) and "Determine Fate of Azores and Madeira" (Portugal, Spain or Italy — each option requires its recipient to exist); "Unite the Iberian Peninsula" decision (visible once IPG founded and ISP exists): ISP annexes IPG and is renamed Governatorato di occupazione militare della penisola Iberica (cosmetic tag ISP_iberia, own flag, ISP cores on Portugal, map highlight, Roatta becomes "Governor of Spain and Portugal"; "cede to Spain" event options become "cede to Iberia" after unification).
- **0.0.18** — New 10th puppet: ISP (Governatorato militare di occupazione della Spagna), founded from Madrid with 20 Spanish states, led by Mario Roatta (Governor of Spain); "Fall of Gibraltar" event (give to Spain — needs ISP to own a neighboring state — or integrate into Italy); "Determine Fate of the Balearic Islands" event (island: needs only ISP to exist); IEG flag remade as the green Egyptian crescent flag with the Italian canton.
- **0.0.17** — New 9th puppet: IEG (Governo militare di occupazione dell'Egitto), founded from Cairo with Matrouh/Alexandria/Western Desert/Aswan/Eastern Desert, led by Italo Gariboldi (Governor of Egypt, your portrait); new grouped direct transfer of all Sudan to IEG (North Darfur, Khartoum, Kassala, Blue Nile, Kurdufan, South Darfur, Upper Nile, Bahr al Ghazal — existence check only, no event); new "Fall of Suez Canal" event (give Suez to Egypt or integrate into Italy, needs IEG to control a neighboring state); Sinai left for a later update.
- **0.0.16** — New 8th puppet: INA (Governatorato di occupazione militare del Nord Africa), founded from Tripoli with all 8 Libyan states, led by Ettore Bastico (Governor of North Africa, your portrait); new grouped direct transfers to INA — Tunisia (Gabès + Tunisia), Algeria (Algiers + Constantine + Tlemcen + Algerian Desert), Morocco (Casablanca + Marrakech) and Spanish Africa (existence check only, no events, no other fate decisions for those states); new Sidi Ifni (783) event (cede to North Africa or integrate into Italy); Dodecanese can now also be ceded to Turkey (ITR).
- **0.0.15** — New 7th puppet: ITR (Governo militare di occupazione della Turchia), founded from Ankara with 18 Anatolian states, led by Rodolfo Graziani (Governor of Turkey, your portrait); new Edirne (341) fate event (Bulgaria or Greece, must border, or annex to Italy with core); new Zara-style Bursa (340) and Istanbul (797) events (cede to Turkey or annex); North Slovenia (102) can now also be handed to a bordering Germany or Austria (plain handover, no cores); restored Parini's "Governor of Greece" description and the missing 0.0.14 README notes.
- **0.0.14** — New 6th puppet: IGR (Governatorato militare di occupazione della Grecia), founded from Attica with Peloponnese/Epirus/Aegean Islands, led by Pietro Parini (Governor of Greece, your portrait); Northern Epirus (805) now goes to Albania or Greece only, with all other nations' requirements removed; new Central Macedonia (731) and Thrace (184) fate events (Greece or Bulgaria, must border); new Zara-style Crete (182) and Dodecanese (164) events — cede to Greece or annex to Italy (islands, so no border check, IGR must exist).
- **0.0.13** — New 5th puppet: IBL (Governatorato di occupazione militare della Bulgaria), founded from Sofia with Moesia/Plovdiv/Burgas, led by Attilio Biseo (Governor of Bulgaria, your portrait); Southern Serbia and Macedonia decisions now need Serbia or Bulgaria to border, and Bulgaria can receive them; Serbia gets your Tito Agosti portrait (Governor of Serbia).
- **0.0.12** — Zara/Istria decisions now require Croatia to border the state (for ceding and annexing alike); North Slovenia/Ljubljana decisions need a Croatian border too, though any bordering puppet can still receive them; IAL gets your Alfredo Guzzoni portrait (Governor of Albania).
- **0.0.11** — IMT renamed to Governatorato del Montenegro, with your custom Pirzio Biroli portrait (Governor of Montenegro); Bastianini is now Governor of Croatia; removed the Morava and Shkoder fate decisions (plus their now-dead events); Albania founding no longer takes Northern Epirus — assign it later via its fate decision; Bačka and West Banat can only go to Croatia or Serbia; Zara/Istria verified Croatia-or-annex only (no change needed).
- **0.0.10** — Bastianini portrait fixed: the DDS moved to `gfx/leaders/ICR/` (the engine only looks inside tag subfolders, so the old flat file was never found); removed the broken `Portrait_Italy_*` picture references for the other three leaders (vanilla portraits cannot resolve for custom tags) — they now use the default portrait with no log errors; `supported_version` updated to `1.19.2`.
- **0.0.9** — Leaders fixed for real: all 16 `create_country_leader` blocks now use valid vanilla sub-ideologies (`fascism_ideology` / `despotism` / `liberalism` / `marxism`) instead of the invalid group names that made the game reject every leader and spawn generics like "lucas brown" — Bastianini now actually leads ICR; removed all 77 invalid `show_as_unavailable` lines from events (unknown key, pure log spam — ineligible options now hide instead of greying out); fixed the missing UTF-8 BOM in the autonomy localisation file.
- **0.0.8** — Colors use the documented `color = rgb { ... }` format (plain braces are ignored by the game — this was why puppet colors never applied); every puppet now has its leader defined for all 4 ideologies (Bastianini leads ICR as fascist, neutral, democratic and communist).
- **0.0.7** — Puppets (and attempted Italy) recolored to rgb(25, 100, 14); Bastianini portrait files renamed to ICR_Giuseppe_Bastianini.* (still ICR's leader).
- **0.0.6** — Fall of Montenegro requires ICR/ISE/IAL to exist; all puppets use Italy's map color { 67 127 63 }; portraits/icons re-encoded as proper DXT5 DDS (fixes Bastianini not showing); leader desc localisation keys; autonomy name mirrored into countries loc as redundancy.
- **0.0.5** — New IAL (Albania: 44/805/934) with full founding + redistribution parity and 4th recipient option in every fate event; Montenegro moved to 'Fall of Montenegro' event (integrate into Croatia/Serbia/Albania or create IMT); capitals can't be redistributed while their puppet is still creatable; Zara/Istria annex no longer mentions cores; Giuseppe Bastianini (custom portrait) leads ICR.
- **0.0.4** — Hotfix: decision category moved to the correct `common/decisions/categories/` path (the old `common/decision_category/` folder is never read by the game, which hid the whole tab); custom Italian-roundel category icon + registered sprite.
- **0.0.3** — Military Occupation autonomy level (0.1, RK-like, 100% civ+mil industry, Italy-only, custom icon); new "Italian Occupation" decision category; map highlighting on all 20 decisions; all decisions free; transfers restricted to bordering puppets (Zara/Istria keep annex-to-Italy); version scheme reset to 0.0.x.
- **0.1.1** — Hotfix: vanilla category, `country_exists` triggers, state-scope cores, repeatable founding, `supported_version` 1.18.*.
- **0.1.0** — First version: ICR / ISE / IMT, Yugoslavia founding + distribution, Zara/Istria special annexation, placeholder flags, English localisation.
r flags, English localisation.
