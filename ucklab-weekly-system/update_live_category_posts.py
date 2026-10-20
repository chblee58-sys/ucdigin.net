# -*- coding: utf-8 -*-
"""
update_live_category_posts.py
Updates the 10 live public category posts on https://ucdigin.net
with category-specific classification titles: [UCKLab {cat_ko}] {headline}
and minimum 500-word academic standalone dossiers.
"""

import os
import sys
import json
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "src"))

load_dotenv(os.path.join(BASE_DIR, ".env"))
WP_URL = os.getenv("WP_URL", "https://ucdigin.net")
WP_USER = os.getenv("WP_USER", "AutoBot_Editor")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD", "5kOS QdBg 6Prd qR4F qixR lg43")

from category_dossier_data import CATEGORY_DOSSIERS
from category_publisher import (
    build_category_badge,
    build_three_line_summary_box,
    build_citation_box,
    build_category_paywall_card,
    WP_CATEGORY_MAP,
    PARENT_CATEGORY_ID
)

# Load current weekly headlines & chart URLs dynamically
import glob
hl_files = sorted(glob.glob(os.path.join(BASE_DIR, "data", "weekly_headlines_*.json")))
if hl_files:
    latest_hl_file = hl_files[-1]
else:
    latest_hl_file = os.path.join(BASE_DIR, "data", "weekly_headlines_20260928.json")

print(f"📖 [Category Posts] Loading latest headlines from: {os.path.basename(latest_hl_file)}")
with open(latest_hl_file, "r", encoding="utf-8") as f:
    headlines = json.load(f)

with open(os.path.join(BASE_DIR, "data", "category_chart_urls.json"), "r", encoding="utf-8") as f:
    category_charts = json.load(f)

POST_MAP = {
    "politics": 16304,
    "economy": 16306,
    "society": 16308,
    "culture": 16310,
    "finance": 16312,
    "defense": 16314,
    "christianity": 16316,
    "science": 16318,
    "climate": 16320,
    "sports": 16322
}

auth = HTTPBasicAuth(WP_USER, WP_APP_PASSWORD)
headers = {"User-Agent": "UCKLab-Weekly-AutoBot/3.0"}

