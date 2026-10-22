# Receipt-responsive content selection

Configure before the first simulation:

```python
model.set_producer_policies(modes, n_strategies=5, epsilon=0.1)
```

Modes are per-user integers: 0 keeps the original uniform innovation path, 1 chooses an opinion bin uniformly, and 2 uses epsilon-greedy feedback. Human agents remain mode 0 in the experiment. Configuration validates modes, strategy count (2 through 32), epsilon, and lifecycle; mid-run reconfiguration is rejected.

The strategy space divides the configured opinion range into equal-width bins. Within the chosen bin, theta is uniform. With probability epsilon, an adaptive producer chooses a bin uniformly. Otherwise it maximizes cumulative receipts of its own accepted original posts in the bin divided by the count of those posts. Empty bins score zero. Greedy ties are randomized. The unconditioned random-bin control has the same uniform marginal opinion distribution as the original innovation rule, but uses an extra random draw.

Receipt feedback is updated at each counted feed insertion, including later cascades carried by other users. Reposts preserve the original producer and strategy, so the reposter does not take reward credit. Background initialization posts do not update strategy scores. Only information observed up to the current iteration is available at choice time. A failed posting-filter attempt increments attempts but neither accepted posts nor receipts. This is an intentionally conditional, per-accepted-post objective, not optimization of receipts per attempt.

`producer_stats` returns user-by-strategy arrays for `attempts`, `accepted`, `receipts`, `early_attempts`, and `late_attempts`. Early and late counts refer to the first and last quarters of each `simulate_dynamics` call; the experiment uses exactly one call per run.

The rule is a minimal feedback mechanism, not a model of actual formats, videos, monetization, account coordination, or learned platform ranking. Estimates use all history without forgetting. Older posts have longer to receive feedback, recent posts are right-censored, and early successes can reinforce exploitation. These assumptions are part of the experiment, not empirically fitted properties of AI-slop producers.

A disabled policy preserves the old engine's RNG path. Tracking mode 0 also preserves the exact old trajectory. Unit tests check that greedy choices change when receipt histories change, epsilon=1 explores all arms, attempts/accepted originals/cascade receipts reconcile, invalid inputs are rejected, and baseline trajectories are unchanged.
