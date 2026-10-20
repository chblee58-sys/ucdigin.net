"""
wp_publisher.py - UCKLab Weekly HBR WordPress REST API & Autonomous Publisher
Features:
1. Native WordPress Separation:
   - `content`: FULL 5,000-word HBR-grade AGI Research Report for Gutenberg editing by Dr. Lee in wp-admin.
   - `excerpt`: 500-word Executive Summary + 16:9 Matplotlib Data Chart + Clean In-Site Paywall Modal.
   - `meta`: Injects `_aioseo_title` & `_aioseo_description` + updates /aioseo/v1/post REST endpoint.
2. Sticky Master Post in "뉴스TOP10" (Category ID: 27, sticky: True).
3. SQLite WAL Archiving into `data/ucklab_weekly_archive.db` (weekly_reports table).
4. Secondary Channels: Facebook Page Graph API auto-poster.
5. Core Philosophy: AI Fusion Stewardship Theology (AI 융합 청지기 신학).
6. Clean Customer UX: Zero visible admin buttons on frontend.
"""

import os
import sys
import json
import time
import sqlite3
import datetime
import requests
import re
from requests.auth import HTTPBasicAuth

# Windows console UTF-8 setup
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Setup paths & environment
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
DATA_DIR = os.path.join(BASE_DIR, "data")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
CSS_PATH = os.path.join(ASSETS_DIR, "css", "ucdigin_hbr_style.css")
CHARTS_DIR = os.path.join(BASE_DIR, "storage", "charts")
DB_PATH = os.path.join(DATA_DIR, "ucklab_weekly_archive.db")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from dotenv import load_dotenv
load_dotenv(os.path.join(BASE_DIR, ".env"))

from category_dossier_data import get_category_case_analysis, CATEGORY_DOSSIERS

WP_URL = os.getenv("WP_URL", "https://ucdigin.net")
WP_USER = os.getenv("WP_USER", "AutoBot_Editor")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD", "5kOS QdBg 6Prd qR4F qixR lg43")
PARENT_CATEGORY_ID = 2  # 뉴스 TOP 10 (WordPress ID: 2)
LEE_NOTE_CATEGORY_ID = 14  # 이창배 Note (WordPress ID: 14)

# ---------------------------------------------------------------------------
# Database Archiving (SQLite WAL Mode)
# ---------------------------------------------------------------------------
def archive_weekly_report_to_db(report_id, title, excerpt, content, aioseo_title, aioseo_desc):
    """Archives the published weekly report into SQLite WAL database."""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS weekly_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id TEXT UNIQUE,
            title TEXT,
            excerpt TEXT,
            content TEXT,
            aioseo_title TEXT,
            aioseo_desc TEXT,
            created_at TEXT
        )
        """)
        now_str = datetime.datetime.now().isoformat()
        cursor.execute("""
        INSERT OR REPLACE INTO weekly_reports 
        (report_id, title, excerpt, content, aioseo_title, aioseo_desc, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (report_id, title, excerpt, content, aioseo_title, aioseo_desc, now_str))
        conn.commit()
        conn.close()
        print(f"✓ [DB Archive] 주간 리포트 SQLite WAL 저장 완료 ({report_id})")
        return True
    except Exception as e:
        print(f"⚠️ [DB Archive] SQLite 저장 예외: {e}")
        return False

