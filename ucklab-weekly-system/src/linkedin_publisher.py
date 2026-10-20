"""
linkedin_publisher.py - UCKLab Weekly HBR LinkedIn Hook & Thought Leadership Publisher
Formats C-Suite executive hook posts for Dr. Lee Chang-bae's LinkedIn profile.
Supports both direct LinkedIn UGC API posting and ready-to-share clipboard/text export.
"""

import os
import sys
import re
import json
try:
    import requests
except ImportError:
    requests = None
try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args, **kwargs):
        pass

# Windows console UTF-8 setup
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
load_dotenv(os.path.join(BASE_DIR, ".env"))

LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN", "")
LINKEDIN_PERSON_URN = os.getenv("LINKEDIN_PERSON_URN", "")  # e.g., urn:li:person:XXXXX or organization URN

def format_linkedin_hook_post(report_data: dict) -> str:
    """
    Creates an authoritative, high-engagement LinkedIn Thought Leadership Post
    with Full Executive Briefing, ucdigin_sns_thumbnail.png preview, and Monograph PDF issuance CTA.
    """
    vol = report_data.get("vol", "41")
    title = report_data.get("title", "2026 AGI 문명 전환기 글로벌 10대 아젠다 & 이창배 Note")
    post_url = report_data.get("post_url", "https://ucdigin.net")
    thumbnail_name = report_data.get("thumbnail", "ucdigin_sns_thumbnail.png")
    thumbnail_url = f"https://ucdigin.net/wp-content/uploads/2026/10/{thumbnail_name}"
    key_takeaway = report_data.get("key_takeaway", "초지능 시대, 지정학적 리스크와 청지기 도덕 주권 확립")
    theses = report_data.get("theses", [])

    theses_text = ""
    if theses:
        theses_text = "\n".join([f"  ▸ {t}" for t in theses[:3]])
    else:
        theses_text = f"  ▸ {key_takeaway}\n  ▸ 소버린 AI 인프라 및 컴퓨팅 그리드 부하율 분석\n  ▸ 기술 패권 경쟁 속 청지기적 책임과 윤리 거버넌스"

    post_content = f"""[Full Executive Briefing | UCKLab Strategic Review Vol. {vol}]
{title}
🖼️ Preview Image: {thumbnail_name} ({thumbnail_url})

기술의 진보 속도가 조직과 국가의 거버넌스를 앞지르고 있습니다. 3D OSINT 멀티 레이더(Argos Atlas · Oroduin AI · Osiris 3D)와 글로벌 싱크탱크 데이터가 가리키는 이번 주 10대 분야 핵심 인텔리전스 브리핑을 전해드립니다.

📌 1. 당주 핵심 전략 명제 (Strategic Theses):
{theses_text}

📌 2. 10대 분야 주간 Executive Note™ 핵심 요약:
  01. [정치·외교] G7 AI 안전 거버넌스 조약 발효와 소버린 알고리즘 주권 확립
  02. [경제·공급망] 5대 거시경제 전환기 자율 지능형 공급망 제어탑 및 조달 다변화
  03. [사회·AI윤리] 지식 노동 자동화 시대 설명 가능한 AI(XAI)와 인간 인지 주권 수호
  04. [문화·예술] 멀티모달 범람 속 C2PA 디지털 워터마크와 인간 창작 오리지널리티 보호
  05. [금융·지정학] 초단타 알고리즘 매매 리스크 통제 및 국경 간 CBDC 유동성 모니터링
  06. [국방·안보] 군집 드론·자율 C4ISR 지휘체계와 양자 내성 암호화(PQC) 방어망
  07. [기독교·청지기] 기술 전능주의를 넘어선 성경적 AI 융합 청지기 신학(Stewardship Theology)
  08. [과학·기술·AGI] 추론형 프론티어 모델과 양자-고전 하이브리드 연산의 학술 검증
  09. [기후·환경] 하이퍼스케일 AI 데이터센터 전력 부하와 SMR 무탄소 기저전력 전환
  10. [스포츠·데이터] 생체역학 텔레메트리 AI 전술 분석과 선수 생체 데이터 주권 보호

✒️ [Lee Chang-bae NOTE | 이창배 박사 시사 정론]
"초지능이 모든 계산을 대신하는 시대일수록, '어디로 가야 하는가'를 묻는 인간 고유의 청지기적 분별력이 문명과 경영의 최종 승부처가 됩니다."
— Dr. Chang-bae Lee (UCKLab AI융합미래연구소장)

🎓 [Call-to-Action: 2,500단어 APA 7th UCKLab Monograph™ PDF 학술 단행본 발급]
본 주간 브리핑의 심층 학술 연구, U-Radar 실증 통계 차트, APA 7th 참고문헌(References)이 완비된 2,500단어 프리미엄 학술 단행본 PDF 및 C-Level 발표용 PPT 덱(3회 수정 거버넌스 포함)을 지금 바로 발급받으실 수 있습니다.
👉 Monograph PDF 즉시 발급 신청: https://ucklab.org/api/v1/academic/upgrade
👉 10대 분야 전문 & 3D OSINT 멀티 레이더 확인: {post_url}

#AGI #AI거버넌스 #청지기경영 #OSINT #ArgosAtlas #Oroduin #Osiris #UCKLab #이창배Note #MonographPDF
"""
    return post_content.strip()

