# Italian Occupation Plus — v0.0.28 (Yugoslavia + Albania + Bulgaria + Greece + Turkey + North Africa + Egypt + Spain + Portugal + Occitania + Levant + Iraq + Arabia + Armenia + Iran)

A Hearts of Iron 4 mod that gives **Italy** its own Reichskommissariat-style occupation system, inspired by *Reichskommissariats Plus*.

As Italy, occupy Yugoslav land → open the decisions tab **"Italian Occupation"** → found military occupation governments as puppets → distribute individual states to them through events where **you pick the recipient (must border the state)**.

> **Version scheme:** `0.0.x` — future updates increment only the last number (0.0.4, 0.0.5, …).

## What's in v0.0.3

### 17 new puppet nations

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
- **IPG** — Giuseppe Lombrassa (Governor of Portugal, custom portrait included)
- **IOC** — Enea Navarini (Governor of Occitania, custom portrait included)
- **ILV** — Niccolò Nicchiarelli (Governor of Levant, custom portrait included)
- **IIQ** — Nino Sozzani (Governor of Iraq, custom portrait included)
- **IAR** — Gianrico Tedeschi (Governor of Arabia, custom portrait included)
- **IAM** — Drastamat "Dro" Kanayan (Governor of Armenia, custom portrait included)
- **IIR** — Giuseppe Pièche (Governor of Iran, custom portrait included)

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

### 68 decisions — all free, all with map highlighting

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

Each founding decision only **appears** once you control **at least half of that puppet's initial states** (rounded up — e.g. 2 of 3 for Croatia, 10 of 20 for Spain), and still needs the **capital state** to click. Any other initial states you control transfer automatically.

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
| **340** | **Bursa (special)** | **Needs ITR border; then Turkey OR annex to Italy** |
| **797** | **Istanbul (special)** | **Needs ITR border; then Turkey OR annex to Italy** |
| 665 + 458 | Tunisia: Gabès + Tunisia (grouped) | INA only — direct transfer, no event |
| 459 + 460 + 513 + 514 | Algeria: Algiers + Constantine + Tlemcen + Algerian Desert (grouped) | INA only — direct transfer, no event |
| 461 + 462 | Morocco: Casablanca + Marrakech (grouped) | INA only — direct transfer, no event |
| 290 | Spanish Africa | INA only — direct transfer, no event |
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
| **183** | **Cyprus (special, island)** | **Turkey OR Levant (exist) OR integrate into Italy** |
| **656** | **Kuwait (special)** | **Iraq OR Arabia (each must own a bordering state) OR integrate into Italy** |
| 293 + 659 + 992 | Yemen: North Yemen + South Yemen + Aden (grouped) | IAR only — direct transfer, no event |
| 1016 + 1015 + 294 | Oman: Dhofar + Oman + Muscat (grouped) | IAR only — direct transfer, no event |
| 658 | Abu Dhabi | IAR only — direct transfer, no event |
| 765 | Qatar | IAR only — direct transfer, no event |
| **77** | **Dobrudja (special)** | **Needs IBL to own a bordering state; then Bulgaria OR integrate into Italy** |
| **354 + 800** | **Trabzon + Van (special, grouped)** | **Turkey OR Armenia — each must own a bordering state; no Italian option** |
| 23 | Poitou | IOC only — direct transfer, no event (owned/controlled by Italy or a subject) |
| — | **Unite the Iberian Peninsula** | **Visible once IPG founded and ISP exists; ISP annexes IPG, gains cores on all Portuguese states and becomes the Governatorato di occupazione militare della penisola Iberica (cosmetic tag `ISP_iberia`); afterwards all "cede to Spain" options read "cede to Iberia"** |

