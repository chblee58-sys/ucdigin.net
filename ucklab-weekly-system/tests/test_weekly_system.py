"""
test_weekly_system.py - Comprehensive Unit & Integration Tests for UCKLab Weekly HBR System
Tests:
1. Collector OSINT indicators & 3-Stage Trend Radar (+zσ classification)
2. Graph Knowledge Mapping (Node resolution & Token optimization)
3. Dual-Agent Writer-Auditor Review Loop (Stewardship Theology >= 85/100)
4. Matplotlib 16:9 Data Chart generation
5. PPT 3-Revision Limit Governance (Requests 1, 2, 3 pass; Request 4 rejected)
6. 12-Hour HMAC Token generation & verification
7. SQLite WAL Database Archiving
8. Clean UX: Zero frontend admin buttons in paywall_modal.html
"""

import os
import sys
import json
import sqlite3
import pytest

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
DATA_DIR = os.path.join(BASE_DIR, "data")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from collector import (
    calculate_vocabulary_velocity,
    classify_trend_stage,
    WeeklyKnowledgeGraph,
    collect_weekly_osint_indicators
)
from column import (
    WeeklyWriterAgent,
    WeeklyAuditorAgent,
    generate_weekly_column
)
from chart_generator import generate_weekly_chart
from ppt_builder import (
    build_weekly_ppt_deck,
    process_ppt_request,
    MAX_PPT_REVISIONS
)
from pdf_builder import (
    generate_weekly_download_token,
    verify_weekly_download_token
)
from server import init_weekly_database, DB_PATH
from wp_publisher import archive_weekly_report_to_db

# ---------------------------------------------------------------------------
# Test 1: Collector & 3-Stage Trend Radar
# ---------------------------------------------------------------------------
def test_trend_radar_velocity_and_stages():
    """Verifies 3-stage velocity mathematical thresholds (+zσ)."""
    # Builder stage (< 1.5σ)
    vel_builder = calculate_vocabulary_velocity(freq_7d=35, baseline_30d=30, std_dev_30d=5.0)
    stage_b = classify_trend_stage(vel_builder)
    assert stage_b["stage_num"] == 1
    assert "Builders" in stage_b["stage"]

    # Community stage (1.5σ <= v < 3.5σ)
    vel_comm = calculate_vocabulary_velocity(freq_7d=45, baseline_30d=30, std_dev_30d=6.0)
    stage_c = classify_trend_stage(vel_comm)
    assert stage_c["stage_num"] == 2
    assert "Community" in stage_c["stage"]

    # Mainstream stage (>= 3.5σ)
    vel_main = calculate_vocabulary_velocity(freq_7d=65, baseline_30d=30, std_dev_30d=5.5)
    stage_m = classify_trend_stage(vel_main)
    assert stage_m["stage_num"] == 3
    assert "Mainstream" in stage_m["stage"]

def test_graph_knowledge_mapping():
    """Verifies token-reducing Graph Knowledge Mapping structure."""
    kg = WeeklyKnowledgeGraph()
    res = kg.resolve_context("collector")
    assert "node" in res
    assert "related_edges" in res
    assert "generator" in res["related_edges"]
    assert "chart" in res["related_edges"]

# ---------------------------------------------------------------------------
# Test 2: Dual-Agent Writer-Auditor Stewardship Evaluation
# ---------------------------------------------------------------------------
def test_writer_auditor_editorial_loop():
    """Verifies that '이창배 Note' column achieves >= 85/100 score."""
    writer = WeeklyWriterAgent()
    auditor = WeeklyAuditorAgent()
    
    osint = collect_weekly_osint_indicators()
    headlines = [{"headline": "G7 AI 규범 조약 합의", "category_ko": "정치"}]
    
    draft = writer.draft_column(headlines, osint)
    evaluation = auditor.audit(draft)
    
    assert evaluation["total_score"] >= 85, f"Score too low: {evaluation['total_score']}"
    assert evaluation["metrics"]["theological_tone"] == 25, "Must achieve full theological tone score"
    assert "청지기" in draft["content"]

