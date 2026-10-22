# DOCES-Slop

An experimental fork of [DOCES (Dynamical Opinion Clusters Exploration Suite)](https://github.com/hfarruda/doces) for studying the spread and amplification of AI-generated content in social-media networks.

This repository contains modifications to the **simulation engine** used in our University of Groningen *Design of Multi-Agent Systems* project.

The implemented study isolates producer activity and prevalence in content diffusion. Its question is:

> How do producer activity and prevalence affect a labelled subgroup's share of feed receipts relative to its share of production in DOCES?

AI-slop production motivates the study, but the synthetic label is a provenance marker. It does not encode content quality, AI generation, coordination, or a learned response to rewards. The current engine includes weighted activation, persistent origin identifiers and receipt counters. Producer weights and content-generation rules remain fixed throughout each run.

See [VALIDATION.md](VALIDATION.md) for verified measurement semantics and the feed-capacity regression test. The sibling research repository contains the main sweep, the separate 200-world capacity experiment, and the final report.

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

The original Oliveira et al. model selects active users uniformly. This fork adds optional non-negative activity weights. With no weights configured, the original selection path remains available. Reposts retain their original producer identity, while receipts count accepted follower feed insertions that are not already present in the recipient's feed.

Adaptive production strategies, reward-driven behaviour, coordinated accounts and platform interventions remain future work. Existing opinion dynamics and follower rewiring do not implement those producer strategies.

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
git clone https://github.com/karbolak/doces-slop.git
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