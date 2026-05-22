# Website Research — TheStage AI

**Source:** публичные страницы продукта и документации (без логина)  
**Primary URL:** [https://app.thestage.ai/](https://app.thestage.ai/)  
**Captured:** 2026-05-17  
**Method:** browser snapshot (marketing SPA), [docs.thestage.ai](https://docs.thestage.ai/), [about.thestage.ai](https://about.thestage.ai/)  
**Docs (детально):** [Documentation Research — docs.thestage.ai](Documentation%20Research%20%E2%80%94%20docs.thestage.ai.md)

> Cloud и Projects в приложении без авторизации редиректят на `/sign-in` — ниже только то, что видно публично + docs.

---

## 1. Позиционирование

| Поле | Содержание |
|------|------------|
| **Title** | TheStage AI Inference Optimization Platform |
| **Tagline (hero)** | Next Gen **AI Infrastructure** |
| **Value prop** | Compress, compile, and deploy models to **cloud, on-prem or on-device**. Tune size vs. quality with a **slider** for faster, cheaper models. |
| **OG / meta** | «Faster, Cheaper AI Inference» — accelerate on NVIDIA & edge; ANNA, QLIP, Elastic Models, CLI & API |
| **Company (about)** | Full-stack AI: find, train, optimize, deploy. Inference acceleration + mathematical framework for accuracy/performance trade-off |

**Связанные домены**

| URL | Назначение |
|-----|------------|
| [app.thestage.ai](https://app.thestage.ai/) | Платформа, модели, pricing, login |
| [docs.thestage.ai](https://docs.thestage.ai/) | Документация (Platform, Elastic Models, Qlip, Tutorials) |
| [about.thestage.ai](https://about.thestage.ai/) | Маркетинг, команда, cases, black paper |
| CDN | `cdn.thestage.ai` (OG images) |
| PyPI registry | `thestage.jfrog.io/artifactory/api/pypi/pypi-thestage-ai-production/simple` |

---

## 2. Навигация app.thestage.ai

**Top nav:** Models · Cloud · Projects · Pricing · Docs · Blog · Log in · Try for free

**Footer — Developers:** Docs · Quickstart · GitHub · Hugging Face  
**Footer — Company:** About · Careers · Contact  
**Footer — Legal:** Terms Of Use · Privacy Policy · AI Use Policy · Manage cookies

**Social:** Twitter · LinkedIn · Hackernoon · Medium · YouTube

---

## 3. Продуктовый стек

### 3.1 QLIP (full-stack optimization framework)

- Quantization, pruning/sparsification, **compilation**, **serving**
- Пакеты: **Qlip.Core**, **Qlip.Algorithms**, **Qlip.Serve** (meta на Nvidia Triton)
- **ANNA** (Automated Neural Networks Accelerator) — подбор конфигурации quality/performance по «слайдеру»
- Targets: **NVIDIA GPUs** + **Apple Silicon** (M1–M4)
- Заявленные speedups (docs): FLUX.1-Schnell **2.1×**, Llama-3.1-8B **4.2×** vs bfloat16 на H100
- Доступ: API token + **доп. approval** → `frameworks@thestage.ai`

### 3.2 Elastic Models

- Pre-compiled модели с **4 tier**: **S, M, L, XL** (fast → slow, accuracy trade-off)
- ANNA-produced; cold start без JIT
- HF-совместимый API: `elastic_models.transformers`, `elastic_models.diffusers`
- Precision: fp16, bf16, int8, fp8, int4, 2:4 sparsity
- **Не зависит** от TensorRT-LLM / SGLang / vLLM (по docs)
- Billing: pay-as-you-go, Wallet (см. Product Terms)

**Supported model families (docs)**

| Type | Models | GPUs |
|------|--------|------|
| Text-to-Text | Mistral, Mistral-Small, Llama, Qwen, DeepSeek-Distill | L40S, H100, B200, RTX 5090, RTX 4090 |
| Text-to-Video | Mochi | H100, B200 |
| Text-to-Image | Flux, SDXL | L40S, H100, B200, RTX 5090 |
| ASR | Whisper, Whisper v3-turbo | L40S, H100, RTX 5090, RTX 4090 |

### 3.3 TheStage AI Platform + CLI

- Self-hosted / cloud: web UI + **CLI** (`pip install thestage`)
- Управление: **projects**, **instances**, **containers**, **tasks**
- GPU rental: провайдеры **Amazon**, **Nebius**; GPU types A100, A10G, H100, L40S, T4
- Remote runs: `thestage project run` — auto-commit, stream logs, queue on container
- Auth: Profile → API tokens; SSH keys upload

### 3.4 Torch Integral (research / about)

- Continuous layer representation (INNs); CVPR 2023 award candidate; до **8×** cost reduction (marketing)

### 3.5 Serving

- **Cloud:** Triton-based serving
- **On-device:** Apple on-device SDK (marketing); per-device billing (pricing footnote)

---

## 4. Workflow на главной (5 шагов)

1. **Start a project** — import model или pre-optimized OSS из библиотеки  
2. **Run a task** — cloud GPUs или own infra  
3. **Optimize with ANNA** — slider: size, latency, quality  
4. **Export to target device** — NVIDIA GPUs · Apple silicon · **NVIDIA Jetson**  
5. **Deploy to production** — serve optimized models anywhere  

**Research workflow:** experiments end-to-end, GPU sharing, link to acceleration stack.

**QLIP pipeline (marketing):** Quantize → Accelerate (ANNA slider) → Compile → Serve

---

## 5. Разделы продукта (marketing)

### Cloud

- Rent GPUs (pay-as-you-go) или connect own instances  
- Flow: create instance → attach to project → create Docker container → CLI connect → run from laptop, stream logs  

### Projects

- Workspace для remote GPU runs  
- Sub-second starts, auto commits, env management  
- Command pattern: `thestage project run`  

### Models marketplace (`/models`)

**Filters:** Search · sort (Playground first / Newest / Oldest) · Use Case · GPU type · Publisher

**Use cases (filter):** Text-to-Video · Text-to-Text · Speech-to-Text · Text-to-Image

**GPU types (filter):** H100 · L40S · B200 · GeForce RTX 5090/4090 · Thor · A100-SXM4-80GB

**Publishers (filter):** openai · Meta · black-forest-labs · mistralai · Qwen · TheStageAI · Wan-AI

**Каталог (видимый срез, 2026-05-17)**

| Section | Model | Publisher | Type | Notes |
|---------|-------|-----------|------|-------|
| Voice | thewhisper-large-v3-turbo | TheStageAI | speech-to-text | optimized for variable audio chunk duration |
| Voice | whisper-large-v3-turbo | openai | speech-to-text | ASR + translation |
| Voice | whisper-large-v3 | openai | speech-to-text | ASR + translation |
| Diffusion | Wan 2.2 | Wan-AI | text-to-video | up to 81 frames @ 480×480 |
| Diffusion | FLUX.1-dev | Black Forest Labs | text-to-image | Elastic Models |
| Diffusion | FLUX.1-schnell | Black Forest Labs | text-to-image | playground |
| LLM | Mistral-Small-24B-Instruct-2501 | mistralai | text-to-text | |
| LLM | Qwen2.5-7B-Instruct | Qwen | text-to-text | Elastic Models |
| LLM | Mistral-7B-Instruct-v0.3 | mistralai | text-to-text | |
| LLM | Llama-3.1-8B-Instruct | Meta | text-to-text | Elastic Models |

*(Полный список в docs: `elastic_models.print_available_models()` — десятки HF IDs с tier по GPU.)*

---

## 6. Solutions / ICP (сайт)

| Vertical | Ключевое сообщение |
|----------|-------------------|
| **AI Tutors** | On-device SDK; private low-latency; streaming STT + TTS; GPU containers when cloud needed |
| **Inference Providers** | Pre-optimized containers (diffusion, streaming transcription, TTS); **up to 4×** inference cost cut |
| **NoteTakers** | Real-time transcription, summaries, voice playback; NVIDIA + Apple |
| **Robotics** | Jetson, ARM MCUs, edge NPUs; ANNA for latency/power/memory |
| **Gen AI Companies** | Own infra; ElasticModels + custom weights/LoRA; up to 4× cost cut |
| **Gaming** | On-device LLMs for NPCs; STT/TTS for conversations; cloud or on-device compile |

**Homepage tabs (product areas):** Overview · ElasticModels · Automated Acceleration · Compile · **Apple on-device SDK** · Pricing

---

## 7. Pricing (app.thestage.ai, публично)

> Plans include GPU hours, inference runtime, ANNA + optimization toolkit. Top up credits.

| Plan | Price | For | Highlights |
|------|-------|-----|------------|
| **Researcher** | $0/mo | research, benchmarks, prototypes | 1 GPU quota · 50 task runs/day · 1 seat · $1 starter credits · inference engine + SDK* · SOC 2 |
| **Individual** | $20/mo | solo builders | 2 GPU quota · 400 runs/day · $2 monthly credits · SDK **15% off*** |
| **Team** | $150/mo | production teams | 8 GPU quotas · 4,000 runs/day · 8 seats · $10 credits · SDK **20% off*** |
| **Enterprise** | Custom | scale, security, private deploy | unlimited runs/seats · flat SDK fees* · custom integrations · custom SLAs |

**Footnote *** Pay per second for **NVIDIA GPU inference engine**; **per active device** for **on-device SDK**.

**CTAs:** Start building free · Book a demo · Talk to us

---

## 8. Security & compliance (marketing)

| Item | Detail |
|------|--------|
| SOC 2 | Type I (vendor reviews) |
| Data privacy | Encrypted; not used for training; not shared with third parties |
| Secure usage | RBAC, access tokens, deploy on your infrastructure |
| Auditability | Audit logs, reproducible runs |

---

## 9. Onboarding (marketing)

1. Sign up  
2. Get Access key  
3. Run Elastic Model or deploy endpoint  
Docs: Quickstart · Talk to us

---

## 10. Документация — установка и требования

### Elastic Models

```bash
pip install thestage
thestage config set --access-token <TOKEN>
pip install 'thestage-elastic-models[nvidia,cudnn]' \
  --extra-index-url https://thestage.jfrog.io/artifactory/api/pypi/pypi-thestage-ai-production/simple
```

- Python **3.10–3.12**, x86_64, CUDA **11.8+**, PyTorch **2.4–2.10**
- LLMs: CuDNN SDPA (no flash-attn required)

### Qlip

```bash
pip install qlip.core[nvidia] --extra-index-url https://thestage.jfrog.io/...
pip install qlip.algorithms --extra-index-url https://thestage.jfrog.io/...
```

- Linux, Python 3.10–3.12, NVIDIA CUDA 11.8+, PyTorch 2.4+

### CLI

- `pip install thestage` · Python **3.9+** · Git · SSH · Linux/macOS (Windows → WSL)

### Tutorials (docs index)

- 2× faster elastic FLUX schnell  
- 4× faster Elastic LLMs  
- Quantization basics  
- FLUX ANNA  
- Text-to-image evaluation  
- Serving ElasticModels on Modal  
- Flux caching  

---

## 11. Юридическое / billing (docs)

| Document | Effective | Entity |
|----------|-----------|--------|
| Elastic Models Product Terms | 2026-04-08 v1.0 | The Stage AI, Inc., 702 Rockland Rd, Rockland, DE 19732 |
| QLIP Stack (ANNA) Product Terms | 2026-04-08 v1.0 | same |
| AI Use Policy | linked from app | AUP for acceptable use |
| Wallet | Stripe top-up; PAYG metering (runtime, tokens, requests, etc.) |

---

## 12. Команда (about.thestage.ai)

| Role | Name |
|------|------|
| CEO / Co-founder | Kirill Solodskikh |
| Chief AI Scientist | Azim Kurbanov |
| Chief AI Architect | Ruslan Aydarkhanov |
| Chief Product Officer | Max Petriev |
| Chief MLOps | Ilya Baryshnikov |
| Chief Design Officer | Daria Kushnarenko |

+ engineering/design roster (Backend lead Alexey Hromov, Frontend Svyatoslav Zytsar, PM Sasha Nevidomaia, etc.)

**Hiring:** Middle AI Engineer (Hybrid / Remote) — listed on about page

---

## 13. Cases & credibility (about.thestage.ai/cases)

| Case | Client / domain | Result (claimed) |
|------|-----------------|------------------|
| AI image compression | on-chain storage | up to **100×** vs PNG on Ethereum |
| AI HDR camera | **Huawei P50/P60** | 4K <1s on Snapdragon 888 NPU; **6×** accelerated |
| AI firewall | **Wallarm** (YC S2016) | malware detection **99%**; 1 Gb/s per CPU core |
| Brain signals | **Nissan** | street sign recognition from EEG **+7%** accuracy |

**Research themes:** Quantizations · Continuous formulations · Compression · INNs / CVPR 2023

---

## 14. Сопоставление с Customer Input (voice notes)

| Voice notes | На сайте |
|-------------|----------|
| SDK + self-service | Platform + CLI + Elastic Models; self-service tiers Researcher→Team |
| Usage-based / GPU | PAYG cloud + per-GPU inference engine; Enterprise custom |
| Voice assistants | Solutions: AI Tutors, NoteTakers, Inference Providers; Whisper models |
| On-device / smart glasses | Apple on-device SDK, Jetson, wearables in solutions copy |
| Orchestration STT→LLM→TTS | Qlip Serve + pipelines (docs); marketing describes multi-model chains |
| Model provider partnerships | Models marketplace + third-party publishers (OpenAI, Meta, BFL, …) |
| Nebius | CLI: `--provider Nebius` for rented instances |
| Praktika / 5M MAU | не упоминается публично |

---

## 15. Пробелы / требует логина

- **Cloud** dashboard, instance creation UI  
- **Projects** workspace, task history  
- **Pricing** calculator / live rates per model (кроме plan tiers)  
- Полный каталог моделей (lazy-load; в snapshot — срез)  
- Black paper download (форма «request» на about)  

---

## 16. Ссылки для углубления

- Platform docs: [docs.thestage.ai](https://docs.thestage.ai/)  
- CLI reference: [thestage-ai-cli](https://docs.thestage.ai/platform/src/thestage-ai-cli.html)  
- Elastic Models: [index](https://docs.thestage.ai/elastic_models/docs/source/index.html)  
- Qlip get started: [get_started](https://docs.thestage.ai/qlip/docs/source/get_started.html)  
- Apple compile API: [deploy_apple_api](https://docs.thestage.ai/qlip.core/docs/source/qlip.deploy_apple_api.html)  
- App: [Models](https://app.thestage.ai/models) · [Pricing](https://app.thestage.ai/) (anchor) · [Sign in](https://app.thestage.ai/sign-in)
