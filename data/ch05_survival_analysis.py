"""Ch5 · persistent iteration vs one-shot skills — survival analysis."""
import json
import statistics as st
from datetime import datetime, timezone

today = datetime(2026, 4, 24, tzinfo=timezone.utc)

d = json.load(open(__file__.rsplit('/',1)[0] + '/ch05_cohort_snapshot.json'))
print(f'\n=== Cohort: {len(d)} skills (created 2025-04 to 2025-10, stars >= 20) ===\n')

def parse(iso):
    if not iso: return None
    s = iso.replace('Z', '')
    if '+' not in s and not s.endswith(':00'):
        pass
    # remove tz if present
    s = s.split('+')[0].rstrip('Z')
    dt = datetime.fromisoformat(s).replace(tzinfo=timezone.utc)
    return dt

def age_days(iso):
    dt = parse(iso)
    return (today - dt).days if dt else None

active, frozen = [], []
for x in d:
    days = age_days(x.get('last_commit_at'))
    if days is None: continue
    (active if days <= 90 else frozen).append(x)

def summary(group, name):
    n = len(group)
    if not n: return
    stars = [x['stars'] for x in group]
    quality = [x['quality_score'] for x in group if x.get('quality_score')]
    gaining = sum(1 for x in group if (x['stars'] or 0) - (x.get('prev_stars') or 0) > 0)

    print(f'--- {name} (n={n}, {n/len(d)*100:.1f}%) ---')
    print(f'  median stars:           {int(st.median(stars))}')
    print(f'  mean stars:             {int(st.mean(stars))}')
    if quality: print(f'  avg quality_score:      {st.mean(quality):.1f}')
    print(f'  % with 100+ stars:      {sum(1 for s in stars if s >= 100)/n*100:.1f}%')
    print(f'  % with 1000+ stars:     {sum(1 for s in stars if s >= 1000)/n*100:.1f}%')
    print(f'  % still gaining stars:  {gaining/n*100:.1f}%')
    print()

summary(d, 'ALL')
summary(active, 'ACTIVE — commit in last 90 days')
summary(frozen, 'FROZEN — no commit > 90 days')

# Deltas
aq = [x['quality_score'] for x in active if x.get('quality_score')]
fq = [x['quality_score'] for x in frozen if x.get('quality_score')]
print('=== Key Deltas ===')
print(f'Quality score:           ACTIVE {st.mean(aq):.1f}  vs  FROZEN {st.mean(fq):.1f}  (+{st.mean(aq)-st.mean(fq):.1f})')

ag = sum(1 for x in active if (x['stars'] or 0) - (x.get('prev_stars') or 0) > 0) / len(active) * 100
fg = sum(1 for x in frozen if (x['stars'] or 0) - (x.get('prev_stars') or 0) > 0) / len(frozen) * 100
print(f'% gaining stars now:     ACTIVE {ag:.1f}%  vs  FROZEN {fg:.1f}%  ({ag-fg:+.1f}pp)')

# Top tier
top_threshold = sorted([x['stars'] for x in d])[int(len(d) * 0.9)]
top_tier = [x for x in d if x['stars'] >= top_threshold]
top_active = sum(1 for x in top_tier if age_days(x.get('last_commit_at')) is not None and age_days(x['last_commit_at']) <= 90)
print(f'\nTop 10% by stars (>= {top_threshold}):  {top_active}/{len(top_tier)} active  ({top_active/len(top_tier)*100:.1f}%)')

bottom_threshold = sorted([x['stars'] for x in d])[int(len(d) * 0.5)]
bottom = [x for x in d if x['stars'] <= bottom_threshold]
bottom_active = sum(1 for x in bottom if age_days(x.get('last_commit_at')) is not None and age_days(x['last_commit_at']) <= 90)
print(f'Bottom 50% by stars (<= {bottom_threshold}): {bottom_active}/{len(bottom)} active  ({bottom_active/len(bottom)*100:.1f}%)')

# Monthly age survival
print('\n=== Survival by age cohort (% active by months since creation) ===')
print(f'{"age mo":<8}{"n":<6}{"active":<8}{"frozen":<8}{"survival %":<10}')
for bucket in range(6, 13):
    lo, hi = bucket * 30, (bucket + 1) * 30
    sub = [x for x in d if age_days(x['created_at']) and lo <= age_days(x['created_at']) < hi]
    if not sub: continue
    sa = sum(1 for x in sub if age_days(x.get('last_commit_at')) is not None and age_days(x['last_commit_at']) <= 90)
    print(f'{bucket:<8}{len(sub):<6}{sa:<8}{len(sub)-sa:<8}{sa/len(sub)*100:.1f}%')
