"""
email_resend.py - UCKLab Weekly HBR 12-Hour Secured Report Email Delivery (Resend API)
Delivers tokenized PDF/PPT download links to readers upon payment or Dr. Lee Admin Bypass.
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Windows console UTF-8 setup
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Base setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
FROM_EMAIL = os.getenv("RESEND_FROM_EMAIL", "UCKLab Research <onboarding@resend.dev>")
SITE_BASE_URL = os.getenv("SITE_BASE_URL", "https://ucklab.org")

def build_delivery_email_html(recipient_name: str, recipient_email: str, download_url: str, report_title: str, expires_in_hours: int = 12, include_ppt: bool = True) -> str:
    """Builds a publication-grade HTML delivery email for UCKLab weekly report subscribers."""
    ppt_section = ""
    if include_ppt:
        ppt_section = f"""
        <div style="background: rgba(16, 185, 129, 0.1); border-left: 4px solid #10b981; border-radius: 8px; padding: 14px 16px; margin-top: 14px;">
            <div style="font-size: 13px; font-weight: 700; color: #6ee7b7; margin-bottom: 4px;">
                📊 16:9 와이드스크린 브리핑용 PPT 덱 포함
            </div>
            <div style="font-size: 12.5px; color: #cbd5e1; line-height: 1.5;">
                • 본 발급 건에는 C-Level 브리핑용 16:9 슬라이드 덱이 포함되어 있습니다.<br/>
                • 슬라이드 수정 및 맞춤 보완은 최대 3회까지 요청 가능합니다 (3회 제한 거버넌스 준수).
            </div>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>{report_title} UCKLab Monograph™ 발급 안내</title>
    </head>
    <body style="margin: 0; padding: 0; background-color: #0f172a; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #f8fafc;">
        <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; margin: 40px auto; background: #1e293b; border-radius: 16px; overflow: hidden; border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: 0 20px 40px rgba(0,0,0,0.5);">
            <!-- Header -->
            <tr>
                <td style="padding: 32px 28px; background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%); text-align: center; border-bottom: 1px solid rgba(255,255,255,0.1);">
                    <div style="font-size: 13px; font-weight: 700; color: #60a5fa; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 8px;">
                        UCKLab AGI Research Institute & Strategic Intelligence Division
                    </div>
                    <h1 style="margin: 0; font-size: 22px; font-weight: 800; color: #ffffff; line-height: 1.35;">
                        {report_title}
                    </h1>
                    <p style="margin: 8px 0 0 0; font-size: 14px; color: #94a3b8;">
                        UCKLab Monograph™ (APA 7th Edition) | 12시간 보안 발급
                    </p>
                </td>
            </tr>

            <!-- Body Content -->
            <tr>
                <td style="padding: 32px 28px;">
                    <p style="font-size: 15px; color: #cbd5e1; line-height: 1.6; margin: 0 0 20px 0;">
                        안녕하세요, <b>{recipient_name}</b>님.<br/>
                        신청하신 <b>UCKLab Monograph™</b> (2,500단어 APA 7th 학술 저널 규격) 및 C-Level 전략 프레젠테이션 덱이 정상 발급되었습니다.
                    </p>

                    <!-- Security Alert Box -->
                    <div style="background: rgba(37, 99, 235, 0.1); border-left: 4px solid #3b82f6; border-radius: 8px; padding: 16px 18px; margin-bottom: 16px;">
                        <div style="font-size: 13px; font-weight: 700; color: #93c5fd; margin-bottom: 4px;">
                            🔒 12시간 보안 다운로드 및 워터마크 안내
                        </div>
                        <div style="font-size: 13px; color: #cbd5e1; line-height: 1.5;">
                            • 본 리포트의 전 페이지에는 신청자 정보(<b>{recipient_email}</b>)가 암호화 워터마크로 인자되어 있습니다.<br/>
                            • 다운로드 링크는 발급 시점으로부터 <b>{expires_in_hours}시간 동안 유효</b>하며, 최대 3회까지 다운로드 가능합니다.
                        </div>
                    </div>

                    {ppt_section}

                    <!-- Download Button -->
                    <div style="text-align: center; margin: 32px 0;">
                        <a href="{download_url}" target="_blank" style="display: inline-block; padding: 16px 36px; background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%); color: #ffffff; text-decoration: none; font-size: 16px; font-weight: 700; border-radius: 12px; box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.5);">
                            📄 UCKLab Monograph™ & PPT 패키지 다운로드 받기 ➔
                        </a>
                    </div>

                    <p style="font-size: 12px; color: #64748b; line-height: 1.5; text-align: center; margin: 0;">
                        버튼이 클릭되지 않을 경우 아래 링크를 브라우저에 직접 붙여넣으세요:<br/>
                        <a href="{download_url}" style="color: #60a5fa; word-break: break-all;">{download_url}</a>
                    </p>
                </td>
            </tr>

            <!-- Footer -->
            <tr>
                <td style="padding: 20px 28px; background: #0b1120; text-align: center; border-top: 1px solid rgba(255,255,255,0.05);">
                    <p style="font-size: 12px; color: #475569; margin: 0 0 6px 0;">
                        발행인: Dr. Chang-bae Lee (이창배 박사) | UCKLab AGI Research Institute & Strategic Intelligence Division
                    </p>
                    <p style="font-size: 11px; color: #334155; margin: 0;">
                        본 메일은 UCKLab Strategic Review™ 자율 인텔리전스 시스템에서 자동으로 발송되었습니다.
                    </p>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

def send_delivery_email(recipient_email: str, recipient_name: str, download_token: str, report_title: str, include_ppt: bool = True) -> dict:
    """
    Sends the 12-hour secured delivery email via Resend API.
    Gracefully falls back to simulation mode if API key is not configured.
    """
    download_url = f"{SITE_BASE_URL}/api/v1/reports/download?token={download_token}"
    html_content = build_delivery_email_html(recipient_name, recipient_email, download_url, report_title, include_ppt=include_ppt)

    if not RESEND_API_KEY:
        print(f"📧 [Resend Email - Simulation] 발송 시뮬레이션 완료:")
        print(f"   수신자: {recipient_name} <{recipient_email}>")
        print(f"   제목: [UCKLab Monograph™] {report_title} 발급 안내")
        print(f"   다운로드 URL: {download_url}")
        return {
            "success": True,
            "simulated": True,
            "message": "RESEND_API_KEY 미설정으로 시뮬레이션 발송 처리되었습니다."
        }

    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "from": FROM_EMAIL,
        "to": [recipient_email],
        "subject": f"[UCKLab Monograph™] {report_title} 발급 안내 (12시간 유효)",
        "html": html_content
    }

    try:
        res = requests.post(url, json=payload, headers=headers, timeout=12)
        if res.status_code in [200, 201]:
            data = res.json()
            email_id = data.get("id")
            print(f"✓ [Resend Email] 메일 발송 성공! (ID: {email_id}) -> {recipient_email}")
            return {"success": True, "simulated": False, "email_id": email_id}
        else:
            print(f"⚠️ [Resend Email] API 오류 ({res.status_code}): {res.text}")
            return {"success": False, "error": res.text}
    except Exception as e:
        print(f"❌ [Resend Email] 예외 발생: {e}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    print("=== UCKLab Weekly Resend Delivery Email Test ===")
    res = send_delivery_email("test@example.com", "테스트 구독자", "sample_token_12345", "[UCKLab Strategic Review Vol. 39] UCKLab Monograph™")
    print("Result:", res)
