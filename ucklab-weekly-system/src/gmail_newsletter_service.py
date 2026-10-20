"""
gmail_newsletter_service.py - UCKLab Google Gmail / Google Contacts Automated Newsletter Broadcaster
Directly sends high-elegance HTML newsletters from Dr. Lee's Google Account (via Gmail SMTP).
Zero third-party fees ($0), uses Google App Password, and imports subscriber list from CSV/Contacts.
"""

import os
import sys
import time
import smtplib
import csv
import urllib.parse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv

# UTF-8 console setup for Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
SUBSCRIBERS_FILE = os.path.join(DATA_DIR, "subscribers.csv")

load_dotenv(os.path.join(BASE_DIR, ".env"))

GMAIL_USER = os.getenv("GMAIL_USER", "chblee58@gmail.com")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "").replace(" ", "").strip()  # 16-digit Google App Password


def create_sample_subscribers_file():
    """Creates a sample subscribers.csv if not present."""
    if not os.path.exists(SUBSCRIBERS_FILE):
        with open(SUBSCRIBERS_FILE, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["email", "name", "organization", "group"])
            writer.writerow(["chblee58@gmail.com", "이창배 소장", "UCKLab AI융합미래연구소", "VIP"])
            writer.writerow(["gypyung@daum.net", "편집위원", "UCKLab Research", "Editorial"])
        print(f"✓ 샘플 구독자 명단 생성 완료: {SUBSCRIBERS_FILE}")