def publish_weekly_hbr_to_linkedin(report_data: dict) -> dict:
    """
    Publishes to LinkedIn API if credentials exist, or writes to data/ for instant 1-click sharing.
    """
    post_text = format_linkedin_hook_post(report_data)
    vol = report_data.get("vol", "39")
    out_file = os.path.join(DATA_DIR, f"linkedin_post_vol{vol}.txt")
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(post_text)

    print(f"\n💼 [LinkedIn Publisher] 링크드인 C-Level 후크 마케팅 포스트 생성 완료")
    print(f"  • 저장 위치: {out_file}")

    if not LINKEDIN_ACCESS_TOKEN or not LINKEDIN_PERSON_URN:
        print("  ℹ️ [시뮬레이션/안내] LINKEDIN_ACCESS_TOKEN 미설정 상태입니다.")
        print(f"  ✓ {out_file} 파일에 완성된 최고급 원문이 저장되었습니다. 링크드인에 바로 복사하여 포스팅하실 수 있습니다.")
        return {
            "success": True,
            "simulated": True,
            "file": out_file,
            "preview": post_text[:200] + "..."
        }

    # If official LinkedIn UGC API is configured
    try:
        url = "https://api.linkedin.com/v2/ugcPosts"
        headers = {
            "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": "application/json"
        }
        payload = {
            "author": LINKEDIN_PERSON_URN,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": post_text},
                    "shareMediaCategory": "ARTICLE",
                    "media": [{
                        "status": "READY",
                        "originalUrl": report_data.get("post_url", "https://ucdigin.net"),
                        "title": {"text": report_data.get("title", "UCKLab Strategic Review")},
                    }]
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
        }
        res = requests.post(url, headers=headers, json=payload, timeout=10)
        if res.status_code in (200, 201):
            post_id = res.json().get("id")
            print(f"  ✅ 링크드인 피드 자동 포스팅 성공! (ID: {post_id})")
            return {"success": True, "post_id": post_id}
        else:
            print(f"  ⚠️ 링크드인 API 응답 오류: {res.text}")
            return {"success": False, "error": res.text}
    except Exception as e:
        print(f"  ⚠️ 링크드인 통신 예외: {e}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    sample_data = {
        "vol": "39",
        "title": "[UCKLab Strategic Review Vol. 39] 2026 AGI 문명 전환기 글로벌 10대 아젠다 & 이창배 Note",
        "key_takeaway": "AGI 문명 전환기 국가불안정지수(CII) 및 소버린 컴퓨팅 그리드 분석",
        "post_url": "https://ucdigin.net",
        "theses": [
            "G7-OECD 다자간 인공지능 안전 조약과 소버린 주권 규범 확립",
            "글로벌 첨단 반도체 파운드리 공급망 블록화와 지정학 방어선 재편",
            "기술 초지능 시대, 성경적 청지기 도덕 주권과 인간 존엄성 수호"
        ]
    }
    publish_weekly_hbr_to_linkedin(sample_data)
