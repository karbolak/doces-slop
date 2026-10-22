"""Characterize receipts/provenance across capacities without changing dynamics."""
import unittest
import doces


class FeedReceiptTest(unittest.TestCase):
    def test_repeated_reposts_already_in_feed_do_not_add_receipts(self):
        # Only node 0 posts; node 1 retains every one of its source posts.
        # Removing duplicate suppression would keep adding receipts indefinitely.
        for capacity in (1, 5, 20):
            with self.subTest(capacity=capacity):
                model = doces.Opinion_dynamics(2, [(1, 0)], True, verbose=False)
                model.set_activity_weights([1., 0.])
                model.simulate_dynamics(
                    number_of_iterations=1000, phi=0., mu=0.,
                    posting_filter=doces.UNIFORM, receiving_filter=doces.UNIFORM, b=[0., 0.],
                    feed_size=capacity, rewire=False, delta=0.,
                    min_opinion=-1., max_opinion=1., verbose=False, rand_seed=42)
                # No innovations: reposting must preserve the background origin.
                self.assertEqual(model.post_origin_user_ids, [-1]*(2*capacity))
                self.assertEqual(sum(model.post_received_counts), capacity)
                self.assertEqual(sum(model.activation_counts), 1001)


if __name__ == '__main__':
    unittest.main()
