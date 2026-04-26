"""Ch9 · Distribution 第四条边 · Hub 数据分析"""
import json, statistics as st
from datetime import datetime, timezone
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
TODAY = datetime(2026, 4, 26, tzinfo=timezone.utc)


def parse(iso):
    if not iso: return None
    s = iso.split('+')[0].rstrip('Z')
    return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)


def main():
    d = json.load(open(HERE / 'ch09_top1000_snapshot.json'))
    print(f'\n=== Top {len(d)} skills (≥100 stars) ===\n')

    # License
    licenses = Counter((x.get('license') or 'NOASSERTION').upper() for x in d)
    print('License distribution:')
    for l, c in licenses.most_common(10):
        print(f'  {l:<20} {c:>4} ({c/len(d)*100:5.1f}%)')

    # Commercial signals
    with_homepage = sum(1 for x in d if (x.get('homepage_url') or '').strip())
    print(f'\nHas homepage URL: {with_homepage}/{len(d)} ({with_homepage/len(d)*100:.1f}%)')
    print(f'No license:       {licenses.get("NOASSERTION", 0)} ({licenses.get("NOASSERTION", 0)/len(d)*100:.1f}%)')

    # Age
    ages = [(TODAY - parse(x['created_at'])).days for x in d if parse(x.get('created_at'))]
    print(f'\nAge distribution (created → today):')
    print(f'  median: {st.median(ages)} days')
    print(f'  mean:   {sum(ages)/len(ages):.0f} days')
    for d_thresh in [30, 90, 180, 365, 730]:
        c = sum(1 for a in ages if a <= d_thresh)
        print(f'  ≤{d_thresh:>3} days: {c:>4} ({c/len(ages)*100:5.1f}%)')

    # Author concentration
    authors = json.load(open(HERE / 'ch09_authors_snapshot.json'))
    counter = Counter(x['author_name'] for x in authors)
    print(f'\nAuthor concentration in Top 1000:')
    print(f'  Unique authors: {len(counter)}')
    single = sum(1 for c in counter.values() if c == 1)
    multi = len(counter) - single
    multi_skills = sum(c for c in counter.values() if c > 1)
    print(f'  Single-skill authors: {single} ({single/len(counter)*100:.1f}%)')
    print(f'  Multi-skill authors:  {multi} ({multi/len(counter)*100:.1f}%)')
    print(f'  Slots owned by multi-skill authors: {multi_skills} ({multi_skills/len(authors)*100:.1f}%)')

    print(f'\nTop 15 prolific authors:')
    for a, c in counter.most_common(15):
        print(f'  {a:<32} {c}')


if __name__ == '__main__':
    main()