Only **Dalmatia, Ljubljana, Zara, Istria, Crete, Dodecanese, Edirne, Bursa, Istanbul, Sidi Ifni, Suez, Gibraltar, the Balearics, the Canaries, Azores/Madeira, Provence, Savoy/Var, Corsica, Sinai, Cyprus, Kuwait and Dobrudja** keep an annex-to-Italy option (core gain is intentionally not shown) — all other transfers must go to a bordering puppet, except North Slovenia which can also be handed to a bordering Germany or Austria (no cores), and the North African and Sudanese group transfers which go straight to INA/IEG (existence check only). Bačka (45) and West Banat (764) can only go to Croatia or Serbia; Central Macedonia (731) and Thrace (184) can only go to Greece or Bulgaria; Northern Epirus (805) can only go to Albania or Greece; Edirne (341) can only go to Bulgaria or Greece (or Italy). Zara and Istria decisions need Croatia to border the state (or the Dalmatia decision to have been taken); Bursa and Istanbul need Turkey to border; Edirne needs Bulgaria or Greece to border; Suez needs Egypt to control a neighboring state; Gibraltar needs Spain to own a neighboring state; the Balearics (island) only need ISP to exist. Crete and Dodecanese are islands, so no border check is possible — Crete needs IGR to exist, Dodecanese needs IGR or ITR to exist (Dodecanese starts Italian, so its decision appears right after founding either). North Slovenia (102) needs Croatia, Germany or Austria to border — occupation governments receive it with cores, Germany/Austria as a plain handover. Dalmatia (103) and Ljubljana (853) need Croatia to own a bordering state and go to Croatia or Italy only. Southern Serbia (803) and Macedonia (106) decisions need Serbia or Bulgaria to border, but any bordering puppet (including Bulgaria) can receive. The Tunisian, Algerian, Moroccan and Spanish-African groups transfer directly to INA with no event and no border checks — and none of those states has any other fate decision. The Sudan group works the same for IEG. Sinai (453) goes to the Levant, Egypt or Italy; Hatay (799) to Turkey or the Levant only. A distribution decision stays unavailable (greyed) until a valid recipient exists, so the event can never fire without one. Capital states (Croatia 109, Serbia 107, Montenegro 105, Albania 44) have no redistribution decision at all while their puppet can still be created — found (or settle) the puppet first.

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
│   ├── country_tags/iop_tags.txt            # ICR / ISE / IMT / IAL / IBL / IGR / ITR / INA / IEG / ISP / IPG / IOC / ILV / IIQ / IAR / IAM / IIR
│   ├── countries/Italy_*.txt                # gfx culture + map color
│   ├── decisions/categories/iop_categories.txt # "Italian Occupation" tab (note: categories/ subfolder!)
│   ├── decisions/IOP_yugoslavia.txt         # 4 founding + Fall of Montenegro + 18 distribution decisions
│   ├── decisions/IOP_greece.txt             # 1 founding (IGR) + 4 distribution decisions (731/184/182/164)
│   ├── decisions/IOP_turkey.txt             # 1 founding (ITR) + 3 distribution decisions (341/340/797)
│   ├── decisions/IOP_north_africa.txt        # 1 founding (INA) + 5 distribution decisions (tunisia/algeria/morocco/spanish_africa/783)
│   ├── decisions/IOP_egypt.txt                    # 1 founding (IEG) + 2 distribution decisions (sudan/suez)
│   ├── decisions/IOP_spain.txt                    # 1 founding (ISP) + 2 distribution decisions (gibraltar/baleares)
│   ├── decisions/IOP_portugal.txt                 # 1 founding (IPG) + canarias + azores/madeira + unite iberia
│   ├── decisions/IOP_occitania.txt                # 1 founding (IOC) + provence + savoy/var + corsica + poitou
│   ├── decisions/IOP_levant.txt                   # 1 founding (ILV) + hatay + sinai + cyprus
│   ├── ideas/IOP_ideas.txt                        # "Military Government" national spirit (all puppets)
│   ├── decisions/IOP_arabia.txt                   # 2 foundings (IIQ, IAR) + kuwait + yemen/oman/abu dhabi/qatar transfers
│   └── decisions/IOP_armenia.txt                  # 2 foundings (IAM, IIR) + trabzon/van
├── history/
│   ├── countries/ICR|ISE|IMT|IAL|IBL|IGR|ITR|INA|IEG|ISP|IPG|IOC|ILV|IIQ|IAR|IAM|IIR*.txt       # capitals, leaders, tech
│   └── units/IOP_empty.txt                  # empty puppet OOB
├── gfx/leaders/ICR/ICR_Giuseppe_Bastianini.dds # custom ICR portrait (tag subfolder required!)
├── gfx/leaders/IMT/IMT_Alessandro_Pirzio_Biroli.dds # custom IMT portrait
├── gfx/leaders/IAL/IAL_Alfredo_Guzzoni.dds # custom IAL portrait
├── gfx/leaders/ISE/ISE_Tito_Agosti.dds # custom ISE portrait
├── gfx/leaders/IBL/IBL_Attilio_Biseo.dds # custom IBL portrait
├── gfx/leaders/IGR/IGR_Pietro_Parini.dds # custom IGR portrait
├── gfx/leaders/ITR/ITR_Rodolfo_Graziani.dds # custom ITR portrait
├── gfx/leaders/INA/INA_Ettore_Bastico.dds # custom INA portrait
├── gfx/leaders/IEG/IEG_Italo_Gariboldi.dds # custom IEG portrait
├── gfx/leaders/ISP/ISP_Mario_Roatta.dds    # custom ISP portrait
├── events/IOP_spain.txt                     # 2 events (iop_spain.118, .177)
├── gfx/leaders/IPG/IPG_Giuseppe_Lombrassa.dds # custom IPG portrait
├── events/IOP_portugal.txt                  # 2 events (iop_portugal.178, .698)
├── gfx/leaders/IOC/IOC_Enea_Navarini.dds   # custom IOC portrait
├── events/IOP_occitania.txt                 # 3 events (iop_occitania.32, .735, .1)
├── gfx/leaders/ILV/ILV_Niccolo_Nicchiarelli.dds # custom ILV portrait
├── events/IOP_levant.txt                    # 3 events (iop_levant.799, .453, .183)
├── gfx/leaders/IIQ/IIQ_Nino_Sozzani.dds     # custom IIQ portrait
├── gfx/leaders/IAR/IAR_Gianrico_Tedeschi.dds # custom IAR portrait
├── events/IOP_arabia.txt                    # 1 event (iop_arabia.656)
├── gfx/leaders/IAM/IAM_Drastamat_Dro_Kanayan.dds # custom IAM portrait
├── gfx/leaders/IIR/IIR_Giuseppe_Pieche.dds  # custom IIR portrait
├── events/IOP_armenia.txt                   # 1 event (iop_armenia.354)
├── events/IOP_yugoslavia.txt                # 19 events (iop_yugo.102, .103, ...)
├── events/IOP_greece.txt                    # 4 events (iop_greece.731, .184, .182, .164)
├── events/IOP_turkey.txt                    # 3 events (iop_turkey.341, .340, .797)
├── events/IOP_north_africa.txt               # 1 event (iop_africa.783)
├── events/IOP_egypt.txt                         # 1 event (iop_egypt.446)
├── interface/iop_autonomy.gfx               # autonomy icon sprite
├── interface/iop_decisions.gfx               # category icon sprite
├── gfx/
│   ├── flags/ (+ medium/, small/)           # placeholder .tga flags (base + 4 ideologies x 3 sizes per tag)
│   └── interface/autonomy/                  # Military Occupation .dds icon
└── localisation/english/IOP_*_l_english.yml # countries / decisions / events / autonomy (BOM!)
```

## Extending (Greece, Albania, France…)

The pattern per new region is:

│   ├── country_tags/iop_tags.txt            # ICR / ISE / IMT / IAL / IBL / IGR / ITR / INA / IEG / ISP / IPG / IOC / ILV / IIQ / IAR / IAM / IIR
│   ├── decisions/IOP_greece.txt             # 1 founding (IGR) + 4 distribution decisions (731/184/182/164)
│   ├── decisions/IOP_turkey.txt             # 1 founding (ITR) + 3 distribution decisions (341/340/797)
│   ├── decisions/IOP_north_africa.txt        # 1 founding (INA) + 5 distribution decisions (tunisia/algeria/morocco/spanish_africa/783)
│   ├── decisions/IOP_egypt.txt                    # 1 founding (IEG) + 2 distribution decisions (sudan/suez)
│   ├── decisions/IOP_spain.txt                    # 1 founding (ISP) + 2 distribution decisions (gibraltar/baleares)
│   ├── decisions/IOP_portugal.txt                 # 1 founding (IPG) + canarias + azores/madeira + unite iberia
│   ├── decisions/IOP_occitania.txt                # 1 founding (IOC) + provence + savoy/var + corsica + poitou
│   └── decisions/IOP_levant.txt                   # 1 founding (ILV) + hatay + sinai
3. **Distribution decisions + events** per state (copy a `iop_decide_*` block and its event, change the state ID — border logic works automatically).
4. **Localisation**: add decision/event/country keys to the `.yml` files (keep the BOM!).

Suggested next regions: Albania protectorate, Corsica/Savoy, Egypt/Libya, Ethiopia/East Africa.

## IMPORTANT: always clean-reinstall

HOI4 does not clean up removed/renamed mod files on update. If puppets show **wrong colors, wrong leaders, or old decisions**, you are almost certainly running **stale files mixed with the new version**. Fix: **delete** `Documents\Paradox Interactive\Hearts of Iron IV\mod\italian_occupation_plus` **and** `italian_occupation_plus.mod` completely, then extract the new zip. Never extract over the old folder.

## Troubleshooting

- **Decisions don't show:** you must be playing the country with `original_tag = ITA`. Founding needs control of the capital state (109 / 107 / 105). Distribution needs ≥1 puppet to exist AND at least one puppet bordering the state.
- **Mod shows as outdated:** edit `supported_version` in both `.mod` files to match your game (e.g. `1.20.*`).
- **"Military Occupation" level missing/wrong:** check `error.log` for `autonomy_military_occupation` — most likely the `.gfx` sprite or `.dds` path. The icon falling back to `?` is cosmetic only.
- **Check errors:** after running the game, look at `Documents\Paradox Interactive\Hearts of Iron IV\logs\error.log` and search for `iop`.
- **Missing portraits:** if a leader shows a silhouette, the portrait `.dds` name doesn't exist in your game version — replace `picture = ...` in the history file with another vanilla portrait. It never crashes, it's cosmetic.

## Changelog

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
