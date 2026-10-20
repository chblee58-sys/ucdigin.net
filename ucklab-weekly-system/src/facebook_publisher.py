"""
facebook_publisher.py - UCKLab Weekly HBR Facebook Group & Page Auto-Poster
Publishes weekly HBR card-news hook posts to official Facebook Group/Page.
"""

import os
import sys
import re
import json
import requests
from dotenv import load_dotenv

# Windows console UTF-8 setup
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Base setup & environment loading
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

FB_GROUP_ID = os.getenv("FB_GROUP_ID") or os.getenv("FACEBOOK_PAGE_ID") or "2024276951100901"
FB_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN") or os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN") or ""

def publish_weekly_hbr_to_facebook(report_data: dict) -> dict:
    """
    주간 HBR 리포트 발행 시 페이스북 그룹/페이지로 카드뉴스 Hook 포스팅 자율 전송
    """
    url = f"https://graph.facebook.com/v19.0/{FB_GROUP_ID}/feed"

    # 4단계 카드뉴스 및 Hook 텍스트 구성
    message_body = f"""🏛️ [UCKLab Strategic Review Vol. {report_data.get('vol', '39')}]
"{report_data.get('title')}"

📊 당주 U-Radar 지수 및 핵심 데이터:
• 글로벌 10대 핵심 분야 AGI 파급력 및 지정학적 리스크 추적
• {report_data.get('key_takeaway')}

📖 "기술의 효율성이 윤리를 앞지르는 시대, 청지기적 분별력과 미래 전략"
- UCKLab AI융합미래연구소장 이창배 박사 Note -

🎓 2,500단어 APA 7th 학술 저널(UCKLab Monograph™) 및 C-Level 발표 PPT 신청:
👉 https://ucklab.org/api/v1/academic/upgrade
"""

    # If access token is not set, gracefully run in simulation mode
    if not FB_ACCESS_TOKEN:
        print(f"📱 [Facebook Publisher - Simulation Mode] FB_PAGE_ACCESS_TOKEN 미설정 (시뮬레이션 포스팅)")
        print(f"   타깃 그룹 ID: {FB_GROUP_ID}")
        print(f"   제목: {report_data.get('title')}")
        print(f"   링크: {report_data.get('post_url')}")
        print(f"   메시지 미리보기 ({len(message_body)}자):\n{message_body[:220]}...\n")
        return {
            "success": True,
            "simulated": True,
            "post_id": f"sim_fb_{os.urandom(6).hex()}",
            "message": "페이스북 토큰 미설정으로 시뮬레이션 모드 정상 통과"
        }

    payload = {
        'message': message_body,
        'link': report_data.get('post_url'),
        'access_token': FB_ACCESS_TOKEN
    }

    try:
        response = requests.post(url, data=payload, timeout=10)
        if response.status_code == 200:
            post_id = response.json().get('id')
            print(f"✅ 페이스북 그룹 포스팅 성공 (Post ID: {post_id})")
            return {"success": True, "post_id": post_id}
        else:
            print(f"❌ 페이스북 포스팅 실패: {response.text}")
            return {"success": False, "error": response.text}
    except Exception as e:
        print(f"⚠️ 페이스북 API 통신 오류: {str(e)}")
        return {"success": False, "error": str(e)}

def publish_to_facebook(title: str, excerpt: str, url: str, tags: list = None) -> dict:
    """
    Backward-compatible wrapper for publish_weekly_hbr_to_facebook.
    """
    clean_excerpt = excerpt.replace("<p>", "").replace("</p>", "\n").replace("<br/>", "\n").replace("<br>", "\n")
    clean_excerpt = re.sub(r"<[^>]+>", "", clean_excerpt).strip()
    if len(clean_excerpt) > 150:
        clean_excerpt = clean_excerpt[:147] + "..."

    report_data = {
        "vol": "38",
        "title": title,
        "key_takeaway": clean_excerpt or "G7 글로벌 AGI 규범 협약 및 주간 핵심 지표 추적",
        "post_url": url
    }
    return publish_weekly_hbr_to_facebook(report_data)

if __name__ == "__main__":
    print("=== UCKLab Weekly Facebook Publisher Test ===")
    sample_data = {
        "vol": "39",
        "title": "[UCKLab Strategic Review] Vol. 39 — 2026 AGI 문명 전환기 글로벌 10대 아젠다 & UCKLab Executive Note™",
        "key_takeaway": "AGI 문명 전환기 국가불안정지수(CII) 및 컴퓨팅 그리드 부하율 심층 분석",
        "post_url": "https://ucdigin.net/category/news-top10/politics"
    }
    res = publish_weekly_hbr_to_facebook(sample_data)
    print("Result:", res)
