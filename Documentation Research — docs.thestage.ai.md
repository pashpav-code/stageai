# Documentation Research — docs.thestage.ai

**Source:** [https://docs.thestage.ai/](https://docs.thestage.ai/) (полный обход разделов, 2026-05-17)  
**Связано:** [Website Research — app.thestage.ai](Website%20Research%20%E2%80%94%20app.thestage.ai.md) · [Customer Input](Customer%20Input.md)

---

## 1. Карта документации

| Раздел | Страницы | Назначение |
|--------|----------|------------|
| **TheStage AI Platform** | [SSH Keys and API Tokens](https://docs.thestage.ai/platform/src/thestage-ai-ssh-keys-and-api-tokens.html) · [CLI Reference](https://docs.thestage.ai/platform/src/thestage-ai-cli.html) | Аккаунт, доступ, remote GPU workflow |
| **Elastic Models** | [Get Started](https://docs.thestage.ai/elastic_models/docs/source/index.html) · [Benchmarking](https://docs.thestage.ai/elastic_models/docs/source/elastic_models.benchmarking.html) · [Product Terms](https://docs.thestage.ai/elastic-models-product-terms.html) | Pre-compiled модели, tiers S/M/L/XL, PAYG |
| **Qlip** | [Get Started](https://docs.thestage.ai/qlip/docs/source/get_started.html) · APIs ниже · [Product Terms](https://docs.thestage.ai/qlip-stack-anna-product-terms.html) | Optimize / compile / serve свои модели |
| **Tutorials** | 8 ноутбуков/гайдов | Практические сценарии |

**Ключевая идея (welcome page):** inference acceleration stack; mathematical framework — **slider** для trade-off accuracy/performance; compile на **NVIDIA GPUs** и **Apple Silicon**.

---

## 2. Доступ и аутентификация

### 2.1 API Tokens

- Генерация: [app.thestage.ai](https://app.thestage.ai/sign-in) → Profile → **API tokens** → Generate  
- **Нельзя скопировать повторно** после закрытия страницы  
- Архив: disabled/expired tokens  
- CLI: `thestage config set --access-token <TOKEN>`

**Два use case токена (docs):**

1. **TheStage CLI** — instances, containers, projects, tasks  
2. **Qlip / Elastic Models** — оптимизация и inference

### 2.2 SSH Keys

- Profile → **SSH keys** — add / generate / delete  
- Обязательно **≥1 ключ** перед арендой instance  
- Доступ: rented instances + Docker containers на них (SSH)  
- CLI: `thestage config upload-ssh-key ~/.ssh/id_rsa.pub`

### 2.3 Qlip — дополнительный доступ

Помимо API token: запрос доступа на **frameworks@thestage.ai** (для `qlip.core`, `qlip.algorithms`).

---

## 3. TheStage AI Platform + CLI

### 3.1 Концепция

Self-hosted platform: web UI + CLI для **projects**, **instances**, **containers**, **models**. Remote GPU runs с laptop: auto-commit, log streaming, reproducibility.

### 3.2 Установка CLI

```bash
pip install thestage
thestage version   # Python 3.9+, Git, SSH; Linux/macOS (Windows → WSL)
```

### 3.3 Основные команды (сводка)

| Область | Команды |
|---------|---------|
| Config | `config set/get/clear`, `upload-ssh-key` |
| Connect | `thestage connect <NAME_OR_ID>` |
| Instances (rented) | `instance rented ls/create/connect/restart/terminate` — providers **Amazon**, **Nebius**; GPU A100, A10G, H100, L40S, T4 |
| Instances (self-hosted) | `instance self-hosted ls/connect` (+ `--username`) |
| Containers | `container ls/info/create/start/stop/restart/delete/connect/upload/download/logs/image ls` |
| Projects | `project init/clone/checkout/pull/reset/delete`, `attach-instance`, `detach-instance` |
| Tasks | `project run <cmd>` — auto-commit, stream logs; `task ls/logs/cancel` |

**Task controls:** Ctrl+C cancel task; Ctrl+D detach logs without stopping.

### 3.4 Project run (типичный flow)

```bash
thestage project run python train.py
thestage project run --container-name my-container python train.py --epochs 100
```

---

## 4. Elastic Models

### 4.1 Что это

Библиотека **pre-compiled** моделей (ANNA + DNN compiler). **4 tier:** S, M, L, XL.

| Tier | Смысл (docs) |
|------|----------------|
| **XL** | Mathematically equivalent + DNN compiler |
| **L** | Near lossless, **<0.5%** degradation (benchmarks) |
| **M** | Faster; между L и S |
| **S** | Fastest; **<~2%** degradation |

**Отличие tier в tutorials (FLUX):** L <1%, M <1.5%, S <2% (FID vs original).

### 4.2 Установка

```bash
pip install thestage
thestage config set --access-token <TOKEN>
pip install 'thestage-elastic-models[nvidia,cudnn]' \
  --extra-index-url https://thestage.jfrog.io/artifactory/api/pypi/pypi-thestage-ai-production/simple
pip install --force-reinstall --no-deps nvidia-cudnn-frontend==1.18.0  # LLMs: CuDNN SDPA
```

**Requirements:** Python 3.10–3.12 · x86_64 · CUDA 11.8+ · PyTorch 2.4–2.10 · Linux (tutorials)

### 4.3 Supported models (docs table)

| Type | Models | GPUs |
|------|--------|------|
| Text-to-Text | Mistral, Mistral-Small, Llama, Qwen, DeepSeek-Distill | L40S, H100, B200, RTX 5090, 4090 |
| Text-to-Video | Mochi | H100, B200 |
| Text-to-Image | Flux, SDXL | L40S, H100, B200, RTX 5090 |
| ASR | Whisper, Whisper v3-turbo | L40S, H100, RTX 5090, 4090 |

### 4.4 Особенности (Get Started)

- HF interface: `elastic_models.transformers`, `elastic_models.diffusers`  
- **No JIT** — pre-compiled, fast cold start  
- LLM attention: **CuDNN SDPA** (no flash-attn)  
- dtypes: fp16, bf16, int8, fp8, int4, 2:4 sparsity  
- **No dependency** on TensorRT-LLM, SGLang, vLLM  
- `elastic_models.print_available_models()` — матрица model × GPU × tiers

### 4.5 Пример (LLM)

```python
from elastic_models.transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-Nemo-Instruct-2407",
    token=hf_token,
    torch_dtype=torch.bfloat16,
    mode='S'  # S, M, L, XL
).to(device)
```

### 4.6 Пример (Flux)

```python
from elastic_models.diffusers import DiffusionPipeline
pipeline = DiffusionPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-schnell",
    torch_dtype=torch.bfloat16,
    mode="S"
)
```

**Shapes (FLUX tutorial):** 512², 768², 1024²; batch 1–4.

### 4.7 Benchmarking

Repo: [github.com/TheStageAI/ElasticModels](https://github.com/TheStageAI/ElasticModels) → `benchmark/`

| Model type | Latency metrics | Quality |
|------------|-----------------|---------|
| LLM | **tps**, **ttft**, max_memory_mb | `lm-eval` (mmlu, arc_challenge, piqa); also on HF model cards |
| Diffusion | time per image (1024²) | — |
| Whisper | tps, ttft | — |

**LLM latency params:** `input_context` small/medium/large (100/1000/4000 tokens); `mode` S/M/L/XL/**original**

**Пример FLUX.1-schnell latency (sec, lower=better):**

| GPU | S | M | L | XL | Original BF16 |
|-----|---|---|---|-----|---------------|
| H100 | 0.5 | 0.57 | 0.65 | 0.7 | 1.04 |
| L40S | 1.4 | 1.6 | 1.9 | 2.1 | 2.5 |
| RTX 5090 | 0.94 | — | — | — | — |

### 4.8 Billing (Product Terms)

- PAYG, **Wallet** (Stripe)  
- Metering: runtime minutes, tokens, requests, etc.  
- Tiers S/M/L/XL = latency/cost/quality trade-off  
- Third-party models: HF token may be required; Third-Party Model Terms apply

---

## 5. Qlip — full-stack framework

### 5.1 Архитектура пакетов

| Package | Роль |
|---------|------|
| **qlip.core** | Quantization/pruning/sparsification APIs; **Nvidia** + **Apple** compile & inference |
| **qlip.algorithms** | PTQ, SmoothQuant, LSQ, **ANNA** |
| **qlip.serve** | Meta-framework на **Nvidia Triton**; async pipelines |

```bash
pip install qlip.core[nvidia] --extra-index-url https://thestage.jfrog.io/...
pip install qlip.algorithms --extra-index-url https://thestage.jfrog.io/...
```

**Requirements:** Linux · Python 3.10–3.12 · x86_64 · CUDA 11.8+ · PyTorch 2.4+

### 5.2 Заявленные speedups (Get Started)

- FLUX.1-Schnell: **2.1×** on H100  
- Llama-3.1-8B: **4.2×** vs bfloat16 on H100  
- ResNet-18 compile: **>2×** vs PyTorch on NVIDIA

---

## 6. API Reference (детально)

### 6.1 Quantization API

**Назначение:** simulation/training; **не** прямой production inference.

- Для deploy → [Nvidia Compiler API](https://docs.thestage.ai/qlip.core/docs/source/qlip.deploy_nvidia_api.html) или [Apple Compiler API](https://docs.thestage.ai/qlip.core/docs/source/qlip.deploy_apple_api.html)  
- Для стандартных workflow → [Quantization Algorithms](https://docs.thestage.ai/qlip/docs/source/qlip_algorithms_api.html)

**Support matrix (simulation):** int/uint 2–16 bit; float8 e4m3fn (NVIDIA Ada/Hopper/Blackwell)

**Compiler support (inference subset):**

| Config | Nvidia | Apple |
|--------|--------|-------|
| w8a8 int8 symmetric | Turing–Blackwell | M4+ Neural Engine |
| w8a8 float8 symmetric | Ada, Hopper, Blackwell | Not supported |
| w4a16 int4 symmetric | (see full table in docs) | — |

### 6.2 Quantization Algorithms API

| Algorithm | Назначение |
|-----------|------------|
| **PostTrainingQuantization** | Static/dynamic PTQ; per-tensor/channel/token |
| **SmoothQuant** | Перераспределение difficulty activations → weights; formula Y = (X⊙s⁻¹)(W⊙s) |
| **LSQ** | Quantization-aware training |

**Architectures:** Transformers (LLaMA, BERT, GPT), CNNs, Diffusion (SD, DALL-E).

**Predefined NVIDIA configs (tutorial):** `NVIDIA_INT_W8A8`, `NVIDIA_INT_W8A8_PER_TOKEN_DYNAMIC`

### 6.3 ANNA (Automated Neural Network Acceleration)

**Полное имя в API:** Automatic Neural Network **Analysis** (в marketing — Accelerator).

**Что делает:**

- Post-training only — **calibration forward passes**, без retrain  
- Bag of algorithms (quantization, pruning, …)  
- Constraints: **size**, **MACs**, memory  
- **Pareto-optimal** configs по constraint sweep  
- Output: `QlipConfig` → hardware compile

**Workflow:**

1. Import ANNA  
2. Configure bag of algorithms  
3. Select model blocks  
4. Initialize **Analyser** (+ calibration data)  
5. `Analyser.run(min/max constraint, constraint_type='size'|'macs')`  
6. Evaluate & visualize  
7. Deploy selected config

**Ключевые классы:**

- `qlip_algorithms.anna.Analyser` — general  
- `qlip_algorithms.anna.LLMAnalyser` — HF models, wikitext calibration, auto Linear layers  
- `qlip_algorithms.anna.PipelineAnalyser` / **FluxAnalyser** (FLUX tutorial)

**Constraint types:** `size`, `macs`; loss estimators: `value`, `grad`

### 6.4 Nvidia Compiler and Inference API

**Backend:** TensorRT **10.6+**, CUDA, custom kernels.

**Pipeline:**

1. `NvidiaCompileManager` + `NvidiaBuilderConfig`  
2. `setup_modules()` / `setup_model()`  
3. `shape_profile()` — dynamic shapes  
4. `compile()`  
5. `NvidiaInferenceManager` + `NvidiaSessionConfig` → inference

**Features:**

- Not JIT; save to disk; minimal cold start  
- Dynamic shapes; block-based compile  
- Mixed precision: w8a8, w4a16, w16a16 + fp16/bf16  
- CUDA Graph support  
- Quantized models from Qlip Algorithms → compile

### 6.5 Apple Compiler and Inference API

- Targets: **Apple Silicon M1–M4**  
- `AppleCompileManager`, `AppleBuilderConfig`, `AppleInferenceManager`  
- Not JIT; disk serialization; dynamic shapes  
- Quantized weights from Qlip → native compile  
- Experimental status in marketing; M4+ for w8a8 int8 Neural Engine

### 6.6 Qlip Serve

- Built on **Nvidia Triton Inference Server**  
- Endpoints + async pipelines (docs mention; Modal tutorial uses Triton + Nginx)

---

## 7. Tutorials — каталог и выводы

| Tutorial | URL | Суть |
|----------|-----|------|
| **Elastic FLUX schnell** | [elastic_flux](https://docs.thestage.ai/tutorials/source/elastic_flux.html) | `elastic_models.diffusers`; XL vs S; batch 1–4; benchmark memory/time; Salad blog ref (10k images/$) |
| **Elastic LLMs** | [elastic_transformers](https://docs.thestage.ai/tutorials/source/elastic_transformers.html) | HF transformers API; tiers; batch; ASCII experiment; H100/L40s |
| **Basics of Quantization** | [quantization_tutorial](https://docs.thestage.ai/tutorials/source/quantization_tutorial.html) | Llama-3.1-8B; PTQ MMLU 0.25 vs 0.67 orig; SmoothQuant 0.60; dynamic 0.67 |
| **FLUX ANNA** | [flux_anna_tutorial](https://docs.thestage.ai/tutorials/source/flux_anna_tutorial.html) | `PipelineAnalyser` / FluxAnalyser; PTQBag; selective vs full quant; FID/quality viz |
| **Text-to-Image Evaluation** | [text2image_evaluation](https://docs.thestage.ai/tutorials/source/text2image_evaluation_tutorial.html) | Qlip eval pipeline for T2I models |
| **Serving on Modal** | [modal_thestage](https://docs.thestage.ai/tutorials/source/modal_thestage.html) | Triton + Nginx; **OpenAI-compatible** `/v1/images/generations`; ECR images; commercial license rules |
| **Flux Caching** | [flux_caching_tutorial](https://docs.thestage.ai/tutorials/source/flux_caching_tutorial.html) | **cache-dit** + Elastic Flux; DualCache aggressive/conservative |

### 7.1 Modal serving (важно для GTM)

**Stack:** ANNA + Nvidia Compiler → TheStage model server (Triton) → Nginx → OpenAI API

**Image:** `public.ecr.aws/i3f7g5s7/thestage/elastic-models:0.2.0-diffusers-24.09c`

**GPUs:** L40S, H100, B200 · Python 3.10–3.12

**Cold start:** first run 10–15 min (cache HF weights); then ~60s

**Commercial license (docs):**

- Free commercial use if **average <4 GPUs/hour** (occasional spikes OK)  
- Above → license request on platform (Contact → «Commercial license request»)

**ECR:** anonymous download cap **500 GB/month**

**OpenAI client example:** `base_url` + header `X-Model-Name: flux-1-dev-s-bs4`

### 7.2 Flux + cache-dit

- Combines Elastic tier (S/XL) + caching for extra speedup  
- **DualCache Aggressive:** Fn=1, Bn=0, rdt=0.2 — static scenes  
- **DualCache Conservative:** Fn=4, rdt=0.05 — dynamic scenes  
- diffusers version conflict: compatibility patch in utils

---

## 8. Репозитории и артефакты

| Repo | Содержание |
|------|------------|
| [TheStageAI/ElasticModels](https://github.com/TheStageAI/ElasticModels) | tutorials, `benchmark/`, `examples/modal`, locust scripts |
| Docs notebooks | Linked from tutorials (e.g. `elastic_flux.ipynb`) |

**PyPI registry:** `https://thestage.jfrog.io/artifactory/api/pypi/pypi-thestage-ai-production/simple`

**Packages:** `thestage`, `thestage-elastic-models`, `qlip.core`, `qlip.algorithms`

---

## 9. Product Terms (кратко)

| Product | Effective | Billing |
|---------|-----------|---------|
| Elastic Models | 2026-04-08 v1.0 | Wallet PAYG; no weights export unless stated |
| QLIP/ANNA | 2026-04-08 v1.0 | Wallet; usage = runtime, node-hours, jobs, storage |

**Entity:** The Stage AI, Inc., 702 Rockland Road, Rockland, DE 19732

**AUP:** [app.thestage.ai/ai-use-policy](https://app.thestage.ai/ai-use-policy)

**Data (platform marketing + QLIP terms):** no training on customer models by default unless agreed in writing.

---

## 10. Сопоставление с Customer Input

| Voice notes | Подтверждение в docs |
|-------------|---------------------|
| SDK + self-service | `thestage` CLI, Elastic Models pip, Platform UI |
| Slider quality/speed | ANNA `Analyser.run` + Elastic tiers S–XL |
| Voice (STT/TTS) | Whisper in Elastic Models; solutions on marketing site |
| On-device | Apple Compiler API; on-device SDK (marketing/pricing) |
| GPU usage-based | Elastic PAYG; CLI rented instances (Amazon, Nebius) |
| Orchestration multi-model | Qlip Serve + Triton pipelines; Modal OpenAI API pattern |
| Model provider marketplace | Elastic third-party HF models + Third-Party Terms |
| Nebius | CLI `--provider Nebius` |
| LiveKit analog | Not in docs; Triton + OpenAI-compatible serving closest |
| Praktika / 5M MAU | Not in docs |

---

## 11. Пробелы / не в docs

- Mobile on-device SDK API reference (только Apple compile path в Qlip)  
- Smart glasses / wearables-specific guides  
- Orchestration UI для STT→LLM→TTS chains  
- Публичный pricing per model (только Product Terms + app marketing)  
- Sulfer / enterprise contract specifics  

---

## 12. Быстрые ссылки

- [docs home](https://docs.thestage.ai/)  
- [SSH & tokens](https://docs.thestage.ai/platform/src/thestage-ai-ssh-keys-and-api-tokens.html)  
- [CLI](https://docs.thestage.ai/platform/src/thestage-ai-cli.html)  
- [Elastic Models](https://docs.thestage.ai/elastic_models/docs/source/index.html)  
- [Qlip get started](https://docs.thestage.ai/qlip/docs/source/get_started.html)  
- [ANNA API](https://docs.thestage.ai/qlip/docs/source/anna_api.html)  
- [Nvidia compile](https://docs.thestage.ai/qlip.core/docs/source/qlip.deploy_nvidia_api.html)  
- [Apple compile](https://docs.thestage.ai/qlip.core/docs/source/qlip.deploy_apple_api.html)
