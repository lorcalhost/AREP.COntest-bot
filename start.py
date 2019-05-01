import os
import sys
from multiprocessing import Pool
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('link', help='Your referral link')
parser.add_argument(
    'num', type=int, help='Number of instances you want to run')
parser.add_argument("-v", "--verbose", action="store_true",
                    dest="isverbose", default=False, help="Make the output verbose")
args = parser.parse_args()

processes = ('done.py', f'main.py 0 {args.link}')
if args.isverbose:
    processes = ('done.py', f'main.py 0 {args.link} -v')

if args.link[0:16] == 'https://arep.co/':
    args.link = f'{args.link}/register'
else:
    print(f'Invalid link {args.link}')
    exit()

if args.num < 0:
    print(f'Invalid number {args.num}, must be > 0')
else:
    for i in range(1, args.num):
            l = list(processes)
            if args.isverbose:
                l.append(f'main.py {i} {args.link} -v')
            else:
                l.append(f'main.py {i} {args.link}')
            processes = tuple(l)


def run_process(process):
    os.system(f'python3 {process}')


pool = Pool(processes=args.num)
pool.map(run_process, processes)
