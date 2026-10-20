"""
run_vol40_publish.py - Publish Vol. 40 (2026-10-05) Weekly HBR Global TOP 10 News Review
"""

import os
import sys

# Windows UTF-8 console output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(CURRENT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from wp_publisher import publish_weekly_hbr_report

if __name__ == "__main__":
    print("=" * 75)
    print("🚀 [Vol. 40] 2026년 10월 5일(월) 주간 글로벌 TOP 10 뉴스리뷰 발행 시작")
    print("=" * 75)
    res = publish_weekly_hbr_report(report_id="WEEKLY-2026-W40")
    print("\n" + "=" * 75)
    print("🎉 발행 결과 요약:")
    print(res)
    print("=" * 75)
