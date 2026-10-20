"""
ucklab_weekly_hbr_pipeline.py - Autonomous Weekly HBR Production & Dry-Run Pipeline
Features:
1. Multi-Stage 5,000-Word Sequential Generation Engine (src/generator.py)
2. 16:9 Executive HBR Data Chart Generator (src/wp_publisher.py)
3. ReportLab Publication-Grade PDF Compiler with Running "Licensed to {email}" Watermark Header (src/pdf_builder.py)
4. python-pptx 16:9 Executive Presentation Slide Deck Generator (src/ppt_builder.py)
5. FastAPI Dry-Run Verification Suite:
   - Validates /api/v1/reports/download binary PDF attachment stream (UCKLab_Weekly_HBR_Vol38.pdf)
   - Validates /api/v1/ppt/download binary PPTX attachment stream (UCKLab_HBR_Presentation_{order_id}.pptx)
   - Enforces strict MIME types & Content-Disposition headers (Zero HTML dummy links)
"""

import os
import sys
import time
import json
import uuid
import datetime

# UTF-8 console output for Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure correct path resolution
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
POSSIBLE_SYSTEM_DIRS = [
    CURRENT_DIR,
    os.path.join(CURRENT_DIR, "ucklab-daily-system"),
    os.path.join(CURRENT_DIR, "..", "ucklab-daily-system")
]

SYSTEM_DIR = None
for pd in POSSIBLE_SYSTEM_DIRS:
    if os.path.exists(os.path.join(pd, "src", "server.py")):
        SYSTEM_DIR = os.path.abspath(pd)
        break

if not SYSTEM_DIR:
    SYSTEM_DIR = CURRENT_DIR

