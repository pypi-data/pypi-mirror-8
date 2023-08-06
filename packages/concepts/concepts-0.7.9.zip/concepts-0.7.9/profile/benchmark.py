# benchmark.py - benchmark time to create bigger lattice and profile it

import sys
import os
import time

sys.path.insert(1, os.pardir)
import concepts


start = time.time()
c = concepts.load_cxt('segments.cxt', encoding='utf-8')
print('%r' % c.lattice)
print(time.time() - start)


import cProfile as Profile

c = concepts.load_cxt('segments.cxt', encoding='utf-8')
Profile.run('c.lattice')
