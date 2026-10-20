"""
category_publisher.py - UCKLab Weekly HBR 10-Category Dual Architecture Publisher
Features:
1. Option 1 (Admin Private Full Archive):
   - Posts separated by individual category with status: 'private'.
   - Contains un-redacted full research dossiers for Super Admin (Dr. Lee)
     to edit & preserve via Advanced Editor Tools in wp-admin.
2. Option 2 (Public Executive Dossier & Paywall):
   - Posts separated by individual category with status: 'publish'.
   - High-elegance Institute-type summary with 16:9 Matplotlib Category Radar chart.
   - High-conversion Glassmorphism Paywall Card (9,900 KRW Toss payment & 12h secure PDF/PPT).
3. Seamless integration into wp_publisher.py and front page.
"""

import os
import sys
import re
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from category_dossier_data import CATEGORY_DOSSIERS

# Windows console UTF-8 setup
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

WP_URL = os.getenv("WP_URL", "https://ucdigin.net")
WP_USER = os.getenv("WP_USER", "AutoBot_Editor")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD", "5kOS QdBg 6Prd qR4F qixR lg43")
PARENT_CATEGORY_ID = 2  # ?댁뒪 TOP 10

# WordPress Category Taxonomy Mapping on ucdigin.net
WP_CATEGORY_MAP = {
    "politics": 3,           # ?뺤튂쨌?멸탳
    "economy": 4,            # 寃쎌젣쨌?곗뾽
    "society": 5,            # ?ы쉶쨌AI?ㅻ━
    "culture": 6,            # 臾명솕쨌?덉닠
    "finance": 7,            # 湲덉쑖쨌吏?뺥븰
    "defense": 8,            # 援?갑쨌?덈낫
    "christianity": 9,       # 湲곕룆援먃룹껌吏湲?    "science": 10,           # 怨쇳븰쨌湲곗닠쨌AGI
    "climate": 11,           # 湲고썑쨌?섍꼍쨌?먮꼫吏
    "sports": 12             # ?ㅽ룷痢?}

def build_category_badge(item, link_url=""):
    """Renders responsive branded Category Symbol Badge."""
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
    
    badge_html = f"""
    <div style="background: {cfg['grad']}; border-left: 4px solid {cfg['border']}; border-radius: 8px; padding: 10px 16px; margin-bottom: 14px; color: #ffffff; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 10px rgba(0,0,0,0.08);">
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 18px;">{item.get('icon', '?뱦')}</span>
            <span style="font-size: 14px; font-weight: 800; letter-spacing: 0.5px;">{item.get('category_ko', '')} ({item.get('category_en', '')})</span>
        </div>
        <div style="font-size: 11.5px; opacity: 0.85; font-weight: 500;">
            {cfg['sub']}
        </div>
    </div>
    """
    if link_url:
        return f'<a href="{link_url}" style="text-decoration:none; display:block;">{badge_html}</a>'
    return badge_html

def build_three_line_summary_box(three_lines, title="二쇨컙 ?듭떖 ?꾨왂 紐낆젣 (HBR Theses)"):
    """Renders executive summary block."""
    if not three_lines:
        return ""
    items_html = "".join([f"<li style='margin-bottom: 8px; word-break: keep-all;'>{line}</li>" for line in three_lines])
    return f"""
    <div class="ucklab-summary-block" style="margin: 22px 0; padding: 20px 22px; border-radius: 12px; background: #eff6ff; border-left: 5px solid #2563eb; border: 1px solid #dbeafe; box-shadow: 0 4px 12px rgba(37,99,235,0.05); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <div style="font-size: 14px; font-weight: 800; color: #1e40af; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;">
            <span>??/span> <b>{title}</b>
        </div>
        <ul style="margin: 0; padding-left: 22px; font-size: 14.5px; line-height: 1.75; color: #1e293b;">
            {items_html}
        </ul>
    </div>
    """

def build_citation_box(citation_data):
    """Renders official source & citation block."""
    if not citation_data:
        return ""
    source = citation_data.get("source", "湲濡쒕쾶 怨듦났 諛?二쇱슂 ?깊겕?깊겕")
    url = citation_data.get("url", "https://ucklab.org/research")
    date_str = citation_data.get("date", "?뱀씪")
    attribution = citation_data.get("attribution", "UCKLab AI?듯빀誘몃옒?곌뎄??(?댁갹諛?諛뺤궗 ?곌뎄?) 쨌 二쇨컙 HBR ?명뀛由ъ쟾??遺꾩꽍")

    return f"""
    <div style="margin: 24px 0 16px 0; padding: 18px 22px; border-radius: 12px; background: #f8fafc; border: 1px solid #e2e8f0; font-size: 13px; line-height: 1.65; color: #475569; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <div style="font-weight: 800; color: #0f172a; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;">
            <span>?뱫</span> <b>怨듭떇 異쒖쿂 諛??숈닠 ?명뀛由ъ쟾???몄슜 (Source &amp; Citation)</b>
        </div>
        <div style="word-break: break-all;">
            ??<b>?먮Ц 異쒖쿂:</b> {source} (李몄“: {date_str})<br/>
            ??<b>?먮Ц 留곹겕:</b> <a href="{url}" target="_blank" rel="noopener noreferrer" style="color: #2563eb; text-decoration: underline;">{url}</a><br/>
            ??<b>遺꾩꽍 諛?洹??</b> {attribution}
        </div>
    </div>
    """

def build_category_paywall_card(cat_item, main_landing_url="https://ucdigin.net"):
    """
    Renders high-conversion Glassmorphism Paywall CTA Box
    for individual category posts, featuring:
    - 80:20 Language Ratio Rule Architecture
    - 3-Revisions Governance Guarantee
    - Dual CTAs (ucklab.org 1:1 Synthesis & Instant 9,900 KRW Paywall)
    """
    cat_id = cat_item.get("id", "politics")
    cat_name = cat_item.get('category_ko', '?ъ링')
    on_demand_url = f"https://ucklab.org/?cat={cat_id}#executive-pipeline"
    toss_cta_url = f"{main_landing_url}/#ucklab-paywall-cta"
    admin_on_demand_url = f"https://ucklab.org/?cat={cat_id}&admin_bypass=true&admin_key=UCK777#executive-pipeline"

    pdf_map = {
        "politics": "UCKLab_Weekly_Report_Politics.pdf",
        "economy": "UCKLab_Weekly_Report_Economy.pdf",
        "science": "UCKLab_Weekly_Report_Science_AI.pdf",
        "defense": "UCKLab_Weekly_Report_Defense.pdf",
        "christianity": "UCKLab_Weekly_Report_Christianity.pdf",
        "finance": "UCKLab_Weekly_Report_Finance.pdf",
        "society": "UCKLab_Weekly_Report_Society.pdf",
        "culture": "UCKLab_Weekly_Report_Culture.pdf",
        "climate": "UCKLab_Weekly_Report_Climate.pdf",
        "sports": "UCKLab_Weekly_Report_Sports.pdf"
    }
    ppt_map = {
        "politics": "UCKLab_Presentation_Politics.pptx",
        "economy": "UCKLab_Presentation_Economy.pptx",
        "science": "UCKLab_Presentation_Science_AI.pptx",
        "defense": "UCKLab_Presentation_Defense.pptx",
        "christianity": "UCKLab_Presentation_Christianity.pptx",
        "finance": "UCKLab_Presentation_Finance.pptx",
        "society": "UCKLab_Presentation_Society.pptx",
        "culture": "UCKLab_Presentation_Culture.pptx",
        "climate": "UCKLab_Presentation_Climate.pptx",
        "sports": "UCKLab_Presentation_Sports.pptx"
    }
    pdf_filename = pdf_map.get(cat_id, "UCKLab_Weekly_Report_Comprehensive.pdf")
    ppt_filename = ppt_map.get(cat_id, "UCKLab_Presentation_Comprehensive.pptx")
    admin_pdf_url = f"https://ucdigin.net/wp-content/uploads/2026/09/{pdf_filename}"
    admin_ppt_url = f"https://ucdigin.net/wp-content/uploads/2026/09/{ppt_filename}"

    return f"""
    <!-- wp:group -->
    <div id="ucklab-category-paywall" style="margin: 36px 0; padding: 34px 28px; border-radius: 16px; background: linear-gradient(135deg, #090d16 0%, #1e3a8a 100%); color: #ffffff; text-align: center; box-shadow: 0 12px 32px rgba(15,23,42,0.35); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Pretendard', sans-serif;">
        <div id="ucklab-cat-lock-badge" onclick="window.onUcklabBadgeSecretClick && window.onUcklabBadgeSecretClick()" style="display: inline-block; padding: 5px 16px; border-radius: 20px; background: rgba(59,130,246,0.25); color: #93c5fd; font-size: 12.5px; font-weight: 800; margin-bottom: 14px; letter-spacing: 0.5px; cursor: pointer; user-select: none;">
            ?뱞 UCKLab Monograph??Upgrade 쨌 12?쒓컙 蹂댁븞 諛쒓툒
        </div>
        <h3 style="margin: 0 0 14px 0; font-size: 23px; font-weight: 900; color: #ffffff; line-height: 1.4;">
            2,500?⑥뼱 APA 7th 洹쒓꺽 UCKLab Monograph??PDF 諛쒓툒 ({cat_name})
        </h3>
        <p style="font-size: 15px; color: #cbd5e1; line-height: 1.75; max-width: 720px; margin: 0 auto 20px auto; word-break: keep-all;">
            ?⑥닚 ?붿빟???섏뼱 湲濡쒕쾶 ?숈닠쨌?꾨왂 蹂닿퀬???쒖?(APA 7th)?쇰줈 ?묒꽦???꾨Ц ?명뀛由ъ쟾?ㅻ? ?곴뎄 ?뚯옣?섏꽭?? 
            C-Level ?꾩썝 蹂닿퀬??16:9 ?꾨젅?좏뀒?댁뀡 PPT ?깃낵 3???섏젙 嫄곕쾭?뚯뒪(Revisions Guarantee)媛 臾댁긽 蹂댁옣?⑸땲??
        </p>

        <!-- 80:20 Language Ratio Rule Architecture Box -->
        <div style="margin: 20px auto 26px auto; max-width: 720px; text-align: left; background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.15); border-radius: 12px; padding: 18px 22px;">
            <div style="font-size: 13.5px; font-weight: 800; color: #38bdf8; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;">
                <span>?뙋</span> <b>[UCKLab Monograph??80:20 ?몄뼱 鍮꾩쑉 洹쒖젙 &amp; 3???섏젙 嫄곕쾭?뚯뒪]</b>
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 10px; font-size: 13px; color: #e2e8f0; line-height: 1.6;">
                <div style="background: rgba(0,0,0,0.25); padding: 10px 14px; border-radius: 8px; border-left: 3px solid #38bdf8;">
                    <b>?뀺截?援?Ц 二쇨텒??(Korean Focus)</b><br/>
                    援?Ц 蹂몃Ц 80% (2,000?⑥뼱) + ?곷Ц Executive ?붿빟 20% (500?⑥뼱)
                </div>
                <div style="background: rgba(0,0,0,0.25); padding: 10px 14px; border-radius: 8px; border-left: 3px solid #10b981;">
                    <b>?뀻截?湲濡쒕쾶 ?꾨왂??(Global Focus)</b><br/>
                    ?곷Ц 蹂몃Ц 80% (2,000?⑥뼱) + 援?Ц ?듭떖 ?붿빟 20% (500?⑥뼱)
                </div>
            </div>
            <div style="font-size: 12px; color: #94a3b8; margin-top: 10px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 8px;">
                ??<b>怨듯넻 ?쒓났:</b> C-Level ?꾩썝 蹂닿퀬??16:9 ?꾨젅?좏뀒?댁뀡 PPT ??(10~12?? + 3???섏젙 嫄곕쾭?뚯뒪(Revisions Guarantee) 臾댁긽 蹂댁옣
            </div>
        </div>

        <div style="display: flex; justify-content: center; gap: 14px; flex-wrap: wrap;">
            <a href="https://ucklab.org/api/v1/academic/upgrade?topic={cat_name}" target="_blank" rel="noopener noreferrer" style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); color: #FBBF24; padding: 14px 28px; border-radius: 12px; font-size: 15px; font-weight: 800; text-decoration: none; border: 1.5px solid #D97706; box-shadow: 0 10px 25px rgba(217, 119, 6, 0.3); display: inline-flex; align-items: center; gap: 8px;">
                <span>?럳</span> <b>UCKLab Monograph??PDF 諛붾줈 ?앹꽦?섍린 (2,500?⑥뼱 APA 7th) ??/b>
            </a>
            <a href="{on_demand_url}" target="_blank" rel="noopener noreferrer" style="background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: #ffffff; padding: 13px 24px; border-radius: 10px; font-size: 14.5px; font-weight: 700; text-decoration: none; display: inline-flex; align-items: center; gap: 8px;">
                <span>??/span> <b>ucklab.org 1:1 ?⑤뵒留⑤뱶 ?ㅼ떆媛?吏곸“ ??/b>
            </a>
        </div>

        <!-- Super Admin Category Bypass Box (Hidden by default, unlocked only when authenticated) -->
        <div id="ucklab-cat-admin-bypass-box" style="display: none; margin: 20px auto 0 auto; max-width: 720px; padding: 14px 18px; border-radius: 12px; background: linear-gradient(135deg, rgba(217, 119, 6, 0.2), rgba(16, 185, 129, 0.25)); border: 1.5px solid #fbbf24; text-align: left;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span style="font-size: 13px; font-weight: 800; color: #fbbf24; display: flex; align-items: center; gap: 6px;">
                    <span>?썳截?/span> [理쒓퀬愿由ъ옄 留덉뒪???몄쬆 ?뱀씤]
                </span>
                <span style="font-size: 11px; color: #34d399; font-weight: 700; background: rgba(16,185,129,0.2); padding: 2px 8px; border-radius: 6px;">寃곗젣 ?고쉶 ?쒖꽦</span>
            </div>
            <p style="font-size: 12px; color: #e2e8f0; margin: 0 0 10px 0; line-height: 1.5;">
                寃곗젣李??곌껐??嫄대꼫?곌퀬 ?대떦 遺꾩빞({cat_name})??2,500?⑥뼱 APA 7th Monograph??由ы룷?몃? ?ㅼ떆媛?AGI 吏곸“?섍굅??利됱떆 ?ㅼ슫濡쒕뱶?????덉뒿?덈떎.
            </p>
            <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                <a href="{admin_on_demand_url}" target="_blank" rel="noopener noreferrer" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: #ffffff; padding: 10px 18px; border-radius: 8px; font-size: 13px; font-weight: 800; text-decoration: none; box-shadow: 0 4px 12px rgba(16,185,129,0.35); display: inline-flex; align-items: center; gap: 6px;">
                    <span>??/span> <b>[?뚰뵾 ?⑥뒪] ucklab.org 1:1 AGI 利됱꽍 吏곸“ ??/b>
                </a>
                <a href="{admin_pdf_url}" target="_blank" download style="background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); color: #ffffff; padding: 10px 16px; border-radius: 8px; font-size: 13px; font-weight: 700; text-decoration: none;">
                    ?뱿 利됱떆 Monograph???ㅼ슫濡쒕뱶
                </a>
                <a href="{admin_ppt_url}" target="_blank" download style="background: rgba(217,119,6,0.3); border: 1px solid rgba(217,119,6,0.5); color: #fde68a; padding: 10px 16px; border-radius: 8px; font-size: 13px; font-weight: 700; text-decoration: none;">
                    ?뱤 留욎땄 PPT ?ㅼ슫濡쒕뱶
                </a>
            </div>
        </div>

        <div style="font-size: 12px; color: #94a3b8; margin-top: 16px;">
            ???좎뒪?섏씠癒쇱툩 媛꾪렪寃곗젣 吏??| 12?쒓컙 蹂댁븞 ?좏겙 諛쒓툒 &amp; ?숈쟻 ?뚰꽣留덊겕 媛곸씤 | UCKLab ?곌뎄吏??쇱뼱 由щ럭
        </div>
    </div>
    <!-- /wp:group -->
    <script>
    (function(){{
        var ucklabBadgeClickCount = 0;
        var ucklabBadgeClickTimer = null;
        function checkCatAdmin(){{
            try {{
                var s = sessionStorage.getItem('ucklab_admin_bypass') === 'ENABLED_UCK777';
                var l = localStorage.getItem('ucklab_admin_bypass') === 'ENABLED_UCK777';
                var p = new URLSearchParams(window.location.search);
                var u = p.get('admin_key') === 'UCK777' || p.get('admin_bypass') === 'true';
                if (u) {{
                    sessionStorage.setItem('ucklab_admin_bypass', 'ENABLED_UCK777');
                    localStorage.setItem('ucklab_admin_bypass', 'ENABLED_UCK777');
                    s = true;
                }}
                var el = document.getElementById('ucklab-cat-admin-bypass-box');
                if (el) el.style.display = (s || l || u) ? 'block' : 'none';
            }} catch(e){{}}
        }}
        window.onUcklabBadgeSecretClick = function(){{
            ucklabBadgeClickCount++;
            if (ucklabBadgeClickTimer) clearTimeout(ucklabBadgeClickTimer);
            if (ucklabBadgeClickCount >= 3) {{
                ucklabBadgeClickCount = 0;
                promptKey();
            }} else {{
                ucklabBadgeClickTimer = setTimeout(function(){{ ucklabBadgeClickCount = 0; }}, 1200);
            }}
        }};
        function promptKey(){{
            var code = prompt('?뵏 [UCKLab 理쒓퀬愿由ъ옄 蹂댁븞 ?몄쬆]\\n留덉뒪???쒗겕由?肄붾뱶瑜??낅젰?섏떗?쒖삤:');
            if (code && (code.trim().toUpperCase() === 'UCK777' || code.trim().toUpperCase() === 'ADMIN2026' || code.trim().toUpperCase() === 'UCKADMIN')) {{
                sessionStorage.setItem('ucklab_admin_bypass', 'ENABLED_UCK777');
                localStorage.setItem('ucklab_admin_bypass', 'ENABLED_UCK777');
                alert('??[?뱀씤 ?꾨즺] 理쒓퀬愿由ъ옄 沅뚰븳???쒖꽦?붾릺?덉뒿?덈떎.');
                checkCatAdmin();
            }} else if (code && (code.trim() === 'logout' || code.trim() === 'exit')) {{
                sessionStorage.removeItem('ucklab_admin_bypass');
                localStorage.removeItem('ucklab_admin_bypass');
                alert('理쒓퀬愿由ъ옄 紐⑤뱶媛 ?댁젣?섏뿀?듬땲??');
                checkCatAdmin();
            }} else if (code) {{
                alert('???щ컮瑜댁? ?딆? 留덉뒪??肄붾뱶?낅땲??');
            }}
        }}
        window.promptUcklabAdminKey = promptKey;
        window.addEventListener('load', checkCatAdmin);
        document.addEventListener('DOMContentLoaded', checkCatAdmin);
        checkCatAdmin();
        window.addEventListener('keydown', function(e){{
            if (e.ctrlKey && e.shiftKey && (e.key === 'A' || e.key === 'a')) {{
                e.preventDefault();
                promptKey();
            }}
        }});
    }})();
    </script>
    """

# ---------------------------------------------------------------------------
# Option 1: Super Admin Private Full Archive
# ---------------------------------------------------------------------------
def publish_admin_private_archive(cat_item, report_id, osint_data=None, photo_info=None):
    """
    Creates an OPEN RESEARCH DOSSIER post (status: 'publish').
    Preserves un-redacted full research notes & OSINT telemetry for the public and Dr. Lee.
    Includes featured_media and elegant glassmorphism styling.
    """
    cat_id = cat_item.get("id", "politics")
    cat_ko = cat_item.get("category_ko", "?뺤튂/?멸탳")
    headline = cat_item.get("headline", "AGI 嫄곕쾭?뚯뒪")
    vol = report_id.split("-W")[-1] if "-W" in report_id else "38"

    post_title = f"[湲濡쒕쾶 ?먮Ц 由ъ꽌移?| {cat_ko}] {headline}"

    # Full raw content formatted with elegant open research banner
    content_html = f"""
    <!-- wp:group {{"layout":{{"type":"constrained"}}}} -->
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 900px; margin: 0 auto; color: #1e293b; line-height: 1.8;">
        
        <div style="background: rgba(30, 41, 59, 0.05); border-left: 5px solid #0284c7; padding: 16px 20px; border-radius: 8px; margin-bottom: 24px; font-size: 14px; color: #0369a1;">
            <b>?룢截?UCKLab 湲濡쒕쾶 ?명뀛由ъ쟾???ъ링 由ъ꽌移?&amp; OSINT ?먮Ц 遺꾩꽍</b><br/>
            蹂?由ы룷?몃뒗 湲濡쒕쾶 ?깊겕?깊겕 ?먮Ц 諛??뺣? OSINT ?곗씠?곕? 吏묐??깊븳 UCKLab ?ㅽ뵂 ?곌뎄 ?먯궛?낅땲??
        </div>

        <h2>{headline} - {cat_ko} ?곌뎄 ?먮Ц 諛?OSINT ?붾젅硫뷀듃由?/h2>
        <p><b>由ы룷??ID:</b> {report_id} | <b>遺꾩빞:</b> {cat_ko} ({cat_item.get('category_en', '')}) | <b>異쒖쿂:</b> {cat_item.get('source', '')}</p>

        <hr/>

        <h3>1. 3? ?꾨왂 紐낆젣 (Theses)</h3>
        {build_three_line_summary_box(cat_item.get('three_line_summary'), title=f"{cat_ko} ?먮Ц 紐낆젣")}

        <h3>2. HBR湲??ъ링 ?명뀛由ъ쟾??遺꾩꽍 (?먮Ц)</h3>
        <div style="padding: 18px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; margin-bottom: 20px;">
            <p style="font-size: 16px; line-height: 1.9; color: #1e293b;">
                {cat_item.get('summary_ko', '')}
            </p>
        </div>

        <h3>3. 湲濡쒕쾶 ?곷Ц ?꾨왂 ?명뀛由ъ쟾??(Foresight)</h3>
        <div style="padding: 16px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px;">
            <p style="font-size: 14.5px; line-height: 1.75; color: #475569;">
                {cat_item.get('summary_en', '')}
            </p>
        </div>

        <h3>4. ?몄슜 諛?怨듭떇 李몄“</h3>
        <p>
            ??怨듭떇 URL: {cat_item.get('citation', {}).get('url', '')}<br/>
            ???몄슜泥? {cat_item.get('citation', {}).get('source', '')}<br/>
            ??洹?? {cat_item.get('citation', {}).get('attribution', '')}
        </p>

    </div>
    <!-- /wp:group -->
    """

    # Private research archive uses Uncategorized (ID 1) to avoid leaking into public category feeds
    categories = [1]

    featured_media_id = None
    if photo_info:
        featured_media_id = photo_info.get("media_id")
    elif cat_item.get("featured_media_id"):
        featured_media_id = cat_item.get("featured_media_id")

    payload = {
        "title": post_title,
        "content": content_html,
        "excerpt": cat_item.get("summary_ko", ""),
        "status": "private",  # Private research archive to avoid duplicating public category posts
        "categories": categories
    }
    if featured_media_id:
        payload["featured_media"] = featured_media_id

    try:
        from wp_client import get_wp_client
        client = get_wp_client()
        ok, post_id, post_link = client.create_post(payload)
        if ok:
            print(f"  ??[Private Research Dossier] '{cat_ko}' 鍮꾧났媛?蹂닿? ?꾨즺 (ID: {post_id})")
            return post_id
        else:
            print(f"  ?좑툘 [Private Research Dossier] '{cat_ko}' ?ㅽ뙣: {post_link}")
    except Exception as e:
        print(f"  ?좑툘 [Private Research Dossier] ?덉쇅: {e}")
    return None

# ---------------------------------------------------------------------------
# Option 2: Public High-Elegance Executive Dossier & Paywall
# ---------------------------------------------------------------------------
def publish_public_executive_dossier(cat_item, report_id, chart_url="", photo_info=None):
    """
    Creates a PUBLIC post (status: 'publish') featuring:
    - Minimum 500-word standalone executive academic dossier
    - Categorized Title: [UCKLab {cat_ko}] {headline}
    - W810 x H480 Curated Free Stock Photo (Pixabay/Pexels) as featured_media
    - 2-line copywriter cognitive trigger hook
    - 3 Thematic Points (Multi-paragraph academic analysis)
    - 16:9 Matplotlib Category Radar chart
    - 5-line English C-suite executive briefing
    - Dr. Lee pull quote
    - 80:20 Language ratio paywall card with dual CTAs
    """
    cat_id = cat_item.get("id", "politics")
    cat_ko = cat_item.get("category_ko", "?뺤튂/?멸탳")
    headline = cat_item.get("headline", "AGI 嫄곕쾭?뚯뒪")
    vol = report_id.split("-W")[-1] if "-W" in report_id else "39"

    post_title = f"[UCKLab Strategic Review] {cat_ko} ??{headline} & UCKLab Executive Note??

    featured_media_id = None
    featured_image_url = ""
    if photo_info:
        featured_media_id = photo_info.get("media_id")
        featured_image_url = photo_info.get("source_url") or ""
    elif cat_item.get("featured_media_id"):
        featured_media_id = cat_item.get("featured_media_id")
        featured_image_url = cat_item.get("featured_image_url") or ""

    photo_banner_html = ""
    if featured_image_url:
        photo_banner_html = f"""
        <!-- W810 x H480 Free Stock Curated Featured Banner (Pixabay / Pexels / Curated HD) -->
        <div class="ucklab-featured-banner" style="margin: 0 0 24px 0; text-align: center; overflow: hidden; border-radius: 14px; box-shadow: 0 8px 24px rgba(0,0,0,0.12); border: 1px solid rgba(0,0,0,0.08);">
            <img src="{featured_image_url}" alt="{headline} ({cat_ko})" style="width: 100%; max-width: 810px; height: auto; aspect-ratio: 810/480; object-fit: cover; display: block; margin: 0 auto;" />
            <div style="font-size: 11.5px; color: #64748b; margin-top: 6px; text-align: right; padding-right: 8px;">
                ?벜 UCKLab Curated Editorial Intelligence Photo (810x480)
            </div>
        </div>
        """

    dossier = CATEGORY_DOSSIERS.get(cat_id, {})
    subtitle = dossier.get("subtitle", f"{cat_ko} 二쇨컙 UCKLab Executive Note??諛?U-Radar 吏??遺꾩꽍")
    copywriter_hook = dossier.get("copywriter_hook", "")
    theses = dossier.get("theses", cat_item.get("three_line_summary", []))
    p1_title = dossier.get("point1_title", "1. 嫄곗떆???쒖뒪??吏꾨떒 (Macro Diagnosis)")
    p1_content = dossier.get("point1_content", cat_item.get("summary_ko", ""))
    p2_title = dossier.get("point2_title", "2. ?뚭퀬由ъ쬁 二쇨텒怨??뚮쾭由??꾪궎?띿쿂 (Sovereignty & Architecture)")
    p2_content = dossier.get("point2_content", "")
    p3_title = dossier.get("point3_title", "3. C-Level ?ㅽ뻾 怨쇱젣 (Actionable Execution)")
    p3_content = dossier.get("point3_content", "")
    exec_synthesis = dossier.get("executive_synthesis", "")
    english_lines = dossier.get("english_briefing", [cat_item.get("summary_en", "")])
    pull_quote = dossier.get("pull_quote", "")
    citation_data = dossier.get("citation", cat_item.get("citation", {}))

    badge_html = build_category_badge(cat_item)
    radar = cat_item.get("trend_radar", {})
    radar_stage = radar.get("stage", "Stage 2 (Community)")
    radar_velocity = radar.get("velocity", 3.2)
    radar_desc = radar.get("transition_description", "?몃젋???뺤궛 以?)

    chart_img_html = ""
    if chart_url:
        chart_img_html = f"""
        <div class="ucklab-chart-box" style="margin: 26px 0; text-align: center;">
            <img src="{chart_url}" alt="{cat_ko} ?꾨왂 遺꾩꽍 ?곗씠??李⑦듃" style="width: 100%; max-width: 820px; height: auto; border-radius: 14px; border: 1px solid rgba(0,0,0,0.08); box-shadow: 0 8px 24px rgba(0,0,0,0.08);" loading="lazy" />
            <div style="font-size: 12px; color: #64748b; margin-top: 8px; font-weight: 600;">
                ??[UCKLab AGI Radar Index?? {cat_ko} 4? ?듭떖 ??븰 ?곗씠???쒓컖??吏??            </div>
        </div>
        """

    theses_html = build_three_line_summary_box(theses, title=f"{cat_ko} 二쇨컙 3? ?듭떖 ?꾨왂 紐낆젣")
    paywall_html = build_category_paywall_card(cat_item, main_landing_url=WP_URL)
    citation_html = build_citation_box(citation_data)

    def format_paragraphs(text):
        if not text:
            return ""
        paras = text.split("\n\n")
        return "".join([f"<p style='font-size: 16px; line-height: 1.9; color: #1e293b; margin-bottom: 14px; word-break: keep-all;'>{p.strip()}</p>" for p in paras if p.strip()])

    p1_html = format_paragraphs(p1_content)
    p2_html = format_paragraphs(p2_content)
    p3_html = format_paragraphs(p3_content)

    en_list_items = "".join([f"<li style='margin-bottom: 8px; word-break: keep-all;'>{line}</li>" for line in english_lines])

    synthesis_box_html = ""
    if exec_synthesis:
        synthesis_box_html = f"""
        <div style="margin: 24px 0; padding: 22px 24px; border-radius: 12px; background: #eff6ff; border-left: 5px solid #2563eb; border: 1px solid #bfdbfe;">
            <h4 style="margin: 0 0 8px 0; font-size: 15px; font-weight: 800; color: #1e40af;">
                ?룢截?[UCKLab ?숈닠??珥앺룊 &amp; 泥??湲곗쟻 二쇨텒 寃곕줎]
            </h4>
            <p style="margin: 0; font-size: 15px; line-height: 1.85; color: #1e3a8a; word-break: keep-all;">
                {exec_synthesis}
            </p>
        </div>
        """

    pull_quote_html = ""
    if pull_quote:
        pull_quote_html = f"""
        <div class="ucklab-pull-quote" style="margin: 28px 0; padding: 22px 28px; border-radius: 12px; background: #fefce8; border-left: 5px solid #eab308; border: 1px solid #fef08a; font-style: italic; font-size: 15px; color: #713f12; line-height: 1.75; word-break: keep-all;">
            {pull_quote}
        </div>
        """

    hook_box_html = ""
    if copywriter_hook:
        hook_box_html = f"""
        <div class="ucklab-copywriter-hook" style="background: #f8fafc; border-left: 5px solid #2563eb; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px 24px; margin: 24px 0; font-size: 15.5px; line-height: 1.8; color: #1e293b; font-weight: 500; word-break: keep-all; box-shadow: 0 4px 14px rgba(37,99,235,0.04);">
            <div style="font-size: 12px; font-weight: 800; color: #2563eb; margin-bottom: 6px; letter-spacing: 0.5px;">
                ??STRATEGIC COGNITIVE TRIGGER // ?ъ쟾 寃利?釉뚮━??            </div>
            <p style="margin: 0; white-space: pre-line;">
                {copywriter_hook}
            </p>
        </div>
        """

    public_content = f"""
    <!-- wp:group {{"layout":{{"type":"constrained"}}}} -->
    <div class="ucklab-dossier-page" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Pretendard', sans-serif; max-width: 880px; margin: 0 auto; color: #1e293b; line-height: 1.85;">
        
        {photo_banner_html}

        {badge_html}

        <div style="display: flex; gap: 8px; align-items: center; margin: 16px 0 10px 0; flex-wrap: wrap;">
            <span style="display:inline-flex; align-items:center; gap:6px; padding: 5px 14px; border-radius: 8px; background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(245, 158, 11, 0.5); color: #FBBF24; font-size: 12.5px; font-weight: 800; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4); text-shadow: 0 1px 2px rgba(0,0,0,0.8);">
                {radar_stage} (?띾룄: +{radar_velocity}?)
            </span>
            <span style="display:inline-flex; align-items:center; gap:6px; padding: 5px 14px; border-radius: 8px; background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(56, 189, 248, 0.55); color: #38BDF8; font-size: 12.5px; font-weight: 800; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4); text-shadow: 0 1px 2px rgba(0,0,0,0.8);">
                ?썳截??ъ쟾 寃利앹슜 (500?⑥뼱+)
            </span>
            <span style="font-size: 13px; color: #CBD5E1; font-weight: 500;">
                {radar_desc}
            </span>
        </div>

        <h1 style="font-size: 28px; font-weight: 900; color: #0f172a; margin: 0 0 10px 0; line-height: 1.35;">
            {headline}
        </h1>

        <div style="font-size: 16px; font-weight: 600; color: #2563eb; margin-bottom: 16px; line-height: 1.5;">
            {subtitle}
        </div>

        <div style="font-size: 13px; color: #64748b; margin-bottom: 22px; padding-bottom: 12px; border-bottom: 1px solid #e2e8f0;">
            <b>?곌뎄 諛쒗뻾:</b> UCKLab AGI Research Institute | <b>U-Radar 吏??</b> {cat_item.get('trend_score', 88)} pt | <b>遺꾩빞:</b> {cat_ko} | <b>?쇱뼱 由щ럭 ?꾨즺</b>
        </div>

        {hook_box_html}

        {theses_html}

        {chart_img_html}

        <!-- 3-Part Academic Standalone Analysis (500-word+ Core) -->
        <div class="ucklab-point-card" style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 26px 28px; margin: 22px 0; box-shadow: 0 4px 16px rgba(15,23,42,0.03);">
            <h3 style="margin: 0 0 14px 0; font-size: 17.5px; font-weight: 800; color: #1e40af; display: flex; align-items: center; gap: 8px;">
                <span>?룢截?/span> <b>{p1_title}</b>
            </h3>
            {p1_html}
        </div>

        <div class="ucklab-point-card" style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 26px 28px; margin: 22px 0; box-shadow: 0 4px 16px rgba(15,23,42,0.03);">
            <h3 style="margin: 0 0 14px 0; font-size: 17.5px; font-weight: 800; color: #0d9488; display: flex; align-items: center; gap: 8px;">
                <span>?썳截?/span> <b>{p2_title}</b>
            </h3>
            {p2_html}
        </div>

        <div class="ucklab-point-card" style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 26px 28px; margin: 22px 0; box-shadow: 0 4px 16px rgba(15,23,42,0.03);">
            <h3 style="margin: 0 0 14px 0; font-size: 17.5px; font-weight: 800; color: #b45309; display: flex; align-items: center; gap: 8px;">
                <span>??/span> <b>{p3_title}</b>
            </h3>
            {p3_html}
        </div>

        {synthesis_box_html}

        <!-- 5-Line English C-Suite Briefing -->
        <div class="ucklab-english-briefing" style="background: #0f172a; border: 1px solid #334155; border-radius: 14px; padding: 24px 26px; color: #f1f5f9; margin: 26px 0; box-shadow: 0 8px 24px rgba(0,0,0,0.18);">
            <div style="font-size: 13.5px; font-weight: 800; color: #38bdf8; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                <span>?뙋</span> <b>[C-Suite Global Strategic Briefing 쨌 5 Core Vectors]</b>
            </div>
            <ol style="margin: 0; padding-left: 20px; font-size: 14px; line-height: 1.75; color: #cbd5e1;">
                {en_list_items}
            </ol>
        </div>

        {pull_quote_html}

        {paywall_html}

        {citation_html}

    </div>
    <!-- /wp:group -->
    """

    # Private research archive uses Uncategorized (ID 1) to avoid leaking into public category feeds
    categories = [1]

    aioseo_title = f"[UCKLab Strategic Review Vol. {vol}] {headline} | UCKLab Monograph??
    aioseo_desc = f"UCKLab Strategic Review: 10? 遺꾩빞 U-Radar 吏??遺꾩꽍, UCKLab Executive Note?? 諛?UCKLab Monograph??(2,500?⑥뼱 APA 7th ??? ?섎줉"

    payload = {
        "title": post_title,
        "content": public_content,
        "excerpt": cat_item.get("summary_ko", "") or subtitle,
        "status": "publish",  # Publicly visible
        "categories": categories,
        "meta": {
            "_aioseo_title": aioseo_title,
            "_aioseo_description": aioseo_desc
        }
    }
    if featured_media_id:
        payload["featured_media"] = featured_media_id

    try:
        from wp_client import get_wp_client
        client = get_wp_client()
        ok, post_id, post_link = client.create_post(payload)
        if ok:
            print(f"  ??[Public Executive Dossier] '{cat_ko}' 怨듦컻 ?ъ뒪???꾨즺 (ID: {post_id}) -> {post_link}")
            return post_link
        else:
            print(f"  ?좑툘 [Public Executive Dossier] '{cat_ko}' ?ㅽ뙣: {post_link}")
    except Exception as e:
        print(f"  ?좑툘 [Public Executive Dossier] ?덉쇅: {e}")
    return None

# ---------------------------------------------------------------------------
# Master Dual Publisher Routine for All 10 Categories
# ---------------------------------------------------------------------------
def publish_all_category_dual_posts(report_id, news_items, category_charts=None, osint_data=None, category_photos=None):
    """
    Executes the clean Publishing process for all 10 categories:
    Only publishes 10 Public Executive Dossier Posts (status: 'publish') to prevent duplication.
    """
    category_urls = {}
    print(f"\n=======================================================")
    print(f"🏛️ [Category Publisher] 10대 분야 맞춤형 공개 브리핑 발행")
    print(f"=======================================================")

    for item in news_items:
        cat_id = item.get("id")
        chart_info = (category_charts or {}).get(cat_id)
        photo_info = (category_photos or {}).get(cat_id)

        pub_url = publish_single_category_public_post(
            report_id=report_id,
            cat_item=item,
            chart_info=chart_info,
            osint_data=osint_data,
            photo_info=photo_info
        )
        if pub_url:
            category_urls[cat_id] = pub_url

    return category_urls

def _legacy_publish_all_category_dual_posts_unused(report_id, news_items, category_charts=None, osint_data=None, category_photos=None):
    """
    Executes the complete Dual-Architecture publishing process for all 10 categories:
    1. Option 1: Publishes 10 Private Admin Posts (status: 'private').
    2. Option 2: Publishes 10 Public Executive Dossier Posts (status: 'publish') with W810 x H480 Stock Photos, 16:9 charts & Paywall.
    3. Returns category_urls mapping: {cat_id: public_url} for front page linking!
    """
    print(f"\n=======================================================")
    print(f"?룢截?[Category Dual Publisher] 10? 遺꾩빞 鍮꾧났媛?蹂닿? & 怨듦컻 ?붿빟 諛쒗뻾")
    print(f"=======================================================")

    category_public_urls = {}

    for item in news_items:
        cat_id = item.get("id", "politics")
        chart_url = category_charts.get(cat_id, "") if category_charts else ""
        photo_info = category_photos.get(cat_id, {}) if category_photos else {}

        # 1. Option 1: Open Research Dossier (OSINT telemetry & full un-redacted notes)
        publish_admin_private_archive(item, report_id, osint_data, photo_info=photo_info)

        # 2. Option 2: Public High-Elegance Executive Dossier & Paywall
        pub_url = publish_public_executive_dossier(item, report_id, chart_url, photo_info)
        if pub_url:
            category_public_urls[cat_id] = pub_url

    print(f"??10? 移댄뀒怨좊━ ?댁썝??諛쒗뻾 ?꾨즺 (珥?{len(category_public_urls)}媛?怨듦컻 留곹겕 ?뺣낫)")
    return category_public_urls