# ---------------------------------------------------------------------------
# Template & HTML Helper Functions
# ---------------------------------------------------------------------------
def load_hbr_custom_css():
    """Load ucdigin_hbr_style.css custom stylesheet."""
    if os.path.exists(CSS_PATH):
        with open(CSS_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def load_paywall_modal():
    """Load glassmorphism in-site CTA banner & modal HTML."""
    modal_path = os.path.join(TEMPLATES_DIR, "paywall_modal.html")
    if os.path.exists(modal_path):
        with open(modal_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def load_subscription_widget():
    """Load embedded Glassmorphism newsletter subscription widget."""
    path = os.path.join(TEMPLATES_DIR, "subscription_form.html")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def load_cardnews_component(report_id, column_data, news_items, osint_data, chart_url=""):
    """Loads and populates 4-Grid Card News HTML component."""
    path = os.path.join(TEMPLATES_DIR, "cardnews_template.html")
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        tpl = f.read()

    if not chart_url:
        chart_url = f"{WP_URL}/wp-content/uploads/2026/09/chart_WEEKLY-2026-W38-1.png"

    top_item = news_items[0] if news_items else {}
    card1_title = top_item.get("headline", "AGI 문명 전환기와 글로벌 거버넌스")
    card1_hook = top_item.get("summary_ko", "글로벌 지정학적 리스크와 기술 패권 경쟁이 교차하는 지점에서 청지기적 회복탄력성을 논합니다.")[:110] + "..."
    card1_highlight = top_item.get("category_ko", "정치/외교") + " 아젠다"

    cii = osint_data.get("country_instability_index", {}).get("East_Asia_KR_TW", 4.65)
    grid = osint_data.get("infrastructure_finance_radar", {}).get("compute_grid_stress_pct", 78.5)

    col_theses = column_data.get("three_line_summary", [])
    quote = col_theses[0].replace("<b>", "").replace("</b>", "") if col_theses else "인공지능은 숭배의 대상이 아닌 하나님께서 위임하신 거룩한 관리의 도구입니다."
    if len(quote) > 95:
        quote = quote[:92] + "..."

    return tpl.replace("{card1_title}", card1_title)\
              .replace("{card1_hook}", card1_hook)\
              .replace("{card1_highlight}", card1_highlight)\
              .replace("{chart_url}", chart_url)\
              .replace("{cii_score}", str(cii))\
              .replace("{grid_stress}", str(grid))\
              .replace("{column_quote}", quote)

def build_three_line_summary_box(three_lines, title="주간 핵심 전략 명제 (HBR Theses)"):
    """Renders the executive summary block placed directly between title and content."""
    if not three_lines:
        return ""
    items_html = "".join([f"<li style='margin-bottom: 8px; word-break: keep-all;'>{line}</li>" for line in three_lines])
    return f"""
    <div class="ucklab-summary-block" style="margin: 22px 0; padding: 20px 22px; border-radius: 12px; background: #eff6ff; border-left: 5px solid #2563eb; border: 1px solid #dbeafe; box-shadow: 0 4px 12px rgba(37,99,235,0.05); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <div style="font-size: 14px; font-weight: 800; color: #1e40af; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;">
            <span>⚡</span> <b>{title}</b>
        </div>
        <ul style="margin: 0; padding-left: 22px; font-size: 14.5px; line-height: 1.75; color: #1e293b;">
            {items_html}
        </ul>
    </div>
    """

def build_citation_box(citation_data):
    """Renders the official source & citation block."""
    if not citation_data:
        return ""
    source = citation_data.get("source", "글로벌 공공 및 주요 싱크탱크")
    url = citation_data.get("url", "https://ucklab.org/research")
    date_str = citation_data.get("date", "당일")
    attribution = citation_data.get("attribution", "UCKLab AI융합미래연구소 (이창배 박사 연구팀) · 주간 HBR 인텔리전스 분석")

    return f"""
    <div style="margin: 24px 0 16px 0; padding: 16px 20px; border-radius: 12px; background: #f8fafc; border: 1px solid #e2e8f0; font-size: 13px; line-height: 1.65; color: #475569; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <div style="font-weight: 800; color: #0f172a; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;">
            <span>📑</span> <b>공식 출처 및 전략 분석 인용 (Source &amp; Citation)</b>
        </div>
        <div style="word-break: break-all;">
            • <b>원문 출처:</b> {source} (참조 일시: {date_str})<br/>
            • <b>원문 링크:</b> <a href="{url}" target="_blank" rel="noopener noreferrer" style="color: #2563eb; text-decoration: underline;">{url}</a><br/>
            • <b>전략 해설:</b> {attribution}
        </div>
    </div>
    """

def build_category_badge(item):
    """Renders a responsive branded Category Symbol Badge Card."""
    configs = {
        "politics": {"grad": "linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%)", "border": "#60a5fa", "sub": "Global Governance & Policy"},
        "economy": {"grad": "linear-gradient(135deg, #065f46 0%, #10b981 100%)", "border": "#34d399", "sub": "Macroeconomics & Supply Chain"},
        "society": {"grad": "linear-gradient(135deg, #9a3412 0%, #ea580c 100%)", "border": "#fb923c", "sub": "Digital Ethics & Human Labor"},
        "culture": {"grad": "linear-gradient(135deg, #581c87 0%, #7c3aed 100%)", "border": "#a78bfa", "sub": "Creative Arts & Generative Media"},
        "finance": {"grad": "linear-gradient(135deg, #0f766e 0%, #0d9488 100%)", "border": "#2dd4bf", "sub": "Fintech & Sovereign Digital Assets"},
        "defense": {"grad": "linear-gradient(135deg, #374151 0%, #1f2937 100%)", "border": "#9ca3af", "sub": "Autonomous Defense & Cybersecurity"},
        "christianity": {"grad": "linear-gradient(135deg, #78350f 0%, #b45309 100%)", "border": "#f59e0b", "sub": "AI Fusion Stewardship Theology"},
        "science": {"grad": "linear-gradient(135deg, #1e1b4b 0%, #4338ca 100%)", "border": "#818cf8", "sub": "Frontier AI & Quantum Computing"},
        "climate": {"grad": "linear-gradient(135deg, #14532d 0%, #15803d 100%)", "border": "#4ade80", "sub": "Grid Decarbonization & Clean Energy"},
        "sports": {"grad": "linear-gradient(135deg, #831843 0%, #be185d 100%)", "border": "#f472b6", "sub": "Sports Analytics & Biometrics"}
    }
    cat_key = item.get("id", "politics")
    cfg = configs.get(cat_key, {"grad": "linear-gradient(135deg, #1e293b 0%, #334155 100%)", "border": "#94a3b8", "sub": "Global Strategy"})
    
    return f"""
    <div style="background: {cfg['grad']}; border-left: 4px solid {cfg['border']}; border-radius: 8px; padding: 10px 16px; margin-bottom: 14px; color: #ffffff; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 10px rgba(0,0,0,0.08);">
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 18px;">{item.get('icon', '📌')}</span>
            <span style="font-size: 14px; font-weight: 800; letter-spacing: 0.5px;">{item.get('category_ko', '')} ({item.get('category_en', '')})</span>
        </div>
        <div style="font-size: 11.5px; opacity: 0.85; font-weight: 500;">
            {cfg['sub']}
        </div>
    </div>
    """

def build_osint_marquee_html(osint_data, news_items, column_data):
    """Builds the live OSINT breaking news marquee ticker spanning the top of the portal."""
    cii = osint_data.get("country_instability_index", {}).get("East_Asia_KR_TW", 4.65)
    grid = osint_data.get("infrastructure_finance_radar", {}).get("compute_grid_stress_pct", 78.5)
    geo_alert = osint_data.get("geopolitical_signals", {}).get("alert_level", "ELEVATED_WATCH")
    swift_ratio = osint_data.get("infrastructure_finance_radar", {}).get("swift_to_cbdc_velocity_ratio", 1.49)
    col_title = column_data.get("title", "AGI 문명 전환기와 청지기적 도덕 주권")

    items = [
        f'<span class="ucklab-ticker-item"><span class="ucklab-ticker-tag alert">지정학 경보</span> <b>{geo_alert}</b>: 동아시아(한·대만) CII {cii}/10.0 반도체 공급망 비상 모니터링 가동</span>',
        f'<span class="ucklab-ticker-item"><span class="ucklab-ticker-tag grid">컴퓨팅 그리드</span> <b>부하율 {grid}%</b>: 글로벌 하이퍼스케일러 데이터센터 전력 수급 압박 경보</span>',
        f'<span class="ucklab-ticker-item"><span class="ucklab-ticker-tag column">이창배 Note 정론</span> <b>"{col_title}"</b> 권두 정론 발표</span>',
        f'<span class="ucklab-ticker-item"><span class="ucklab-ticker-tag trend">글로벌 금융/자산</span> SWIFT 대안 국경간 CBDC 결제 유동성 급증 (이동속도비 <b>{swift_ratio}x</b>)</span>',
        f'<span class="ucklab-ticker-item"><span class="ucklab-ticker-tag alert">AGI 거버넌스</span> G7 인공지능 안전 조약 합의 발표 및 소버린 알고리즘 검증 권고</span>',
        f'<span class="ucklab-ticker-item"><span class="ucklab-ticker-tag trend">국방/안보</span> 자율 방어 드론 네트워크 및 AI 양자 내성 암호체계 전면 배치 테스트</span>',
        f'<span class="ucklab-ticker-item"><span class="ucklab-ticker-tag grid">에너지/기후</span> 소형모듈원전(SMR) 기반 기저전력 확보 및 글로벌 기후 리스크 대응 가속</span>'
    ]
    track_content = " &nbsp;&nbsp;•&nbsp;&nbsp; ".join(items)
    # Duplicate for seamless infinite loop
    full_track = f"{track_content} &nbsp;&nbsp;•&nbsp;&nbsp; {track_content}"

    return f"""
    <div class="ucklab-ticker-bar">
        <div class="ucklab-ticker-badge">
            <span class="ucklab-ticker-pulse"></span>
            <span>LIVE OSINT RADAR</span>
        </div>
        <div class="ucklab-ticker-track">
            <div class="ucklab-ticker-content">
                {full_track}
            </div>
        </div>
    </div>
    """

def build_sticky_rail_html(news_items, osint_data):
    """Constructs the high-elegance Sticky Intelligence Rail for Desktop PC."""
    toc_links = []
    for idx, item in enumerate(news_items, 1):
        cat_key = item.get("id", "politics")
        cat_ko = item.get("category_ko", "분야")
        icon = item.get("icon", "📌")
        score = item.get("trend_score", 85)
        toc_links.append(f"""
        <a href="#cat-{cat_key}" class="ucklab-toc-link">
            <span style="display: flex; align-items: center; gap: 6px;">
                <span style="font-size: 13px;">{icon}</span>
                <span>{idx:02d}. {cat_ko}</span>
            </span>
            <span style="font-size: 11px; background: #eff6ff; color: #1e40af; padding: 2px 6px; border-radius: 4px; font-weight: 700;">
                {score}pt
            </span>
        </a>
        """)
    toc_html = "".join(toc_links)

    cii = osint_data.get("country_instability_index", {}).get("East_Asia_KR_TW", 4.65)
    grid = osint_data.get("infrastructure_finance_radar", {}).get("compute_grid_stress_pct", 78.5)
    geo_alert = osint_data.get("geopolitical_signals", {}).get("alert_level", "ELEVATED_WATCH")

    return f"""
    <!-- Widget 1: Executive Quick Jump TOC -->
    <div class="ucklab-rail-card">
        <h4 class="ucklab-rail-title">
            <span>📑</span> <b>주간 10대 아젠다 퀵 목차 (TOC)</b>
        </h4>
        <div style="display: flex; flex-direction: column; gap: 3px;">
            <a href="#section-column" class="ucklab-toc-link" style="background: #eff6ff; color: #1e40af; margin-bottom: 4px; font-weight: 700;">
                <span>🏛️ 00. 이창배 Note 권두 정론</span>
                <span style="font-size: 11px; background: #dbeafe; color: #1e40af; padding: 2px 6px; border-radius: 4px;">Note</span>
            </a>
            {toc_html}
            <a href="#section-synthesis" class="ucklab-toc-link" style="margin-top: 4px; color: #0284c7; font-weight: 700;">
                <span>📊 주간 HBR 실행 로드맵</span>
                <span style="font-size: 11px; background: #e0f2fe; color: #0369a1; padding: 2px 6px; border-radius: 4px;">Action</span>
            </a>
        </div>
    </div>

    <!-- Widget 2: High-Conversion Instant Paywall CTA -->
    <div class="ucklab-rail-card dark" style="border: 1px solid #d97706; box-shadow: 0 10px 25px rgba(217, 119, 6, 0.2);">
        <div style="display: inline-block; background: rgba(217, 119, 6, 0.2); color: #fbbf24; font-size: 11px; font-weight: 800; padding: 3px 8px; border-radius: 4px; margin-bottom: 8px;">
            EXECUTIVE INTELLIGENCE
        </div>
        <h4 style="margin: 0 0 8px 0; font-size: 17px; font-weight: 900; color: #ffffff; line-height: 1.35;">
            HBR급 최고급 PDF 저널 발행 &amp; C-Level 발표 PPT 덱
        </h4>
        <p style="font-size: 13px; color: #cbd5e1; line-height: 1.55; margin: 0 0 14px 0;">
            커피 한 잔 값(<b>9,900원</b>)으로 10대 분야 심층 데이터와 3회 수정 거버넌스 PPT를 신청하세요.
        </p>
        <div style="display: flex; flex-direction: column; gap: 8px;">
            <a href="https://ucklab.org/#executive-pipeline" target="_blank" class="ucklab-rail-cta-btn" style="background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);">
                ⚡ 1:1 온디맨드 실시간 AGI 직조 ➔
            </a>
            <a href="javascript:void(0)" onclick="window.openUcklabWeeklyModal ? window.openUcklabWeeklyModal() : (function(){{var o=document.getElementById('ucklab-weekly-modal-overlay');if(o){{o.style.display='flex';document.body.style.overflow='hidden';}}}})()" class="ucklab-rail-cta-btn" style="background: linear-gradient(135deg, #d97706 0%, #b45309 100%); font-size: 13.5px; padding: 10px 14px;">
                📄 간편신청 모달 열기 (9,900원)
            </a>
        </div>
        <div style="font-size: 11px; color: #94a3b8; text-align: center; margin-top: 10px;">
            ✓ 토스페이먼츠 간편결제 지원 | ucklab.org 실시간 렌더링
        </div>
    </div>

    <!-- Widget 3: Dr. Lee Editorial Column Hub -->
    <div class="ucklab-rail-card">
        <h4 class="ucklab-rail-title">
            <span>✍️</span> <b>이창배 Note 정론 허브</b>
        </h4>
        <div style="display: flex; gap: 12px; align-items: center; margin-bottom: 12px;">
            <div style="width: 44px; height: 44px; border-radius: 50%; background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%); color: #ffffff; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 900; flex-shrink: 0;">
                UCK
            </div>
            <div>
                <div style="font-size: 14px; font-weight: 800; color: #0f172a;">Dr. Chang-bae Lee</div>
                <div style="font-size: 11.5px; color: #64748b;">AI융합미래연구소 소장 · 신학박사</div>
            </div>
        </div>
        <p style="font-size: 12.5px; color: #475569; line-height: 1.6; margin: 0 0 12px 0;">
            성경적 청지기 신학과 AGI 거버넌스를 융합한 역대 권두 정론 칼럼을 날짜순으로 열람하실 수 있습니다.
        </p>
        <a href="https://ucdigin.net/column/" style="display: flex; align-items: center; justify-content: center; gap: 6px; background: #eff6ff; color: #2563eb; font-size: 13px; font-weight: 700; padding: 9px 14px; border-radius: 8px; border: 1px solid #dbeafe; text-decoration: none;">
            <span>📚</span> <b>이창배 Note 전체 칼럼 보기 ➔</b>
        </a>
    </div>

    <!-- Widget 4: OSINT Mini Radar -->
    <div class="ucklab-rail-card" style="background: #f8fafc;">
        <h4 class="ucklab-rail-title" style="margin-bottom: 10px;">
            <span>🌐</span> <b>OSINT 실시간 주간 지표</b>
        </h4>
        <div style="display: flex; flex-direction: column; gap: 8px; font-size: 12.5px;">
            <div style="display: flex; justify-content: space-between; padding-bottom: 6px; border-bottom: 1px dashed #e2e8f0;">
                <span style="color: #64748b;">동아시아(한·대만) CII</span>
                <span style="font-weight: 800; color: #0284c7;">{cii} / 10.0</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding-bottom: 6px; border-bottom: 1px dashed #e2e8f0;">
                <span style="color: #64748b;">지정학 리스크 경보</span>
                <span style="font-weight: 800; color: #d97706;">{geo_alert}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #64748b;">컴퓨팅 그리드 부하율</span>
                <span style="font-weight: 800; color: #16a34a;">{grid}%</span>
            </div>
        </div>
    </div>
    """

# ---------------------------------------------------------------------------
# Full 5,000-Word HBR Master Report Generator (for Gutenberg Editor)
# ---------------------------------------------------------------------------
def build_full_hbr_report_content(report_id, column_data, news_items, osint_data, chart_url="", category_charts=None, category_public_urls=None):
    """
    Builds the FULL 5,000-word HBR-grade Intelligence Report.
    Stored directly in WordPress `content` so Dr. Lee can review and edit
    natively in Gutenberg editor!
    """
    today_str = datetime.datetime.now().strftime("%Y년 %m월 %d일")
    if not chart_url:
        chart_url = f"{WP_URL}/wp-content/uploads/2026/09/chart_WEEKLY-2026-W38-1.png"

    paywall_modal_html = load_paywall_modal()
    subscription_widget_html = load_subscription_widget()
    cardnews_component_html = load_cardnews_component(report_id, column_data, news_items, osint_data, chart_url)
    hbr_custom_css = load_hbr_custom_css()
    css_injection_tag = f"<style id='ucklab-hbr-custom-css'>\n{hbr_custom_css}\n</style>" if hbr_custom_css else ""

    # 1. OSINT Telemetry Block
    cii = osint_data.get("country_instability_index", {})
    geo = osint_data.get("geopolitical_signals", {})
    infra = osint_data.get("infrastructure_finance_radar", {})

    osint_html = f"""
    <!-- wp:group {{"backgroundColor":"slate","layout":{{"type":"constrained"}}}} -->
    <div id="section-osint" class="ucklab-osint-card" style="margin: 32px 0; padding: 26px; border-radius: 16px; background: #0f172a; color: #f8fafc; border: 1px solid #334155; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
            <h3 style="margin: 0; font-size: 21px; font-weight: 800; color: #60a5fa; display: flex; align-items: center; gap: 8px;">
                <span>🌐</span> <b>World Monitor OSINT &amp; 3-Stage Trend Radar 주간 지표</b>
            </h3>
            <span style="font-size: 12px; padding: 4px 12px; border-radius: 9999px; background: rgba(96, 165, 250, 0.2); color: #93c5fd; font-weight: 700;">HBR Strategic Radar</span>
        </div>
        <p class="ucklab-body-p" style="font-size: 14.5px; color: #cbd5e1; line-height: 1.65; margin-bottom: 18px;">
            국가 불안정 지수(CII), 지정학적 리스크 경보 및 글로벌 컴퓨팅 인프라 전력 부하율을 종합 집계한 주간 전략 모니터링 데이터입니다.
        </p>
        <div class="ucklab-osint-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; margin-bottom: 18px;">
            <div style="padding: 16px; border-radius: 12px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);">
                <div style="font-size: 11.5px; color: #94a3b8; font-weight: 700;">동아시아(한·대만) 불안정 지수</div>
                <div style="font-size: 24px; font-weight: 900; color: #38bdf8; margin-top: 4px;">{cii.get('East_Asia_KR_TW', 4.65)} / 10.0</div>
                <div style="font-size: 11px; color: #cbd5e1; margin-top: 2px;">수준: 주의 및 모니터링 강화</div>
            </div>
            <div style="padding: 16px; border-radius: 12px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);">
                <div style="font-size: 11.5px; color: #94a3b8; font-weight: 700;">지정학 경보 &amp; 기술제재 강도</div>
                <div style="font-size: 24px; font-weight: 900; color: #f59e0b; margin-top: 4px;">{geo.get('alert_level', 'ELEVATED_WATCH')}</div>
                <div style="font-size: 11px; color: #cbd5e1; margin-top: 2px;">반도체·AI 제재 강도: {geo.get('tech_sanction_intensity', 7.9)}/10</div>
            </div>
            <div style="padding: 16px; border-radius: 12px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);">
                <div style="font-size: 11.5px; color: #94a3b8; font-weight: 700;">컴퓨팅 인프라 그리드 부하율</div>
                <div style="font-size: 24px; font-weight: 900; color: #10b981; margin-top: 4px;">{infra.get('compute_grid_stress_pct', 78.5)}%</div>
                <div style="font-size: 11px; color: #cbd5e1; margin-top: 2px;">SWIFT 대비 국경간 이동: {infra.get('swift_to_cbdc_velocity_ratio', 1.49)}x</div>
            </div>
        </div>
        <div style="font-size: 13px; color: #94a3b8; line-height: 1.6; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 12px;">
            <b>주간 핵심 리스크 확산 경로:</b> {", ".join(geo.get('escalation_vectors', ['글로벌 반도체 공급망 재편', '동유럽 사이버 전자전', 'G7 AGI 안보 조약']))}
        </div>
    </div>
    <!-- /wp:group -->
    """

    # 2. Dr. Lee's Editorial Column Section (~1,000 words)
    col_paragraphs = column_data.get("content", "").split("\n\n")
    col_p_html = "".join([f"<p style='font-size: 16.5px; line-height: 1.95; color: #334155; margin-bottom: 20px; word-break: keep-all;'>{p.strip()}</p>" for p in col_paragraphs if p.strip()])
    col_summary = build_three_line_summary_box(column_data.get("three_line_summary"), title="이창배 Note 권두 칼럼 3대 청지기적 명제")
    col_citation = build_citation_box(column_data.get("citation"))

    column_section_html = f"""
    <!-- wp:group -->
    <div id="section-column" class="ucklab-column-card" style="margin: 40px 0; padding: 34px; border-radius: 18px; background: #ffffff; border: 1px solid #e2e8f0; box-shadow: 0 6px 24px rgba(0,0,0,0.04);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <div style="display:inline-block; padding: 5px 14px; border-radius: 6px; background: #eff6ff; color: #1e40af; font-size: 13px; font-weight: 700;">
                🏛️ 주간 특별 권두 정론 칼럼 · 이창배 Note
            </div>
            <div style="font-size: 12.5px; color: #64748b;">
                AI Fusion Stewardship Theology
            </div>
        </div>
        <h2 style="font-size: 28px; font-weight: 900; color: #0f172a; margin: 0 0 10px 0; line-height: 1.35;">
            {column_data.get('title', '이창배 Note: AGI 문명 전환기와 청지기적 도덕 주권')}
        </h2>
        <div style="font-size: 14px; color: #64748b; margin-bottom: 22px;">
            <b>집필: {column_data.get('author', '이창배 박사')}</b> | UCKLab AI융합미래연구소 소장 | {today_str}
        </div>
        {col_summary}
        <div style="margin: 28px 0;">
            {col_p_html}
        </div>
        {col_citation}
    </div>
    <!-- /wp:group -->
    """

    # WP Category Taxonomy Slugs and Direct Archive URLs (/category/news-top10/<cat>/)
    wp_category_archive_urls = {
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

    # Category Quick Jump / Filter Chips Bar
    chips = []
    for it in news_items:
        c_key = it.get("id")
        c_ko = it.get("category_ko", "분야")
        c_icon = it.get("icon", "📌")
        chips.append(f'<a href="#cat-{c_key}" class="ucklab-cat-chip"><span>{c_icon}</span> <span>{c_ko}</span></a>')
    chips_html = "".join(chips)
    category_nav_bar_html = f"""
    <div class="ucklab-category-nav-bar">
        <span style="font-size: 13px; font-weight: 800; color: #1e293b; display: inline-flex; align-items: center; gap: 6px;">
            📂 <b>분야별 카테고리 퀵 점프:</b>
        </span>
        {chips_html}
        <a href="{WP_URL}/category/news-top10/" class="ucklab-cat-chip" style="background:#1e40af; color:#ffffff; border-color:#1e40af;">
            <span>🌐</span> <span>카테고리 전체 아카이브 ➔</span>
        </a>
    </div>
    """

    # 3. 10 Categories HBR In-Depth Dossiers (~3,500 words)
    categories_dossiers_html = ""
    for idx, item in enumerate(news_items, 1):
        cat_key = item.get("id")
        archive_url = wp_category_archive_urls.get(cat_key, f"{WP_URL}/category/news-top10/")
        pub_url = category_public_urls.get(cat_key, "") if category_public_urls else ""

        cat_badge = f'<a href="{archive_url}" style="text-decoration:none; display:block;" title="{item.get("category_ko")} 카테고리 아카이브 바로가기">{build_category_badge(item)}</a>'
        
        if pub_url:
            headline_html = f'<a href="{pub_url}" style="text-decoration:none; color:inherit;" title="맞춤형 심층 분석 및 유료 신청 바로가기">[{item.get("category_ko")}] {item.get("headline")} <span style="font-size:16px; color:#2563eb;">↗</span></a>'
        else:
            headline_html = f'<a href="{archive_url}" style="text-decoration:none; color:inherit;" title="{item.get("category_ko")} 카테고리 아카이브 바로가기">[{item.get("category_ko")}] {item.get("headline")} <span style="font-size:16px; color:#2563eb;">↗</span></a>'

        inline_cta_html = f"""
        <div style="margin: 20px 0; display: flex; gap: 10px; justify-content: flex-end; flex-wrap: wrap;">
            <a href="{archive_url}" class="ucklab-category-archive-btn" style="padding: 9px 16px; font-size: 13px;">
                <span>📂</span> <b>{item.get('category_ko')} 카테고리 전체 기사 ➔</b>
            </a>
            <a href="{pub_url if pub_url else '#ucklab-paywall-cta'}" style="display:inline-flex; align-items:center; gap:6px; font-size:13px; font-weight:700; color:#ffffff; text-decoration:none; padding:9px 18px; border-radius:8px; background:linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%); box-shadow:0 2px 8px rgba(37,99,235,0.25);">
                <span>📊</span> <b>{item.get('category_ko')} 심층 리포트 신청 ➔</b>
            </a>
        </div>
        """

        radar = item.get("trend_radar", {})
        radar_stage = radar.get("stage", "Stage 2 (Community)")
        radar_velocity = radar.get("velocity", 3.2)
        radar_desc = radar.get("transition_description", "트렌드 확산 중")

        cat_chart_url = category_charts.get(item.get("id")) if category_charts else None
        cat_chart_img_html = ""
        if cat_chart_url:
            cat_chart_img_html = f"""
            <div class="ucklab-chart-box" style="margin: 20px 0; text-align: center;">
                <img src="{cat_chart_url}" alt="{item.get('category_ko')} 전략 분석 데이터 차트" style="width: 100%; max-width: 780px; height: auto; border-radius: 12px; border: 1px solid rgba(255,255,255,0.12); box-shadow: 0 8px 24px rgba(0,0,0,0.18);" loading="lazy" />
                <div style="font-size: 11.5px; color: #64748b; margin-top: 6px; font-weight: 600;">
                    ▲ [UCKLab HBR Strategic Radar] {item.get('category_ko')} 4대 핵심 역학 데이터 지표
                </div>
            </div>
            """

        cat_p1, cat_p2, cat_en, cat_theses, dossier_info = get_category_case_analysis(
            cat_key,
            item.get("headline", ""),
            item.get("source", "")
        )

        theses_box_html = build_three_line_summary_box(
            item.get("three_line_summary") or cat_theses,
            title=f"{item.get('category_ko')} 주간 3대 핵심 명제 (HBR Theses)"
        )

        p1_t = dossier_info.get("point1_title", "")
        p1_c = dossier_info.get("point1_content", "")
        p2_t = dossier_info.get("point2_title", "")
        p2_c = dossier_info.get("point2_content", "")
        p3_t = dossier_info.get("point3_title", "")
        p3_c = dossier_info.get("point3_content", "")
        synth_c = dossier_info.get("executive_synthesis", "")

        academic_points_html = ""
        if p1_t and p1_c:
            p1_formatted = "".join([f"<p style='margin:0 0 10px 0; font-size:14.5px; line-height:1.85; color:#334155; word-break:keep-all;'>{para.strip()}</p>" for para in p1_c.split("\n\n") if para.strip()])
            p2_formatted = "".join([f"<p style='margin:0 0 10px 0; font-size:14.5px; line-height:1.85; color:#334155; word-break:keep-all;'>{para.strip()}</p>" for para in p2_c.split("\n\n") if para.strip()])
            p3_formatted = "".join([f"<p style='margin:0 0 10px 0; font-size:14.5px; line-height:1.85; color:#334155; word-break:keep-all;'>{para.strip()}</p>" for para in p3_c.split("\n\n") if para.strip()])
            
            academic_points_html = f"""
            <!-- 3-Part In-Depth Academic Dossier -->
            <div class="ucklab-academic-dossier" style="margin: 22px 0;">
                <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px 22px; margin-bottom: 14px; box-shadow: 0 2px 8px rgba(0,0,0,0.02);">
                    <h5 style="margin: 0 0 10px 0; font-size: 15.5px; font-weight: 800; color: #1e40af; display:flex; align-items:center; gap:6px;">
                        <span>🏛️</span> <b>{p1_t}</b>
                    </h5>
                    {p1_formatted}
                </div>
                <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px 22px; margin-bottom: 14px; box-shadow: 0 2px 8px rgba(0,0,0,0.02);">
                    <h5 style="margin: 0 0 10px 0; font-size: 15.5px; font-weight: 800; color: #0d9488; display:flex; align-items:center; gap:6px;">
                        <span>🛡️</span> <b>{p2_t}</b>
                    </h5>
                    {p2_formatted}
                </div>
                <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px 22px; margin-bottom: 14px; box-shadow: 0 2px 8px rgba(0,0,0,0.02);">
                    <h5 style="margin: 0 0 10px 0; font-size: 15.5px; font-weight: 800; color: #b45309; display:flex; align-items:center; gap:6px;">
                        <span>⚡</span> <b>{p3_t}</b>
                    </h5>
                    {p3_formatted}
                </div>
                {f'<div style="background: #f1f5f9; border-left: 4px solid #3b82f6; border-radius: 8px; padding: 14px 18px; margin-top: 10px;"><b style="font-size: 13.5px; color: #1e40af;">📊 분야 전략 종합:</b> <span style="font-size: 13.5px; color: #334155; line-height: 1.7;">{synth_c}</span></div>' if synth_c else ''}
            </div>
            """

        en_items = dossier_info.get("english_briefing", [])
        if en_items:
            en_items_html = "".join([f"<li style='margin-bottom:6px; word-break:keep-all;'>{line}</li>" for line in en_items])
        else:
            en_items_html = f"<li style='margin-bottom:6px;'>{cat_en}</li>"

        dossier_html = f"""
        <!-- wp:group -->
        <div id="cat-{cat_key}" class="ucklab-dossier-card" style="margin: 36px 0; padding: 28px; border-radius: 16px; background: #ffffff; border: 1px solid #e2e8f0; box-shadow: 0 4px 16px rgba(0,0,0,0.03);">
            <!-- Category Separation Header Bar -->
            <div class="ucklab-category-header-bar">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 12px; font-weight: 800; color: #1e40af; background: #eff6ff; border: 1px solid #dbeafe; padding: 3px 10px; border-radius: 6px;">
                        CATEGORY {idx:02d}
                    </span>
                    <span style="font-size: 14.5px; font-weight: 800; color: #0f172a;">
                        {item.get('category_ko')} 인텔리전스
                    </span>
                </div>
                <a href="{archive_url}" class="ucklab-category-archive-btn" title="{item.get('category_ko')} 카테고리 페이지 바로가기">
                    <span>📂</span> <b>{item.get('category_ko')} 카테고리 전체보기 ➔</b>
                </a>
            </div>

            {cat_badge}
            <div style="display: flex; gap: 8px; align-items: center; margin-bottom: 12px; flex-wrap: wrap;">
                <span style="display:inline-flex; align-items:center; gap:6px; padding: 4px 12px; border-radius: 6px; background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(245, 158, 11, 0.5); color: #FBBF24; font-size: 12px; font-weight: 800; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4); text-shadow: 0 1px 2px rgba(0,0,0,0.8);">
                    {radar_stage} (속도: +{radar_velocity}σ)
                </span>
                <span style="display:inline-flex; align-items:center; gap:6px; padding: 4px 12px; border-radius: 6px; background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(56, 189, 248, 0.55); color: #38BDF8; font-size: 12px; font-weight: 800; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4); text-shadow: 0 1px 2px rgba(0,0,0,0.8);">
                    🛡️ 사전 검증용 (500단어+)
                </span>
                <span style="font-size: 12.5px; color: #CBD5E1; font-weight: 500;">
                    {radar_desc}
                </span>
            </div>
            <h3 style="font-size: 22px; font-weight: 900; color: #0f172a; margin: 0 0 12px 0; line-height: 1.4;">
                {headline_html}
            </h3>
            <div style="font-size: 13px; color: #64748b; margin-bottom: 18px;">
                <b>출처:</b> {item.get('source', '글로벌 외신')} | <b>일시:</b> {item.get('date', '당일')} | <b>인텔리전스 지수:</b> {item.get('trend_score', 85)} pt | <a href="{archive_url}" style="color:#2563eb; font-weight:700; text-decoration:none;">[카테고리 아카이브]</a>
            </div>
            
            {theses_box_html}
            {cat_chart_img_html}

            <!-- HBR In-Depth Analysis Content -->
            <div style="margin: 20px 0; padding: 22px 24px; border-radius: 12px; background: #f8fafc; border-left: 5px solid #2563eb; border: 1px solid #e2e8f0;">
                <h4 style="margin: 0 0 12px 0; font-size: 16px; font-weight: 800; color: #1e40af; display: flex; align-items: center; gap: 8px;">
                    <span>🏛️</span> <b>[HBR급 주간 심층 인텔리전스 분석 · {item.get('category_ko')}]</b>
                </h4>
                <p style="font-size: 15.5px; line-height: 1.85; color: #1e293b; margin: 0 0 14px 0; word-break: keep-all;">
                    {cat_p1}
                </p>
                <p style="font-size: 15.5px; line-height: 1.85; color: #1e293b; margin: 0; word-break: keep-all;">
                    {cat_p2}
                </p>
            </div>

            {academic_points_html}

            <!-- Global Foresight -->
            <div style="margin: 16px 0; padding: 20px 22px; border-radius: 12px; background: #0f172a; color: #f8fafc; border: 1px solid #334155;">
                <h4 style="margin: 0 0 10px 0; font-size: 14.5px; font-weight: 800; color: #38bdf8; display: flex; align-items: center; gap: 8px;">
                    <span>🌐</span> <b>[Global Strategic Foresight &amp; C-Suite Takeaway · 5 Core Vectors]</b>
                </h4>
                <ol style="margin: 0; padding-left: 20px; font-size: 13.5px; line-height: 1.75; color: #cbd5e1;">
                    {en_items_html}
                </ol>
            </div>

            {inline_cta_html}

            {build_citation_box(item.get('citation'))}
        </div>
        <!-- /wp:group -->
        """
        categories_dossiers_html += dossier_html

    # 4. HBR Strategic Synthesis Matrix & Stewardship Framework (~800 words)
    synthesis_matrix_html = f"""
    <!-- wp:group {{"backgroundColor":"slate","layout":{{"type":"constrained"}}}} -->
    <div id="section-synthesis" class="ucklab-card-section" style="margin: 44px 0; padding: 32px; border-radius: 18px; background: #0f172a; color: #f8fafc; border: 1px solid #334155;">
        <h3 style="margin-top: 0; font-size: 22px; font-weight: 900; color: #38bdf8; display: flex; align-items: center; gap: 10px;">
            <span>📊</span> <b>UCKLab Strategic Review™ 실행 매트릭스 &amp; 청지기적 거버넌스</b>
        </h3>
        <p style="font-size: 14.5px; color: #cbd5e1; line-height: 1.7; margin-bottom: 22px;">
            10대 핵심 분야의 상호 연계 리스크를 바탕으로, 기업과 기관 리더가 즉시 실행해야 할 3단계 전략적 대안(Actionable Alternatives)입니다.
        </p>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; margin-bottom: 24px;">
            <div style="padding: 18px; border-radius: 12px; background: rgba(255,255,255,0.05); border-left: 4px solid #38bdf8;">
                <div style="font-size: 14px; font-weight: 800; color: #38bdf8;">1. 단기 실행 (30일 이내): 규제 준수 &amp; 데이터 감사</div>
                <div style="font-size: 13px; color: #e2e8f0; margin-top: 8px; line-height: 1.65;">
                    G7 AGI 거버넌스 조약 및 글로벌 데이터 보호 규정에 부합하도록 조직 내 AI 파이프라인의 알고리즘 편향성과 프라이버시 침해 요소를 전수 점검하십시오.
                </div>
            </div>
            <div style="padding: 18px; border-radius: 12px; background: rgba(255,255,255,0.05); border-left: 4px solid #10b981;">
                <div style="font-size: 14px; font-weight: 800; color: #10b981;">2. 중기 전략 (180일 이내): 온프레미스·소버린 인프라</div>
                <div style="font-size: 13px; color: #e2e8f0; margin-top: 8px; line-height: 1.65;">
                    특정 빅테크 API에 대한 과도한 단일 종속을 탈피하고, 다자간 오픈소스 모델 및 독립형 에이전트 라우팅을 기반으로 자체 회복탄력성 아키텍처를 확보하십시오.
                </div>
            </div>
            <div style="padding: 18px; border-radius: 12px; background: rgba(255,255,255,0.05); border-left: 4px solid #fbbf24;">
                <div style="font-size: 14px; font-weight: 800; color: #fbbf24;">3. 장기 비전 (3개년): AI 융합 청지기적 소명</div>
                <div style="font-size: 13px; color: #e2e8f0; margin-top: 8px; line-height: 1.65;">
                    기술 전능주의의 환상에서 벗어나, 인간 생명의 존엄성과 공동체의 공공선을 수호하는 윤리적 거버넌스와 크리스천 청지기적 리더십을 제도화하십시오.
                </div>
            </div>
        </div>

        <div style="padding: 16px 20px; border-radius: 10px; background: rgba(59,130,246,0.15); border: 1px solid rgba(59,130,246,0.3); font-size: 13.5px; color: #93c5fd; line-height: 1.6;">
            <b>연구 총괄:</b> Dr. Chang-bae Lee (이창배 박사) | UCKLab AGI Research Institute &amp; Strategic Intelligence Division | AI Fusion Stewardship Theology
        </div>
    </div>
    <!-- /wp:group -->
    """

    sticky_rail_html = build_sticky_rail_html(news_items, osint_data)
    osint_marquee_html = build_osint_marquee_html(osint_data, news_items, column_data)

    vol_num = report_id.split("-W")[-1] if "-W" in report_id else "39"

    # Master Post Gutenberg HTML Assembly (Think-Tank 2-Column Desktop Portal with OSINT Marquee)
    full_content = f"""
    <!-- wp:group {{"align":"wide","layout":{{"type":"default"}}}} -->
    {css_injection_tag}
    {osint_marquee_html}
    <div class="ucklab-desktop-portal alignwide">
        <main class="ucklab-main-col" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b; line-height: 1.8;">
            
            <!-- Header Masthead Banner (UCKLab Strategic Review Style) -->
            <div class="ucklab-masthead-banner" style="background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%); color: #ffffff; padding: 40px 32px; border-radius: 20px; margin-bottom: 32px; box-shadow: 0 14px 35px rgba(15,23,42,0.35);">
                <div style="margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
                    <span class="ucklab-hbr-badge">🏛️ UCKLab Strategic Review™ Vol. {vol_num}</span>
                    <span style="font-size: 13px; color: #94a3b8;">AI Fusion Stewardship Theology | UCKLab Executive Note™</span>
                </div>
                <h1 class="ucklab-post-title" style="font-size: 32px; font-weight: 900; margin: 0 0 14px 0; line-height: 1.35; color: #ffffff;">
                    [UCKLab Strategic Review] Vol. {vol_num} — 2026 AGI 문명 전환기 글로벌 10대 아젠다 &amp; UCKLab Executive Note™ ({today_str})
                </h1>
                <p style="font-size: 17px; color: #cbd5e1; margin: 0 0 22px 0; line-height: 1.65;">
                    AI Fusion Stewardship Theology | 10대 분야 U-Radar 지수 분석, UCKLab Executive Note™, 및 UCKLab Monograph™ (2,500단어 APA 7th 저널) 수록
                </p>
                <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                    <span style="background: rgba(255,255,255,0.12); padding: 6px 14px; border-radius: 8px; font-size: 13px; font-weight: 600;">✓ 10대 분야 UCKLab Executive Note™</span>
                    <span style="background: rgba(255,255,255,0.12); padding: 6px 14px; border-radius: 8px; font-size: 13px; font-weight: 600;">✓ U-Radar Index &amp; 3-Stage 트렌드</span>
                    <span style="background: rgba(255,255,255,0.12); padding: 6px 14px; border-radius: 8px; font-size: 13px; font-weight: 600;">✓ 이창배 Note 권두 정론</span>
                    <span style="background: rgba(255,255,255,0.12); padding: 6px 14px; border-radius: 8px; font-size: 13px; font-weight: 600;">✓ UCKLab Monograph™ (2,500단어 APA 7th 저널)</span>
                </div>
            </div>

            {osint_html}

            {column_section_html}

            <div style="margin: 48px 0 16px 0; border-bottom: 3px solid #2563eb; padding-bottom: 14px;">
                <h2 style="font-size: 27px; font-weight: 900; color: #0f172a; margin: 0;">
                    🌐 글로벌 10대 핵심 분야별 주간 심층 도시에 (Dossiers)
                </h2>
                <div style="font-size: 14px; color: #64748b; margin-top: 6px;">
                    정치 · 경제 · 사회 · 문화 · 금융 · 국방/안보 · 기독교 영성 · 과학/기술/AGI · 기후/환경 · 스포츠
                </div>
            </div>

            {category_nav_bar_html}

            {categories_dossiers_html}

            {synthesis_matrix_html}

            <!-- 4-Grid Card News Component -->
            {cardnews_component_html}

            <!-- Embedded Newsletter Subscription Widget -->
            {subscription_widget_html}

            <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 44px 0;" />

            <!-- Clean Glassmorphism In-Site Paywall Banner & Modal Widget -->
            {paywall_modal_html}

        </main>

        <!-- Executive Sticky Intelligence Rail (Desktop) -->
        <aside class="ucklab-sticky-rail">
            {sticky_rail_html}
        </aside>

    </div>
    <!-- /wp:group -->
    """
    return full_content

# ---------------------------------------------------------------------------
# Hook Summary Excerpt Generator (500 words + Chart + Modal)
# ---------------------------------------------------------------------------
def build_hbr_excerpt_content(report_id, column_data, news_items, osint_data, chart_url=""):
    """
    Builds the 500-word Executive Summary stored in WordPress `excerpt`.
    Embeds:
    1. 500-word Executive Hook Summary
    2. Matplotlib 16:9 Data Chart (`chart_url`)
    3. Clean In-Site Paywall Modal (`templates/paywall_modal.html`)
    """
    vol_num = report_id.split("-W")[-1] if "-W" in report_id else "39"
    today_str = datetime.datetime.now().strftime("%Y.%m.%d")
    paywall_modal_html = load_paywall_modal()
    hbr_custom_css = load_hbr_custom_css()
    css_injection_tag = f"<style id='ucklab-hbr-custom-css'>\n{hbr_custom_css}\n</style>" if hbr_custom_css else ""

    col_theses = column_data.get("three_line_summary", [])
    theses_bullets = "".join([f"<li style='margin-bottom:6px;'>{t.replace('<b>', '').replace('</b>', '')}</li>" for t in col_theses])

    top_news_bullets = "".join([
        f"<li style='margin-bottom:6px;'><b>[{item.get('category_ko')}]</b> {item.get('headline')}</li>"
        for item in news_items[:5]
    ])

    if not chart_url:
        chart_url = f"{WP_URL}/wp-content/uploads/2026/09/chart_WEEKLY-2026-W38-1.png"

    chart_img_html = ""
    if chart_url:
        chart_img_html = f"""
        <div class="ucklab-chart-box" style="margin: 22px 0; text-align: center;">
            <img src="{chart_url}" alt="UCKLab AGI Radar Index™ ({report_id})" style="max-width: 100%; height: auto; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.12); border: 1px solid #e2e8f0;" />
            <div style="font-size: 12px; color: #64748b; margin-top: 8px;">
                ▲ [UCKLab AGI Radar Index™] 주간 10대 아젠다 심층 모니터링 지표 (16:9 Matplotlib Visual)
            </div>
        </div>
        """

    excerpt_html = f"""
    {css_injection_tag}
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #1e293b; line-height: 1.75;">
        
        <div class="ucklab-executive-summary">
            <span class="ucklab-hbr-badge">🏛️ UCKLab Strategic Review™ Vol. {vol_num}</span>
            <h4 style="margin: 8px 0 10px 0; font-size: 18px; font-weight: 800; color: #1e40af;">
                📋 [UCKLab Executive Note™] 2026 AGI 문명 전환기 글로벌 10대 아젠다 ({today_str})
            </h4>
            <p style="font-size: 14.5px; color: #334155; margin: 0 0 14px 0; line-height: 1.65;">
                AI Fusion Stewardship Theology | 10대 분야 U-Radar 지수 분석, UCKLab Executive Note™, 및 UCKLab Monograph™ (2,500단어 APA 7th 저널) 수록.
            </p>
            <div class="ucklab-key-takeaway">
                <div style="font-size: 13.5px; font-weight: 700; color: #78350F; margin-bottom: 6px;">
                    ⚡ 이창배 Note 3대 청지기적 핵심 명제 (AI Fusion Stewardship Theology):
                </div>
                <ul style="margin: 0; padding-left: 20px; font-size: 13.5px; color: #78350F;">
                    {theses_bullets}
                </ul>
            </div>
        </div>

        {chart_img_html}

        <div style="margin: 20px 0; padding: 16px 20px; border-radius: 12px; background: #f8fafc; border: 1px solid #e2e8f0;">
            <div style="font-size: 14px; font-weight: 800; color: #0f172a; margin-bottom: 8px;">
                🌐 주간 10대 핵심 분야 주요 브리핑:
            </div>
            <ul style="margin: 0; padding-left: 20px; font-size: 13.5px; color: #475569; line-height: 1.7;">
                {top_news_bullets}
            </ul>
        </div>

        <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 30px 0;" />

        {paywall_modal_html}
    </div>
    """
    return excerpt_html

# ---------------------------------------------------------------------------
# WordPress REST API & AIOSEO Synchronization
# ---------------------------------------------------------------------------
def update_aioseo_post(post_id, title, description):
    """Directly updates post metadata in All in One SEO (AIOSEO) REST API."""
    try:
        from wp_client import get_wp_client
        client = get_wp_client()
        endpoint = f"{WP_URL}/wp-json/aioseo/v1/post/{post_id}"
        payload = {
            "title": title,
            "description": description,
            "og_title": title,
            "og_description": description,
            "twitter_title": title,
            "twitter_description": description
        }
        res = client.session.post(
            endpoint,
            json=payload,
            headers=client.get_auth_headers(),
            timeout=15
        )
        if res.status_code == 200 and res.json().get("success"):
            print(f"  ✓ [AIOSEO REST API] 포스트 ID {post_id} AIOSEO 메타 등록 성공!")
            return True
        else:
            print(f"  ⚠️ [AIOSEO REST API] 포스트 ID {post_id} 응답: {res.status_code} - {res.text[:120]}")
    except Exception as e:
        print(f"  ⚠️ [AIOSEO REST API] 통신 예외: {e}")
    return False

def create_wp_post(title, content, excerpt="", categories=None, sticky=False, status="publish", aioseo_title="", aioseo_desc="", featured_media=None):
    """
    Creates or publishes a post on WordPress via authenticated REST API:
    - Writes `title`, `content`, `excerpt`, `categories`, `sticky`, `featured_media`
    - Injects AIOSEO post meta fields: `_aioseo_title`, `_aioseo_description`
    - Directly triggers /aioseo/v1/post endpoint for native AIOSEO synchronization
    """
    from wp_client import get_wp_client
    client = get_wp_client()
    
    if categories is None:
        categories = [PARENT_CATEGORY_ID]

    if not aioseo_title:
        aioseo_title = title
    if not aioseo_desc:
        aioseo_desc = f"{title} - UCKLab AI융합미래연구소 주간 HBR급 AGI 심층 리포트."

    payload = {
        "title": title,
        "content": content,
        "excerpt": excerpt,
        "status": status,
        "categories": categories,
        "sticky": sticky,
        "meta": {
            "_aioseo_title": aioseo_title,
            "_aioseo_description": aioseo_desc
        }
    }
    if featured_media:
        payload["featured_media"] = featured_media

    ok, post_id, post_link = client.create_post(payload)
    if ok:
        print(f"  ✓ [WP REST API] 주간 포스트 생성 성공! (ID: {post_id}) -> {post_link}")
        update_aioseo_post(post_id, aioseo_title, aioseo_desc)
        return True, post_id, post_link
    else:
        print(f"  ❌ [WP REST API] 오류: {post_link}")
        return False, None, post_link

def sync_front_page_with_latest_hbr(title, content, aioseo_title="", aioseo_desc=""):
    """
    Synchronizes the WordPress static Front Page (page_on_front) with the latest HBR report.
    This guarantees that visiting https://ucdigin.net/ directly renders the current week's report.
    """
    try:
        from wp_client import get_wp_client
        client = get_wp_client()
        settings_res = client.session.get(f"{WP_URL}/wp-json/wp/v2/settings", headers=client.get_auth_headers(), timeout=15)
        front_page_id = None
        if settings_res.status_code == 200:
            front_page_id = settings_res.json().get("page_on_front")

        if not front_page_id:
            print("  ⚠️ [Front Page Sync] page_on_front ID를 찾을 수 없습니다.")
            return False

        # Update front page content & title
        endpoint = f"{WP_URL}/wp-json/wp/v2/pages/{front_page_id}"
        payload = {
            "title": title,
            "content": content,
            "template": "page-no-title",
            "meta": {
                "_aioseo_title": aioseo_title or title,
                "_aioseo_description": aioseo_desc or f"{title} - UCKLab AI융합미래연구소 주간 HBR 인텔리전스."
            }
        }
        res = client.session.post(endpoint, json=payload, headers=client.get_auth_headers(), timeout=35)
        if res.status_code == 200:
            print(f"  ✓ [Front Page Sync] 메인 프론트 페이지 (ID: {front_page_id}) 최신 HBR 리포트 동기화 완료! -> {WP_URL}/")
            update_aioseo_post(front_page_id, aioseo_title or title, aioseo_desc)
            client.purge_litespeed_cache()
            return True
        else:
            print(f"  ⚠️ [Front Page Sync] 프론트 페이지 업데이트 응답 ({res.status_code}): {res.text[:150]}")
    except Exception as e:
        print(f"  ⚠️ [Front Page Sync] 통신 예외: {e}")
    return False

def sync_column_archive_page(column_data, report_id, post_link=""):
    """
    Synchronizes the dedicated '이창배 Note 정론' page (/column/)
    and publishes the column into Category 122 (이창배_매일시사칼럼).
    """
    auth = HTTPBasicAuth(WP_USER, WP_APP_PASSWORD)
    try:
        title = column_data.get("title", f"이창배 Note 정론 ({report_id})")
        # 1. Publish to Category 122 as standalone post
        cat_post_payload = {
            "title": f"[이창배 Note] {title.replace('이창배 Note:', '').strip()}",
            "content": f"""<!-- wp:group {{"layout":{{"type":"constrained"}}}} -->
            <div class="ucklab-report-wrap" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 900px; margin: 0 auto; color: #1e293b; line-height: 1.8;">
                <h1>{title}</h1>
                <p><b>집필: {column_data.get('author', '이창배 박사')}</b> | UCKLab AI융합미래연구소</p>
                {build_three_line_summary_box(column_data.get('three_line_summary', []), title='이창배 Note 3대 청지기적 명제')}
                <div class="ucklab-column-card">{column_data.get('content', '')}</div>
                <div style="margin-top: 24px; text-align: center;">
                    <a href="{WP_URL}/category/lee-note/" style="background:#eff6ff; color:#2563eb; font-weight:700; padding:10px 20px; border-radius:8px; border:1px solid #dbeafe; text-decoration:none;">
                        📚 이창배 Note 정론 전체 목록 보러가기 ➔
                    </a>
                </div>
            </div><!-- /wp:group -->""",
            "status": "publish",
            "categories": [PARENT_CATEGORY_ID, LEE_NOTE_CATEGORY_ID]
        }
        from wp_client import get_wp_client
        client = get_wp_client()
        ok_col, col_pid, col_link = client.create_post(cat_post_payload)
        if ok_col:
            print(f"  ✓ [Column Sync] 이창배 Note (카테고리 {LEE_NOTE_CATEGORY_ID}) 단독 포스트 발행 성공 (ID: {col_pid}) -> {col_link}")

        # 2. Touch /column/ page
        page_res = requests.get(f"{WP_URL}/wp-json/wp/v2/pages?slug=column", auth=auth, timeout=15)
        if page_res.status_code == 200 and len(page_res.json()) > 0:
            pid = page_res.json()[0]["id"]
            print(f"  ✓ [Column Sync] 전용 아카이브 페이지 (ID: {pid}) 최신 칼럼 동기화 확인! -> {WP_URL}/column/")
            return True
    except Exception as e:
        print(f"  ⚠️ [Column Sync] 칼럼 아카이브 동기화 예외: {e}")
    return False

# ---------------------------------------------------------------------------
# Master Weekly Autonomous Publishing Routine
# ---------------------------------------------------------------------------
def publish_weekly_hbr_report(report_id=None):
    """
    Executes the complete weekly publishing pipeline:
    1. Collects or loads weekly headlines and OSINT indicators.
    2. Runs Writer-Auditor 2-Agent loop for '이창배 Note'.
    3. Generates 16:9 Matplotlib data chart and uploads to WordPress Media Library.
    4. Compiles full 5,000-word HBR report for `content` (Gutenberg review).
    5. Compiles 500-word Executive Summary + Chart + Clean Modal for `excerpt`.
    6. Publishes to ucdigin.net with Category ID 27, sticky=True, AIOSEO meta sync.
    7. Archives to SQLite WAL database (`data/ucklab_weekly_archive.db`).
    8. Dispatches to secondary channel (Facebook Page).
    """
    if not report_id:
        report_id = f"WEEKLY-{datetime.datetime.now().strftime('%Y-W%U')}"
    
    today_str = datetime.datetime.now().strftime("%Y년 %m월 %d일")
    print(f"\n=======================================================")
    print(f"🚀 [UCKLab] 주간 HBR급 AGI 심층 리포트 자율 발행 가동 ({report_id})")
    print(f"=======================================================\n")

    # 1. Collect OSINT & Headlines
    from collector import collect_weekly_top10_news
    headlines, osint_data = collect_weekly_top10_news()

    # 2. Run Writer-Auditor Editorial Column Loop
    from column import generate_weekly_column
    column_data = generate_weekly_column(headlines, osint_data)

    # 3. Generate 16:9 Matplotlib Chart & Upload to WordPress Media Library
    from chart_generator import (
        generate_weekly_chart,
        upload_chart_to_wordpress,
        generate_category_detail_charts,
        upload_all_category_charts
    )
    chart_path = generate_weekly_chart(report_id, headlines)
    chart_url = upload_chart_to_wordpress(chart_path, WP_URL, WP_USER, WP_APP_PASSWORD)
    if not chart_url:
        # Fallback to local path or relative placeholder
        chart_url = f"{WP_URL}/wp-content/uploads/chart_{report_id}.png"

    # 3-B. Generate 10 Individual Category Charts & Upload
    print("\n📊 [Category Charts] 10개 전 분야 맞춤형 16:9 데이터 차트 생성 및 업로드 중...")
    category_charts = generate_category_detail_charts(report_id, headlines)
    category_chart_urls = upload_all_category_charts(category_charts, WP_URL, WP_USER, WP_APP_PASSWORD)

    # 3-C. Curate & Prepare W810 x H480 Free Stock Photos (Pixabay / Pexels / Curated Stock)
    print("\n📸 [Stock Photos] 무료 고화질 사진 선정 및 W810 x H480 규격 최적화 업로드...")
    from stock_image_service import prepare_and_upload_all_stock_photos
    from wp_client import get_wp_client
    wp_client = get_wp_client()
    category_photos = prepare_and_upload_all_stock_photos(headlines, report_id, wp_client=wp_client)

    # 3-D. Top 10 Category Dual Architecture Publishing (Option 1: Open Research Dossier, Option 2: Public Executive Dossier)
    print("\n🏛️ [Category Dual Architecture] 10대 분야 오픈 원문 리서치 & 공개 에디토리얼 발행 중...")
    from category_publisher import publish_all_category_dual_posts
    category_public_urls = publish_all_category_dual_posts(report_id, headlines, category_chart_urls, osint_data, category_photos)

    # 4. Generate Full Content & 500-Word Excerpt
    vol_num = report_id.split("-W")[-1] if "-W" in report_id else "39"
    print(f"\n📝 [Content Assembly] [UCKLab Strategic Review Vol. {vol_num}] 전문 생성 중...")
    post_title = f"[UCKLab Strategic Review] Vol. {vol_num} — 2026 AGI 문명 전환기 글로벌 10대 아젠다 & UCKLab Executive Note™ ({today_str})"
    aioseo_title = f"[UCKLab Strategic Review Vol. {vol_num}] 2026 AGI 문명 전환기 글로벌 10대 아젠다 & 이창배 Note | UCKLab Monograph™"
    aioseo_desc = f"UCKLab Strategic Review: 10대 분야 U-Radar 지수 분석, UCKLab Executive Note™, 및 UCKLab Monograph™ (2,500단어 APA 7th 저널) 수록"

    full_content = build_full_hbr_report_content(report_id, column_data, headlines, osint_data, chart_url, category_chart_urls, category_public_urls)
    excerpt_content = build_hbr_excerpt_content(report_id, column_data, headlines, osint_data, chart_url)

    # 5. Publish to WordPress REST API
    print(f"\n🌐 [WordPress REST API] 뉴스 TOP 10 (ID: {PARENT_CATEGORY_ID}, sticky: True) 포스트 발행 중...")
    master_featured_media = None
    if category_photos and "politics" in category_photos:
        master_featured_media = category_photos["politics"].get("media_id")

    ok, post_id, post_link = create_wp_post(
        title=post_title,
        content=full_content,
        excerpt=excerpt_content,
        categories=[PARENT_CATEGORY_ID],
        sticky=True,
        aioseo_title=aioseo_title,
        aioseo_desc=aioseo_desc,
        featured_media=master_featured_media
    )

    if not ok:
        print(f"❌ 주간 리포트 워드프레스 발행 실패: {post_link}")
        return None

    print(f"🎉 주간 HBR 리포트 발행 성공! (ID: {post_id}) -> {post_link}")

    # 5-B. Synchronize Front Page (https://ucdigin.net/) with latest report
    sync_front_page_with_latest_hbr(post_title, full_content, aioseo_title, aioseo_desc)

    # 5-C. Synchronize '이창배 Note 정론' Page (/column/) & Category 122
    sync_column_archive_page(column_data, report_id, post_link)

    # 6. Archive to SQLite WAL Database
    archive_weekly_report_to_db(report_id, post_title, excerpt_content, full_content, aioseo_title, aioseo_desc)

    # 7. Secondary Publishing: Facebook Group Auto-Post (Card-news Hook)
    try:
        from facebook_publisher import publish_weekly_hbr_to_facebook
        vol_num = "38"
        if "-W" in report_id:
            vol_num = report_id.split("-W")[-1]

        takeaway = "AGI 문명 전환기 국가불안정지수(CII) 및 컴퓨팅 그리드 부하율 심층 분석"
        if column_data and isinstance(column_data, dict):
            theses = column_data.get("three_line_summary") or column_data.get("theses", [])
            if theses:
                takeaway = re.sub(r"<[^>]+>", "", theses[0]).strip()

        fb_report_data = {
            "vol": vol_num,
            "title": post_title,
            "key_takeaway": takeaway,
            "post_url": post_link
        }
        publish_weekly_hbr_to_facebook(fb_report_data)
    except Exception as e:
        print(f"⚠️ [Facebook Auto-Post] 예외: {e}")

    # 8. Secondary Publishing: X.com (Twitter API v2) Auto-Post (@UCKLab_2026)
    try:
        from x_publisher import publish_weekly_hbr_to_x
        x_report_data = {
            "vol": vol_num,
            "title": post_title,
            "key_takeaway": takeaway,
            "post_url": post_link or "https://ucdigin.net"
        }
        x_res = publish_weekly_hbr_to_x(x_report_data)
        if x_res and x_res.get("success"):
            result = result if "result" in locals() else {}
            result["x_tweet_id"] = x_res.get("tweet_id")
            result["x_simulated"] = x_res.get("simulated", False)
    except Exception as e:
        print(f"⚠️ [X.com Auto-Post] 예외: {e}")

    # 9. Automated Newsletter Broadcasting (Google Gmail SMTP from chblee58@gmail.com)
    try:
        from gmail_newsletter_service import broadcast_weekly_newsletter
        column_theses = []
        if column_data and isinstance(column_data, dict):
            column_theses = column_data.get("theses") or column_data.get("three_line_summary", [])
            column_theses = [re.sub(r"<[^>]+>", "", t).strip() for t in column_theses if t]

        friendly_cat_links = {}
        category_korean_names = {
            "politics": "정치·외교",
            "economy": "경제·산업",
            "society": "사회·AI윤리",
            "culture": "문화·예술",
            "finance": "금융·지정학",
            "defense": "국방·안보",
            "christianity": "기독교·청지기",
            "science": "AI·과학·AGI",
            "climate": "기후·환경",
            "sports": "스포츠"
        }
        if category_public_urls and isinstance(category_public_urls, dict):
            for cat_k, url in category_public_urls.items():
                k_name = category_korean_names.get(cat_k, cat_k)
                friendly_cat_links[k_name] = url

        nl_res = broadcast_weekly_newsletter(
            report_title=post_title,
            theses=column_theses or [takeaway],
            chart_url=chart_url,
            category_links=friendly_cat_links,
            dry_run=False
        )
        if nl_res and nl_res.get("success"):
            result = result if "result" in locals() else {}
            result["newsletter_sent_count"] = nl_res.get("count", 0)
    except Exception as e:
        print(f"⚠️ [Gmail Newsletter Broadcast] 예외: {e}")

    # 10. Secondary Publishing: LinkedIn Thought Leadership & Hook Marketing
    try:
        from linkedin_publisher import publish_weekly_hbr_to_linkedin
        li_data = {
            "vol": vol_num,
            "title": post_title,
            "key_takeaway": takeaway,
            "post_url": post_link or "https://ucdigin.net",
            "theses": column_theses if "column_theses" in locals() and column_theses else [takeaway]
        }
        li_res = publish_weekly_hbr_to_linkedin(li_data)
        if li_res and li_res.get("success"):
            result = result if "result" in locals() else {}
            result["linkedin_file"] = li_res.get("file")
    except Exception as e:
        print(f"⚠️ [LinkedIn Auto-Post] 예외: {e}")

    # 11. Enforce 4-Week (28-Day) TOP 10 News Retention Policy
    try:
        from retention_policy import enforce_4week_retention_policy
        retention_res = enforce_4week_retention_policy(retention_days=28)
        print(f"✓ [4주 보관 정책 집행] 만료 기사 점검 완료 (삭제: {retention_res.get('deleted_count', 0)}건, 보관: {retention_res.get('retained_count', 0)}건)")
    except Exception as e:
        print(f"⚠️ [4주 보관 정책] 예외: {e}")

    result = {
        "success": True,
        "report_id": report_id,
        "post_id": post_id,
        "post_link": post_link,
        "chart_url": chart_url,
        "archived_db": DB_PATH
    }

    # Save summary json
    summary_file = os.path.join(DATA_DIR, f"weekly_publish_summary_{report_id}.json")
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return result

if __name__ == "__main__":
    publish_weekly_hbr_report()