# ---------------------------------------------------------------------------
# Test 3: 16:9 Matplotlib Data Chart Generation
# ---------------------------------------------------------------------------
def test_matplotlib_chart_generation():
    """Verifies 16:9 widescreen chart creation without CSS color bugs."""
    test_report_id = "TEST-CHART-2026"
    chart_path = generate_weekly_chart(report_id=test_report_id)
    assert os.path.exists(chart_path)
    assert os.path.getsize(chart_path) > 1000  # valid image file

def test_category_detail_charts_generation():
    """Verifies generation of 10 distinct category-specific data charts."""
    from chart_generator import generate_category_detail_charts, CATEGORY_METRICS
    test_report_id = "TEST-CAT-CHART-2026"
    detail_charts = generate_category_detail_charts(report_id=test_report_id)
    assert len(detail_charts) == 10
    for cat_id in CATEGORY_METRICS.keys():
        assert cat_id in detail_charts
        fpath = detail_charts[cat_id]
        assert os.path.exists(fpath)
        assert os.path.getsize(fpath) > 1000

# ---------------------------------------------------------------------------
# Test 4: PPT 3-Revision Limit Governance
# ---------------------------------------------------------------------------
def test_ppt_3_revision_limit_governance():
    """
    Verifies strict 3-revision limit governance:
    Requests 1, 2, 3 return updated PPT decks.
    Request 4 is rejected with polite governance notice.
    """
    test_order_id = "test_order_gov_001"
    user_email = "executive_subscriber@example.com"
    
    # Clean previous test entries if any
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM ppt_requests WHERE order_id = ?", (test_order_id,))
    conn.commit()
    conn.close()

    # Request 1
    res1 = process_ppt_request(test_order_id, user_email, "종합", "1차 슬라이드 수정")
    assert res1["success"] is True
    assert res1["revision_count"] == 1
    assert res1["remaining_revisions"] == 2

    # Request 2
    res2 = process_ppt_request(test_order_id, user_email, "종합", "2차 폰트 및 데이터 조정")
    assert res2["success"] is True
    assert res2["revision_count"] == 2
    assert res2["remaining_revisions"] == 1

    # Request 3
    res3 = process_ppt_request(test_order_id, user_email, "종합", "3차 최종 요약 다듬기")
    assert res3["success"] is True
    assert res3["revision_count"] == 3
    assert res3["remaining_revisions"] == 0

    # Request 4 -> Governance Limit Reached!
    res4 = process_ppt_request(test_order_id, user_email, "종합", "4차 추가 수정 요청")
    assert res4["success"] is False
    assert res4["governance_limit_reached"] is True
    assert "3회 수정 제공 한도를 모두 완료" in res4["message"]
    assert "새로운 주간 구독" in res4["message"]

# ---------------------------------------------------------------------------
# Test 5: 12-Hour HMAC Token Security
# ---------------------------------------------------------------------------
def test_hmac_12hr_token_generation_and_verification():
    """Verifies that 12-hour HMAC download tokens validate correctly."""
    order_id = "ord_test_999"
    email = "subscriber@example.com"
    scope = "comprehensive"

    token = generate_weekly_download_token(order_id, email, scope=scope)
    assert len(token) > 20

    # Valid token verification
    ok, data = verify_weekly_download_token(token, max_age_hours=12)
    assert ok is True
    assert data["order_id"] == order_id
    assert data["email"] == email
    assert data["scope"] == scope

    # Tampered token verification
    tampered_token = token[:-4] + "abcd"
    bad_ok, bad_data = verify_weekly_download_token(tampered_token)
    assert bad_ok is False