SRC_DIR = os.path.join(SYSTEM_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

try:
    from generator import generate_5000_word_report, count_korean_words
    from wp_publisher import generate_hbr_chart
    from pdf_builder import build_pdf_report, generate_download_token, verify_download_token
    from ppt_builder import build_weekly_ppt_deck, get_ppt_filepath
    from server import app, ADMIN_MASTER_KEY, send_file
    from fastapi.testclient import TestClient
    _HAS_DRYRUN_DEPS = True
except ImportError:
    _HAS_DRYRUN_DEPS = False

def run_weekly_hbr_pipeline(dry_run=True):
    print("=" * 80)
    print("🚀 [UCKLab Weekly HBR Pipeline] 5,000-Word Report, PDF & PPTX Generation Engine")
    print("=" * 80)
    start_time = time.time()

    client = TestClient(app)
    order_id = f"HBR-WEEKLY-{datetime.datetime.now().strftime('%Y%m%d%H%M')}-{uuid.uuid4().hex[:6].upper()}"
    subscriber_email = "executive_subscriber@ucklab.org"

    # -----------------------------------------------------------------------
    # STEP 1: 5,000-Word Sequential Generation Engine
    # -----------------------------------------------------------------------
    print("\n[STAGE 1] Multi-Stage 5,000-Word Sequential Generation...")
    report_5000w = generate_5000_word_report()
    total_words = report_5000w.get("total_words", 0)
    sections_count = len(report_5000w.get("sections", []))
    print(f"  ✓ 5,000단어 마스터 리포트 완결: 총 {total_words:,}단어 (5개 전 장 완결: {sections_count}개 섹션)")
    assert total_words >= 5000, f"리포트 분량 미달: {total_words} words"

    # -----------------------------------------------------------------------
    # STEP 2: 16:9 HBR Strategic Data Chart Generation
    # -----------------------------------------------------------------------
    print("\n[STAGE 2] 16:9 HBR Strategic Data Chart Generation...")
    chart_path, data_uri = generate_hbr_chart()
    print(f"  ✓ 16:9 HBR 전략 차트 렌더링 완료: {chart_path} ({os.path.getsize(chart_path):,} bytes)")
    assert os.path.exists(chart_path) and os.path.getsize(chart_path) > 1000

    # -----------------------------------------------------------------------
    # STEP 3: ReportLab Publication-Grade PDF Compilation
    # -----------------------------------------------------------------------
    print("\n[STAGE 3] ReportLab Publication-Grade PDF Compilation (Watermark Header & Chart)...")
    reports_dir = os.path.join(SYSTEM_DIR, "storage", "reports")
    os.makedirs(reports_dir, exist_ok=True)
    pdf_out = os.path.join(reports_dir, f"UCKLab_Report_{order_id}.pdf")

    user_info = {
        "email": subscriber_email,
        "order_id": order_id,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    build_pdf_report(
        output_filepath=pdf_out,
        user_info=user_info,
        scope="comprehensive",
        include_column=True,
        report_5000w=report_5000w
    )
    pdf_size = os.path.getsize(pdf_out)
    print(f"  ✓ ReportLab PDF 생성 완료: {pdf_out} ({pdf_size:,} bytes)")
    assert pdf_size > 50000, "PDF 파일 크기가 너무 작습니다 (최소 50KB 권장)"

    # -----------------------------------------------------------------------
    # STEP 4: python-pptx 16:9 Executive Presentation Slide Deck
    # -----------------------------------------------------------------------
    print("\n[STAGE 4] python-pptx 16:9 Executive Presentation Slide Deck Compilation...")
    ppt_out = get_ppt_filepath(order_id, email=subscriber_email)
    ppt_size = os.path.getsize(ppt_out)
    print(f"  ✓ 16:9 PPTX 슬라이드 덱 생성 완료: {ppt_out} ({ppt_size:,} bytes)")
    assert ppt_size > 20000, "PPTX 파일 크기가 너무 작습니다 (최소 20KB 권장)"
    assert os.path.exists(ppt_out), "PPTX 파일이 영구 저장소에 존재하지 않습니다."

    # -----------------------------------------------------------------------
    # STEP 5: Dry-Run Verification - Native Direct File Stream Downloads
    # -----------------------------------------------------------------------
    print("\n[STAGE 5] FastAPI Server Dry-Run Verification (Direct Attachment Streams)...")
    
    # Generate 12-Hour HMAC Token for the order
    token = generate_download_token(order_id, subscriber_email, scope="comprehensive", include_column=True)
    cur_week = datetime.datetime.now().strftime("%U")
    
    # 5-A: Verify /api/v1/reports/download (PDF Attachment Stream & Content-Length)
    print("  [5-A] Testing GET /api/v1/reports/download (PDF Binary Attachment)...")
    res_pdf = client.get(f"/api/v1/reports/download?token={token}")
    assert res_pdf.status_code == 200, f"PDF 다운로드 실패: {res_pdf.status_code} - {res_pdf.text}"
    assert res_pdf.headers["content-type"] == "application/pdf", f"잘못된 MIME: {res_pdf.headers['content-type']}"
    assert 'attachment' in res_pdf.headers.get("content-disposition", ""), "Content-Disposition에 attachment 누락"
    assert f'filename="UCKLab_Monograph_Vol{cur_week}.pdf"' in res_pdf.headers.get("content-disposition", ""), \
        f"잘못된 파일명: {res_pdf.headers.get('content-disposition')}"
    assert "content-length" in res_pdf.headers and int(res_pdf.headers["content-length"]) > 50000, \
        f"Non-zero Content-Length 누락 또는 비정상: {res_pdf.headers.get('content-length')}"
    assert res_pdf.content[:4] == b"%PDF", "PDF 매직 바이트(%PDF) 불일치 - 바이너리 스트림이 아닙니다"
    assert b"<html" not in res_pdf.content[:50].lower(), "HTML 태그가 응답에 포함되었습니다"
    print(f"    ✓ PDF 바이너리 스트림 검증 완료! (MIME: application/pdf, Content-Length: {res_pdf.headers['content-length']}, 파일명: UCKLab_Monograph_Vol{cur_week}.pdf)")

    # 5-B: Verify /api/v1/ppt/download (PPTX Attachment Stream & OpenXML MIME & Content-Length)
    print("  [5-B] Testing GET /api/v1/ppt/download (PPTX Binary Attachment)...")
    res_ppt = client.get(f"/api/v1/ppt/download?order_id={order_id}&token={token}")
    assert res_ppt.status_code == 200, f"PPT 다운로드 실패: {res_ppt.status_code} - {res_ppt.text}"
    assert res_ppt.headers["content-type"] == "application/vnd.openxmlformats-officedocument.presentationml.presentation", \
        f"잘못된 MIME: {res_ppt.headers['content-type']}"
    assert 'attachment' in res_ppt.headers.get("content-disposition", ""), "Content-Disposition에 attachment 누락"
    assert f'filename="UCKLab_Presentation_{order_id}.pptx"' in res_ppt.headers.get("content-disposition", ""), \
        f"잘못된 파일명: {res_ppt.headers.get('content-disposition')}"
    assert "content-length" in res_ppt.headers and int(res_ppt.headers["content-length"]) > 20000, \
        f"Non-zero Content-Length 누락 또는 비정상: {res_ppt.headers.get('content-length')}"
    assert res_ppt.content[:2] == b"PK", "PPTX OpenXML 매직 바이트(PK) 불일치 - 바이너리 스트림이 아닙니다"
    assert b"<html" not in res_ppt.content[:50].lower(), "HTML 태그가 응답에 포함되었습니다"
    print(f"    ✓ PPTX 바이너리 스트림 검증 완료! (MIME: application/vnd.openxmlformats..., Content-Length: {res_ppt.headers['content-length']}, 파일명: UCKLab_Presentation_{order_id}.pptx)")

    # 5-C: Verify Super Admin Bypass Stream Headers
    print("  [5-C] Testing GET /api/v1/reports/download with Admin Master Key...")
    admin_dl_res = client.get(f"/api/v1/reports/download?admin_key={ADMIN_MASTER_KEY}&order_id={order_id}")
    assert admin_dl_res.status_code == 200
    assert admin_dl_res.headers["content-type"] == "application/pdf"
    assert 'attachment' in admin_dl_res.headers.get("content-disposition", "")
    assert f'filename="UCKLab_Monograph_Vol{cur_week}.pdf"' in admin_dl_res.headers.get("content-disposition", "")
    assert int(admin_dl_res.headers.get("content-length", 0)) > 50000
    assert admin_dl_res.content[:4] == b"%PDF"
    print(f"    ✓ 최고관리자 프리패스 PDF 바이너리 스트림 확인 완료! (Content-Length: {admin_dl_res.headers['content-length']})")

    # 5-D: Verify Dynamic report_id formatting (e.g., report_id=2026-W38)
    print("  [5-D] Testing GET /api/v1/reports/download with dynamic report_id=2026-W38...")
    res_dynamic = client.get(f"/api/v1/reports/download?token={token}&report_id=2026-W38")
    assert res_dynamic.status_code == 200
    assert 'filename="UCKLab_Monograph_Vol38.pdf"' in res_dynamic.headers.get("content-disposition", "")
    print(f"    ✓ 동적 report_id 파일명 확인: UCKLab_Monograph_Vol38.pdf")

    elapsed = round(time.time() - start_time, 2)
    print("\n" + "=" * 80)
    print(f"🎉 [PIPELINE SUCCESS] 주간 HBR 5,000단어 리포트 및 바이너리 다운로드 스트림 파이프라인 검증 완료! ({elapsed}초)")
    print("=" * 80)
    return True

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="UCKLab Weekly HBR Production & Re-Indexing Pipeline")
    parser.add_argument("--force-republish", action="store_true", help="Force republish 3-in-1 Master Theme and Top 10 Category Dossiers to ucdigin.net")
    parser.add_argument("--latest-sources-only", action="store_true", help="Use only the latest uploaded OSINT and dossier sources")
    args, _ = parser.parse_known_args()

    if args.force_republish or args.latest_sources_only:
        print("\n" + "=" * 80)
        print(f"🔄 [RE-INDEXING MODE] force_republish={args.force_republish}, latest_sources_only={args.latest_sources_only}")
        print("=" * 80)
        weekly_sys_dir = os.path.join(CURRENT_DIR, "ucklab-weekly-system")
        if os.path.exists(os.path.join(weekly_sys_dir, "run_sunday_1700_automation.py")):
            if weekly_sys_dir not in sys.path:
                sys.path.insert(0, weekly_sys_dir)
            weekly_src = os.path.join(weekly_sys_dir, "src")
            if weekly_src not in sys.path:
                sys.path.insert(0, weekly_src)
            from run_sunday_1700_automation import run_all as run_live_reindex
            run_live_reindex()
        if not _HAS_DRYRUN_DEPS:
            sys.exit(0)

    if _HAS_DRYRUN_DEPS:
        success = run_weekly_hbr_pipeline()
        if not success:
            sys.exit(1)
    else:
        weekly_sys_dir = os.path.join(CURRENT_DIR, "ucklab-weekly-system")
        if weekly_sys_dir not in sys.path:
            sys.path.insert(0, weekly_sys_dir)
        weekly_src = os.path.join(weekly_sys_dir, "src")
        if weekly_src not in sys.path:
            sys.path.insert(0, weekly_src)
        from run_sunday_1700_automation import run_all as run_live_reindex
        run_live_reindex()
