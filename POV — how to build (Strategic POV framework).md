# POV — how to build (Strategic POV framework)

---

## 1. Зачем отдельный процесс POV

Из ESC framework: плохой POV = потеря сделки, champion «уходит в rogue», год задержки.

**Для TheStage:** без POV outbound смешивает **4 продуктовых слоя**, обещает on-device на Snapdragon, или продаёт tiers ML-команде CEO/CFO — и сделка разваливается.

**Три опоры ESC (адаптация):**

| ESC pillar | TheStage meaning |
|------------|------------------|
| **Consensus** | Champion + ML + CFO согласны на **одной гипотезе** до exec meeting |
| **Collaboration** | V1 → V2 → V3; champion **ведёт** exec pitch, не vendor solo |
| **Ownership** | POV становится **их историей** (OEM metric, IR line), не «презентация TheStage» |

---

## 2. Что такое POV (и чем не является)

**POV** = perspective на проблему клиента, которую **можно решить** TheStage и **стоит решать** в их P&L / стратегии.

| POV **не** заменяет | POV **готовит** |
|---------------------|-----------------|
| Business case (ROI, cost of inaction) | Нарратив для consensus |
| Silver bullet / product deck | Unique insight + soundbite |
| Технический benchmark alone | Proof of impact (PoI) **после** POV buy-in |

**TheStage:** POV = **стратегическая рамка**; PoC benchmark = **PoI** (proof of impact) в business case.

---

## 3. Трёхстадийный процесс (ESC → TheStage)

| Stage | ESC | TheStage actions |
|-------|-----|------------------|
| **1. Hypothesis** | Research: 10-K, Street, walk the building | S-сегмент, IR, architecture honesty, savings map |
| **2. Consensus** | Rough V1 → build V2/V3 **with** champion | ML validates tech; CFO line on $/session; **you own doc** |
| **3. Executive** | **Champion presents**; you support | CEO/CFO hear **MUD / soundbite**; eng owns PoC scope |

```
Stage 1 (you)     →  Stage 2 (you + champion)  →  Stage 3 (champion leads)
Research/hypothesis    Consensus drafts V1–V3       Exec engagement
```

---

## 4. Stage 1 — Research & initial hypothesis

### 4.1 Источники (ESC «Steve research» + TheStage)

| Источник | Что искать |
|----------|------------|
| **10-K / 10-Q / earnings** | Going concern, AI in MD&A, cloud spend signals, OEM strategy |
| **The Street / IR** | Analyst questions on AI, margin, partnerships |
| **LinkedIn / podcasts** | CEO/CFO language (not only eng blog) |
| **Product / CES** | Where inference runs (cloud vs on-glass) — brief §3.12.2 |
| **Walk the building** (internal) | Confirm S-segment, motion A vs B, prod vs roadmap |

**Не заменять:** business acumen одним LLM-summary — сверять гипотезу с **architecture fit** (S1–S7).

### 4.2 Initial hypothesis (шаблон)

> Because **[industry/OEM shift — e.g. AI in every reference design]**, **[company]** must **[solve inference unit economics / ship measurable AI]** or **[lose OEM deals / burn cloud COGS]**. TheStage can **[optimize NVIDIA inference / publish $/1k sessions]** where **[cloud/partner path exists]**. We **cannot** today **[compile on their on-glass Snapdragon]** without **[custom / roadmap]**.

### 4.3 Map initiatives → executive objectives (value pyramid)

Используйте три столпа ESC — framework § Mapping initiatives:

| Executive objective | TheStage initiative examples |
|---------------------|------------------------------|
| **Decrease cost** | Cloud inference COGS ↓; fewer GPU-hours per OEM pilot; R&D time on tiers |
| **Increase revenue** | OEM wins with priced AI unit economics; faster SKU with AI spec; services/licensing |
| **Manage risk** | Honest architecture slide; phased PoC; no over-promise on SDK |

**Value pyramid (заполнить per account):**

```
Goal (from 10-K / CEO): e.g. "OEM smart glasses growth without margin collapse"
  → Strategies: efficient growth | partnership scale | defend niche
    → Challenges: cloud AI COGS | no AI unit metric | Snapdragon vs cloud split
      → TheStage wedge: Layer A optimize + benchmark spec
```

---

## 5. Stage 2 — Consensus building

### 5.1 Вы — keeper of the POV

- Приносите **факты они не знали** (research: Ramblr cloud, AR1 vs cloud, $/session math).  
- **Frame around hypothesis** — не каталог фич.  
- **OK to be wrong on purpose** — пусть champion поправит архитектуру (ESC pro tip).

### 5.2 Audience layers (ESC «PoV by audience» → TheStage)

