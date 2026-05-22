# TheStage AI — briefing: понимание предметной области

**Для:** синхронизации с TheStage AI (StageAI project)  
**Роль документа:** **главный контекст по продукту** — сюда стекаются выводы из research, voice notes и GTM; остальные файлы в `context/` — углубления и рабочие артефакты.  
**Язык:** простой, без лишнего жаргона (глоссарий — в конце)  
**Собрано из:** voice notes заказчика, [app.thestage.ai](https://app.thestage.ai/), [docs.thestage.ai](https://docs.thestage.ai/), совместного разбора  
**Дата:** 2026-05-17 · **обновлено:** 2026-05-22 (finance-first buyers, Vuzix savings map, exec vs ML; **где AI** по клиентам: ☁️/📱/🕶️)

> Углубления: [Customer Input](Customer%20Input.md) · [Website Research](Website%20Research%20%E2%80%94%20app.thestage.ai.md) · [Documentation Research](Documentation%20Research%20%E2%80%94%20docs.thestage.ai.md) · [Diagram workflow](Diagram%20%E2%80%94%20ML%20workflow%20classic%20vs%20Stage%20AI.md) · [ICP stories (Reddit)](ICP%20use%20cases%20%E2%80%94%20Reddit-style%20stories.md) · **[POV how to build](POV%20%E2%80%94%20how%20to%20build%20(Strategic%20POV%20framework).md)** ([ESC method](../../gtm_stuff/ESC%20&%20Whyzer/Strategic%20POV%20Development.md)) · [POV finance-first](POV%20%E2%80%94%20finance-first%20outbound%20(enterprise%20wearables).md) · [Roadmap](StageAI%20Roadmap.md)

**Содержание:** [1 Кто такие](#1-кто-такие-thestage-ai-в-одном-абзаце) · [2 Бизнес](#2-что-мы-понимаем-про-их-бизнес-сейчас) · [3 Технология + ICP (§3.11)](#311-icp-четыре-уровня-s--p--l--w) · [4 Voice](#4-voice-on-device--предметная-область) · [5 Юз-кейсы](#5-практические-юз-кейсы-глубина) · [6–11](#6-два-gtm-motion-как-продавать-разным-покупателям) · [12–15 Вопросы / глоссарий](#12-что-понятно--не-очень--непонятно-для-звонка)

**Легенда достоверности в этом документе:**  
- **Факт** — voice notes, docs.thestage.ai, или явный press с цитатой.  
- **Рабочая гипотеза** — логика GTM / ICP, нужно подтвердить на звонке.  
- **Шаблон ICP** — учебный пример в [ICP stories](ICP%20use%20cases%20%E2%80%94%20Reddit-style%20stories.md), не verified architecture клиента.

---

## 1. Кто такие TheStage AI (в одном абзаце)

**TheStage AI** — компания, которая помогает **запускать нейросети быстрее, легче и дешевле** при inference (когда модель уже отвечает пользователю). Они сжимают и компилируют модели под **NVIDIA GPU** и **Apple Silicon** (телефон), дают **готовые ускоренные модели** и платформу для ML-команд. Сильный повторяющийся спрос — **голосовые ассистенты on-device** (приложения, wearables, AI tutor). В перспективе хотят стать **оркестратором on-device** (цепочка микрофон → текст → LLM → голос), аналог **LiveKit**, но локально на устройстве.

---

## 2. Что мы понимаем про их бизнес сейчас

### Клиенты

| Факт | Пояснение |
|------|-----------|
| **~6 paying clients** | Есть платящие, не «ищем PMF с нуля» |
| **Nebius** | Скорее единственный **infra / enterprise-тип** (GPU cloud) |
| **Recraft, Brilliant Labs, Phonic** и др. | **Стартапы**, не классический enterprise |
| Шестой клиент | В voice notes не назван (в Plan также **Usmile**) |

### Якорные клиенты — как читать сегменты (рабочая карта)

**Где AI:** **☁️** = облако (GPU/серверы) · **📱** = телефон (app, on-device) · **🕶️** = wearable / IoT / чип в устройстве · **🔀** = несколько мест сразу. **Сейчас** = как работает продукт сегодня; **цель** = куда мигрируют / куда целится TheStage. Статус: **факт** (подтверждено) · **гипотеза** · **TBD** (уточнить на звонке). Детальная карта paying + cases: таблицы ниже; сводка по архитектуре: §3.9.

| Клиент (публично / из notes) | Тип | **Где AI (сейчас → цель)** | Вероятная боль | Продуктовый слой TheStage | Практический угол |
|------------------------------|-----|---------------------------|----------------|---------------------------|-------------------|
| **Praktika** | AI language tutor, ~2M active | **☁️ сейчас** → **📱 iOS on-device** (Android **TBD**) | Cloud inference cost × MAU; latency | Optimize + Deploy (Apple); позже SDK | Гибрид STT local → LLM cloud → LLM local |
| **Brilliant Labs** | Smart glasses / wearables | **🔀** **📱** phone (TheStage press) + **🕶️** on-glass NPU (Alif); **☁️** возможно для части сценариев — **TBD** | Latency; privacy | Deploy phone path; не Qualcomm on-glass | §3.8 — не «только iPhone hub» |
| **Recraft** | Gen AI, LoRA | **☁️** NVIDIA **сейчас** → **📱** mobile **гипотеза** phase 2 | GPU COGS; preview speed | Elastic (Flux) + ANNA + cloud | Cloud-first |
| **Phonic** | B2B voice agents | **☁️** enterprise serving **гипотеза**; **📱** capture on-device для mobile — **уточнить** | Security; STT @ scale | Whisper tiers + cloud containers | Не meeting-notes без verify |
| **Nebius** | Infra / GPU cloud | **☁️** (их клиенты на GPU); TheStage = софт **на** их облаке | Cost perf для **их** клиентов | Platform + license | Канал, не voice app |
| **SaladCloud** (case) | Inference provider | **☁️** distributed GPU network | $/inference | Optimize + containers | Proof case |

*Цифры по экономике Praktika и чекам по клиентам — **уточнить на звонке**; таблица для GTM-логики, не для публичных claims.*

### Реестр известных клиентов и кейсов (на май 2026)

**Источники:** voice notes / Plan v0.1 (~6 paying), [about.thestage.ai/cases](https://about.thestage.ai/cases), GTM Framework (SaladCloud), industry press (Brilliant Labs + TheStage).  
**Важно:** paying clients ≠ все кейсы на сайте; **Praktika** в публичных материалах TheStage **не названа**; **6-й paying client** в записях не идентифицирован.  
**Колонка «Где AI»:** см. легенду в § «Якорные клиенты» выше; **не** verified architecture — уточнять на discovery.

#### A. Paying clients (~6) — из разговоров с заказчиком

| Компания | Сайт | Кто они | **Где AI (сейчас → цель / TheStage)** | Связь с TheStage (по нашим notes) | Статус |
|----------|------|---------|----------------------------------------|-----------------------------------|--------|
| **Recraft** | [recraft.ai](https://www.recraft.ai) | Gen AI: image/vector, LoRA, 3M+ users | **☁️** NVIDIA **сейчас** · **📱** mobile on-device — **гипотеза** (phase 2) | Elastic (Flux), ANNA; GPU COGS | Paying; не на cases page |
| **Nebius** | [nebius.com](https://nebius.com) | AI cloud (H100/B200…) | **☁️** — inference **у конечных клиентов Nebius** на их GPU; TheStage = Platform на Nebius | CLI `--provider Nebius`, ~$1k/GPU/год license | Партнёр/infra |
| **Brilliant Labs** | [brilliant.xyz](https://brilliant.xyz) | AI-очки **Halo** | **🔀** **📱** paired smartphone (TheStage + Neuphonic, press) + **🕶️** Alif NPU **on-glass** (не TheStage compile) · **☁️** — **TBD** | ANNA / deploy **phone path** | Press [TechDay 2026](https://techday.co.nz/story/privacy-first-ai-smart-glasses-run-models-on-device) |
| **Phonic** | [phonic.co](https://phonic.co) | Speech-to-speech **voice agents**, enterprise | **☁️** serving **гипотеза** (sub-500ms cloud) · **📱** on-device capture для mobile sales — **уточнить** | Voice inference / latency | Paying; продукт TheStage **TBD** |
| **Usmile** | [usmile.com](https://www.usmile.com) | Smart-щётки, AI brushing | **🕶️** on-device в щётке/IoT **гипотеза** · **☁️**/**📱** — **неизвестно** | Имя в 6 paying only | **TBD**; не glasses/voice ICP |
| **6-й клиент** | — | — | **?** | — | Не идентифицирован |

#### B. Якорный кейс / фокус (не обязательно в «6 paying»)

| Компания | Сайт | Кто они | **Где AI (сейчас → цель / TheStage)** | Связь с TheStage | Статус |
|----------|------|---------|----------------------------------------|------------------|--------|
| **Praktika** | [praktika.ai](https://www.praktika.ai) · [App Store](https://apps.apple.com/us/app/praktika-ai-language-tutor/id1624701477) | AI language tutor, **~2M active** | **☁️** cloud **сейчас** (voice notes) → **📱** on-device **цель** (iOS first; Android **TBD**) · возможен **🔀** STT local + LLM cloud/local | Cloud → on-device migration; главный focus | **Факт** apps; split OS — **TBD** |

#### C. Публичные кейсы на [about.thestage.ai/cases](https://about.thestage.ai/cases)

| Кейс / клиент | Сайт | Домен | **Где AI** | Заявленный результат (TheStage) |
|---------------|------|-------|------------|----------------------------------|
| **SaladCloud** | [salad.com](https://salad.com) | Distributed inference | **☁️** GPU network (Salad nodes) | **10k+ images per dollar** (ANNA) |
| **Wallarm** | [wallarm.com](https://www.wallarm.com) | API security ML | **☁️** / **сервер CPU** (1 Gb/s per core — не phone) | **99%** malware detection |
| **Huawei P50/P60** | [consumer.huawei.com](https://consumer.huawei.com) | Camera HDR | **📱** **🕶️** Snapdragon 888 **NPU on-phone** (кастом compile) | 4K **&lt;1s**, **6×** speedup |
| **Nissan** | [nissan-global.com](https://www.nissan-global.com) | Automotive R&D | **☁️** / lab pipeline **гипотеза** (EEG model) | **+7%** accuracy |
| **On-chain image compression** | — | Web3 storage | **☁️** / batch **гипотеза** | До **100×** vs PNG |

*Huawei / Nissan — скорее **R&D / OEM** кейсы, не типичный ICP voice startup.*

#### D. Не клиенты, но важные интеграции в продукте

| Имя | Сайт | Роль |
|-----|------|------|
| **Amazon AWS** | [aws.amazon.com](https://aws.amazon.com) | GPU provider в Platform CLI |
| **Nebius** | [nebius.com](https://nebius.com) | GPU provider в CLI (см. также paying выше) |
| **Model publishers** (OpenAI, Meta, BFL, Mistral…) | HF / vendor sites | Elastic Models marketplace, не «клиенты» TheStage |

---

### Продукты в разговоре

- **TheStage platform** — софт + CLI + (частично) cloud GPU.
- **Sulfer** — недавно запустили, детали не раскрыты.
- Скоро: **SDK + self-service** — массовый вход для разработчиков.

### Монетизация (как говорил заказчик)

- **Usage-based**, софт **~$1 000/год за GPU** (сама GPU оплачивается отдельно у провайдера).
- Типичный деплой: **30–100 GPU/год**; в облаке (Nebius) объёмы могут быть **значительно выше**.

### GTM-ситуация

- Спрос и pipeline **есть** (в т.ч. ~15 тёплых лидов, сотни в воронке — по внутреннему плану).
- Главная боль — **не лиды**, а **системный execution**: outbound, partnerships, self-service funnel.

### Цели роста (не путать с фактом сегодня)

| Цифра | Что это |
|-------|---------|
| **~5M MAU** | **Амбиция** — суммарно по портфелю partner-приложений в будущем, **не** текущая база TheStage |
| **Praktika ~2M active** | Отдельный якорный кейс: сейчас **cloud**, переводят на **on-device** |

---

## 3. Что входит в их технологию и офер

Публично это **не один продукт**, а **стек из четырёх слоёв**. Важно не смешивать их в одном предложении для клиента.

### Слой A — Оптимизация inference (ядро)

**Что делают:** уменьшают модель и ускоряют inference без полного переобучения.

| Компонент | Простыми словами |
|-----------|------------------|
| **ANNA** | Автоматически подбирает, как сжать модель (качество ↔ размер ↔ скорость), по сути «слайдер» |
| **Qlip** | Framework: квантизация, compile, deploy **вашей** модели |
| **Elastic Models** | **Уже готовые** ускоренные модели (Whisper, Llama, Mistral, Flux…) |
| **Tiers S / M / L / XL** | Четыре готовых уровня сжатия: от «максимум скорости» до «почти как оригинал» |

**Технически:** compile под **NVIDIA** (TensorRT и др.) и **Apple Silicon**; в docs — метрики **tps**, **ttft**, **max_memory_mb**.

### Слой B — Platform / Cloud (инфраструктура)

**Что делают:** дают **GPU и среду** для экспериментов и иногда serving — это **не** сама магия ускорения.

- Аренда GPU (**Amazon, Nebius**) или **свои** сервера.
- Docker-контейнеры, проекты, `thestage project run` с ноутбука.
- Удобно гонять калибровку ANNA и бенчмарки без своего кластера.

**На сайте:** «Cloud for AI workloads — Rent GPUs…» — про **compute**, не про «мы ускоряем inference» как отдельную кнопку.

### Слой C — Deploy / Serving

- **Cloud:** inference engine (Triton), OpenAI-compatible API в туториалах (Modal).
- **On-device:** Apple compile path, **on-device SDK** (в маркетинге; детали API — слабее в docs).

### Поддерживаемые платформы (важно для ICP)

Публично задокументированный **compile / on-device SDK** — не «любой смартфон», а узкий набор целей.

| Слой | Платформы | Статус |
|------|-----------|--------|
| **Cloud / on-prem inference** | **NVIDIA GPU** (CUDA, TensorRT-путь, Triton) | ✅ Основной продукт (Elastic, Qlip, Platform) |
| **On-device (телефон)** | **Apple Silicon** (M1–M4), Core ML path | ✅ Маркетинг + Apple Compiler API в docs |
| **Edge embedded** | **NVIDIA Jetson** | ✅ Упоминается в «Export to device» на сайте |
| **Android / Snapdragon / Qualcomm NPU** | — | ❌ **Нет** в product matrix и Qlip compiler API |
| **Исключение** | Huawei P50/P60 (Snapdragon 888 NPU) в cases | ⚠️ Похоже на **кастомный** проект (HDR camera), не self-serve SDK |

**Вывод для GTM (не перегибать):**

- **«Большинство девайсов не подходят»** — верно, если продавать **универсальный on-device SDK на любой телефон** (глобально ~70% парка — Android / Snapdragon).
- **Не верно** для всего бизнеса TheStage: стартап может годами быть клиентом только на **NVIDIA cloud** (Praktika сейчас cloud → device; Nebius-type).
- **Типичный fit on-device сегодня:** **iOS** (tutor, **phone-as-hub** для wearables), опционально **Jetson** в железе; **гибрид** — local на iPhone + тяжёлое в cloud на NVIDIA.

| Сценарий клиента | Fit сейчас |
|------------------|------------|
| Оптимизация inference в **облаке на NVIDIA** | ✅ Сильный |
| **iOS** on-device (voice, glasses → phone hub) | ✅ В зоне roadmap / SDK |
| **Android-only**, inference на Snapdragon в APK | ❌ Вне стандартного продукта |
| Android app, но on-device только на **iPhone** у части users + cloud для Android | ⚠️ Два стека у клиента |
| **Jetson** в устройстве / edge-box | ✅ В маркетинге |

**Открытые вопросы им:** roadmap **Android / QNN / Snapdragon**; Praktika on-device **iOS-first** или оба OS; Brilliant Labs — **доля** compute на iPhone vs на очках (Alif NPU); Huawei-кейс — повторяемый продукт или one-off R&D.

### 3.6 Jetson — что это и зачем в офере

**Jetson** — линейка **NVIDIA** edge-модулей (Orin, Nano и др.): не телефон и не SoC в consumer-очках, а **встроенный AI-компьютер** в роботах, smart-камерах, промышленных боксах, иногда в «тяжёлом» wearable hub.

| | Jetson | Apple Silicon (iPhone) | Snapdragon в очках |
|---|--------|------------------------|-------------------|
| Кто ставит | OEM / hardware team | Consumer phone | Glasses OEM |
| TheStage path | ✅ В marketing «Export to device» | ✅ Apple Compiler / SDK | ❌ Нет self-serve |
| Типичный wearable | Edge-box рядом с линией, не в дужке | Paired phone hub | Inference **на** очках |

**Для GTM:** Jetson = **тот же NVIDIA-стек**, что cloud (Qlip/Elastic + compile), но на **фиксированном edge**. Не замена «очки + iPhone», если продукт клиента — mass-market glasses с телефоном в кармане.

**Факт:** Jetson упоминается на сайте/docs. **Не факт:** именованный paying client «только на Jetson» в наших материалах нет.

### 3.7 Wearables: рынок, Snapdragon и «~80% недоступны»

**Рабочая формулировка (не перегибать):**

| Если продаём… | «Большинство wearables не fit» |
|---------------|-------------------------------|
| **On-device compile на SoC очков** (Qualcomm / Android glasses) | ✅ **Да** — у TheStage нет стандартного Snapdragon/QNN SDK |
| **On-device на любом Android-телефоне** (companion app) | ✅ **Да** — тот же gap |
| **Cloud inference на NVIDIA** (STT/LLM/TTS в облаке, очки только mic/display) | ❌ **Нет** — wearables с AI **остаются** в TAM; другой слой (A+B) |
| **iOS companion + hybrid** | ⚠️ Часть рынка (см. prospect map §3.9) |

**Snapdragon в smart glasses (индустрия, не TheStage roadmap):** RealWear, Vuzix, DigiLens ARGO, ThirdEye, Envision и др. часто крутят AI **на Android / на устройстве** — для **on-device TheStage** это слабый fit; для **cloud optimize** — нормальный разговор.

### 3.8 Нет iOS app у клиента — что всё равно можно продать

```
Есть iOS app? ──НЕТ──► Apple on-device / SDK  ❌
        │
        ├── Есть cloud / свой GPU inference? ──ДА──► ✅ Elastic + Qlip + ANNA (NVIDIA)
        │                                        ✅ Platform / containers / per-GPU license
        │
        ├── Только Android on-glass / Snapdragon? ──► ❌ стандартный on-device TheStage
        │                    └── обход: cloud NVIDIA ИЛИ ждать roadmap / custom (Huawei-type)
        │
        └── Edge box / Jetson в архитектуре? ──ДА──► ✅ Jetson export path (маркетинг)
```

| Ситуация клиента | TheStage сегодня | Комментарий |
|------------------|------------------|-------------|
| Нет приложения вообще, только firmware на очках | Cloud **или** Jetson, если их архитектура такая | Не «SDK в APK» |
| Android app, inference в cloud | ✅ Optimize serving | Типичный путь до on-device |
| Android app, хотят inference **в APK** на Snapdragon | ❌ | llama.cpp / cloud / другой вендор |
| iOS + Android apps, on-device только iOS | ✅ iOS + ⚠️ Android users на cloud | Два продукта у клиента |
| Wearable + **обязательный** iPhone companion | ✅ Hybrid / hub (если iOS) | Brilliant-class |

### 3.9 Клиенты: где запущен AI (подтверждено / inferred)

*Дублирует колонку «Где AI» в реестре §2 (таблицы A–C) — здесь с источниками и оговорками.*

| Компания | ☁️ Облако | 📱 Телефон | 🕶️ Device | Источник | Статус |
|----------|:---:|:---:|:---:|----------|--------|
| **Brilliant Labs** | ◐ | ✓ TheStage press | ✓ Alif on-glass | [TechDay 2026](https://techday.co.nz/story/privacy-first-ai-smart-glasses-run-models-on-device); Alif press | **Press**; iOS/Android split **TBD** |
| **Praktika** | ✓ сейчас | ◐ → on-device | — | App Store; voice notes | **Факт** ☁️; **TBD** OS split |
| **Recraft** | ✓ | ◐ phase 2 | — | Notes + GTM | **Гипотеза** 📱 |
| **Phonic** | ✓? | ◐? | — | phonic.co | **Уточнить** |
| **Nebius** | ✓ (ecosystem) | — | — | Docs CLI | **Факт** |
| **Usmile** | ? | ? | ✓? IoT | usmile.com | **TBD** |
| **SaladCloud** | ✓ | — | — | Case blog | **Факт** |
| **Wallarm** | ✓ | — | — | thestage.ai/cases | **Факт** |
| **Huawei** | — | ✓ NPU | — | Case | **Факт** (кастом) |
| **Vuzix** (prospect) | ✓ partner/R&D | — | ✓ AR1 + local Speech SDK | §3.12; Vuzix illustration | TheStage **☁️** only |

**Важная коррекция (2026-05-20):** формулировка «Brilliant = BLE → только iPhone, inference не на очках» была **рабочей гипотезой** в ICP story, **не** цитатой из voice notes. Публично: **privacy-first hybrid**, TheStage + Neuphonic; on-glass NPU (Alif) — **железо Brilliant**, не документированный compile-path TheStage на Qualcomm.

### 3.10 Prospect map: кому питчить on-device vs cloud (не клиенты)

> **Не путать с §3.11:** списки **A / B / C** ниже — **размер рынка / reachability**, не tech-сегменты **S1–S7** и не приоритеты **P0–P2**.

**Список A — startup glasses (проверять S4 + iOS):**

| Компания | Сайт | Почему в списке |
|----------|------|-----------------|
| Halliday | [halliday.ai](https://www.halliday.ai) | AI glasses, consumer |
| Gobi | (verify domain) | AI glasses startup tier |
| Even Realities | [evenrealities.com](https://evenrealities.com) | Lightweight AR + AI |
| Mentra | [mentraglass.com](https://mentraglass.com) | Open glasses + dev community |

**Список B — mid-enterprise wearables (часто S7 on-glass → питч S1 cloud):**

| Компания | AI на wearables | On-device fit TheStage |
|----------|-----------------|-------------------------|
| RealWear | ✅ voice assistant industrial | ❌ on-glass Snapdragon → ✅ cloud NVIDIA |
| Vuzix | ✅ | то же |
| DigiLens (ARGO) | ✅ | то же |
| ThirdEye | ✅ | то же |
| Envision | ✅ accessibility AI | то же |

**Список C — mega-cap (Meta, Apple, Google, Samsung):** **не outbound landmarks** — свой стек, procurement. Только partnership fantasy.

**Lookalike по размеру ≠ lookalike по технологии:** Halliday, Mentra, Gobi, Even Realities, See It AI — назначать **S-сегмент** (§3.11), не копировать список «как Brilliant по headcount».

### 3.11 ICP: четыре уровня (S · P · L · W)

**Главное:** **S1–S7 — не тиры приоритета.** Это **tech-сегменты** (классификация: где крутится inference).  
**P0–P2** — отдельно: **приоритет outbound** сейчас.  
**L1–L6 / W1–W4** — **landmark-паттерны** (кого искать как «следующий X»).

| Код | Название | Вопрос | Пример |
|-----|----------|--------|--------|
| **S** | **Segment** (архитектура) | Где inference? | Brilliant = **S4** |
| **P** | **Priority** (GTM сейчас) | Кого звонить в первую очередь? | Praktika-line = **P0** |
| **L** | **Landmark** (широкий портфель) | Повторяемый паттерн + имена | L1 = следующая Praktika |
| **W** | **Wearable landmark** (тема фаундера) | То же, но **только voice + wearables** | W2 = следующие AI glasses + iOS |

*Раньше в черновиках использовали **T1–T7** = то же, что **S1–S7**.*

#### North star фаундера vs тактический фильтр

**Факт из voice notes / Plan:** тема компании — **voice + wearables** (+ mobile AI apps), vision — **on-device orchestration** (STT→LLM→TTS), «unlock wearables use case», SDK под smart glasses.

**Это не отменяет S-сегменты.** Это **внешний контур**, внутри которого мы режем по архитектуре:

```
North star (фаундер): voice + wearables + on-device orchestration
        │
        ├── В теме, P0 сейчас:  S2→S3 (Praktika), S1 cloud voice
        ├── В теме, flagship wearable:  S4 (Brilliant-line) — часто P1, не P0
        ├── В теме, вход без on-device:  S7 wearables → питч S1 cloud (RealWear-class)
        └── Вне north star, но paying:  S1 Recraft, S6 Nebius — revenue / proof
```

**Синхронизация с фаундером (одна фраза):**  
> Мы остаёмся в **voice + wearables**. **S-сегмент** говорит, **какой продукт** TheStage обещать (phone compile vs cloud vs не сейчас). **P-приоритет** — кого искать в pipeline в этом квартале.

#### Семь tech-сегментов (S1–S7)

| ID | Сегмент | Где inference | TheStage fit | Питч (один слой) |
|----|---------|---------------|--------------|------------------|
| **S1** | **NVIDIA cloud @ scale** | GPU cloud / own cluster | ✅ **Сильнейший** | A: Elastic + Qlip + ANNA |
| **S2** | **Cloud → on-device migration** | Сейчас cloud → телефон | ✅ **Якорный narrative** | A→C: tiers + Apple compile |
| **S3** | **iOS on-device (app = продукт)** | iPhone/iPad | ✅ **SDK / Deploy** | C (+ A) |
| **S4** | **Wearable + iOS companion (hybrid)** | Phone path + часто on-glass NPU | ⚠️ **Частичный** — только **phone path** | C на companion |
| **S5** | **Jetson / edge-box** | NVIDIA edge | ✅ В marketing | A+C export |
| **S6** | **Infra / channel** | Продают GPU другим | ✅ Nebius-модель | B + license |
| **S7** | **Snapdragon / Android on-device only** | APK или on-glass, без iOS path | ⚠️ **Скоро** — Qualcomm поддержка разработана, **не в публичном релизе** | S1 cloud сейчас; on-device — **upcoming, не обещать до анонса** |

*S7 обновление (май 2026):* Qualcomm-поддержка **разработана**, но **не в публичном релизе**. До официального анонса — не обещать on-device клиентам. Питч: «S1 cloud сейчас + on-device unlock скоро — зайти раньше рынка». Huawei-style кастом — всё равно не масштабируемый ICP.

##### Почему Brilliant Labs = **S4** (не S3, не S7)

| | **S3** (Praktika) | **S4** (Brilliant) | **S7** (Android-only glasses) |
|---|-------------------|--------------------|--------------------------------|
| Продукт | **Телефон = продукт** | **Очки = продукт**, phone = companion | Очки без нормального iOS path |
| Inference | В **app** на iPhone | **Split:** phone (TheStage press) + on-glass NPU (Alif) | На **Snapdragon** в дужке |
| TheStage | Полный phone path | ⚠️ Только **phone path** | ⚠️ on-device **в разработке** (не релиз); S1 cloud сейчас |

Brilliant **не «tier 4 по важности»** — это **четвёртый архитектурный класс**. По **P-приоритету** Praktika (S2→S3) часто **выше**, чем Brilliant (S4), хотя оба в теме voice/wearables фаундера.

#### Карта клиентов и кейсов по S-сегментам (май 2026)

| Компания | S | **☁️ Облако** | **📱 Телефон** | **🕶️ Device** | Сводка (сейчас → цель) | В теме voice/wearables? | P |
|----------|---|:---:|:---:|:---:|------------------------|-------------------------|---|
| **Praktika** | S2→S3 | ✓ сейчас | ◐ цель iOS | — | **☁️ → 📱** | ✅ voice app | **P0** |
| **Brilliant Labs** | S4 | ◐ TBD | ✓ TheStage path | ✓ Alif NPU | **🔀 📱 + 🕶️** | ✅ flagship wearable | **P1** |
| **Phonic** | S1 | ✓ гипотеза | ◐ capture? | — | **☁️** (+ 📱?) | ✅ voice | **P1** |
| **Recraft** | S1→S3? | ✓ сейчас | ◐ phase 2 | — | **☁️ → 📱?** | ⚠️ gen AI | **P1** |
| **Nebius** | S6 | ✓ (клиенты) | — | — | **☁️** infra | ❌ | **P2** |
| **Usmile** | **?** | ? | ? | ✓ IoT? | **🕶️?** | ⚠️ IoT | уточнить |
| **SaladCloud** | S1 | ✓ | — | — | **☁️** | ❌ | proof |
| **Wallarm** | S1 | ✓/CPU | — | — | **☁️** security | ❌ | другой vertical |
| **Huawei case** | S7 custom | — | ✓ NPU | — | **📱** Snapdragon | ❌ | one-off |

*✓ = основной путь сейчас · ◐ = частично / в миграции / TBD · — = не в scope.*

**Prospects (не paying, для сравнения):** **Vuzix** (S7→W3) — **🕶️** voice on AR1 chip + **☁️** partner/R&D cloud (TheStage = **☁️** сейчас · **Qualcomm on-device в разработке** → стратегически интересны) · **RealWear** — то же W3-паттерн.

#### Landmarks **L** (весь портфель) и **W** (voice + wearables фаундера)

**L — широкие** (включая Recraft, Nebius, Salad):

| ID | Паттерн | S | Ориентиры |
|----|---------|---|-----------|
| **L1** | Следующая Praktika | S2/S3 | iOS voice apps @ MAU |
| **L2** | Следующий Recraft | S1 | Gen AI + LoRA на GPU |
| **L3** | Следующий Brilliant (phone path) | S4 | Halliday, Even Realities, Mentra* |
| **L4** | Следующий Phonic | S1 | B2B voice agents |
| **L5** | Следующий Nebius | S6 | GPU clouds |
| **L6** | Следующий SaladCloud | S1 | Inference providers |

**W — внутри темы фаундера** (voice / wearables / mobile voice AI):

| ID | Паттерн | S | Ориентиры | Питч |
|----|---------|---|-----------|------|
| **W1** | Voice @ MAU | S2→S3 | AI tutors, companions | on-device iOS |
| **W2** | AI glasses + voice + **iOS** | S4 | Halliday, Even Realities, Mentra* | phone path only |
| **W3** | Wearable + voice, пока **cloud** | S7→S1 | RealWear, Vuzix (список B) | cloud NVIDIA сейчас; **Qualcomm on-device в разработке** — unlock скоро, зайти раньше рынка |
| **W4** | B2B voice @ scale | S1 | Phonic-class | containers + Whisper |

\* *verify iOS companion перед outbound.*

**Anti-landmarks:** Meta, Apple, Google XR, Samsung — не operational W/L; RealWear и др. — только **W3** (cloud), не **W2** (on-device glasses SDK).

#### Чеклист ICP (~60 сек)

1. **В теме фаундера?** voice / wearable / mobile voice AI  
2. **S-сегмент:** где inference (cloud / iPhone / hybrid / Snapdragon)  
3. **iOS companion?** нет → не обещать S3/S4 on-device · S7 Snapdragon — on-device **в разработке**, не обещать до публичного релиза  
4. **Scale / боль:** COGS, latency, privacy — не «AI в деке»  
5. **Один слой** в первом касании (A/B/C)  
6. **P:** P0/P1/P2 — не путать с номером S

#### Приоритет outbound (P) — отдельно от S

| P | S-сегменты | Почему |
|---|------------|--------|
| **P0** | **S2, S3** | SDK + Praktika narrative; voice @ MAU |
| **P1** | **S1**, **S4** (if iOS verified), **W2** | Revenue + flagship wearable story |
| **P2** | **S5**, **S6** | Jetson edge; infra channel |
| **Deprioritize** | **S7** без cloud | До Android/QNN roadmap |

**W2 (glasses) может быть стратегически важнее для фаундера, но тактически P1**, пока S4 partial fit и меньше scale, чем W1.

### 3.12 Finance-first outbound (S7 / public OEM) — не только ML

Для аккаунтов **S7 → W3** (AI на Snapdragon on-glass, weak on-device SDK) и **публичных** OEM под IR-давлением — отдельный GTM-режим: продавать **variable inference COGS + OEM benchmark spec**, не «compile на очки».

| Режим | Аудитория | Lead message |
|-------|-----------|--------------|
| **Technical-first** | VP Eng, ML | tiers, tps, ttft, export time |
| **Finance-first** | CFO, CEO, VP BD/OEM | $/1k voice sessions, margin per pilot, RFP-grade SLO |

**Как строить POV (любой аккаунт):** [POV — how to build](POV%20%E2%80%94%20how%20to%20build%20(Strategic%20POV%20framework).md) — 3 stages (hypothesis → consensus → exec), MUD, Strategic Soundbite, value pyramid; методология [ESC & Whyzer](../../gtm_stuff/ESC%20&%20Whyzer/Strategic%20POV%20Development.md).

**Playbook S7 / public OEM:** [POV — finance-first outbound](POV%20%E2%80%94%20finance-first%20outbound%20(enterprise%20wearables).md) (VUZI, savings map, CEO/CFO vs ML).

**Worked illustration (VUZI):** [Vuzix — POV and business case (illustration)](Vuzix%20%E2%80%94%20POV%20and%20business%20case%20(illustration).md) — полный GTM-флоу: MDP, POV, metrics, unit economics (`12k × $5`), business case, exec checklist (illustration only). **Словарь для нетехнических** — в начале того же файла.

**GTM strategy (finance-first motion):** [GTM — finance-first motion (strategy & prep)](GTM%20%E2%80%94%20finance-first%20motion%20(strategy%20%26%20prep).md) — landmark-клиенты (W3), метрики Tier 1–3, сигналы таргетинга, financial literacy checklist, operational backlog.

**Связка с Roadmap:** недели 2–4 — POV template, consensus checklist, dual playbooks, champion-led exec.

#### 3.12.1 CEO / CFO в сделке — когда да и как не конфликтовать с ML

**Рабочее предположение:** для **public / distressed OEM** (VUZI-class) **разумно планировать** участие **CEO и CFO** (sponsor + хотя бы одна встреча), не только VP Engineering. Для **W1** (Praktika-like app) economic buyer чаще **product + ML + CFO позже**.

| Сигнал аккаунта | CEO / CFO в сделке | ML / platform — главный |
|-----------------|--------------------|-------------------------|
| Microcap, going-concern в 10-K | ✅ | исполняют PoC |
| AI в IR/CES, выручка от hardware | ✅ story + budget | строят stack |
| OEM / licensing model | ✅ + VP BD | RFP + integration |
| PoC &lt; ~$50–100k, без multi-year | может делегировать | **часто достаточно** eng-led |
| Series B voice app, нет IR давления | реже | **eng-led** |

**Два языка — одна сделка:**

| Персона | Ценность (lead) | Proof |
|---------|-----------------|-------|
| **CEO** | OEM differentiation; AI metric для partnerships/IR | «Metric on reference design» |
| **CFO** | Variable COGS cloud AI; ROI PoC | $ in → GPU $ out; $/1k sessions |
| **VP BD / OEM** | RFP-ready AI appendix | Benchmark sheet |
| **ML / platform** | tps, ttft, tiers; time-to-deploy | PoC benchmark |

**Правила:**

- Executive mail — **стратегия + P&L**; technical appendix отдельно (не tier S/M/L в первых 10 строках CEO).  
- **Не обходить ML:** CEO intro → сразу VP Eng на scope PoC.  
- **Один PoC → два deliverable:** finance memo (CFO) + tech report (Eng).  
- **Не обещать CFO** срез $8M OpEx — только **variable inference** и **OEM pilot economics**.

**Схема потоков:** executive (why + budget) → technical (how + proof) → sponsor sync → Phase 1. Детали: [POV doc §12](POV%20%E2%80%94%20finance-first%20outbound%20(enterprise%20wearables).md#12-executive-vs-ml-двухуровневая-продажа).

**CRM-тег (Roadmap):** `buyer_motion: exec-led | eng-led | hybrid`.

#### 3.12.2 Где наибольшие savings (пример Vuzix) — не везде

TheStage **не** режет waveguide, payroll или Snapdragon on-glass. Максимум — **там, где уже есть или появится cloud / GPU inference**.

| # | Зона (VUZI-class) | Тип savings | TheStage | Величина |
|---|-------------------|-------------|----------|----------|
| 1 | **Cloud AI** (partners, enterprise, multimodal backend) | Variable GPU COGS | Elastic + ANNA (слой A) | **Наибольшая** (если cloud есть) |
| 2 | **OEM pilots / licensing** | Margin per design-win; меньше R&D на SKU | Benchmark + tiers | **Высокая** (стратегически) |
| 3 | **Internal R&D GPU** | GPU-hours на пресейл | Platform + Elastic | Средняя |
| 4 | iPhone companion (if any) | On-device $ | Apple compile | Средняя, unconfirmed |
| 5 | Jetson / defense edge | Edge inference | Jetson path | Ниша |
| 6 | On-glass AR1 / M400 Speech SDK | — | ❌ self-serve | **~0** сегодня |

**Архитектурная оговорка (Vuzix):** M400 — embedded [Speech SDK](https://support.vuzix.com/docs/overview) (local); Ultralite — AI on **Snapdragon AR1**; партнёры (e.g. Ramblr) — **cloud** contextual AI. Если **весь** новый AI только on-device без cloud → ценность TheStage = R&D cloud + будущие сервисы; приоритет аккаунта ↓.

**Discovery перед цифрой:** monthly cloud/GPU AI spend? кто платит inference в OEM pilot? самый дорогой workload (STT / LLM / vision)?

Полная карта: [POV doc §11](POV%20%E2%80%94%20finance-first%20outbound%20(enterprise%20wearables).md#11-vuzix-где-наибольшие-benefits--cost-savings).

### Слой D — Vision (ещё не вся в продукте)

- **Orchestration** STT → LLM → TTS, выбор моделей из marketplace.
- Партнёрства с **model providers** как distribution.
- **SDK** для встраивания в приложения.

### Публичный pricing ([app.thestage.ai](https://app.thestage.ai/))

| План | Цена | Суть |
|------|------|------|
| Researcher | $0/mo | 1 GPU quota, мало runs, $1 credits |
| Individual | $20/mo | 2 GPU, 400 runs/day |
| Team | $150/mo | 8 GPU, 4000 runs/day |
| Enterprise | Custom | Без лимитов |

**Плюс metered:** inference engine — **за секунду GPU**; on-device SDK — **за активное устройство**.

**Отдельно в docs:** Elastic Models и Qlip — **Wallet**, pay-as-you-go.  
**Из разговора:** ~$1k/GPU/год за софт — **другая линейка**, ближе к сделкам со стартапами/Nebius.

### Elastic Models + LoRA (зачем на сайте)

«Ready-to-go + LoRA» — для **стартапов со своей моделью**: быстрый старт на готовой базе, не месяцы ручного export. Детали LoRA (recompile или runtime) — **уточнить у них**.

### Почему не смешивать 4 слоя в одном питче

У TheStage **четыре разных обещания** — в одном разговоре слушатель выбирает **самое знакомое** (часто «ещё один GPU cloud») и теряет суть.

| Слой | Вопрос в голове покупателя | Что показывать в proof |
|------|----------------------------|-------------------------|
| **A. Optimize** | «Сколько быстрее/дешевле inference?» | tps, ttft, tiers S/M/L/XL, 2–4× cost (сайт) |
| **B. Platform** | «Зачем мне ваш GPU, если есть Nebius?» | CLI, reproducibility, калибровка ANNA |
| **C. Deploy** | «Заработает на **моём** iPhone / GPU?» | compile artifact, max_memory_mb, Jetson |
| **D. Vision** | «Вы уже LiveKit on-device?» | Roadmap; не продавать как готовое |

**Что ломается при смешении:** путаница категории · разные buyer personas (ML vs founder vs procurement) · разные цены ($20/mo vs $1k/GPU/год vs per-device) · риск **over-promise** (orchestration в roadmap выдаётся за prod).

**Как питчить:** один главный слой под боль + остальное вторым слайдом. Примеры:
- Voice startup, cloud дорого → **A+C** (Elastic + Apple compile), Platform — «как калибруем».
- Nebius / infra → **A+B**, без SDK-narrative.
- Wearables → **C** (hybrid phone + device; не обещать Snapdragon on-glass), vision — «дорожная карта».
- Model provider → **Motion A**: optimize их модель, не orchestration.

---

## 4. Voice on-device — предметная область

### Что просят клиенты

Не «просто LLM на телефоне», а цепочка:

```
Микрофон → STT (речь в текст) → LLM (ответ) → TTS (голос) → динамик
```

Часто wearable **слабый** → тяжёлое крутится на **телефоне в кармане** (hub) или на **edge-box**; в облако — только сложные запросы.

**Ограничение по железу:** on-device через TheStage сегодня = в первую очередь **Apple Silicon** (см. §3 «Поддерживаемые платформы»). Стратегия «очки + **iPhone** hub» укладывается; «весь inference на **любом** Android-телефоне» — **нет**, без отдельного стека (llama.cpp, cloud и т.д.).

### Типичные клиенты TheStage

AI tutor, note-taker, **умные очки/кольца**, gaming NPC, banking assistant, inference providers (контейнеры под voice/diffusion).

### Три архитектурных паттерна (практика)

| Паттерн | Схема | Когда | TheStage сегодня |
|---------|--------|-------|------------------|
| **Cloud-first** | App → API (STT/LLM/TTS в облаке) | MVP, максимум «умности» | Elastic + NVIDIA serving; cut COGS |
| **Hybrid** | STT local, LLM cloud (или наоборот) | Первый шаг с Praktika-like | Whisper tier S на iPhone + cloud LLM |
| **Hub / hybrid (wearable)** | Очки (mic/sensors) + **phone** и/или on-glass NPU → STT→LLM→TTS | Brilliant Labs-type (press: hybrid) | Compile на **Apple Silicon** для phone path; on-glass Qualcomm — **вне** TheStage SDK |
| **Edge-box** | Устройство → Jetson / NUC | Robotics, фиксированный edge | Jetson в marketing/docs |

**Android:** массовый on-device inference на Snapdragon — **вне** стандартного продукта; типичный обход — cloud для Android-users или отдельный стек (llama.cpp), пока нет roadmap от TheStage.

---

## 5. Практические юз-кейсы (глубина)

Ниже — **как это выглядит в жизни** команды клиента: боль → что пробовали → что даёт TheStage → что **остаётся** на стороне клиента. Развёрнутые «Reddit-истории» — в [ICP use cases](ICP%20use%20cases%20%E2%80%94%20Reddit-style%20stories.md).

---

### 5.1 AI language tutor (Praktika-like)

**Контекст:** B2C, ~40 FTE, 3 ML / 8 mobile, **~2M active**, LATAM+EU. Voice loop: пользователь говорит → STT → диалоговый LLM → TTS → обратная связь по произношению.

**Боль (как формулирует CFO / product):**
- Inference line item растёт **быстрее revenue** (минуты STT + токены × DAU).
- **1–2 сек** тишины после фразы = «приложение тупое».
- Плохой LTE (метро, rural) → обрывы сессий.
- Конкуренты: «your voice stays on device» — у вас пока нельзя честно.

**Что обычно пробуют без TheStage:**

| Подход | Результат |
|--------|-----------|
| Оставить OpenAI-class + Deepgram/ElevenLabs | Качество ок, **$** и latency на scale |
| Свой GPU + vLLM | Дешевле token, **не** решает offline/latency на телефоне |
| llama.cpp on-device | Месяцы export/OOM; Android mid-range — thermal |
| Гибрид вручную | Нужны routing + **две** модели в проде |

**Практический путь с TheStage (поэтапно):**

| Фаза | Действие | Слой TheStage | Ожидаемый эффект |
|------|----------|---------------|------------------|
| 0 | Baseline metrics в cloud | Platform GPU для бенчмарков | ttft/tps/$ на 1k сессий |
| 1 | **STT on-device** (iOS) | Elastic Whisper tier S/M + Apple compile | Минус round-trip на самый частый вызов |
| 2 | Small **LLM tier S** local для коротких реплик | Elastic Llama/Qwen tier + compile | Снижение token bill; сложное — cloud |
| 3 | LoRA update (новый accent pack) | Elastic/ANNA path vs полный re-export | Недели → дни (оценка ~60% на v2) |

**Что TheStage не закрывает:** barge-in, turn-taking, выбор TTS, UX «когда слушать», A/B продуктовые метрики retention.

**Питч одной фразой:** «Срежем месяцы mobile ML и переведём самый дорогой кусок voice pipeline на телефон без потери измеримых SLO.»

---

### 5.2 Smart glasses + hybrid compute (Brilliant Labs-like)

**Контекст (шаблон ICP + публичные данные по Brilliant):** малый hardware+ML; consumer AI glasses. **Не утверждаем**, что у Brilliant ровно «mic-only очки + весь inference на iPhone» — это было упрощение в [ICP stories §2](ICP%20use%20cases%20%E2%80%94%20Reddit-style%20stories.md). Детальная карта: §3.8–3.9.

**Что известно публично про Brilliant Halo (май 2026):**

| Элемент | Источник | Вывод |
|---------|----------|--------|
| TheStage + Neuphonic + Brilliant, privacy-first on-device narrative | [TechDay Mar 2026](https://techday.co.nz/story/privacy-first-ai-smart-glasses-run-models-on-device) | **Факт** партнёрства в прессе |
| Vision on glasses, **значимая** обработка на **paired smartphone** (TheStage compile на phone GPU/NPU) | То же | **Гибрид**, не «тупые очки» |
| **Alif Balletto B1** NPU on-glass | Alif / industry press | On-glass AI **есть**; это **не** документированный путь TheStage на Qualcomm |

**Типичные боли (для любого glasses startup в этом кластере):**
- E2E latency vs Siri/ChatGPT voice; budget **<2–3 сек** после фразы.
- Cloud = radio + battery drain.
- Privacy marketing требует **реального** local/hybrid pipeline.
- Mirai/Cactus смотрели — по оценке TheStage «не идеал под form factor» (детали TBD).

**Практика с TheStage (если архитектура клиента = phone path):**
- Pre-compiled **Whisper + small LLM** под **Apple Silicon** companion app.
- **Benchmark pack** p95 на iPhone 15/16 класса.
- **Jetson** — только если у клиента отдельный edge hub, не mass phone.

**Практика, если клиент = Snapdragon-on-glass (список B, §3.10 → **W3 / S7→S1**):**
- Питч **cloud NVIDIA** (слой A), не on-device SDK.
- Честно: без roadmap Android/QNN — не обещать compile в APK на очках.

**Что остаётся у клиента:** BLE, firmware, orchestration, TTS, store compliance, on-glass NPU stack (если не Apple).

**На звонке у TheStage:** доля compute Brilliant на iPhone vs glasses; iOS-only или Android companion; Jetson в планах.

---

### 5.3 Gen AI + свои LoRA (Recraft-like)

**Контекст:** ~25 FTE, 4 ML, image/asset generation + voice в roadmap. Inference = **главная COGS**, свой GPU + Nebius-class provider.

**Боль:**
- Каждый новый стиль LoRA → «ещё один deployment?» VRAM?
- Pro users: «preview 4 сек» vs конкуренты быстрее.
- Mobile «assistant in pocket» отложен, пока cloud Flux не оптимизирован.

**Практика с TheStage:**
- **Elastic FLUX** / LLM в каталоге — быстрый A/B tier S/M/L без месяца TensorRT вручную.
- **ANNA + Qlip** для **своего** checkpoint, не из каталога.
- **CLI + Nebius** — калибровка без своего k8s (в docs: `--provider Nebius`).
- OpenAI-compatible serving (Modal tutorial) — если остаются cloud-first, но дешевле.

**Риск для клиента:** vendor lock-in → нужен **exit plan** (artifacts, self-host license).

**Питч:** «2–4× inference cost cut на **вашем** GPU — сначала cloud economics, mobile compile потом.»

---

### 5.4 B2B meeting AI (Phonic-like)

**Контекст:** ~20 FTE, B2B SaaS: запись → transcript → summary → action items. Платят **команды**, не consumers.

**Боль:**
- EU bank pilot: «audio не в OpenAI» — deal breaker.
- 500-seat pilot = огромные **STT minutes**.
- Live captions во время звонка — latency.

**Практика с TheStage:**
- **Whisper elastic tiers** on-device для **mobile capture** (field sales).
- Pre-optimized **cloud containers** + on-prem GPU.
- **SOC 2** в pricing — checkbox procurement.

**Питч:** «Enterprise security + предсказуемый $/minute на scale, не только API wrapper.»

---

### 5.5 Infra / inference provider (Nebius, SaladCloud-like)

**Контекст:** не voice app, а **платформа**, которая продаёт inference своим клиентам.

**Боль:** unit economics — $ за inference hour / за 1k images / за token.

**Практика с TheStage:**
- ANNA + optimized containers (**до 4×** в messaging сайта).
- Case **SaladCloud:** «10k images per dollar» — social proof для provider motion.
- Модель **~$1k/GPU/год** за софт на задеплоенных GPU.

**Питч:** «Сделайте inference ваших клиентов дешевле без найма quant team на каждую модель.»

---

### 5.6 Сводка: ICP → боль → вход в продукт

| Сегмент | Главная боль | Вход в TheStage | Анти-паттерн |
|---------|--------------|-----------------|--------------|
| Language app 2M MAU | $ cloud × MAU | Elastic voice + hybrid + Apple | «Замените GPT-4 одной кнопкой» |
| Wearables | Latency + privacy + compile | Apple hub compile | Inference на слабых очках |
| Gen AI + LoRA | GPU COGS | Elastic Flux/LLM + ANNA | Обещать full SDK orchestration сегодня |
| B2B voice | Security + STT minutes | Whisper tiers + SOC2 + containers | Только self-serve $20/mo |
| Infra provider | $/inference | per-GPU + containers | LiveKit-narrative |

---

## 6. Два GTM motion (как продавать разным покупателям)

> **POV development:** всегда через [3-stage framework](POV%20%E2%80%94%20how%20to%20build%20(Strategic%20POV%20framework).md) ([ESC](../../gtm_stuff/ESC%20&%20Whyzer/Strategic%20POV%20Development.md)) — consensus, champion ownership, POV ≠ business case.  
> **Enterprise wearables / public OEM:** [finance-first POV](POV%20%E2%80%94%20finance-first%20outbound%20(enterprise%20wearables).md) — CEO/CFO/BD + ML.

| | **Motion A — Model providers** | **Motion B — End customers (apps)** |
|---|----------------------------------|-------------------------------------|
| **Кто** | ElevenLabs, AssemblyAI, Deepgram, CAMB.AI… | Praktika, Brilliant Labs, Recraft, Phonic |
| **Обещание** | Day-zero optimize вашей модели → быстрее/дешевле у **их** клиентов | Срежем months of export hell + cloud bill на scale |
| **Слой** | A (Optimize) + иногда B | A + C (+ D в roadmap) |
| **Distribution** | Их бренд в marketplace TheStage | Прямые сделки + case studies |
| **Цена** | Rev-share / co-sell (уточнить) | per-GPU, enterprise, позже per-device SDK |

**Ошибка:** вести оба motion в **одной** CRM-воронке и одним deck — разные циклы сделки и разные decision makers.

---

## 7. Бенефиты для клиентов (компания с приложением)

Каждая выгода — с **примером** и границами честности.

### Экономика на scale

**Механика:** cloud API = variable cost **линейно** с MAU (минуты STT + токены LLM + TTS). On-device / optimized self-host = больше **фиксированных** затрат на ML-infra, но другой наклон кривой после порога.

**Пример (иллюстративный, не claim TheStage):**  
2M MAU × 10 voice-min/мес × ($0.006 STT + $0.02 LLM) ≈ **сотни тысяч $/мес** порядка величины — CFO видит строку inference. Гибрид «STT local» снимает долю STT-minutes; optimized LLM tier снищает $/token в cloud.

**Что нужно доказать на звонке:** реальные цифры Praktika cloud vs target on-device.

### Быстрый отклик (voice UX)

**Механика:** каждый cloud hop = RTT + queue. Local STT + local small LLM убирает 1–2 сетевых круга.

**Пример:** пользователь закончил фразу → **ttft** LLM с 800 ms cloud RTT vs 150 ms on-device — разница ощущается как «живой» vs «робот».

**Метрики TheStage:** **ttft**, **tps**, **p95 latency** — спорить цифрами с product, не ощущениями.

### Сеть и офлайн

**Пример:** language tutor в Mexico City metro — cloud-only падает в «не слышит»; local STT + cached prompts держит core loop.

**Граница:** полный offline dialog без cloud — только если **весь** loop помещается в RAM/tier; часто hybrid.

### Приватность и enterprise

**Пример:** B2B note-taker — bank pilot требует «raw audio не уходит к OpenAI». On-device STT + self-hosted optimized container закрывает narrative.

**Плюс:** SOC 2 Type I в публичных планах — procurement checkbox.

### Свой бренд / LoRA

**Пример:** Recraft — новый visual style через LoRA; без Elastic/ANNA каждый стиль = недели quant + deploy.

**Граница:** LoRA recompile vs runtime — **уточнить у TheStage**.

### Time-to-market

**Оценка из нашего workflow-сравнения:** первый production voice v1 **~18 нед → ~11 нед** (Elastic path); обновление LoRA v2 **~6 нед → ~2 нед**.

**В деньгах (грубо):** 7–14 engineer-weeks × $4–8k loaded = **$30k–110k** payroll на этапе compress/export/profile (не весь продукт).

### Гибрид (рекомендуемый реализм)

**Практика Praktika-type:** не «big bang» migration.

1. Замерить cloud baseline ($, p95 latency).  
2. STT on-device (iOS).  
3. Short replies local (tier S LLM).  
4. Long tutoring explanations — cloud.  
5. Пересчитать unit economics каждый квартал.

**Честно:** on-device ≠ GPT-4 в кармане — **хороший voice UX в своём сценарии**, trade-off по «супер-умности».

---

## 8. Бенефиты для конечных пользователей

| Выгода | Что чувствует пользователь | Пример сценария |
|--------|----------------------------|-----------------|
| **Меньше тишины** | Ответ сразу после фразы | Language drill: сказал фразу → мгновенная поправка |
| **Работает «в метро»** | Не «проверьте соединение» | Tutor в поездке без Wi‑Fi на core STT |
| **Доверие** | «Мой голос не уходит в облако» | Репетиция произношения, health-adjacent темы |
| **Стабильность** | Реже «сервис недоступен» | Пик нагрузки у провайдера API не убивает сессию целиком |
| **Батарея (иногда)** | Меньше постоянной передачи audio | Hub-модель: меньше upload сырого audio в cloud |

Пользователь **не** видит tiers S/M/L/XL — видит «приложение стало отзывчивее и не стыдно включать микрофон в публичном месте».

---

## 9. Как продукт встраивается в работу ML-команды

### Классический путь (без TheStage)

```
Обучили LoRA → вручную PTQ/GPTQ → export Core ML/ONNX →
профили на 10 телефонах → OOM/thermal → собрали STT→LLM→TTS →
часто прод через cloud API
```

**Больные этапы:** сжатие + export + профилирование — **недели–месяцы**, много циклов.

### Путь с TheStage AI

```
Обучили LoRA → Elastic baseline ИЛИ ANNA+Qlip →
выбрали tier S/M/L/XL → compile (Apple/Nvidia) →
benchmark (tps, ttft, memory) → artifact/SDK в app →
STT→LLM→TTS (wiring всё ещё ваша) → on-device + опционально cloud
```

**Параллельно:** TheStage Cloud/CLI — GPU для калибровки ANNA, не свой k8s.

### Где TheStage **не** экономит время

- Обучение / fine-tune.
- Сборка voice pipeline (BLE с очками, UX, выбор TTS).
- Большая часть mobile-интеграции.

### Где **экономит** (оценка порядка величин)

| Сценарий | Классика | TheStage (Elastic path) | Экономия |
|----------|----------|-------------------------|----------|
| **Первый production voice v1** | ~18 недель | ~11 недель | **~7 нед (~40%)** |
| **Обновление LoRA v2** | ~6 недель | ~2 недели | **~4 нед (~60%)** |

*Допущения: 2–4 ML, wearable+phone, первый on-device voice. Custom ANNA path — ближе к ~13–15 нед на v1.*

В деньгах (грубо): **7–14 engineer-weeks** на v1 × $4–8k = **$30k–110k** только на payroll ML-infra этапа (без учёта более раннего выхода в прод).

### Практический пример: одна неделя ML-инженера

**Без TheStage:** GPTQ → Core ML export → OOM на iPhone 13 mini → thermal profiling → эскалация в mobile.

**С TheStage:** Elastic Whisper M + Llama S benchmark → ANNA constraints → Apple artifact в TestFlight → p95 vs cloud → cohort rollout.

### Диаграмма

См. [Diagram — ML workflow classic vs Stage AI.md](Diagram%20%E2%80%94%20ML%20workflow%20classic%20vs%20Stage%20AI.md) (Mermaid: классика vs Stage, runtime wearable).

---

## 10. Бенефиты для ML-команд (wearable / voice)

| # | Бенефит |
|---|---------|
| 1 | **Не изобретать mobile export** — готовые tiers и compile path |
| 2 | **Явный knob** quality ↔ latency ↔ RAM (S/M/L/XL, ANNA constraints) |
| 3 | **Измеримость** — tps, ttft, max_memory, не «кажется быстрее» |
| 4 | **Один pipeline** research GPU → compiled artifact → device |
| 5 | **Voice baseline** — Whisper/LLM уже в каталоге |
| 6 | **LoRA / custom weights** — итерации без полного re-platform (детали уточнить) |
| 7 | **Свои SLO** — p95 latency, OOM rate на своём железе, не у API-vendor |
| 8 | **Burst GPU** через Platform — калибровка без своего кластера |

| Задача | TheStage | Команда клиента |
|--------|----------|-----------------|
| Tier под RAM / benchmarks | ✅ | ✅ product constraints |
| LoRA training | ❌ | ✅ |
| BLE, TTS, barge-in, routing | ❌ | ✅ |

**Не обещают из коробки:** полный orchestration STT→LLM→TTS; TTS; wake word; замену mobile team.

---

## 11. Конкурентный контекст (простыми словами)

| Как решают без TheStage | Роль TheStage |
|-------------------------|---------------|
| **Cloud API** (OpenAI, AssemblyAI…) | Замена/снижение доли cloud при scale |
| **vLLM / TensorRT-LLM** на своих GPU | Альтернатива/дополнение для cloud serving |
| **llama.cpp, Core ML, ONNX** вручную | Ускоренный путь compile + tiers |
| **Mirai AI, Cactus** (on-device) | Близкие по теме; заказчик говорит — не идеал под smart glasses (почему — TBD) |
| **LiveKit** (cloud voice orchestration) | Их vision — похожее, но **on-device** |

**Как отвечать на «мы сами поднимем vLLM»:** TheStage не всегда замена — часто **слой ниже**: сжатая модель + compile + metrics; vLLM остаётся serving fabric.

**Как отвечать на «зачем вы, если есть Core ML»:** Core ML — формат; TheStage — **как** получить правильный trade-off accuracy/RAM без месяца ручного PTQ.

---

## 12. Что понятно / не очень / непонятно (для звонка)

### Понятно

- Ядро = **inference acceleration** (ANNA, Qlip, Elastic), не «ещё один GPU marketplace».
- Cloud = **инфра для ML**, оптимизация = **отдельный слой**.
- Спрос **voice + on-device**; клиенты в основном **стартапы + Nebius**.
- GTM gap = **execution**, не отсутствие PMF.
- **5M MAU** = цель по портфелю apps; **Praktika 2M** = отдельный кейс.
- **Платформы:** NVIDIA cloud ✅ · Apple on-device ✅ · Jetson (edge) ✅ в marketing · Snapdragon/Android on-device ❌ self-serve.
- **«~80% wearables недоступны»** — только для **on-device на их SoC/телефоне**, не для **cloud optimize**.
- **Brilliant** в прессе = **hybrid** (phone + glasses), не доказанный «только iPhone hub» из наших notes.
- **ICP-рамка §3.11:** **S** = tech-сегмент (не приоритет) · **P** = приоритет outbound · **W/L** = landmarks · north star = **voice + wearables**.
- **S7 / public OEM (§3.12):** CEO/CFO + ML — два языка; savings в **cloud/OEM**, не on-glass Snapdragon.
- **POV:** 3 stages + consensus + champion presents ([framework](POV%20%E2%80%94%20how%20to%20build%20(Strategic%20POV%20framework).md) · [ESC](../../gtm_stuff/ESC%20&%20Whyzer/Strategic%20POV%20Development.md)).

### Не очень понятно

- **Android / Snapdragon** в roadmap vs стратегия «только Apple on edge».
- **Brilliant Labs:** точная архитектура (iOS/Android split, % on phone vs Alif on-glass, что именно компилирует TheStage).
- **Usmile:** за что платят и есть ли inference / on-device вообще.
- **Jetson:** есть ли revenue от edge vs только marketing.
- Главный продукт на 12 мес: Platform vs SDK vs enterprise per-GPU?
- Как связаны $0–$150/mo, Wallet и ~$1k/GPU/год в реальных сделках?
- Sulfer, orchestration, LoRA — что уже в проде vs roadmap?
- Статус Praktika migration (iOS-first?)?

### Совсем непонятно

- Outbound list и ICP criteria.
- Unit economics proof (2M users: $ saved vs cloud).
- Кто платит за что у Recraft / Phonic.
- Partnerships с model providers (кто подписан).
- Owner GTM внутри, KPI на 90 дней для внешней помощи.

---

## 13. Вопросы на следующий разговор (топ-10)

1. Что **№1 в revenue** на 12 месяцев: Platform, Elastic, SDK, per-GPU license?
2. Как **Recraft / Praktika / Nebius** платят сегодня (план, GPU fee, custom)?
3. **SDK + orchestration** — дата и scope (iOS/Android, voice pipeline included?); **Android / Snapdragon** — roadmap или сознательно out of scope?
4. **Praktika**: timeline cloud → on-device, метрики успеха?
5. **LoRA**: recompile каждый раз или runtime swap?
6. **Brilliant Labs:** что именно компилирует TheStage (phone vs glasses), iOS/Android, доля on Alif NPU?
7. Почему **Mirai/Cactus** не подходят под glasses?
8. **Sulfer** — что это?
9. Cloud — **margin на GPU** или только on-ramp в софт?
10. **Outbound list** — можно ли увидеть сегменты?
11. **Success 90 дней** для GTM-партнёрства — в цифрах?

*(Нумерация расширена; полный список в Roadmap.)*

*Полный реестр (~45 вопросов):* [StageAI Roadmap § Реестр](StageAI%20Roadmap.md#реестр-вопросов-master)

---

## 14. Глоссарий (короткий)

| Термин | Значение |
|--------|----------|
| **Inference** | Модель уже обучена; она **отвечает** пользователю |
| **PTQ / GPTQ / AWQ** | Способы **сжать** обученную модель |
| **OOM** | Не хватило **памяти** на устройстве |
| **Tier S/M/L/XL** | Степень сжатия готовой модели |
| **tps** | Токенов в секунду (скорость LLM) |
| **ttft** | Задержка до **первого** токена ответа |
| **LoRA** | Маленький adapter поверх большой модели |
| **STT / TTS** | Speech-to-text / text-to-speech |
| **On-device** | Считает на телефоне/очках, не только в облаке |
| **Hub / hybrid** | Телефон или edge-box + опционально compute на самих очках (NPU); не всегда «всё на iPhone» |
| **Snapdragon** | Чип Qualcomm в большинстве Android-телефонов; **не** в стандартном compile path TheStage |
| **Jetson** | NVIDIA edge-плата; отдельная цель deploy, не массовый смартфон |
| **SLO / p95** | Ваши целевые метрики качества сервиса |
| **Elastic Models** | Готовые ускоренные модели TheStage |
| **ANNA** | Автоподбор сжатия под ограничения |
| **Motion A / B** | Provider co-sell vs прямые app-клиенты |
| **Hybrid** | Часть pipeline local, часть cloud |
| **S1–S7** | **Tech-сегмент** (где inference); **не** приоритет |
| **P0 / P1 / P2** | **Приоритет outbound** (кого искать сейчас) |
| **L1–L6** | Landmark-паттерны (весь портфель) |
| **W1–W4** | Wearable/voice landmarks (тема фаундера) |
| **S4** | Wearable + iOS companion hybrid (Brilliant-class) |

---

## 15. Одна фраза — наше понимание

> TheStage AI — это **стек ускорения и деплоя inference** (особенно voice) на GPU и телефон, с платформой для ML-экспериментов и дорогой к **on-device orchestration**; их сильная сторона для клиентов — **быстрее и дешевле на scale**, для ML-команд — **срезать месяцы** на compress/export/profile; главный открытый вопрос — **единый продукт и GTM**, потому что на сайте сегодня смешаны cloud, optimization и будущий SDK.

---

*Документ можно отправлять заказчику как демонстрацию понимания домена перед roadmap / discovery call.*