# ---------------------------------------------------------------------------
# Test 6: SQLite WAL Archiving
# ---------------------------------------------------------------------------
def test_sqlite_wal_archiving():
    """Verifies weekly report record archiving to SQLite in WAL mode."""
    init_weekly_database()
    
    test_id = "WEEKLY-2026-W38-TEST"
    ok = archive_weekly_report_to_db(
        report_id=test_id,
        title="테스트 주간 리포트",
        excerpt="테스트 요약",
        content="테스트 본문",
        aioseo_title="테스트 SEO 제목",
        aioseo_desc="테스트 SEO 설명"
    )
    assert ok is True

    # Check database query
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT title, aioseo_title FROM weekly_reports WHERE report_id = ?", (test_id,))
    row = cursor.fetchone()
    conn.close()
    
    assert row is not None
    assert row[0] == "테스트 주간 리포트"
    assert row[1] == "테스트 SEO 제목"

# ---------------------------------------------------------------------------
# Test 7: Clean Customer UX (Zero Admin Buttons)
# ---------------------------------------------------------------------------
def test_paywall_modal_zero_admin_buttons():
    """
    Verifies that the customer-facing paywall_modal.html contains
    ABSOLUTELY NO visible admin buttons or admin bypass containers,
    strictly satisfying Dr. Lee's clean customer UX requirement.
    """
    modal_path = os.path.join(TEMPLATES_DIR, "paywall_modal.html")
    assert os.path.exists(modal_path)
    
    with open(modal_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Must NOT have public admin buttons
    assert "👑 최고관리자" not in content
    assert "0원 프리패스" not in content
    assert "Dr.LEE 최고관리자 전용" not in content
    assert "bypass_admin_btn" not in content
    
    # Must have 11-scope select options and 9,900 KRW pricing
    assert "9,900원" in content
    assert "comprehensive" in content
    assert "politics" in content
    assert "christianity" in content

# ---------------------------------------------------------------------------
# Test 8: Custom CSS, Card News & Subscription Components
# ---------------------------------------------------------------------------
def test_hbr_custom_css_and_components():
    """Verifies that custom CSS and HTML components are properly created and embedded."""
    from wp_publisher import (
        CSS_PATH,
        load_hbr_custom_css,
        load_subscription_widget,
        load_cardnews_component,
        build_hbr_excerpt_content,
        build_full_hbr_report_content
    )

    # 1. CSS file validation
    assert os.path.exists(CSS_PATH)
    css_content = load_hbr_custom_css()
    assert ".ucklab-hbr-badge" in css_content
    assert ".ucklab-executive-summary" in css_content
    assert ".ucklab-paywall-modal" in css_content
    assert ".ucklab-subscription-card" in css_content
    assert ".ucklab-cardnews-grid" in css_content

    # 2. Subscription widget validation
    sub_html = load_subscription_widget()
    assert "ucklab-subscription-card" in sub_html
    assert "api/v1/subscribe" in sub_html

    # 3. Card news validation
    col_mock = {"three_line_summary": ["청지기적 책임으로 기술을 다스려야 합니다."]}
    news_mock = [{"headline": "글로벌 AGI 규범 협약", "summary_ko": "요약", "category_ko": "정치"}]
    osint_mock = {"country_instability_index": {"East_Asia_KR_TW": 4.65}, "infrastructure_finance_radar": {"compute_grid_stress_pct": 78.5}}
    card_html = load_cardnews_component("TEST-W38", col_mock, news_mock, osint_mock, "https://ucdigin.net/test.png")
    assert "CARD 01 // OVERVIEW" in card_html
    assert "CARD 02 // RADAR" in card_html
    assert "CARD 03 // 이창배 NOTE" in card_html
    assert "CARD 04 // EXECUTIVE REPORT" in card_html

    # 4. Excerpt formatting with CSS classes
    excerpt_html = build_hbr_excerpt_content("TEST-W38", col_mock, news_mock, osint_mock, "https://ucdigin.net/test.png")
    assert "ucklab-executive-summary" in excerpt_html
    assert "ucklab-hbr-badge" in excerpt_html
    assert "ucklab-key-takeaway" in excerpt_html
    assert "ucklab-hbr-custom-css" in excerpt_html

    # 5. Full Content formatting with CSS and embedded widgets
    full_html = build_full_hbr_report_content("TEST-W38", col_mock, news_mock, osint_mock, "https://ucdigin.net/test.png")
    assert "ucklab-hbr-badge" in full_html
    assert "ucklab-post-title" in full_html
    assert "ucklab-subscription-card" in full_html
    assert "ucklab-cardnews-grid" in full_html

# ---------------------------------------------------------------------------
# Test 9: Newsletter Subscription API Endpoint
# ---------------------------------------------------------------------------
def test_newsletter_subscription_endpoint():
    """Verifies that /api/v1/subscribe saves subscriber to SQLite WAL database."""
    from server import app, DB_PATH
    from fastapi.testclient import TestClient

    client = TestClient(app)
    test_email = "newsletter_test_user@example.com"
    res = client.post("/api/v1/subscribe", json={
        "name": "홍길동",
        "email": test_email,
        "category": "politics"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True

    # Verify SQLite WAL DB insertion
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, email, category FROM subscribers WHERE email = ?", (test_email,))
    row = cursor.fetchone()
    conn.close()

    assert row is not None
    assert row[0] == "홍길동"
    assert row[1] == test_email
    assert row[2] == "politics"

# ---------------------------------------------------------------------------
# Test 10: Facebook Weekly HBR Card-News Hook Publisher
# ---------------------------------------------------------------------------
def test_facebook_weekly_hbr_publisher():
    """Verifies publish_weekly_hbr_to_facebook formatting, mock 200, mock failure, and simulation."""
    from unittest.mock import patch, MagicMock
    import facebook_publisher
    from facebook_publisher import publish_weekly_hbr_to_facebook

    sample_report = {
        "vol": "38",
        "title": "[UCKLab 주간 HBR] 2026 AGI 문명 전환기 글로벌 10대 아젠다 & 이창배 Note",
        "key_takeaway": "AGI 문명 전환기 국가불안정지수(CII) 및 그리드 부하율 추적",
        "post_url": "https://ucdigin.net/test-post-hbr/"
    }

    # 1. Simulation mode (when token is empty)
    with patch.object(facebook_publisher, "FB_ACCESS_TOKEN", ""):
        res_sim = publish_weekly_hbr_to_facebook(sample_report)
        assert res_sim["success"] is True
        assert res_sim.get("simulated") is True
        assert "sim_fb_" in res_sim["post_id"]

    # 2. Mock Facebook Graph API 200 Success
    with patch.object(facebook_publisher, "FB_ACCESS_TOKEN", "mock_fb_token_12345"):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"id": "2024276951100901_9988776655"}

        with patch("requests.post", return_value=mock_resp) as mock_post:
            res_live = publish_weekly_hbr_to_facebook(sample_report)
            assert res_live["success"] is True
            assert res_live["post_id"] == "2024276951100901_9988776655"
            mock_post.assert_called_once()
            call_kwargs = mock_post.call_args[1]
            assert "2024276951100901" in mock_post.call_args[0][0]
            assert "이창배 박사 Note" in call_kwargs["data"]["message"]
            assert call_kwargs["data"]["link"] == "https://ucdigin.net/test-post-hbr/"
            assert call_kwargs["data"]["access_token"] == "mock_fb_token_12345"

    # 3. Mock Facebook Graph API 400 Failure
    with patch.object(facebook_publisher, "FB_ACCESS_TOKEN", "mock_fb_token_invalid"):
        mock_fail_resp = MagicMock()
        mock_fail_resp.status_code = 400
        mock_fail_resp.text = '{"error": {"message": "Invalid OAuth access token"}}'

        with patch("requests.post", return_value=mock_fail_resp):
            res_fail = publish_weekly_hbr_to_facebook(sample_report)
            assert res_fail["success"] is False
            assert "Invalid OAuth" in res_fail["error"]

    # 4. Mock Network Exception
    with patch.object(facebook_publisher, "FB_ACCESS_TOKEN", "mock_fb_token_valid"):
        with patch("requests.post", side_effect=Exception("Connection timed out")):
            res_err = publish_weekly_hbr_to_facebook(sample_report)
            assert res_err["success"] is False
            assert "Connection timed out" in res_err["error"]


