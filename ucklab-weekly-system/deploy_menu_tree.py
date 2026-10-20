import os
import sys
import json
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

WP_URL = os.getenv("WP_URL", "https://ucdigin.net")
WP_USER = os.getenv("WP_USER", "AutoBot_Editor")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD", "5kOS QdBg 6Prd qR4F qixR lg43")
auth = HTTPBasicAuth(WP_USER, WP_APP_PASSWORD)

def get_menu_tree_gutenberg():
    return """<!-- wp:navigation-submenu {"label":"🏛️ 주간 HBR 인텔리전스","url":"https://ucdigin.net/"} -->
<!-- wp:navigation-link {"label":"🌐 전체 인텔리전스 홈 / 최신 브리핑","url":"https://ucdigin.net/","kind":"custom"} /-->
<!-- wp:navigation-link {"label":"🏛️ 정치/외교","url":"https://ucdigin.net/category/intelligence_news_review/politics_diplomacy/","kind":"taxonomy"} /-->
<!-- wp:navigation-link {"label":"📈 경제/공급망","url":"https://ucdigin.net/category/intelligence_news_review/economy_supply_chain/","kind":"taxonomy"} /-->
<!-- wp:navigation-link {"label":"👥 사회/AI윤리","url":"https://ucdigin.net/category/intelligence_news_review/society_ai_ethics/","kind":"taxonomy"} /-->
<!-- wp:navigation-link {"label":"🎨 문화/예술","url":"https://ucdigin.net/category/intelligence_news_review/culture-arts/","kind":"taxonomy"} /-->
<!-- wp:navigation-link {"label":"💳 금융/디지털자산","url":"https://ucdigin.net/category/intelligence_news_review/finance_dgital_assets/","kind":"taxonomy"} /-->
<!-- wp:navigation-link {"label":"🛡️ 국방/안보","url":"https://ucdigin.net/category/intelligence_news_review/defense_security/","kind":"taxonomy"} /-->
<!-- wp:navigation-link {"label":"✝️ 기독교/영성","url":"https://ucdigin.net/category/intelligence_news_review/christianity_spirituality/","kind":"taxonomy"} /-->
<!-- wp:navigation-link {"label":"🔬 과학/기술/AGI","url":"https://ucdigin.net/category/intelligence_news_review/science_technology_agi/","kind":"taxonomy"} /-->
<!-- wp:navigation-link {"label":"🌱 기후/환경/에너지","url":"https://ucdigin.net/category/intelligence_news_review/climate_environment_energy/","kind":"taxonomy"} /-->
<!-- wp:navigation-link {"label":"🏅 스포츠/건강","url":"https://ucdigin.net/category/intelligence_news_review/sports_health/","kind":"taxonomy"} /-->
<!-- /wp:navigation-submenu -->

<!-- wp:navigation-submenu {"label":"🎓 AI 융합 아카데미","url":"https://ucdigin.net/category/ai_convergence_academy/"} -->
<!-- wp:navigation-link {"label":"📘 아카데미 종합 안내","url":"https://ucdigin.net/category/ai_convergence_academy/","kind":"taxonomy"} /-->
<!-- wp:navigation-link {"label":"🧠 Track A: AI 지성 리터러시 & 목회실습","url":"https://ucdigin.net/category/ai_convergence_academy/track_a/","kind":"taxonomy"} /-->
<!-- wp:navigation-link {"label":"🌿 Track B: 뇌과학 디지털 웰니스 & 디톡스","url":"https://ucdigin.net/category/ai_convergence_academy/track_b/","kind":"taxonomy"} /-->
<!-- wp:navigation-link {"label":"🌍 Track C: 소셜 임팩트 & 미래 사역 (ESG)","url":"https://ucdigin.net/category/ai_convergence_academy/track_c/","kind":"taxonomy"} /-->
<!-- wp:navigation-link {"label":"🎓 Oikos MBA & 학위 연계 석·박사 과정","url":"https://ucdigin.net/category/ai_convergence_academy/oikos_mba/","kind":"taxonomy"} /-->
<!-- /wp:navigation-submenu -->

<!-- wp:navigation-link {"label":"✍️ 이창배 Note 정론","url":"https://ucdigin.net/category/lees_note_coloum/","kind":"taxonomy"} /-->
<!-- wp:navigation-link {"label":"🌐 UCKLab 연구소","url":"https://ucklab.org","kind":"custom"} /-->
<!-- wp:navigation-link {"label":"💳 리포트 신청 & 멤버십","url":"https://ucdigin.net/#ucklab-paywall-cta","kind":"custom"} /-->"""

def update_fse_navigations():
    content = get_menu_tree_gutenberg()
    headers = {"Content-Type": "application/json"}
    
    for nav_id in [4, 15517]:
        print(f"Updating FSE Navigation {nav_id}...")
        url = f"{WP_URL}/wp-json/wp/v2/navigation/{nav_id}"
        payload = {
            "content": content,
            "title": "UCKLab Main Global Navigation Tree"
        }
        r = requests.post(url, auth=auth, headers=headers, json=payload, timeout=30)
        print(f"  Result for {nav_id}: Status {r.status_code}")
        if r.status_code == 200:
            print(f"  ✓ Navigation {nav_id} updated successfully!")
        else:
            print(f"  ✗ Failed: {r.text[:200]}")

if __name__ == "__main__":
    update_fse_navigations()
