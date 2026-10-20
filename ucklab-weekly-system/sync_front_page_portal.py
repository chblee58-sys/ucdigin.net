import os
import sys
import glob
import json
import datetime
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Ensure UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "src"))

load_dotenv(os.path.join(BASE_DIR, ".env"))
WP_URL = os.getenv("WP_URL", "https://ucdigin.net")
WP_USER = os.getenv("WP_USER", "AutoBot_Editor")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD", "5kOS QdBg 6Prd qR4F qixR lg43")

from wp_publisher import build_full_hbr_report_content, update_aioseo_post
from chart_generator import generate_weekly_chart, upload_chart_to_wordpress, generate_category_detail_charts, upload_all_category_charts

def get_latest_data_files():
    """Dynamically finds the latest available weekly data files or runs collectors if needed."""
    data_dir = os.path.join(BASE_DIR, "data")
    hl_files = sorted(glob.glob(os.path.join(data_dir, "weekly_headlines_*.json")))
    today_num = datetime.datetime.now().strftime("%Y%m%d")
    today_hl = os.path.join(data_dir, f"weekly_headlines_{today_num}.json")

    # If today's headlines don't exist, try collecting
    if not os.path.exists(today_hl):
        try:
            from collector import collect_weekly_top10_news
            print("🔄 [Portal Sync] 당일 헤드라인 미존재 -> 실시간 OSINT 수집기 가동...")
            collect_weekly_top10_news()
            hl_files = sorted(glob.glob(os.path.join(data_dir, "weekly_headlines_*.json")))
        except Exception as e:
            print(f"⚠️ OSINT 수집 예외: {e}")

    if not hl_files:
        raise FileNotFoundError("주간 헤드라인 데이터 파일(weekly_headlines_*.json)을 찾을 수 없습니다.")

    latest_hl_path = hl_files[-1]
    date_part = os.path.basename(latest_hl_path).replace("weekly_headlines_", "").replace(".json", "")
    
    osint_path = os.path.join(data_dir, f"weekly_osint_radar_{date_part}.json")
    col_path = os.path.join(data_dir, f"weekly_column_{date_part}.json")

    # If column does not exist for this date, generate it
    if not os.path.exists(col_path):
        try:
            from column import generate_weekly_column
            print(f"🔄 [Portal Sync] {date_part} 칼럼 미존재 -> 2-에이전트 칼럼 생성기 가동...")
            with open(latest_hl_path, "r", encoding="utf-8") as f:
                hl_data = json.load(f)
            os_data = {}
            if os.path.exists(osint_path):
                with open(osint_path, "r", encoding="utf-8") as f:
                    os_data = json.load(f)
            generate_weekly_column(hl_data, os_data)
        except Exception as e:
            print(f"⚠️ 칼럼 생성 예외: {e}")

    return latest_hl_path, osint_path, col_path, date_part

