#CoutnMinSketch
==============
The Count–min sketch (or CM sketch) is a probabilistic sub-linear space streaming algorithm which can be used to summarize a data stream in many different ways. The algorithm was invented in 2003 by Graham Cormode and S. Muthu Muthukrishnan.

Count–min sketches are somewhat similar to Bloom filters; the main distinction is that Bloom filters represent sets, while CM sketches represent multisets and frequency tables. Spectral Bloom filters with multi-set policy, are conceptually isomorphic to the Count-Min Sketch.

This particular implementation has been optimized for speed by utilizing numpy, using the fnv64 hash function, and making use of as much of each hash as possible.

Usage
>>> cms = CountMinSketch(200, 500)
>>> cms['foo']
0
>>> cms['foo'] += 5
>>> cms['foo']
5
