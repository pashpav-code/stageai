# ICP use cases — истории в стиле Reddit

**Зачем:** показать TheStage AI, что мы понимаем **живых** клиентов, не абстрактный «enterprise AI».  
**Формат:** как пост на r/LocalLLaMA / r/MachineLearning — кто мы, что строим, боль, что пробовали, куда смотрим.  
**Связано:** [Stage AI — understanding brief](Stage%20AI%20%E2%80%94%20understanding%20brief.md) (главный документ; здесь — развёрнутые «голоса» ICP)

---

## Что нашли на Reddit и рядом (релевантные треды)

Прямой парсинг Reddit из tooling часто бьётся об 403, поэтому ниже — **подтверждённые** обсуждения с тем же вайбом и болями:

| Тема | Где обсуждают | Ссылка |
|------|----------------|--------|
| GGUF / quantize / свой стек | r/LocalLLaMA | [Quick Start Guide To Converting Your Own GGUFs](https://old.reddit.com/r/LocalLLaMA/comments/18av9aw/quick_start_guide_to_converting_your_own_ggufs/) |
| Core ML / ONNX export — боль | HN (те же инженеры) | [ONNX → CoreML feasibility](https://news.ycombinator.com/item?id=37082447) |
| llama.cpp на Android — OOM, battery, OEM | DEV | [P2P inference on Android phones — what we learned](https://dev.to/vishal_sharma_nataris/we-built-a-p2p-ai-inference-network-that-runs-on-android-phones-heres-what-we-learned-3lhb) |
| INT8 на разных телефонах — quality drift | разбор Reddit ML | [Same INT8 ONNX, accuracy drift across Snapdragon tiers](https://insights.marvin-42.com/articles/reddit-ml-report-same-int8-onnx-model-showed-major-accuracy-drift-across-snapdragon-tiers) |
| Бюджетный Android — RAM, thermal | блог | [LLM on a $150 Android phone](https://www.runanywhere.ai/blog/on-device-llm-android) |
| Smart glasses + local inference | новости / OSS | [Brilliant Labs Halo + on-device AI](https://techday.co.nz/story/privacy-first-ai-smart-glasses-run-models-on-device) (упоминают **TheStage AI** как партнёра) |

**Повторяющиеся мотивы из комьюнити:** OOM, thermal throttle, «export занял вечность», cloud bill растёт с MAU, на каждом Snapdragon своя accuracy.

---

# ICP 1 — «Мы language learning app, 2M users, cloud съел margin»

*Профиль: B2C startup, voice-first tutor, похож на кейс **Praktika** из voice notes.*

---

### Кто мы

Небольшая команда, **~40 человек**, 3 ML, 8 mobile. Делаем **AI language tutor** — пользователь **говорит**, приложение слушает, отвечает голосом, поправляет произношение. **~2M MAU**, основной рынок — LATAM + EU.

### Что строим

Полноценный **voice loop**:

```
микрофон → STT → LLM (диалог) → TTS → наушники
```

Сейчас **почти всё в облаке**. Локально только UI и кэш.

### Где болит (реально болит)

1. **Счёт за API** — каждый активный юзер = минуты STT + токены LLM + TTS. На 2M MAU даже с кэшем и лимитами **unit economics плавает**. CFO уже два квартала спрашивает «почему inference line item растёт быстрее revenue».

2. **Latency** — пользователь замолчал → **1–2 сек тишины** → ответ. В language learning это не «ну подождите», это «приложение тупое».

3. **Сеть** — Mexico City metro, rural Spain: люди реально пользуются в плохом LTE. Cloud-only = плохие сессии = churn.

4. **Privacy narrative** — конкуренты начали писать «your voice stays on device». Мы пока не можем честно.

### Что пробовали

| Подход | Плюсы | Минусы |
|--------|-------|--------|
| **Оставить cloud** (OpenAI-class + Deepgram/ElevenLabs) | Быстро, качество топ | $$$, latency, privacy story слабая |
| **Свой GPU + vLLM** | Контроль, дешевле на token при scale | Всё равно latency + нужен MLOps, не решает offline |
| **Маленькая модель on-device (llama.cpp)** | Круто в демо | 3 ML **5 месяцев** в export/OOM; на Android mid-range — **thermal hell**; качество хуже cloud |
| **Гибрид** «простые реплики local, сложное cloud» | Разумно | Нужна **routing logic** + две модели в проде = ещё complexity |

Мы застряли между «**founder хочет on-device к Q3**» и «**команда не успевает второй раз invent mobile ML**».

### Как Stage AI вписывается (если зайдёт)

Не магия «замените OpenAI одной кнопкой». Скорее:

- **Elastic Whisper + small LLM tiers** — baseline за **дни**, не месяцы (проверить quality на *нашем* accent mix).
- **ANNA + compile под Apple** — iPhone hub (у большинства users телефон есть) → срезаем **compress/export/profile** (в наших оценках **~2–3 месяца** на этом этапе).
- **Измеримые метрики** — ttft, tps, max_memory → спорим с product цифрами, не ощущениями.
- **Постепенный гибрид** — сначала STT on-device, LLM пока cloud; потом tier S LLM local.

**Edit:** нам всё ещё нужен свой **orchestration** (когда говорить, barge-in, TTS vendor). Stage не заменяет mobile team. Но **убирает адскую часть** «почему на Pixel 6a OOM».

---

# ICP 2 — «Мы делаем smart glasses, железо слабое, телефон — hub»

*Профиль: wearable startup, **Brilliant Labs**-adjacent; в индустрии уже есть связка **Brilliant Labs + TheStage** для on-device Halo.*

> **⚠️ Шаблон, не verified architecture Brilliant.** Публично (TechDay Mar 2026): **гибрид** — vision on glasses + значимый compute на **paired smartphone** (TheStage на phone); на Halo также **Alif NPU** on-glass. См. [understanding brief §3.8–5.2](Stage%20AI%20%E2%80%94%20understanding%20brief.md).

---

### Кто мы

**12 человек**, hardware + firmware + 2 ML. Делаем **AI очки** — голосовой ассистент, contextual hints, позже camera. Pre-order есть, **production Q1–Q2**.

### Что строим

**Учебная схема (упрощение):** очки: микрофон, BLE → **телефон** (hub) → STT → LLM → TTS → эарбад.  
На самих очках **нет** места для 7B — типичный стартап-паттерн; у **реального** Brilliant может быть **доп. compute на очках** (NPU).

### Где болит

1. **End-to-end latency budget** — пользователи сравнивают с **Siri / ChatGPT voice**. У нас **BLE + inference + TTS** — если >2–3 сек, продукт «ломаный».

2. **Батарея** — если всё гонять в cloud, очки + phone жрут radio. Если local — phone CPU/GPU греется.

3. **Privacy как selling point** — «raw audio never leaves device» — но только если **реально** local pipeline.

4. **Mirai / Cactus** — смотрели YC-стартапы в on-device hybrid. Founder говорит «не влезает в наш form factor / toolchain» — **детали не докопали**.

### Что пробовали

| Подход | Плюсы | Минусы |
|--------|-------|--------|
| **Cloud-only MVP** | Быстрый launch | Убивает battery + privacy story + latency в EU |
| **Whisper.cpp на phone** | Ок для STT | LLM всё равно отдельная боль |
| **Core ML export вручную** | Apple-native | **Месяцы**; transformer support meh; каждый iOS — сюрприз |
| **Партнёр inference** (TheStage и др.) | Time-to-market | Vendor risk, pricing, lock-in страхи |

### Reddit/HN вайб

Тот же кругляш: «хотел on-device → **ended up writing inference engine from scratch**» или «**llama.cpp OOM** on Android».

### Как Stage AI вписывается

- **Pre-compiled tiers** под **Apple Silicon** (phone hub) — не собираем Core ML graph с нуля в garage.
- **Whisper tier S** для always-listening-adjacent (с осторожностью по battery).
- **Jetson / edge-box** — если завтра hub не только phone (их docs упоминают Jetson).
- **Benchmark pack** — доказать investor'ам «<2s on iPhone 15» до mass manufacturing.

**Честно:** orchestration glasses↔phone **всё ещё наш код**. Stage — **мозги быстрее**, не весь продукт.

---

# ICP 3 — «Gen AI app со своими LoRA — cloud GPU дорогой, mobile хотим позже»

*Профиль: **Recraft**-like — creative / gen AI, свои модели, стартап.*

---

### Кто мы

**25 человек**, сильный research, 4 ML. Генерация **images / assets** + начали **voice** для «опиши что хочешь». Users — creators, SMB.

### Что строим

Свои модели + **LoRA** под стили. Inference сейчас **cloud GPU** (свой кластер + Nebius-style provider). Mobile app в roadmap — «assistant in pocket».

### Где болит

1. **GPU bill** — inference — **главная COGS**. Каждый новый LoRA = ещё deployment? Ещё VRAM?

2. **Speed для pro users** — «почему 4 сек на preview» — конкуренты быстрее.

3. **Mobile** — founders видят **Elastic / on-device** у конкурентов. ML team: «мы ещё **Flux tier optimize** в cloud не допилили».

### Что пробовали

| Подход | Плюсы | Минусы |
|--------|-------|--------|
| **TensorRT / custom CUDA** | Max perf on H100 | Дорого в engineer time |
| **vLLM / Triton** | Scale serving | Не переносится 1:1 на phone |
| **Elastic Models (TheStage)** для Flux/LLM | **2x–4x** в бенчмарках у них | Нужен HF token, Third-party terms, **новый vendor** |
| **Свой quant team** | Полный контроль | 2 senior ML **заняты месяцами** |

### Как Stage AI вписывается

- **Elastic Models** — «ready-to-go + **LoRA support**» на сайте = **быстрый A/B** нового стиля без полного re-export pipeline.
- **ANNA** — когда нужен **свой** checkpoint, не каталог.
- **Platform CLI** — калибровка на **Nebius** (у них в CLI есть provider) без своего k8s.
- **Modal / OpenAI-compatible serving** tutorial — если остаёмся cloud-first, но дешевле.

**Минус для нас:** не хотим, чтобы **весь** inference stack зависел от одного startup vendor. Нужен **exit plan** (artifacts, self-host).

---

# ICP 4 — «Voice notes / meeting AI — enterprise спрашивает on-prem»

*Профиль: B2B note-taker, **Phonic**-adjacent, transcription + summary.*

---

### Кто мы

**20 человек**, B2B SaaS. Запись звонков → transcript → summary → action items. Платят **teams**, не consumers.

### Где болит

1. **Enterprise security** — «audio не уходит в OpenAI» — deal breaker в EU bank pilot.

2. **Cost at scale** — 500-seat pilot = **огромные** STT minutes.

3. **Real-time** — live captions during call — latency matters.

### Что пробовали

Self-hosted Whisper on GPU; пробовали API; смотрим **on-device** для **mobile app** (field sales).

### Stage AI angle

- **Whisper elastic tiers** on-device для mobile capture.
- **SOC2** на platform (у них в pricing mentions) — checkbox для procurement.
- Cloud **containers** pre-optimized — если on-prem GPU customer.

---

# Сводная таблица ICP → боль → Stage AI hook

| ICP | Мы такие | Главная боль | Что пробовали | Stage AI заходит через |
|-----|----------|--------------|---------------|------------------------|
| **Language app** | 2M MAU, voice tutor | API $ + latency + offline | Cloud, llama.cpp fail | Elastic voice + compile + hybrid path |
| **Wearable** | Smart glasses, 12 FTE | Latency, battery, privacy | Cloud MVP, Core ML pain | Apple compile, Whisper tier, benchmarks |
| **Gen AI + LoRA** | Creative, own models | GPU COGS, speed | TRT, vLLM | Elastic + LoRA, ANNA, Nebius CLI |
| **Voice B2B** | Meeting AI | Security, STT minutes | Self-host Whisper | On-device STT + enterprise checkboxes |

---

# Шаблон «как спросить на Reddit» (для outreach / community)

> **Title:** Anyone shipped STT → small LLM → TTS fully on-device for iOS (phone as hub for wearable)?
>
> **Body:** We're a 12-person team, glasses + phone architecture. Cloud bill and latency killing us. Tried llama.cpp but OOM on mid Android and thermal throttling after 90s ([similar thread vibes](https://dev.to/vishal_sharma_nataris/we-built-a-p2p-ai-inference-network-that-runs-on-android-phones-heres-what-we-learned-3lhb)). Looking at pre-compiled stacks (TheStage Elastic, etc.) vs rolling our own Core ML export ([HN pain](https://news.ycombinator.com/item?id=37082447)). For those who shipped: did you tier models S/M/L? How bad was LoRA recompile?
>
> *Not asking for vendor ads — want war stories.*

---

# Для звонка с TheStage

Спросить по каждому ICP:

1. **Кто из текущих клиентов** ближе к какой истории?
2. **Где вы выиграли** vs проиграли против «мы сами llama.cpp»?
3. **LoRA** — реальный production или roadmap?
4. **Orchestration** — когда можно честно продавать ICP 1 и 2?

---

*Тон намеренно разговорный — для внутреннего GTM / empathy map, не для копипасты в Reddit без адаптации.*
