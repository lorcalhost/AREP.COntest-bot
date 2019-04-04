import os
import sys
from multiprocessing import Pool

num = 1
isverbose = False
processes = ('done.py', 'main.py 0')

if len(sys.argv) > 1:
    num = int(sys.argv[1])
    if len(sys.argv) > 2:
        if sys.argv[2] == 'v':
            isverbose = True
    if isverbose:
        processes = ('done.py', 'main.py 0 v')
    for i in range(1, num):
        l = list(processes)
        if isverbose:
            l.append(f'main.py {i} v')
        else:
            l.append(f'main.py {i}')
        processes = tuple(l)


def run_process(process):
    os.system(f'python3 {process}')

pool = Pool(processes=num)
pool.map(run_process, processes)
