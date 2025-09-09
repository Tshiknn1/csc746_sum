import re
import argparse
import os

PEAK_FLOPS = 3.92e10
PEAK_BANDWIDTH = 2.048e11

TRANSFORM_LUT = {
    'runtime': {
        'sum_direct'    :   lambda n, t: t,
        'sum_vector'    :   lambda n, t: t,
        'sum_indirect'  :   lambda n, t: t,
    },
    'mflops_per_s': {
        'sum_direct'    :   lambda n, t: (n / t) / 1e9,
        'sum_vector'    :   lambda n, t: (n / t) / 1e9,
        'sum_indirect'  :   lambda n, t: (n / t) / 1e9,
    },
    'bandwidth': {
        'sum_direct'    :   lambda n, t: 0,
        'sum_vector'    :   lambda n, t: (4 * n / t) / 1e6, 
        'sum_indirect'  :   lambda n, t: (4 * n / t) / 1e6
    },
    'pct_bandwidth': {
        'sum_direct'    :   lambda n, t: 0,
        'sum_vector'    :   lambda n, t: 100 * (4 * n / t) / PEAK_BANDWIDTH,
        'sum_indirect'  :   lambda n, t: 100 * (4 * n / t) / PEAK_BANDWIDTH
    },
    'avg_latency':  {
        'sum_direct'    :   lambda n, t: 0,
        'sum_vector'    :   lambda n, t: (t / n) * 1e9,
        'sum_indirect'  :   lambda n, t: (t / n) * 1e9
    }
}

parser = argparse.ArgumentParser(prog='summarize.py')
parser.add_argument('filename')
parser.add_argument('indirect')
parser.add_argument('trial')
parser.add_argument('-t', '--transformation', default='runtime')
parser.add_argument('-a', '--average', action='store_true')
args = parser.parse_args()
fn = args.filename

if args.transformation not in TRANSFORM_LUT.keys():
    raise Exception('not a recognized transformation')

with open(fn, 'r') as f:
    lines = f.readlines()

current_case = None
current_trial = None
current_output = None
all_outputs = {}
for l in lines:
    m = re.search('Working on method (.+), trial (\d+)', l)
    if m:
        if current_output is not None:
            if current_case in ('sum_direct', 'sum_vector') or \
                    (current_case == args.indirect and current_trial == args.trial):
                for n, t in current_output.items():
                    if n == 'average':
                        if not 'average' in all_outputs.keys():
                            all_outputs['average'] = {}
                        all_outputs['average'][current_case] = t
                        continue
                    if n not in all_outputs.keys():
                        all_outputs[int(n)] = {}
                    if current_case == 'sum_indirect_seed':
                        current_case = 'sum_indirect'
                    all_outputs[int(n)][current_case] = t
        current_case = m[1]
        current_trial = m[2]
        current_output = {}
    else:
        m = re.search('Problem size N=(\d+) took (\d+\.\d+) seconds Sum result = (\d+\.\d+)', l)
        if m:
            n = float(m.group(1))
            t = float(m.group(2))
            current_output[int(m.group(1))] = TRANSFORM_LUT[args.transformation]['sum_indirect' if current_case == 'sum_indirect_seed' else current_case](n, t)
            if args.average:
                current_output['average'] = sum([v for k, v in current_output.items()]) / len(list(current_output.keys()))
            if current_output is None:
                raise Exception('file may be misformatted or there may be an issue with the code.')

# do it again
if current_case in ('sum_direct', 'sum_vector') or \
        (current_case == args.indirect and current_trial == args.trial):
    for n, t in current_output.items():
        if n not in all_outputs.keys():
            all_outputs[int(n)] = {}
        if current_case == 'sum_indirect_seed':
            current_case = 'sum_indirect'
        all_outputs[int(n)][current_case] = t

to_write = []
to_write.append('Problem size,Direct sum,Vector sum,Indirect sum\n')
for n in sorted([k for k in all_outputs.keys() if k != 'average']):
    to_write.append(f'{n},{all_outputs[n]["sum_direct"]},{all_outputs[n]["sum_vector"]},{all_outputs[n]["sum_indirect"]}\n')
if args.average:
    to_write.append(f'average,{all_outputs["average"]["sum_direct"]},{all_outputs["average"]["sum_vector"]},{all_outputs["average"]["sum_indirect"]}')

fn_out = fn.split('.')[0] + f'_{args.indirect}_{args.trial}_{args.transformation}.csv'
with open(fn_out, 'w+') as f:
    f.writelines(to_write)