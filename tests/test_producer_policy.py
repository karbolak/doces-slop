"""Real-engine checks for content selection, accounting and compatibility."""
import unittest
import numpy as np
import doces


def simulate(modes=None, **options):
    model=doces.Opinion_dynamics(3, [(0,1),(1,0),(2,0),(0,2)], True, verbose=False)
    if modes is not None:
        model.set_producer_policies(modes, n_strategies=5, epsilon=.1)
    settings=dict(number_of_iterations=10000, phi=0., mu=.2,
                  posting_filter=0, receiving_filter=0, b=[0.,-.3,.3],
                  feed_size=5, rewire=False, delta=.0, verbose=False, rand_seed=42)
    settings.update(options)
    model.simulate_dynamics(**settings)
    return model


class ProducerPolicyTest(unittest.TestCase):
    def test_tracking_baseline_does_not_change_original_trajectory(self):
        original=simulate()
        tracked=simulate([0,0,0])
        for name in ['opinions','edge_list','activation_counts','post_thetas',
                     'post_received_counts','post_origin_user_ids']:
            self.assertEqual(getattr(original,name),getattr(tracked,name),name)

    def test_attempt_acceptance_and_cascade_receipts_reconcile(self):
        model=simulate([2,0,0])
        stats=model.producer_stats
        attempts=np.asarray(stats['attempts'])
        accepted=np.asarray(stats['accepted'])
        receipts=np.asarray(stats['receipts'])
        self.assertTrue((attempts>=accepted).all())
        self.assertGreater(int(attempts.sum()),int(accepted.sum()))
        expected_posts=np.zeros((3,5),dtype=int)
        expected_receipts=np.zeros((3,5),dtype=int)
        for origin, theta, received in zip(model.post_origin_user_ids,model.post_thetas,model.post_received_counts):
            if origin>=0:
                arm=min(4,int((theta+1)*2.5))
                expected_posts[origin,arm]+=1
                expected_receipts[origin,arm]+=received
        np.testing.assert_array_equal(accepted,expected_posts)
        np.testing.assert_array_equal(receipts,expected_receipts)
        self.assertTrue((np.asarray(stats['early_attempts'])+np.asarray(stats['late_attempts'])<=attempts).all())
        self.assertGreater(int(receipts.sum()),0)

    def test_invalid_and_midrun_configuration_is_rejected(self):
        for modes,k,eps in [([0,2],5,.1),([0,3,0],5,.1),([0,2,0],0,.1),
                            ([0,2,0],5,float('nan')),([0,2,0],5,1.1),([0,1.5,0],5,.1)]:
            model=doces.Opinion_dynamics(3,[(0,1)],True,verbose=False)
            with self.assertRaises((ValueError,TypeError)):
                model.set_producer_policies(modes,k,eps)
        model=simulate()
        with self.assertRaises(ValueError):
            model.set_producer_policies([0,2,0])


if __name__=='__main__': unittest.main()
