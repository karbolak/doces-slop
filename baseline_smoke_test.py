"""
Minimal smoke test for DOCES.

Purpose:
- verify that the local DOCES build imports correctly;
- create a small directed social network;
- run the unmodified opinion-dynamics model;
- verify that opinions, edges, and cascade statistics are returned.

This is NOT intended to reproduce Oliveira et al. yet.
"""

import random

import doces


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

SEED = 42
N_AGENTS = 100
EDGE_PROBABILITY = 0.05
N_ITERATIONS = 10_000

PHI = 0.5
MU = 1.0
DELTA = 0.1
FEED_SIZE = 5


def make_directed_random_network(
    n_agents: int,
    edge_probability: float,
    seed: int,
) -> list[tuple[int, int]]:
    """
    Generate a simple directed Erdos-Renyi-style network.

    Each ordered pair (i, j), i != j, becomes an edge independently
    with probability edge_probability.
    """
    rng = random.Random(seed)

    edges = []

    for source in range(n_agents):
        for target in range(n_agents):
            if source == target:
                continue

            if rng.random() < edge_probability:
                edges.append((source, target))

    return edges


def main() -> None:
    print("=== DOCES baseline smoke test ===")
    print(f"Agents:      {N_AGENTS}")
    print(f"Iterations:  {N_ITERATIONS}")
    print(f"Seed:        {SEED}")

    # ---------------------------------------------------------------
    # 1. Build a small network
    # ---------------------------------------------------------------

    edges = make_directed_random_network(
        n_agents=N_AGENTS,
        edge_probability=EDGE_PROBABILITY,
        seed=SEED,
    )

    print(f"Initial edges: {len(edges)}")

    assert len(edges) > 0, "Generated network contains no edges."

    # ---------------------------------------------------------------
    # 2. Create the DOCES model
    # ---------------------------------------------------------------

    model = doces.Opinion_dynamics(
        N_AGENTS,
        edges,
        True,
    )

    posting_filter = 0
    receiving_filter = 0

    # DOCES requires initial opinions for a fresh simulation.
    opinion_rng = random.Random(SEED + 1)

    initial_opinions = [
        opinion_rng.uniform(-1.0, 1.0)
        for _ in range(N_AGENTS)
    ]

    # ---------------------------------------------------------------
    # 3. Run simulation
    # ---------------------------------------------------------------

    result = model.simulate_dynamics(
        N_ITERATIONS,
        PHI,
        MU,
        posting_filter,
        receiving_filter,
        b=initial_opinions,
        feed_size=FEED_SIZE,
        rewire=True,
        cascade_stats_output_file=None,
        min_opinion=-1,
        max_opinion=1,
        delta=DELTA,
        verbose=False,
        rand_seed=SEED,
    )

    # ---------------------------------------------------------------
    # 4. Basic output checks
    # ---------------------------------------------------------------

    assert isinstance(result, dict), (
        f"Expected dictionary from simulate_dynamics(), "
        f"got {type(result)}"
    )

    assert "b" in result, "Simulation output has no 'b' opinion vector."
    assert "edges" in result, "Simulation output has no 'edges'."

    opinions = result["b"]
    final_edges = result["edges"]

    assert len(opinions) == N_AGENTS, (
        f"Expected {N_AGENTS} opinions, got {len(opinions)}"
    )

    assert all(-1 <= opinion <= 1 for opinion in opinions), (
        "At least one opinion lies outside [-1, 1]."
    )

    # ---------------------------------------------------------------
    # 5. Cascade statistics
    # ---------------------------------------------------------------

    cascade_stats = model.get_cascade_stats_dict()

    assert isinstance(cascade_stats, dict), (
        "Expected cascade statistics to be returned as a dictionary."
    )

    # ---------------------------------------------------------------
    # 6. Print useful summary
    # ---------------------------------------------------------------

    mean_opinion = sum(opinions) / len(opinions)

    print()
    print("--- Simulation completed successfully ---")
    print(f"Final edges:  {len(final_edges)}")
    print(f"Mean opinion: {mean_opinion:.4f}")
    print(f"Min opinion:  {min(opinions):.4f}")
    print(f"Max opinion:  {max(opinions):.4f}")

    print()
    print("Cascade-stat keys:")
    for key in cascade_stats:
        value = cascade_stats[key]

        try:
            length = len(value)
            print(f"  {key}: {length} entries")
        except TypeError:
            print(f"  {key}: {value}")

    print()
    print("✓ DOCES smoke test passed.")


if __name__ == "__main__":
    main()