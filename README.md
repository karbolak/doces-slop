# DOCES-Slop

An experimental fork of [DOCES (Dynamical Opinion Clusters Exploration Suite)](https://github.com/hfarruda/doces) for studying the spread and amplification of AI-generated content in social-media networks.

This repository contains modifications to the **simulation engine** used in our University of Groningen *Design of Multi-Agent Systems* project.

The research project investigates whether high-volume, adaptive synthetic-content producers can obtain disproportionate exposure through their interaction with social-media recommendation mechanisms.

## Research motivation

Recent work on AI-generated low-effort content, commonly referred to as **AI slop**, suggests that generative AI enables a distinct form of content production characterised by:

- high production volume,
- rapid experimentation,
- replication of successful formats,
- operation of multiple accounts,
- adaptation to algorithmic feedback.

Our project studies these behaviours using an agent-based model.

The main research question is:

> **Under what conditions does the interaction between high-volume synthetic content production, adaptive attention-seeking behaviour, and algorithmic recommendation lead to disproportionate synthetic-content exposure in a social-media network?**

The project builds primarily on:

- Oliveira, K. A., de Arruda, H. F., & Moreno, Y.  
  *Mechanistic interplay between information spreading and opinion polarization.*

- Tang et al.  
  *Behind the "AI slop": exploring the AI-generated viral short video production in China.*

The conceptual feedback mechanism is additionally motivated by:

- Pendergrass, W., Johnson, M., & Bacarella, R.  
  *A strategic cycle of slop: Understanding the commodification of AI feculence and its place in the attention economy.*

## Why fork DOCES?

DOCES already implements many of the mechanisms required by the project:

- directed social networks,
- user opinions,
- posting and reposting,
- limited-memory feeds,
- recommendation filters,
- friendship rewiring,
- information cascades,
- per-user behavioural configuration.

The original Oliveira et al. model selects active users uniformly at random. One of the first extensions in this project will replace this assumption with **heterogeneous activity**, allowing synthetic and human producers to differ in how frequently they become active.

Later extensions may introduce:

- human and synthetic producer types,
- content provenance,
- heterogeneous activity rates,
- adaptive synthetic-producer strategies,
- reward-driven behaviour,
- coordinated synthetic accounts,
- platform interventions.

The goal is to modify the existing model incrementally rather than reimplement the social-media simulation from scratch.

---

# Repository role

This repository contains the **modified DOCES simulation engine**.

The intended project structure is:

```text
DMAS/
├── doces-slop/       # this repository: modified simulator
└── dmas-ai-slop/     # experiments, configs, analysis, figures and paper
```

## Quick start

This repository is our modified fork of DOCES. If you want to work on the simulator or run the current baseline, follow these steps.

### 1. Clone the repository

```bash
git clone <OUR-REPOSITORY-URL>
cd doces-slop
```

You do not need to fork the repository yourself. Clone the shared team repository directly.

### 2. Create the Conda environment

We use Python 3.12 because DOCES currently depends on numpy<2.0 and includes a compiled C extension.

Create the environment from the provided file:

```bash
conda env create -f environment.yaml
```

Activate it:

```bash
conda activate doces-slop
```

Check that the correct Python version is active:

```bash
python --version
```

Expected:

```bash
Python 3.12.x
```

### 3. Install the local DOCES fork

From the repository root:

```bash
pip install -e .
```

The -e flag installs DOCES in editable mode. This means changes to the source code in this repository are immediately reflected when importing doces.

Verify that the package loads:

```bash
python -c "import doces; print('DOCES import works')"
```

Expected output:

DOCES import works

### 4. Run the baseline smoke test

Run:

```bash
python baseline_smoke_test.py
```

The script creates a small directed network, runs the unmodified DOCES simulation for 10,000 iterations, and verifies that opinions, edges, and cascade statistics can be retrieved.

A successful run ends with:

```bash
✓ DOCES smoke test passed.
```

If this works, your local environment is ready for development.