| Audience | Today | Tomorrow (with TheStage) |
|----------|-------|---------------------------|
| **ML / platform** | Manual quant, slow tiers, cloud bill | Reproducible tiers S/M/L; benchmark in weeks |
| **VP BD / OEM** | AI slideware in partner decks | Latency + **$/1k sessions** в P&L / business case |
| **CFO** | Unmodeled AI variable cost | PoC $ in → GPU $ out; directional ROI |
| **CEO** | AI demo without IR metric | One metric on reference design / partnership |

**Один POV doc — секции по персоне**, не разные обещания.

### 5.3 Consensus checklist

- [ ] Champion named; agrees to **present** to exec (Stage 3)  
- [ ] ML sign-off: PoC scope **one model**, feasible stack  
- [ ] CFO/CEO line: **no** fake OpEx savings; **yes** variable inference  
- [ ] Architecture honesty documented (what we **don't** do on-glass)  
- [ ] CRM: `buyer_motion: exec-led | eng-led | hybrid`  
- [ ] V2/V3 drafts co-edited with champion  

---

## 6. Stage 3 — Executive engagement

### 6.1 Opener is the new close (ESC)

**One slide / one sentence** before product.

#### Strategic Soundbite (CEO / strategy — Nasralla format)

> Because **[massive shift — e.g. every OEM expects AI in glasses]**, now is the time to **[publish unit-economic AI in reference designs]**. When you do, **[OEM win-rate, partnership credibility, measurable $/1k sessions]**. If you do not, **[cloud COGS per pilot, AI remains demo not P&L]**.

#### MUD statement (CFO — Meaningful, Unique, Defensible)

> We will **[reduce cloud inference cost per AI session by X–Y% (PoC)]** through **[Elastic + ANNA on NVIDIA]** by **[benchmarking your highest-volume cloud workload]** resulting in **[lower $/1k sessions / predictable pilot COGS]** as supported by **[SaladCloud-class proof / PoC on your model]**.

**TheStage MUD guardrails:**

- **M**eaningful = ties to **their** 10-K language (going concern, OEM, COGS)  
- **U**nique = inference optimization + tiers, not «another GPU cloud»  
- **D**efensible = PoC benchmark, not marketing 2–4× without measurement  

### 6.2 Champion presents; you support

- Не pitch solo exec meeting без internal champion.  
- Вы можете быть в комнате; **они ведут** слайды POV.  
- Technical deep-dive — **после** strategic buy-in или отдельная сессия с ML.

### 6.3 POV ≠ business case

| Artifact | When | Content |
|----------|------|---------|
| **POV** | Stage 2–3 | Narrative, insight, strategic fit |
| **Business case / PoC proposal** | After POV buy-in | ROI, timeline, $, success metrics |
| **PoI (proof of impact)** | After PoC | Measured $/session, tps, ttft |

---

## 7. POV document template (TheStage)

Use for any account; for **S7/public OEM** copy finance sections from finance-first POV.

```markdown
# POV — [Company] ([TICKER])

## Meta
- S-segment: S_
- W-landmark: W_
- buyer_motion: exec-led | eng-led | hybrid
- Stage: 1 | 2 | 3

## Strategic Soundbite (CEO)
[1 paragraph]

## MUD (CFO)
[1 paragraph]

## Situation / Complication / Insight (ESC + brief)
...

## Value pyramid
Goal → Strategies → Challenges → TheStage wedge

## By audience (Today → Tomorrow table)
ML | BD | CFO | CEO

## Architecture honesty
What we do / do not do on-device

## Savings / impact zones (ranked)
1. ...
## Consensus log
Champion | ML sign-off | draft versions

## Phase 0 PoC (PoI path)
Scope | metric | timeline

## Do not promise
- ...
```

**Filled example (S7 / public OEM):** Vuzix — POV and business case (illustration)) — MDP, O→I→I, Soundbite, MUD, metrics registry, layered unit economics (`12k × $5`), business case, Stage 1–3 checklist.

---

## 8. Когда какой playbook

| Account type | Primary doc |
|--------------|-------------|
| **S7 / public OEM** (VUZI-class) | Finance-first POV) + this framework |
| **W1 voice @ MAU** (Praktika-class) | This framework; lead **eng + product**; CFO later |
| **W4 B2B voice** (Phonic-class) | MUD on $/minute; security row |
| **Motion A providers** | Unique insight = day-zero optimize; different soundbite |

---

## 9. Three secrets (ESC) — TheStage reminders

1. **Keep it simple** — industry shift on AI unit economics; ask their view; have an opinion.  
2. **Consensus** — business acumen + OK to be wrong; never skip ML on S7 accounts.  
3. **Transfer ownership** — «their OEM metric», «their measured unit economics» — anchor all follow-up.

**Blend with business case:** POV wins the narrative; **PoC SOW** carries POI metrics (Roadmap week 2–4).

---
