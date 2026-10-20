"""
retention_policy.py - UCKLab 4-Week (1-Month) TOP 10 News Retention Policy Enforcer
규칙: 10대 뉴스는 최근 4주(28일) 분량만 보관하고, 4주차를 초과한 기사는 자동 삭제(영구 폐기)합니다.
"""

import os
import sys
import datetime
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Windows console UTF-8 setup
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

WP_URL = os.getenv("WP_URL", "https://ucdigin.net").rstrip("/")
PARENT_CATEGORY_ID = 2  # 뉴스 TOP 10

def enforce_4week_retention_policy(retention_days=28, dry_run=False):
    """
    Enforces the 4-week retention policy for Category 2 (뉴스 TOP 10) posts:
    - Finds all published posts in Category 2 older than `retention_days` (default: 28 days).
    - Deletes them permanently via WordPress REST API with force=true.
    """
    print("=" * 75)
    print(f"🛡️ [UCKLab 교칙 집행] 글로벌 TOP 10 뉴스 4주(28일) 보관 & 초과분 자동 삭제 가동")
    print(f"[*] 대상 사이트: {WP_URL} | 카테고리 ID: {PARENT_CATEGORY_ID} | 기준: {retention_days}일 초과")
    print("=" * 75)

    from wp_client import get_wp_client
    client = get_wp_client()

    now = datetime.datetime.now()
    cutoff_date = now - datetime.timedelta(days=retention_days)
    print(f"[*] 현재 일시: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[*] 보관 한계선 (Cutoff Date): {cutoff_date.strftime('%Y-%m-%d %H:%M:%S')} 이전 기사 영구 삭제")

    # Fetch all posts in Category 2
    posts_url = f"{WP_URL}/wp-json/wp/v2/posts?categories={PARENT_CATEGORY_ID}&per_page=100&status=publish,private,draft"
    res = client.session.get(posts_url, headers=client.get_auth_headers(), timeout=20)
    if res.status_code != 200:
        print(f"❌ 포스트 목록 조회 실패 (응답 코드: {res.status_code})")
        return {"success": False, "deleted_count": 0}

    posts = res.json()
    print(f"✓ 카테고리 내 총 {len(posts)}개 포스트 전수 검사 중...")

    expired_posts = []
    active_posts = []

    for p in posts:
        post_id = p["id"]
        title = p["title"]["rendered"]
        post_date_str = p["date"]
        try:
            post_date = datetime.datetime.fromisoformat(post_date_str)
        except Exception:
            post_date = datetime.datetime.strptime(post_date_str[:19], "%Y-%m-%dT%H:%M:%S")

        age_days = (now - post_date).days
        if post_date < cutoff_date:
            expired_posts.append((post_id, title, post_date_str, age_days))
        else:
            active_posts.append((post_id, title, post_date_str, age_days))

    print(f"  • 4주 이내 정상 보관 기사: {len(active_posts)}건")
    print(f"  • 4주 초과 삭제 대상 기사: {len(expired_posts)}건")

    deleted_count = 0
    if not expired_posts:
        print("✅ [정책 준수] 현재 4주(28일)를 초과한 만료 뉴스가 없습니다. (모든 기사 4주 보관 범위 내 유지)")
    else:
        for pid, ptitle, pdate, page in expired_posts:
            print(f"  🗑️ [삭제 대상 감지] ID: {pid} | {page}일 경과 ({pdate}) | {ptitle[:50]}")
            if not dry_run:
                del_url = f"{WP_URL}/wp-json/wp/v2/posts/{pid}?force=true"
                del_res = client.session.delete(del_url, headers=client.get_auth_headers(), timeout=15)
                if del_res.status_code == 200:
                    print(f"    ✓ [영구 삭제 완료] 포스트 ID {pid} 제거됨")
                    deleted_count += 1
                else:
                    print(f"    ⚠️ 삭제 실패 ({del_res.status_code}): {del_res.text[:100]}")
            else:
                print("    [Dry-run] 실제 삭제 생략")

    print(f"\n🎉 4주 보관 정책 집행 완료! (삭제 처리: {deleted_count}건, 보관 유지: {len(active_posts)}건)")
    return {
        "success": True,
        "total_checked": len(posts),
        "retained_count": len(active_posts),
        "deleted_count": deleted_count,
        "expired_found": len(expired_posts)
    }

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=28, help="Retention period in days (default: 28)")
    parser.add_argument("--dry-run", action="store_true", help="Dry run without actual deletion")
    args = parser.parse_args()

    enforce_4week_retention_policy(retention_days=args.days, dry_run=args.dry_run)
