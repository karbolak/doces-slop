The report revision retains simulator revision `2062803b4de482a6ec6abc1e0913abd88542119f` without changing its C or Python dynamics.

`tests/test_feed_receipts.py` checks capacities 1, 5, and 20 on a controlled two-user graph with no innovations and uniform posting/receiving filters. It verifies that reposts retain background provenance and already-retained posts do not add receipts. Run from the parent folder with the rebuilt local engine on `PYTHONPATH`:

```sh
PYTHONPATH="$PWD/doces-slop" python -m unittest discover -s doces-slop/tests -v
```

Interpretation details verified against `Source/dynamics.c`, `Source/post.c`, and `Python/opinionDynamics.c`:

- A request of T iterations executes T+1 activations in a fresh simulation. This inherited convention is retained for comparison with the beta sweep.
- Receipt counts increase only for accepted follower deliveries absent from that feed. Reinsertion after displacement can count again; receipts are not unique-user reach.
- Accepted deliveries can affect opinions even when duplicate suppression prevents a new receipt.
- The initial background stock has N times feed capacity distinct posts. These have origin -1 and can spread despite exclusion from group metrics.
- Feed capacity changes initialization, retention, repost order and duplicate suppression together.
- Activation weights affect both innovation opportunities and repost opportunities under a fixed total event budget.

The experiment and its complete data are in the sibling research repository. The pre-existing build emits setuptools/NumPy deprecation and C indentation warnings; these are not test failures.
