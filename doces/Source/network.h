/*
MIT License

Copyright (c) 2023 Henrique F. de Arruda, Kleber A. Oliveira, and Yamir Moreno

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/
#include "utils.h"

/* Modes: 0 original uniform innovation, 1 random bin, 2 epsilon-greedy bin.
 * Counts include only original innovations and their provenance-preserving receipts. */
typedef struct {
    unsigned int nStrategies;
    double epsilon;
    int *modes;
    unsigned long long *attempts, *accepted, *receipts;
    unsigned long long *earlyAttempts, *lateAttempts;
} ProducerPolicy;

unsigned int selectProducerArm(ProducerPolicy *policy, unsigned int user);
void destroyProducerPolicy(ProducerPolicy *policy);

typedef struct {
    ProducerPolicy *producerPolicy;
    unsigned int vCount;
    unsigned int **invertedAdjlist;
    unsigned int *neighborsCount;
    bool isDirected;

    FLOAT *activityCumulativeWeights;
    FLOAT totalActivityWeight;

    /* Number of times each user has been activated. */
    unsigned long long *activationCounts;
} Network;

typedef struct {
    unsigned int source;
    unsigned int target;
} Edge;

typedef struct {
    bool isDirected;
    unsigned int vCount;
    unsigned int eCount;
    Edge *edges;
} EdgeList;

void edgeList2Network(Network *network, EdgeList edgeList, bool verbose);
void network2EdgeList(Network *network, EdgeList *edgeList, bool verbose);
void printNetwork(Network *network);
void rewireConnectionNewTarget(Network *network, unsigned int nodeId, unsigned int target, unsigned int newTarget);
bool rewireConnectionToRandom(Network *network, unsigned int nodeId, unsigned int target);
unsigned int randomNeighbor(Network *network, unsigned int agent);
unsigned int randomNode(Network *network);
unsigned int selectActiveNode(Network *network);

bool setActivityWeights(
    Network *network,
    const FLOAT *weights,
    unsigned int count
);

void clearActivityWeights(Network *network);

void destroyNetwork(Network *network);

