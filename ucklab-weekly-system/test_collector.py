import sys, os
sys.path.insert(0, r'c:\UCKLab\ucklab.org\ucklab-app\ucklab-weekly-system\src')
from collector import collect_weekly_top10_news

headlines, osint = collect_weekly_top10_news()
print(f'Collected {len(headlines)} headlines:')
for h in headlines:
    hid = h["id"]
    title = h["headline"]
    source = h["source"]
    print(f"[{hid}] {title[:70]} ({source})")