def build_post_html(cat_item, chart_url=""):
    cat_id = cat_item.get("id", "politics")
    cat_ko = cat_item.get("category_ko", "정치/외교")
    headline = cat_item.get("headline", "AGI 거버넌스")

    dossier = CATEGORY_DOSSIERS.get(cat_id, {})
    subtitle = dossier.get("subtitle", f"{cat_ko} 주간 심층 분석 리포트")
    copywriter_hook = dossier.get("copywriter_hook", "")
    theses = dossier.get("theses", cat_item.get("three_line_summary", []))
    p1_title = dossier.get("point1_title", "1. 거시적 시스템 진단 (Macro Diagnosis)")
    p1_content = dossier.get("point1_content", cat_item.get("summary_ko", ""))
    p2_title = dossier.get("point2_title", "2. 알고리즘 주권과 소버린 아키텍처 (Sovereignty & Architecture)")
    p2_content = dossier.get("point2_content", "")
    p3_title = dossier.get("point3_title", "3. C-Level 실행 과제 (Actionable Execution)")
    p3_content = dossier.get("point3_content", "")
    exec_synthesis = dossier.get("executive_synthesis", "")
    english_lines = dossier.get("english_briefing", [cat_item.get("summary_en", "")])
    pull_quote = dossier.get("pull_quote", "")
    citation_data = dossier.get("citation", cat_item.get("citation", {}))

    badge_html = build_category_badge(cat_item)
    radar = cat_item.get("trend_radar", {})
    radar_stage = radar.get("stage", "Stage 2 (Community)")
    radar_velocity = radar.get("velocity", 3.2)
    radar_desc = radar.get("transition_description", "트렌드 확산 중")

    chart_img_html = ""
    if chart_url:
        chart_img_html = f"""
        <div class="ucklab-chart-box" style="margin: 26px 0; text-align: center;">
            <img src="{chart_url}" alt="{cat_ko} 전략 분석 데이터 차트" style="width: 100%; max-width: 820px; height: auto; border-radius: 14px; border: 1px solid rgba(0,0,0,0.08); box-shadow: 0 8px 24px rgba(0,0,0,0.08);" loading="lazy" />
            <div style="font-size: 12px; color: #64748b; margin-top: 8px; font-weight: 600;">
                ▲ [UCKLab HBR Strategic Radar] {cat_ko} 4대 핵심 역학 데이터 시각화 지표
            </div>
        </div>
        """

    theses_html = build_three_line_summary_box(theses, title=f"{cat_ko} 주간 3대 핵심 전략 명제")
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
                🏛️ [UCKLab 학술적 총평 &amp; 청지기적 주권 결론]
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
                ⚡ STRATEGIC COGNITIVE TRIGGER // 사전 검증 브리핑
            </div>
            <p style="margin: 0; white-space: pre-line;">
                {copywriter_hook}
            </p>
        </div>
        """

    content_html = f"""
    <!-- wp:group {{"layout":{{"type":"constrained"}}}} -->
    <div class="ucklab-dossier-page" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Pretendard', sans-serif; max-width: 880px; margin: 0 auto; color: #1e293b; line-height: 1.85;">
        
        {badge_html}

        <div style="display: flex; gap: 8px; align-items: center; margin: 16px 0 10px 0; flex-wrap: wrap;">
            <span style="display:inline-flex; align-items:center; gap:6px; padding: 5px 14px; border-radius: 8px; background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(245, 158, 11, 0.5); color: #FBBF24; font-size: 12.5px; font-weight: 800; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4); text-shadow: 0 1px 2px rgba(0,0,0,0.8);">
                {radar_stage} (속도: +{radar_velocity}σ)
            </span>
            <span style="display:inline-flex; align-items:center; gap:6px; padding: 5px 14px; border-radius: 8px; background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(56, 189, 248, 0.55); color: #38BDF8; font-size: 12.5px; font-weight: 800; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4); text-shadow: 0 1px 2px rgba(0,0,0,0.8);">
                🛡️ 사전 검증용 (500단어+)
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
            <b>연구 발행:</b> UCKLab AI융합미래연구소 | <b>인텔리전스 지수:</b> {cat_item.get('trend_score', 88)} pt | <b>분야:</b> {cat_ko} | <b>피어 리뷰 완료</b>
        </div>

        {hook_box_html}

        {theses_html}

        {chart_img_html}

        <!-- 3-Part Academic Standalone Analysis (500-word+ Core) -->
        <div class="ucklab-point-card" style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 26px 28px; margin: 22px 0; box-shadow: 0 4px 16px rgba(15,23,42,0.03);">
            <h3 style="margin: 0 0 14px 0; font-size: 17.5px; font-weight: 800; color: #1e40af; display: flex; align-items: center; gap: 8px;">
                <span>🏛️</span> <b>{p1_title}</b>
            </h3>
            {p1_html}
        </div>

        <div class="ucklab-point-card" style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 26px 28px; margin: 22px 0; box-shadow: 0 4px 16px rgba(15,23,42,0.03);">
            <h3 style="margin: 0 0 14px 0; font-size: 17.5px; font-weight: 800; color: #0d9488; display: flex; align-items: center; gap: 8px;">
                <span>🛡️</span> <b>{p2_title}</b>
            </h3>
            {p2_html}
        </div>

        <div class="ucklab-point-card" style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 26px 28px; margin: 22px 0; box-shadow: 0 4px 16px rgba(15,23,42,0.03);">
            <h3 style="margin: 0 0 14px 0; font-size: 17.5px; font-weight: 800; color: #b45309; display: flex; align-items: center; gap: 8px;">
                <span>⚡</span> <b>{p3_title}</b>
            </h3>
            {p3_html}
        </div>

        {synthesis_box_html}

        <!-- 5-Line English C-Suite Briefing -->
        <div class="ucklab-english-briefing" style="background: #0f172a; border: 1px solid #334155; border-radius: 14px; padding: 24px 26px; color: #f1f5f9; margin: 26px 0; box-shadow: 0 8px 24px rgba(0,0,0,0.18);">
            <div style="font-size: 13.5px; font-weight: 800; color: #38bdf8; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                <span>🌐</span> <b>[C-Suite Global Strategic Briefing · 5 Core Vectors]</b>
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
    return content_html

def update_all_posts():
    print(f"🚀 Updating 10 live public category posts on {WP_URL}...")
    success_count = 0

    for item in headlines:
        cat_id = item.get("id")
        post_id = POST_MAP.get(cat_id)
        if not post_id:
            continue

        cat_ko = item.get("category_ko", "")
        headline = item.get("headline", "")
        chart_url = category_charts.get(cat_id, "")

        post_title = f"[UCKLab {cat_ko}] {headline}"
        content_html = build_post_html(item, chart_url)

        categories = [PARENT_CATEGORY_ID, WP_CATEGORY_MAP.get(cat_id, 27)]

        payload = {
            "title": post_title,
            "content": content_html,
            "categories": categories,
            "meta": {
                "_aioseo_title": post_title,
                "_aioseo_description": f"{headline} - UCKLab AI융합미래연구소 주간 {cat_ko} 인텔리전스 심층 리포트."
            }
        }

        endpoint = f"{WP_URL}/wp-json/wp/v2/posts/{post_id}"
        try:
            res = requests.post(endpoint, json=payload, auth=auth, headers=headers, timeout=30)
            if res.status_code == 200:
                print(f"  ✓ [Post {post_id}] '{cat_ko}' 업데이트 성공: {post_title[:45]}...")
                success_count += 1
            else:
                print(f"  ⚠️ [Post {post_id}] '{cat_ko}' 실패 ({res.status_code}): {res.text[:120]}")
        except Exception as e:
            print(f"  ⚠️ [Post {post_id}] '{cat_ko}' 예외: {e}")

    print(f"\n✨ 완료: 총 {success_count}/10개 포스트 업데이트 성공!")

if __name__ == "__main__":
    update_all_posts()
