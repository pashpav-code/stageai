# ML workflow: классика vs TheStage AI (wearable / voice)

**Аудитория:** ML-команда (wearable, on-device voice)  
**Формат:** Mermaid — рендерится в GitHub, Cursor, Notion, [mermaid.live](https://mermaid.live)

**Как читать:** §1 — два столбца **рядом** (одна строка = один этап); §2–3 — полный путь сверху вниз; §4 — паттерны runtime + **только** клиенты из наших notes; §5–6 — таблица и легенда.

---

## 1. Два процесса рядом (overview) — side by side

Слева — классика, справа — TheStage. Вертикальные стрелки **внутри каждого столбца**; горизонтально на одной строке — **один и тот же № этапа**.

| № | Общее название | Классика | TheStage AI | Бенефит TheStage | Ориентир срока |
|---|----------------|----------|-------------|------------------|----------------|
| **0** | Цель | voice on wearable + hub | то же | — | — |
| **1** | Обучение | fine-tune / LoRA | то же | train без изменений | **дни–недели** |
| **2** | Сжатие | PTQ/GPTQ/AWQ вручную | ANNA+Qlip / Elastic | меньше перебора | **2–6 нед** → **дни** |
| **3** | Export / compile | Core ML / ONNX / TFLite | Apple / NVIDIA / Jetson | один compile path | **1–3 нед** → **часы–дни** |
| **4** | Валидация | профиль на девайсах | benchmark tiers | re-tier без полного re-quant | **1–2 нед** → **часы–2 дня** |
| **5** | Pipeline | STT→LLM→TTS своё | SDK + ваша wiring | готовый artifact | **1–3 нед** |
| **6** | Прод | часто cloud API | on-device + cloud opt. | ваши SLO | runtime |

```mermaid
flowchart TB
  classDef classic   fill:#fde8e8,stroke:#c0392b,stroke-width:2px,color:#7b241c,font-weight:bold
  classDef stage     fill:#d5f5e3,stroke:#1e8449,stroke-width:2px,color:#145a32,font-weight:bold
  classDef note_pain fill:#fff0f0,stroke:#e74c3c,stroke-width:1px,color:#922b21,font-style:italic
  classDef note_gain fill:#f0fff4,stroke:#27ae60,stroke-width:1px,color:#145a32,font-style:italic

  ROOT[ ]

  C0["⓪  voice on wearable + hub\n⛅ Классика"]:::classic
  S0["⓪  voice on wearable + hub\n⚡ TheStage AI"]:::stage

  C1["①  fine-tune / LoRA · cloud GPU\n⏱ дни–недели"]:::classic
  S1["①  fine-tune / LoRA · ваши веса\n⏱ без изменений"]:::stage

  A2(["⚠️ ручной перебор\n2–6 нед"]):::note_pain
  C2["②  PTQ / GPTQ / AWQ\nсвои скрипты"]:::classic
  S2["②  ANNA + Qlip\nElastic tiers"]:::stage
  G2(["✔ Pareto-поиск авто\n→ дни"]):::note_gain

  A3(["⚠️ отдельный toolchain\n1–3 нед per backend"]):::note_pain
  C3["③  Core ML · ONNX · TFLite\nper-backend toolchain"]:::classic
  S3["③  Compile API\nApple · NVIDIA · Jetson"]:::stage
  G3(["✔ один compile path\n→ часы–дни"]):::note_gain

  A4(["⚠️ ручной профиль\n1–2 нед per device"]):::note_pain
  C4["④  p95 latency · OOM · battery\nна каждом девайсе вручную"]:::classic
  S4["④  tps · ttft · max_memory_mb\nbenchmark scripts"]:::stage
  G4(["✔ re-tier без re-quant\n→ часы–2 дня"]):::note_gain

  A5(["⚠️ orchestration с нуля\nнет artifact"]):::note_pain
  C5["⑤  STT + LLM + TTS\nсвой orchestration"]:::classic
  S5["⑤  compiled artifact + SDK\nваша wiring поверх"]:::stage
  G5(["✔ готовый artifact\nне с нуля"]):::note_gain

  A6(["⚠️ чужие SLO · $ at scale\nvendor lock"]):::note_pain
  C6["⑥  cloud API: OpenAI · Deepgram\nчужие SLO · $ at scale"]:::classic
  S6["⑥  on-device + cloud опционально\nваши SLO · ваш cost"]:::stage
  G6(["✔ ваши SLO · ваш cost\nartifact — не API"]):::note_gain

  ROOT --> C0
  ROOT --> S0
  C0 --> C1
  S0 --> S1
  C1 ~~~ A2
  C1 --> C2
  S1 --> S2
  S1 ~~~ G2
  C2 ~~~ A3
  C2 --> C3
  S2 --> S3
  S2 ~~~ G3
  C3 ~~~ A4
  C3 --> C4
  S3 --> S4
  S3 ~~~ G4
  C4 ~~~ A5
  C4 --> C5
  S4 --> S5
  S4 ~~~ G5
  C5 ~~~ A6
  C5 --> C6
  S5 --> S6
  S5 ~~~ G6

  style ROOT fill:#ffffff,stroke:#ffffff,color:#ffffff

  linkStyle default stroke:#2c3e50,stroke-width:3px,fill:none
  linkStyle 0,1,4,7,8,11,12,15,16,19,20,23 stroke:none,stroke-width:0px,fill:none
  linkStyle 2,5,9,13,17,21 stroke:#c0392b,stroke-width:3.5px,fill:none
  linkStyle 3,6,10,14,18,22 stroke:#1e8449,stroke-width:3.5px,fill:none
```

*Сроки — ориентиры для pitch; PoC у клиента может отличаться.*

---

## 2. Классический процесс (детально)

**Вход:** нужен voice assistant (wearable + phone hub / cloud).  
**Выход:** прод с известными SLO — либо cloud API, либо частично on-device, если цикл **②→③→④** сошёлся.  
**Петля:** новый LoRA / v2 → снова **② Сжатие**.

```mermaid
flowchart TB
  classDef io      fill:#eaf4fb,stroke:#2980b9,stroke-width:2px,color:#1a5276
  classDef step    fill:#f4f6f7,stroke:#7f8c8d,stroke-width:2px,color:#2c3e50
  classDef pain    fill:#fde8e8,stroke:#e74c3c,stroke-width:3px,color:#922b21,font-weight:bold
  classDef decide  fill:#fef9e7,stroke:#f39c12,stroke-width:2px,color:#7d6608
  classDef out_bad fill:#fde8e8,stroke:#c0392b,stroke-width:2px,color:#7b241c

  IN(["▶ ВХОД\nVoice assistant · wearable + hub / cloud"]):::io

  IN --> TRAIN["① Обучение\nfine-tune / LoRA · cloud GPU\n⏱ дни–недели"]:::step

  TRAIN --> QUANT["② Сжатие  ⚠️ БОЛЬ\nPTQ · GPTQ · AWQ · SmoothQuant\nсвои скрипты · ручной перебор\n⏱ 2–6 нед экспериментов"]:::pain

  QUANT --> EXPORT["③ Export  ⚠️ БОЛЬ\nCore ML · ONNX · ExecuTorch\nотдельный toolchain per backend\n⏱ 1–3 нед"]:::pain

  EXPORT --> PROFILE["④ Валидация  ⚠️ БОЛЬ\np95 latency · OOM · battery drain\nна каждом целевом девайсе вручную\n⏱ 1–2 нед"]:::pain

  PROFILE --> FIX{"Влезает?\nSLO OK?"}:::decide
  FIX -->|"🔄 Нет — повтор цикла\n(часто 2–5 итераций)"| QUANT
  FIX -->|"✅ Да"| WIRE["⑤ Pipeline\nSTT lib + LLM runtime + TTS\nсвой orchestration\n⏱ 1–3 нед"]:::step

  WIRE --> PROD["⑥ Продакшен"]:::step
  PROD --> CLOUD["Путь A ☁️  Cloud API\nOpenAI · Deepgram · Whisper API\n⚠️ ongoing $ · чужие SLO · vendor lock"]:::out_bad
  PROD --> LOCAL["Путь B 📱  On-device\nтолько если цикл ②→④ сошёлся"]:::step

  CLOUD --> OUT(["◀ ВЫХОД\nProd: STT→LLM→TTS · SLO зафиксированы\nили зависимость от API-vendor"]):::io
  LOCAL --> OUT

  UPDATE(["↻ Новый LoRA / model v2\n→ весь цикл ②→④ заново"]) -.->|"полный повтор"| QUANT

  linkStyle default stroke:#2c3e50,stroke-width:3px,fill:none
  linkStyle 5 stroke:#e74c3c,stroke-width:4px,fill:none
  linkStyle 12 stroke:#95a5a6,stroke-width:2px,stroke-dasharray:6 4,fill:none
```

**Боли:** цикл **②→③→④** повторяется; cloud API = чужие SLO и cost at scale.

---

## 3. Процесс с TheStage AI (детально)

**Вход:** та же цель — voice assistant.  
**Выход:** прод с **compiled artifact** на вашем железе (tiers), опционально гибрид с cloud; SLO ваши.  
**Петля:** новый LoRA → только **③ tier re-pick + recompile** (не весь ②).  
**Параллельно:** Platform/CLI — GPU для **②b** (ANNA) и **④** (benchmark).

```mermaid
flowchart TB
  classDef io       fill:#eaf4fb,stroke:#2980b9,stroke-width:2px,color:#1a5276
  classDef step     fill:#d5f5e3,stroke:#1e8449,stroke-width:2px,color:#145a32
  classDef elastic  fill:#d6eaf8,stroke:#2471a3,stroke-width:2px,color:#1a5276,font-weight:bold
  classDef qlip     fill:#e8d5f5,stroke:#7d3c98,stroke-width:2px,color:#4a235a,font-weight:bold
  classDef compile  fill:#cce5ff,stroke:#0066cc,stroke-width:3px,color:#003366,font-weight:bold
  classDef decide   fill:#fef9e7,stroke:#f39c12,stroke-width:2px,color:#7d6608
  classDef platform fill:#f0f3f4,stroke:#7f8c8d,stroke-width:2px,color:#2c3e50,font-style:italic
  classDef prod_ok  fill:#d5f5e3,stroke:#1e8449,stroke-width:2px,color:#145a32,font-weight:bold

  IN(["▶ ВХОД\nVoice assistant · wearable + hub / cloud"]):::io

  IN --> TRAIN["① Обучение\nfine-tune / LoRA · ваши веса\n⏱ дни–недели (без изменений)"]:::step

  TRAIN --> CHOICE{"② Путь сжатия?"}:::decide

  CHOICE -->|"⚡ Быстрый старт\n(готовые модели)"| ELASTIC["②a Elastic Models\nWhisper · LLM tiers S–M–L–XL\nHF-style API · предобученные\n⏱ часы–дни"]:::elastic
  CHOICE -->|"🎯 Своя модель\n(максимальный контроль)"| QLIP["②b Qlip + ANNA\nPareto-поиск · constraint size/MACs\nкалибровка на Platform GPU\n⏱ дни"]:::qlip

  ELASTIC --> TIER["③ Tier Select + Compile\nS · M · L · XL\n→ Apple Silicon · NVIDIA · Jetson\n⏱ часы–дни"]:::compile
  QLIP    --> TIER

  TIER --> BENCH["④ Валидация\nbenchmark scripts\ntps · ttft · max_memory_mb\n⏱ часы–1–2 дня"]:::step

  BENCH --> FIX{"Влезает?\nSLO OK?"}:::decide
  FIX -->|"↻ Подкрутить tier\n(без re-quant)"| TIER
  FIX -->|"✅ Да"| DEPLOY["⑤a Deploy artifact\ncompiled model → iOS / Android / hub\n+ SDK integration\n⏱ дни–1 нед"]:::step

  DEPLOY --> ORCH["⑤b Pipeline wiring\nSTT → LLM → TTS\nваш orchestration layer\n⏱ 1–3 нед"]:::step

  ORCH --> PROD["⑥ Продакшен"]:::step
  PROD --> LOCAL["Путь A 📱  On-device / Phone hub\nваш artifact · ваши SLO · ваш cost ✔"]:::prod_ok
  PROD --> HYBRID["Путь B ☁️  Гибрид\nсложные запросы → cloud NVIDIA\nваш control plane ✔"]:::step

  LOCAL  --> OUT(["◀ ВЫХОД\nArtifact на device + ваша orchestration\nSLO ваши · cloud — опционально"]):::io
  HYBRID --> OUT

  PLATFORM["TheStage Cloud / CLI\n🖥 GPU для ANNA (②b)\n📊 benchmark scripts (④)"]:::platform -.->|"GPU compute"| QLIP
  PLATFORM -.->|"benchmark"| BENCH

  LORA(["↻ Новый LoRA / model v2\n→ tier re-pick + recompile\n(не повторяет весь ②)"]) -.->|"быстрее классики"| TIER

  linkStyle default stroke:#2c3e50,stroke-width:3px,fill:none
  linkStyle 16,17,18 stroke:#7f8c8d,stroke-width:2px,stroke-dasharray:6 4,fill:none
```

**Сдвиг:** меньше ручного export; измеримые tiers; GPU-калибровка через Platform; прод — ваш artifact, не только API.

---

## 4. Архитектура runtime (wearable) — где крутятся модели

**Важно:** wearable ≠ всегда «только слабое железо». Ниже — **паттерны из product matrix** (docs/сайт) и **как ими пользуются известные клиенты** (~6 paying + якорные notes). Без вымышленных OEM.

| Паттерн | Где inference | Железо | TheStage сегодня | Кто так делает (наши данные) |
|---------|---------------|--------|------------------|------------------------------|
| **A. On-glass** | STT/LLM в дужке | Snapdragon / Android SoC, NPU on-glass (OEM) | ❌ нет self-serve QNN/SDK | **Brilliant Labs** — on-glass NPU (Alif) + **не** документированный compile TheStage на Qualcomm; типовой industry gap |
| **B. Phone hub** | STT/LLM на paired phone | Apple Silicon (compile path) | ✅ tiers S–M, Apple compile | **Brilliant Labs** — TheStage на **paired smartphone** (press); **Praktika** — приложение на телефоне, migration on-device |
| **C. Edge-box** | Hub в кейсе / на линии | Jetson (NVIDIA) | ✅ export path в маркетинге | Product matrix; **именованного paying только-Jetson** в notes нет |
| **D. Cloud-first** | Очки/апп = capture; AI в облаке | NVIDIA GPU | ✅ Elastic + Qlip + ANNA | **Praktika** (сейчас cloud → device); **Phonic**; **Recraft**; **Nebius** — infra/канал, не wearable app |
| **E. Split wake** | Wake/VAD на device, тяжёлое — hub/cloud | MCU + BLE | ⚠️ wake — vendor; STT/LLM — TheStage на B или D | Типовый mass-market glasses; **Brilliant**-class hybrid |

**Публичные кейсы (не все wearable):** SaladCloud, Wallarm — cloud optimize; Huawei P50/P60 — **кастомный** on-device Snapdragon (R&D), не self-serve SDK для glasses.

```mermaid
flowchart TB
  classDef gap     fill:#fde8e8,stroke:#e74c3c,stroke-width:2px,color:#922b21,font-weight:bold
  classDef glass   fill:#e8d5f5,stroke:#7d3c98,stroke-width:2px,color:#4a235a
  classDef phone   fill:#d6eaf8,stroke:#2471a3,stroke-width:2px,color:#154360,font-weight:bold
  classDef edge_c  fill:#fef9e7,stroke:#d4ac0d,stroke-width:2px,color:#7d6608
  classDef cloud_n fill:#d5f5e3,stroke:#1e8449,stroke-width:2px,color:#145a32
  classDef stage   fill:#2c3e50,stroke:#2c3e50,color:#ffffff,font-weight:bold
  classDef client  fill:#f4f6f7,stroke:#aab7b8,stroke-width:1px,color:#2c3e50
  classDef user_o  fill:#eaf4fb,stroke:#2980b9,stroke-width:2px,color:#1a5276

  subgraph WEAR["👓 Wearable"]
    direction LR
    MIC["🎙 Микрофон"]
    P_A["A · On-glass\nSoC / NPU в дужке\n❌ нет TheStage self-serve SDK"]:::gap
    P_E["E · Wake / VAD only\nMCU → BLE offload"]:::glass
    MIC --> P_A
    MIC --> P_E
  end

  subgraph HUB["📱 B · Phone hub — Apple Silicon"]
    STT_B["STT · tier S–M\n✅ TheStage compile"]:::phone
    LLM_B["LLM · tier S–M\n✅ TheStage compile"]:::phone
    TTS_B["TTS"]:::phone
    STT_B --> LLM_B --> TTS_B
  end

  subgraph EDGE_BOX["🖥 C · Edge-box"]
    JET["Jetson NVIDIA\n✅ export path\n(product matrix)"]:::edge_c
  end

  subgraph CLOUD_D["☁️ D · Cloud NVIDIA"]
    BIG["STT / LLM / TTS\n✅ Elastic · Qlip · ANNA\nfull TheStage support"]:::cloud_n
  end

  P_E -->|"аудио / BLE"| STT_B
  P_A -->|"опционально\n(если нет on-glass stack)"| STT_B

  LLM_B -->|"тяжёлый запрос\n→ cloud fallback"| BIG
  BIG   -->|"ответ"| LLM_B

  STT_B -.->|"edge path"| JET
  LLM_B -.->|"edge path"| JET

  TTS_B --> USER_OUT["🔊 Ответ пользователю"]:::user_o

  COMP["⚡ TheStage\ncompiled tiers\n+ cloud optimize"]:::stage
  COMP -.-> STT_B
  COMP -.-> LLM_B
  COMP -.-> BIG
  COMP -.-> JET

  subgraph CLIENTS["Клиенты → паттерн"]
    direction LR
    BL["Brilliant Labs\nA (on-glass, без SDK)\n+ B (phone hub, TheStage)"]:::client
    PR["Praktika\nB phone hub · D cloud → on-device"]:::client
    PH["Phonic · Recraft\nD cloud NVIDIA"]:::client
  end

  BL -.-> WEAR
  BL -.-> HUB
  PR -.-> HUB
  PR -.-> CLOUD_D
  PH -.-> CLOUD_D

  linkStyle default stroke:#2c3e50,stroke-width:3px,fill:none
  linkStyle 8,9,11,12,13,14,15,16,17,18,19 stroke:#7f8c8d,stroke-width:2px,stroke-dasharray:6 4,fill:none
```

**На звонке:** спросить prospect — **A / B / C / D** в roadmap. On-glass Qualcomm **вне** стандартного продукта; для wearables с AI сегодня чаще **B + D** (Brilliant, Praktika).

---

## 5. Что меняется одной таблицей

| № этап | Классика | С TheStage AI | Бенефит + срок |
|--------|----------|---------------|----------------|
| ② Сжатие | Свои PTQ/GPTQ эксперименты | ANNA + tiers или Elastic | **2–6 нед → дни** |
| ③ Export | Ручной Core ML / ONNX | Compile API | **1–3 нед → часы–дни** |
| ④ Валидация | Свои бенчмарки на девайсах | tps, ttft, max_memory_mb | Быстрее re-tier **часы–2 дня** |
| GPU для экспериментов | Свой k8s / ноутбук | Platform CLI, Nebius/AWS | Не строить кластер |
| Обновление LoRA | Часто весь цикл заново | Tier re-pick + recompile | Меньше повтор **②③** |
| ⑥ Прод SLO | Зависит от API vendor | Ваш artifact на железе | Cost + latency под контролем |
| ⑤ Orchestration | 100% ваша | В основном ваша | Vision: orchestrator позже |

---

## 6. Легенда

| Термин | Значение |
|--------|----------|
| PTQ/GPTQ/AWQ | Способы сжать уже обученную модель |
| Tier S/M/L/XL | Степень сжатия (быстрее ↔ качественнее) |
| tps / ttft | Скорость генерации / задержка до первого токена |
| OOM | Не хватило памяти на устройстве |
| Phone hub | Paired smartphone — compute (Brilliant, Praktika) |
| On-glass | Inference на SoC в очках — обычно **без** TheStage self-serve SDK |
| Edge-box | Jetson / промышленный hub (product matrix) |
| Cloud-first | Capture на device; модели на NVIDIA (Praktika, Phonic, Recraft) |

**Источник по клиентам:** [Stage AI — understanding brief](Stage%20AI%20%E2%80%94%20understanding%20brief.md) §3.8–3.9, реестр §2–3.