def load_subscribers():
    """Loads subscriber email list from subscribers.csv."""
    create_sample_subscribers_file()
    subscribers = []
    if os.path.exists(SUBSCRIBERS_FILE):
        with open(SUBSCRIBERS_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                email = row.get("email", "").strip()
                if email and "@" in email:
                    subscribers.append({
                        "email": email,
                        "name": row.get("name", "구독자").strip(),
                        "organization": row.get("organization", "").strip()
                    })
    return subscribers

def build_newsletter_html(recipient_name, report_title, theses, chart_url, category_links=None, recipient_email=""):
    """Builds a responsive, high-elegance dark glassmorphism newsletter email with refined unsubscribe block."""
    theses_items = "".join([f"<li style='margin-bottom:8px; color:#FEF08A;'><b>•</b> {t}</li>" for t in theses])
    
    cat_links_html = ""
    if category_links:
        links_list = []
        for cat_name, url in list(category_links.items())[:6]:
            links_list.append(f"<a href='{url}' style='display:inline-block; margin:4px; padding:6px 14px; background:rgba(255,255,255,0.08); border:1px solid rgba(245,158,11,0.5); border-radius:9999px; color:#FDE047; text-decoration:none; font-size:12px; font-weight:700;'>{cat_name} ➔</a>")
        cat_links_html = "".join(links_list)

    # Refined Unsubscribe mailto URL encoding
    email_for_unsub = recipient_email or "구독자"
    sub_subject = urllib.parse.quote(f"[UCKLab 수신거부] 주간 뉴스레터 구독 해지 ({email_for_unsub})")
    sub_body = urllib.parse.quote(
        f"안녕하세요.\n\n"
        f"UCKLab 주간 전략 브리핑 정기 뉴스레터 수신거부를 정중히 요청합니다.\n\n"
        f"• 수신 거부 이메일: {email_for_unsub}\n"
        f"• 수신자 성함: {recipient_name}\n\n"
        f"위 주소를 발송 명단에서 제외해 주시기 바랍니다.\n"
        f"감사합니다."
    )
    unsub_mailto_url = f"mailto:{GMAIL_USER}?subject={sub_subject}&body={sub_body}"

    return f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>{report_title}</title>
    </head>
    <body style="margin:0; padding:0; background-color:#070B14; font-family:-apple-system, BlinkMacSystemFont, 'Pretendard', 'Noto Sans KR', sans-serif; color:#F8FAFC;">
        <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:640px; margin:30px auto; background:linear-gradient(145deg, #0F172A 0%, #070B14 100%); border-radius:18px; overflow:hidden; border:1px solid rgba(245,158,11,0.4); box-shadow:0 25px 60px rgba(0,0,0,0.8);">
            
            <!-- Top Gold Brand Bar -->
            <tr>
                <td style="padding:28px 32px; background:linear-gradient(135deg, #1E293B 0%, #0F172A 100%); border-bottom:1px solid rgba(255,255,255,0.1); text-align:center;">
                    <div style="font-size:12px; font-weight:800; color:#F59E0B; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:8px;">
                        🏛️ UCKLab AGI Research Institute · Weekly Strategic Review
                    </div>
                    <h1 style="margin:0; font-size:22px; font-weight:900; color:#FFFFFF; line-height:1.4;">
                        {report_title}
                    </h1>
                    <div style="font-size:12.5px; color:#94A3B8; margin-top:6px;">
                        소장 이창배 박사 직필 정론 브리핑 · 월요 C-Suite 아젠다
                    </div>
                </td>
            </tr>

            <!-- Body -->
            <tr>
                <td style="padding:32px 30px;">
                    <p style="font-size:15px; color:#E2E8F0; line-height:1.8; margin:0 0 20px 0;">
                        안녕하세요, <b>{recipient_name}</b> 리더님.<br/>
                        글로벌 지정학적 격변과 초지능(AGI) 가속화 속에서 국가와 기업이 견지해야 할 최고위 전략 프레임워크와 당주 10대 핵심 지표를 전해드립니다.
                    </p>

                    <!-- Theses Gold Box -->
                    <div style="background:rgba(245,158,11,0.12); border-left:4px solid #F59E0B; border-radius:10px; padding:18px 20px; margin-bottom:24px;">
                        <div style="font-size:13.5px; font-weight:800; color:#FBBF24; margin-bottom:10px;">
                            ⚡ 이번 주 핵심 청지기적 전략 명제 (Theses):
                        </div>
                        <ul style="margin:0; padding-left:14px; list-style:none; font-size:13.5px; line-height:1.75;">
                            {theses_items}
                        </ul>
                    </div>

                    <!-- 16:9 Chart Visual -->
                    <div style="text-align:center; margin:24px 0;">
                        <a href="https://ucdigin.net" target="_blank">
                            <img src="{chart_url}" alt="UCKLab AGI Radar Index" style="width:100%; max-width:580px; height:auto; border-radius:12px; border:1px solid rgba(255,255,255,0.15); box-shadow:0 8px 24px rgba(0,0,0,0.6);" />
                        </a>
                        <div style="font-size:11.5px; color:#94A3B8; margin-top:8px;">
                            ▲ 당주 10대 아젠다 U-Radar 인텔리전스 지수 (차트를 클릭하면 실시간 상황실로 이동)
                        </div>
                    </div>

                    <!-- Category Quick Links -->
                    <div style="margin:26px 0; text-align:center;">
                        <div style="font-size:13px; font-weight:800; color:#38BDF8; margin-bottom:10px;">
                            📂 관심 분야별 500단어 단독 심층 저널 바로보기:
                        </div>
                        <div>
                            {cat_links_html}
                        </div>
                    </div>

                    <!-- Big CTA Button -->
                    <div style="text-align:center; margin:32px 0 20px 0;">
                        <a href="https://ucdigin.net" target="_blank" style="display:inline-block; padding:15px 36px; background:linear-gradient(135deg, #F59E0B 0%, #D97706 100%); color:#FFFFFF; text-decoration:none; font-size:15px; font-weight:900; border-radius:9999px; box-shadow:0 10px 25px rgba(217,119,6,0.45);">
                            🌐 UCKLab 웹사이트 전문 및 실시간 OSINT 레이더 열람 ➔
                        </a>
                    </div>
                </td>
            </tr>

            <!-- Footer & Unsubscribe -->
            <tr>
                <td style="padding:26px 30px; background:#0B101E; text-align:center; border-top:1px solid rgba(255,255,255,0.08); font-size:12px; color:#64748b; line-height:1.7;">
                    <div style="margin-bottom:14px;">
                        <span style="font-weight:700; color:#E2E8F0;">발행처:</span> UCKLab AI융합미래연구소 (이창배 박사 연구팀)<br/>
                        <span style="font-weight:700; color:#E2E8F0;">공식 포털:</span> <a href="https://ucdigin.net" style="color:#FBBF24; text-decoration:none; font-weight:700;">ucdigin.net</a> &nbsp;|&nbsp; <a href="https://ucklab.org" style="color:#38BDF8; text-decoration:none; font-weight:700;">ucklab.org</a><br/>
                        <span style="color:#64748B; font-size:11.5px;">글로벌 AGI 문명 전환기 거버넌스 및 성경적 청지기 정론 싱크탱크</span>
                    </div>

                    <!-- Elegant Unsubscribe Notice Card -->
                    <div style="margin-top:18px; padding:16px 20px; background:rgba(255,255,255,0.02); border:1px dashed rgba(255,255,255,0.12); border-radius:12px; text-align:center;">
                        <p style="margin:0 0 10px 0; font-size:11.5px; color:#94A3B8; line-height:1.7;">
                            본 브리핑은 글로벌 미래 전략을 공유하는 UCKLab 핵심 네트워크 리더님께 정중히 전해드리는 전략 리포트입니다.<br/>
                            더 이상의 정기 수신을 희망하지 않으실 경우, 아래 버튼을 통해 언제든 편안하게 구독을 해지하실 수 있습니다.
                        </p>
                        <a href="{unsub_mailto_url}" style="display:inline-block; margin-top:4px; padding:7px 18px; background:rgba(244,63,94,0.08); border:1px solid rgba(244,63,94,0.3); border-radius:9999px; color:#FDA4AF; text-decoration:none; font-size:11.5px; font-weight:700; letter-spacing:0.3px;">
                            ✉️ 수신거부 (Unsubscribe) ➔
                        </a>
                        <div style="font-size:10.5px; color:#475569; margin-top:8px;">
                            (클릭하시면 원클릭 수신거부 메일 창이 자동으로 생성됩니다)
                        </div>
                    </div>
                </td>
            </tr>

        </table>
    </body>
    </html>
    """

def broadcast_weekly_newsletter(report_title, theses, chart_url, category_links=None, dry_run=False):
    """
    Broadcasts the newsletter to all subscribers in subscribers.csv via Gmail SMTP.
    """
    subscribers = load_subscribers()
    print(f"\n=======================================================")
    print(f"📧 [Gmail Newsletter Service] 주간 뉴스레터 대량 발송")
    print(f"=======================================================")
    print(f"  • 발신 계정: {GMAIL_USER}")
    print(f"  • 수신 대상: 총 {len(subscribers)}명 (data/subscribers.csv)")

    if not GMAIL_APP_PASSWORD or dry_run:
        print("\nℹ️ [안내] GMAIL_APP_PASSWORD 미설정 또는 dry_run 모드입니다.")
        print(f"   구글 이메일({GMAIL_USER}) 앱 비밀번호(16자리)를 .env에 설정하시면 즉시 실발송됩니다.")
        for idx, sub in enumerate(subscribers[:3], 1):
            print(f"   [{idx}] 발송 시뮬레이션 성공: {sub['name']} <{sub['email']}>")
        return {"success": True, "simulated": True, "count": len(subscribers)}

    # Real SMTP send via Gmail
    success_count = 0
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        print("  ✓ Gmail SMTP 서버 인증 성공 (smtp.gmail.com:465)")

        for idx, sub in enumerate(subscribers, 1):
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"[UCKLab Strategic Review] {report_title}"
            msg["From"] = f"이창배 소장 (UCKLab) <{GMAIL_USER}>"
            msg["To"] = sub["email"]

            html_body = build_newsletter_html(sub["name"], report_title, theses, chart_url, category_links, recipient_email=sub["email"])
            msg.attach(MIMEText(html_body, "html", "utf-8"))

            try:
                server.sendmail(GMAIL_USER, sub["email"], msg.as_string())
                print(f"  [{idx}/{len(subscribers)}] ✓ 발송 완료: {sub['name']} <{sub['email']}>")
                success_count += 1
                time.sleep(0.2)  # Polite delay
            except smtplib.SMTPResponseException as sre:
                print(f"  ⚠️ SMTP 제한/오류 ({sub['email']}): {sre.smtp_code} {sre.smtp_error}")
                if sre.smtp_code in (421, 452, 550) and "limit" in str(sre.smtp_error).lower():
                    print("  🛑 [안내] Google 계정 일일 발송 한도(Daily sending limit)에 도달하여 발송을 일시 중단합니다.")
                    break
            except Exception as e:
                print(f"  ⚠️ 발송 실패 ({sub['email']}): {e}")

        server.quit()
        print(f"✅ [완료] 총 {success_count}/{len(subscribers)}명에게 주간 뉴스레터 발송 완료!")
        return {"success": True, "count": success_count}
    except Exception as e:
        print(f"❌ [Gmail SMTP] 접속/인증 예외: {e}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    test_theses = [
        "G7-OECD 다자간 인공지능 안전 조약과 소버린 주권 규범 확립",
        "글로벌 첨단 반도체 파운드리 공급망 블록화와 지정학 방어선 재편",
        "기술 초지능 시대, 성경적 청지기 도덕 주권과 인간 존엄성 수호"
    ]
    test_links = {
        "정치·외교": "https://ucdigin.net/category/politics/",
        "경제·공급망": "https://ucdigin.net/category/economy/",
        "금융·핀테크": "https://ucdigin.net/category/finance/",
        "이창배 Note": "https://ucdigin.net/category/lee-note/"
    }
    broadcast_weekly_newsletter(
        report_title="[Vol. 39] 2026 AGI 문명 전환기 글로벌 10대 아젠다 & 이창배 Note",
        theses=test_theses,
        chart_url="https://ucdigin.net/wp-content/uploads/2026/10/stock_WEEKLY-2026-W39_politics_810x480.jpg",
        category_links=test_links,
        dry_run=False
    )

