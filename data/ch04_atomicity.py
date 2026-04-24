"""
Atomicity analysis for Blue Book Chapter 4.
Hypothesis: 宝玉's "原子化" principle — more focused skills score higher quality.
Test: bucketed correlation between README size (proxy for scope) and quality_score.
"""
import json, statistics

d = json.load(open('/tmp/ch4_top500.json'))
d = [x for x in d if x.get('readme_size') is not None and x.get('quality_score') is not None and x.get('stars')]

# Bucket by readme size (bytes, not tokens)
buckets = {
    '<2KB': (0, 2000),
    '2-5KB': (2000, 5000),
    '5-10KB': (5000, 10000),
    '10-20KB': (10000, 20000),
    '20-40KB': (20000, 40000),
    '40KB+': (40000, 10**9),
}

print(f'=== Atomicity Analysis · Top 500 Skills (≥500 stars) ===')
print(f'Total: {len(d)} skills\n')
print(f'{"Size bucket":<12} {"# skills":<10} {"avg quality":<14} {"avg stars":<12} {"max stars":<10}')
print('-' * 60)

for name, (lo, hi) in buckets.items():
    subset = [x for x in d if lo <= x['readme_size'] < hi]
    if not subset: continue
    avg_q = statistics.mean(x['quality_score'] for x in subset)
    avg_s = statistics.mean(x['stars'] for x in subset)
    max_s = max(x['stars'] for x in subset)
    print(f'{name:<12} {len(subset):<10} {avg_q:<14.1f} {avg_s:<12.0f} {max_s:<10}')

# Correlation
import math
def pearson(xs, ys):
    mx, my = sum(xs)/len(xs), sum(ys)/len(ys)
    num = sum((x-mx)*(y-my) for x,y in zip(xs,ys))
    den = math.sqrt(sum((x-mx)**2 for x in xs) * sum((y-my)**2 for y in ys))
    return num/den if den else 0

sizes = [x['readme_size'] for x in d]
qscores = [x['quality_score'] for x in d]
stars = [x['stars'] for x in d]

r_size_quality = pearson(sizes, qscores)
r_size_stars = pearson(sizes, [math.log10(s) for s in stars])
print(f'\nPearson r (README size ↔ quality score):  {r_size_quality:+.3f}')
print(f'Pearson r (README size ↔ log10 stars):     {r_size_stars:+.3f}')

# Category analysis — which category is more atomic on avg?
from collections import defaultdict
cat_sizes = defaultdict(list)
cat_quality = defaultdict(list)
for x in d:
    cat_sizes[x['category']].append(x['readme_size'])
    cat_quality[x['category']].append(x['quality_score'])
print(f'\n=== By Category ===')
print(f'{"Category":<20} {"median size":<14} {"avg quality":<14} {"n":<4}')
print('-' * 60)
for cat in sorted(cat_sizes, key=lambda c: -len(cat_sizes[c])):
    print(f'{cat:<20} {statistics.median(cat_sizes[cat]):<14.0f} {statistics.mean(cat_quality[cat]):<14.1f} {len(cat_sizes[cat]):<4}')

# Find the SWEET SPOT — which bucket has BOTH highest stars AND highest quality?
print(f'\n=== Top 10 by stars — their README sizes ===')
top10 = sorted(d, key=lambda x: -x['stars'])[:10]
for x in top10:
    print(f'  {x["stars"]:>6}★ | {x["readme_size"]:>6}B | q={x["quality_score"]:>2} | {x["repo_full_name"]}')

print(f'\n=== Top 10 by quality_score — their README sizes ===')
topq = sorted([x for x in d if x['stars'] >= 500], key=lambda x: -x['quality_score'])[:10]
for x in topq:
    print(f'  q={x["quality_score"]:>2} | {x["stars"]:>6}★ | {x["readme_size"]:>6}B | {x["repo_full_name"]}')
