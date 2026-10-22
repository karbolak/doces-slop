"""Test the native decision rule against independently specified reward histories."""
import subprocess
import tempfile
import unittest
from pathlib import Path


class NativeSelectionTest(unittest.TestCase):
    def test_greedy_choice_changes_when_receipt_feedback_changes(self):
        source=Path(__file__).resolve().parents[1]/'doces/Source'
        harness=r'''
#include "network.h"
#include <assert.h>
int main(void){
    int modes[1]={2};
    unsigned long long accepted[5]={2,2,2,2,2};
    unsigned long long receipts[5]={0,0,0,0,20};
    ProducerPolicy policy={0};
    policy.nStrategies=5; policy.modes=modes; policy.epsilon=0.;
    policy.accepted=accepted; policy.receipts=receipts;
    for(int i=0;i<100;i++) assert(selectProducerArm(&policy,0)==4);
    receipts[0]=100;
    for(int i=0;i<100;i++) assert(selectProducerArm(&policy,0)==0);
    policy.epsilon=1.;
    int counts[5]={0};
    for(int i=0;i<1000;i++) counts[selectProducerArm(&policy,0)]++;
    for(int i=0;i<5;i++) assert(counts[i]>100 && counts[i]<300);
    return 0;
}
'''
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)
            (path/'check.c').write_text(harness)
            build=subprocess.run(['gcc','-std=c11','-D_GNU_SOURCE','-I',str(source),
                                  str(path/'check.c'),str(source/'network.c'),str(source/'utils.c'),
                                  '-lm','-o',str(path/'check')],capture_output=True,text=True)
            self.assertEqual(build.returncode,0,build.stderr)
            subprocess.run([str(path/'check')],check=True)


if __name__=='__main__': unittest.main()
