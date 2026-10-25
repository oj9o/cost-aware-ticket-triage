"""Score this policy using a separately obtained, unchanged instructor lab."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import platform
import sys

os.environ.setdefault('OMP_NUM_THREADS', '1')
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--lab', required=True, type=Path, help='Original Lab 9 directory containing lab.py and default.py')
parser.add_argument('--output', type=Path, default=Path('reproduced-metrics.json'))
args = parser.parse_args()
lab_dir = args.lab.resolve()
for name in ('lab.py', 'default.py'):
    if not (lab_dir/name).is_file():
        parser.error(f'Lab directory is missing {name}')
sys.path.insert(0, str(lab_dir))
import lab
import sklearn

world = lab.build_world()
policy_path = Path(__file__).resolve().with_name('policy.py')
results = {}
for name, path in [('default', lab_dir/'default.py'), ('student', policy_path)]:
    fitted = lab.fit_policy(path, world)
    assert fitted['labeling']['oracle_used'] <= lab.LABEL_BUDGET
    for split in ('eval', 'championship'):
        score = lab.score_fitted(fitted, world[split], lab.resolve_econ(), split == 'championship')
        m = score['metrics']
        assert m['oracle_calls'] <= m['oracle_budget'] and m['oracle_invalid'] == 0
        results[f'{name}_{split}'] = {key: m[key] for key in
            ['n', 'net_per_1000', 'cost_per_1000', 'baseline_per_1000', 'critical_total',
             'critical_misses', 'oracle_calls', 'oracle_budget', 'oracle_invalid',
             'sla_violations', 'mean_l2_wait']}
        results[f'{name}_{split}']['total_savings_aed'] = m['net_per_1000'] * m['n']/1000
        if name == 'student' and split == 'championship':
            regional_misses = lab.shift_summary(world, score['tickets'])['student_regional_misses']
        print(f"{name:7s} {split:12s}: AED {m['net_per_1000']:,.2f}/1,000; critical misses {m['critical_misses']}", flush=True)
for split in ('eval', 'championship'):
    assert results[f'student_{split}']['net_per_1000'] > results[f'default_{split}']['net_per_1000']
output = {'seed': lab.SEED, 'python': platform.python_version(), 'sklearn': sklearn.__version__,
          'runs': results, 'regional_network_critical_misses': regional_misses}
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(lab.json_safe(output), indent=2)+'\n')
print(f'Budget and starter-improvement checks passed. Saved {args.output}')
