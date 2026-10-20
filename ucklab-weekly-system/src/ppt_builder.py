"""
ppt_builder.py - UCKLab Weekly HBR Custom PPT Generator & 3-Revision Limit Governance
Features:
1. Generates publication-grade 16:9 executive presentation slide decks (python-pptx).
2. Adheres to dark-mode executive styling (#0f172a background, #f59e0b accents, clean typography).
3. Strictly enforces 3-Revision Limit Governance (max 3 revisions per order) in SQLite WAL DB.
"""

import os
import sys
import json
import sqlite3
import datetime
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# Windows console UTF-8 setup
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PPT_DIR = os.path.join(BASE_DIR, "storage", "ppt")
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "ucklab_weekly_archive.db")
os.makedirs(PPT_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# Color Constants
MAX_PPT_REVISIONS = 3
DARK_BG = RGBColor(15, 23, 42)       # #0f172a
CARD_BG = RGBColor(30, 41, 59)       # #1e293b
GOLD_TEXT = RGBColor(245, 158, 11)   # #f59e0b
BLUE_TEXT = RGBColor(56, 189, 248)   # #38bdf8
WHITE_TEXT = RGBColor(248, 250, 252) # #f8fafc
MUTED_TEXT = RGBColor(148, 163, 184) # #94a3b8

def apply_slide_background(slide):
    """Sets a solid dark executive background (#0f172a) on the slide."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = DARK_BG

def build_weekly_ppt_deck(output_filepath, report_data, user_email="guest@ucklab.org", revision_num=1):
    """
    Builds a 16:9 6-slide executive PPT deck for Dr. Lee & executive subscribers.
    """
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    title = report_data.get("title", "[주간 HBR 리포트] AGI 문명 전환기와 글로벌 거버넌스")
    today_str = datetime.datetime.now().strftime("%Y년 %m월 %d일")

    # ==========================================
    # Slide 1: Title & Executive Masthead
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_slide_background(s1)

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(4.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "UCKLab AI융합미래연구소 · 주간 HBR 인텔리전스"
    p0.font.size = Pt(16)
    p0.font.bold = True
    p0.font.color.rgb = GOLD_TEXT

    p1 = tf1.add_paragraph()
    p1.text = title
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = WHITE_TEXT
    p1.space_before = Pt(16)

    p2 = tf1.add_paragraph()
    p2.text = f"발행인: Dr. Chang-bae Lee (이창배 박사) | 일시: {today_str} | 맞춤 덱 v{revision_num}"
    p2.font.size = Pt(14)
    p2.font.color.rgb = MUTED_TEXT
    p2.space_before = Pt(20)

    # Watermark Notice
    p3 = tf1.add_paragraph()
    p3.text = f"🔒 정식 라이선스 발급 계정: {user_email} (최대 3회 수정 거버넌스)"
    p3.font.size = Pt(12)
    p3.font.color.rgb = BLUE_TEXT
    p3.space_before = Pt(10)

    # ==========================================
    # Slide 2: Executive Summary (Core Theses)
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_slide_background(s2)

    tb2_t = s2.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.3), Inches(0.8))
    p2_t = tb2_t.text_frame.paragraphs[0]
    p2_t.text = "1. 주간 핵심 요약 및 3대 명제 (Executive Summary)"
    p2_t.font.size = Pt(24)
    p2_t.font.bold = True
    p2_t.font.color.rgb = GOLD_TEXT

    tb2_b = s2.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(5.0))
    tf2_b = tb2_b.text_frame
    tf2_b.word_wrap = True

    theses = [
        ("문명적 진단", "기술 가속도와 글로벌 지정학적 불안정이 결합하는 문명사적 대전환기 속에서 기술 만능주의와 디스토피아적 허무주의를 동시에 경계해야 합니다."),
        ("청지기적 원칙", "인공지능은 숭배의 대상이 아닌 하나님께서 인간에게 위임하신 거룩한 관리의 도구이며, 그 지향점은 오직 인간 존엄성과 공공선에 있어야 합니다."),
        ("실천적 제언", "기술 패권의 독점적 집중을 방지하고 알고리즘 거버넌스의 도덕적 주권을 확립하여 약자와 공동체의 번영을 섬기는 정론의 길을 열어야 합니다.")
    ]
    for idx, (label, desc) in enumerate(theses):
        p = tf2_b.paragraphs[0] if idx == 0 else tf2_b.add_paragraph()
        p.text = f"• [{label}] {desc}"
        p.font.size = Pt(15)
        p.font.color.rgb = WHITE_TEXT
        p.space_before = Pt(16)

    # ==========================================
    # Slide 3: 10 Categories Strategic Overview
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_slide_background(s3)

    tb3_t = s3.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.3), Inches(0.8))
    p3_t = tb3_t.text_frame.paragraphs[0]
    p3_t.text = "2. 글로벌 10대 도메인 주간 트렌드 매트릭스"
    p3_t.font.size = Pt(24)
    p3_t.font.bold = True
    p3_t.font.color.rgb = GOLD_TEXT

    tb3_b = s3.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(5.0))
    tf3_b = tb3_b.text_frame
    tf3_b.word_wrap = True

    cat_points = [
        "🏛️ 정치/외교: G7 AGI 자율 안전 협약 체결 및 다자간 규범 집행력 가속",
        "📈 경제/공급망: 반도체 리쇼어링과 글로벌 거시 인플레이션 방어 체계",
        "👥 사회/AI윤리: 생성형 AI 저작권 및 인간 노동 소외 방지 심포지엄",
        "💳 금융/핀테크: 중앙은행 CBDC 상용화 추진과 디지털 자산 유동성 재편",
        "🛡️ 국방/안보: 동맹 자율 방위 체계 및 극초음속·전자전 억제 전략",
        "✝️ 기독교/영성: 포스트휴머니즘 시대의 목회 윤리와 청지기적 소명 실천",
        "🔬 과학/기술/AGI: 차세대 파운데이션 모델 및 퀀텀 뉴로모픽 칩 혁신"
    ]
    for idx, cp in enumerate(cat_points):
        p = tf3_b.paragraphs[0] if idx == 0 else tf3_b.add_paragraph()
        p.text = cp
        p.font.size = Pt(14)
        p.font.color.rgb = WHITE_TEXT
        p.space_before = Pt(10)

    # ==========================================
    # Slide 4: '이창배 Note' Theological Governance
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_slide_background(s4)

    tb4_t = s4.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.3), Inches(0.8))
    p4_t = tb4_t.text_frame.paragraphs[0]
    p4_t.text = "3. 특별 권두 정론 칼럼: '이창배 Note'"
    p4_t.font.size = Pt(24)
    p4_t.font.bold = True
    p4_t.font.color.rgb = GOLD_TEXT

    tb4_b = s4.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(5.0))
    tf4_b = tb4_b.text_frame
    tf4_b.word_wrap = True

    p4_1 = tf4_b.paragraphs[0]
    p4_1.text = "기술의 가속도가 인간의 도덕적 나침반을 앞지르는 유례없는 거대한 전환점 속에서, 우리는 기술을 경배의 대상도, 공포의 대상도 아닌 하나님께서 위임하신 거룩한 관리와 봉사의 도구로 명확히 인식해야 합니다."
    p4_1.font.size = Pt(16)
    p4_1.font.color.rgb = WHITE_TEXT

    p4_2 = tf4_b.add_paragraph()
    p4_2.text = "진정한 지혜는 알고리즘의 연산 속도에서 나오지 않으며, 오직 시대를 꿰뚫어 보는 영적 분별력과 진리에 뿌리내린 청지기적 책임 의식에서 비롯됩니다. 기술이 인간을 지배하지 않고, 인간이 공의와 사랑으로 기술을 다스릴 때 문명의 영속성이 보장됩니다."
    p4_2.font.size = Pt(15)
    p4_2.font.color.rgb = MUTED_TEXT
    p4_2.space_before = Pt(20)

    # ==========================================
    # Slide 5: 3-Stage Actionable Alternatives
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_slide_background(s5)

    tb5_t = s5.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.3), Inches(0.8))
    p5_t = tb5_t.text_frame.paragraphs[0]
    p5_t.text = "4. 최고의사결정자를 위한 3단계 실행 대안 (Action Plan)"
    p5_t.font.size = Pt(24)
    p5_t.font.bold = True
    p5_t.font.color.rgb = GOLD_TEXT

    tb5_b = s5.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(5.0))
    tf5_b = tb5_b.text_frame
    tf5_b.word_wrap = True

    steps = [
        ("1단계: 리스크 모니터링 체계의 원자화 (Granular Surveillance)", "공급망 지연 및 AI 보안 취약점을 조기 포착할 수 있는 다중 센서 기반 인텔리전스 체계 구축"),
        ("2단계: 알고리즘 거버넌스 투명성 확보 (Governance Auditing)", "블랙박스 의사결정을 배제하고 설명 가능한 청지기적 책임성 검증 프로토콜 도입"),
        ("3단계: 청지기 가치 기반의 지속 가능한 자산 운용 (Stewardship Deployment)", "단기 수익성 극대화보다 공동체의 공공선과 장기적 문명적 복원력에 자본 배분")
    ]
    for idx, (head, sub) in enumerate(steps):
        p_h = tf5_b.paragraphs[0] if idx == 0 else tf5_b.add_paragraph()
        p_h.text = head
        p_h.font.size = Pt(15)
        p_h.font.bold = True
        p_h.font.color.rgb = BLUE_TEXT
        p_h.space_before = Pt(16)

        p_s = tf5_b.add_paragraph()
        p_s.text = f"  -> {sub}"
        p_s.font.size = Pt(13.5)
        p_s.font.color.rgb = WHITE_TEXT
        p_s.space_before = Pt(4)

    # Save presentation
    prs.save(output_filepath)
    print(f"✅ [PPT Builder] 16:9 발표용 슬라이드 덱 생성 완료: {output_filepath}")
    return output_filepath

def get_ppt_filepath(order_id="DEFAULT", email="subscriber@ucklab.org", category="종합"):
    """
    Returns absolute file path to the order's PPTX deck in persistent storage.
    Generates it on the fly if not already present.
    Ensures PPTX exists in persistent storage (/workspace/scratch/storage/ & scratch/storage/).
    """
    clean_order_id = str(order_id).replace("/", "_").replace("\\", "_")
    ppt_filename = f"UCKLab_Presentation_{clean_order_id}.pptx"
    old_filename = f"UCKLab_HBR_Presentation_{clean_order_id}.pptx"

    storage_candidates = [
        PPT_DIR,
        os.path.join(BASE_DIR, "scratch", "storage", "ppt"),
        os.path.join(BASE_DIR, "scratch", "storage"),
        os.path.join(BASE_DIR, "..", "scratch", "storage"),
        "/workspace/scratch/storage"
    ]

    primary_dir = PPT_DIR
    os.makedirs(primary_dir, exist_ok=True)
    ppt_path = os.path.join(primary_dir, ppt_filename)
    old_path = os.path.join(primary_dir, old_filename)

    if not os.path.exists(ppt_path) and os.path.exists(old_path) and os.path.getsize(old_path) > 1000:
        import shutil
        shutil.copyfile(old_path, ppt_path)

    if not os.path.exists(ppt_path) or os.path.getsize(ppt_path) < 1000:
        report_data = {
            "title": f"[주간 HBR 리포트] AGI 문명 전환기와 {category} 거버넌스 (Vol. 38)"
        }
        build_weekly_ppt_deck(ppt_path, report_data, user_email=email, revision_num=1)

    # Mirror to persistent scratch/storage directories
    for cand in storage_candidates[1:]:
        try:
            os.makedirs(cand, exist_ok=True)
            cand_path = os.path.join(cand, ppt_filename)
            if not os.path.exists(cand_path) or os.path.getsize(cand_path) != os.path.getsize(ppt_path):
                import shutil
                shutil.copyfile(ppt_path, cand_path)
        except Exception:
            pass

    return ppt_path

# ---------------------------------------------------------------------------
# PPT 3-Revision Limit Governance Logic
# ---------------------------------------------------------------------------
def process_ppt_request(order_id, user_email, category="종합", requested_revision="기본 수정", db_path=DB_PATH):
    """
    Strictly enforces MAX 3 REVISIONS rule for custom PPT deck requests in SQLite DB.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")

    cursor.execute("SELECT revision_count FROM ppt_requests WHERE order_id = ?", (order_id,))
    row = cursor.fetchone()

    current_count = row[0] if row else 0

    if current_count >= MAX_PPT_REVISIONS:
        conn.close()
        return {
            "success": False,
            "message": f"⚠️ 맞춤형 PPT 3회 수정 제공 한도를 모두 완료하였습니다. 추가 수정은 새로운 주간 구독으로 이용 가능합니다.",
            "revision_count": current_count,
            "remaining_revisions": 0,
            "allowed": False,
            "governance_limit_reached": True
        }

    new_count = current_count + 1
    if row:
        cursor.execute("UPDATE ppt_requests SET revision_count = ?, status = 'PROCESSING' WHERE order_id = ?", (new_count, order_id))
    else:
        cursor.execute("INSERT INTO ppt_requests (order_id, user_email, category, revision_count, status, created_at) VALUES (?, ?, ?, ?, 'PROCESSING', ?)",
                       (order_id, user_email, category, new_count, datetime.datetime.now().isoformat()))

    conn.commit()
    conn.close()

    # Generate custom PPT
    ppt_filename = f"UCKLab_Presentation_{order_id}_v{new_count}.pptx"
    ppt_filepath = os.path.join(PPT_DIR, ppt_filename)
    
    sample_report = {
        "title": f"[주간 HBR 리포트] AGI 문명 전환기와 {category} 거버넌스",
    }
    build_weekly_ppt_deck(ppt_filepath, sample_report, user_email=user_email, revision_num=new_count)

    remaining = MAX_PPT_REVISIONS - new_count
    return {
        "success": True,
        "message": f"✅ 맞춤형 PPT 수정 요청이 접수되었습니다. (현재 {new_count}/{MAX_PPT_REVISIONS}회 사용 중)",
        "revision_count": new_count,
        "remaining_revisions": remaining,
        "allowed": True,
        "governance_limit_reached": False,
        "ppt_download_url": f"https://ucklab.org/storage/ppt/{ppt_filename}",
        "local_filepath": ppt_filepath
    }

if __name__ == "__main__":
    test_out = os.path.join(PPT_DIR, "UCKLab_Presentation_Sample.pptx")
    build_weekly_ppt_deck(test_out, {"title": "[주간 HBR 리포트] AGI 문명 전환기와 글로벌 거버넌스"})
    print("Test PPT created.")