def run_sync():
    # 1. Discover latest data files
    latest_hl_path, osint_path, col_path, date_part = get_latest_data_files()
    
    try:
        dt = datetime.datetime.strptime(date_part, "%Y%m%d")
        date_display = dt.strftime("%Y년 %m월 %d일")
        week_num = dt.strftime("%U")
        year_str = dt.strftime("%Y")
        report_id = f"WEEKLY-{year_str}-W{week_num}"
    except Exception:
        date_display = datetime.datetime.now().strftime("%Y년 %m월 %d일")
        report_id = f"WEEKLY-{datetime.datetime.now().strftime('%Y-W%U')}"

    print(f"🚀 [Portal Sync] 최신 주간 데이터 동기화 시작 (날짜: {date_display}, ID: {report_id})...")

    with open(latest_hl_path, "r", encoding="utf-8") as f:
        headlines = json.load(f)

    with open(osint_path, "r", encoding="utf-8") as f:
        osint_data = json.load(f)

    with open(col_path, "r", encoding="utf-8") as f:
        column_data = json.load(f)

    # 2. Master Chart check/upload
    chart_file = os.path.join(BASE_DIR, "storage", "charts", f"chart_{report_id}.png")
    if not os.path.exists(chart_file):
        print(f"📊 [Portal Sync] 메인 차트 생성 중: {chart_file}")
        chart_file = generate_weekly_chart(report_id, headlines)

    print(f"📤 [Portal Sync] 메인 차트 워드프레스 미디어 라이브러리 연동 중...")
    master_chart_url = upload_chart_to_wordpress(chart_file, WP_URL, WP_USER, WP_APP_PASSWORD)
    if not master_chart_url:
        master_chart_url = f"{WP_URL}/wp-content/uploads/{dt.strftime('%Y/%m')}/chart_{report_id}.png"

    # Category Charts
    cat_charts_json = os.path.join(BASE_DIR, "data", "category_chart_urls.json")
    category_charts = {}
    if os.path.exists(cat_charts_json):
        try:
            with open(cat_charts_json, "r", encoding="utf-8") as f:
                category_charts = json.load(f)
        except Exception:
            pass

    # Category Public URLs mapping
    auth = HTTPBasicAuth(WP_USER, WP_APP_PASSWORD)
    category_public_urls = {
        "politics": f"{WP_URL}/category/news-top10/politics/",
        "economy": f"{WP_URL}/category/news-top10/economy/",
        "society": f"{WP_URL}/category/news-top10/society/",
        "culture": f"{WP_URL}/category/news-top10/culture/",
        "finance": f"{WP_URL}/category/news-top10/finance/",
        "defense": f"{WP_URL}/category/news-top10/defense/",
        "christianity": f"{WP_URL}/category/news-top10/christianity/",
        "science": f"{WP_URL}/category/news-top10/science/",
        "climate": f"{WP_URL}/category/news-top10/climate/",
        "sports": f"{WP_URL}/category/news-top10/sports/"
    }
    print(f"✓ Category public URLs mapped to /category/news-top10/<category>/: {len(category_public_urls)} categories")

    # 3. Build 2-Column Desktop Portal Gutenberg content
    print("🎨 [Portal Sync] Building 2-Column Desktop Portal HTML...")
    full_content = build_full_hbr_report_content(
        report_id=report_id,
        column_data=column_data,
        news_items=headlines,
        osint_data=osint_data,
        chart_url=master_chart_url,
        category_charts=category_charts,
        category_public_urls=category_public_urls
    )

    print(f"✓ Rendered content size: {len(full_content)} characters")

    # 4. Discover & Update Front Page (ID: 16296 or dynamically via settings)
    front_page_id = 16296
    try:
        settings_res = requests.get(f"{WP_URL}/wp-json/wp/v2/settings", auth=auth, timeout=15)
        if settings_res.status_code == 200:
            discovered_id = settings_res.json().get("page_on_front")
            if discovered_id:
                front_page_id = int(discovered_id)
    except Exception as e:
        print(f"Settings discovery notice: {e}")

    vol_num = week_num if 'week_num' in locals() else "39"
    title = f"[UCKLab Strategic Review] Vol. {vol_num} — 2026 AGI 문명 전환기 글로벌 10대 아젠다 & UCKLab Executive Note™ ({date_display})"
    aioseo_title = f"[UCKLab Strategic Review Vol. {vol_num}] 2026 AGI 문명 전환기 글로벌 10대 아젠다 | UCKLab Monograph™"
    aioseo_desc = f"UCKLab Strategic Review: 10대 분야 U-Radar 지수 분석, UCKLab Executive Note™, 및 UCKLab Monograph™ (2,500단어 APA 7th 저널) 수록 ({date_display})."

    endpoint = f"{WP_URL}/wp-json/wp/v2/pages/{front_page_id}"
    payload = {
        "title": title,
        "content": full_content,
        "template": "page-no-title",
        "meta": {
            "_aioseo_title": aioseo_title,
            "_aioseo_description": aioseo_desc
        }
    }

    print(f"📤 [Portal Sync] Pushing to WordPress Front Page ID: {front_page_id} ('{title}')...")
    res = requests.post(endpoint, json=payload, auth=auth, headers={"User-Agent": "UCKLab-Weekly-AutoBot/3.0"}, timeout=120)
    if res.status_code == 200:
        print(f"🎉 [SUCCESS] Front Page {front_page_id} successfully updated with HBR/Bloomberg 2-Column Portal!")
        update_aioseo_post(front_page_id, aioseo_title, aioseo_desc)
    else:
        print(f"❌ [ERROR] Failed to update Front Page ({res.status_code}): {res.text[:200]}")
        return False

    # 5. Purge LiteSpeed & CDN Cache
    print("🧹 [Portal Sync] Purging LiteSpeed Cache...")
    try:
        purge_res = requests.get(f"{WP_URL}/", headers={"X-LiteSpeed-Purge": "*"}, timeout=15)
        print(f"✓ Cache purge requested (HTTP {purge_res.status_code})")
    except Exception as e:
        print(f"Warning cache purge: {e}")

    return True

if __name__ == "__main__":
    run_sync()
