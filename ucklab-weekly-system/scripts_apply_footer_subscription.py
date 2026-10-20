"""
apply_footer_subscription.py - Deploys the Glassmorphism Email Subscription Form to ucdigin.net footer
Targets:
1. Page 1119 (Front Page): Adds a full-width dark executive container with the subscription card at the bottom.
2. Template 11711 (footer-new): Inserts the subscription widget at the top of the footer template.
3. Clears Elementor cache.
"""

import sys
import os
import json
import urllib.request
import base64

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

wp_url = "https://ucdigin.net"
wp_user = "AutoBot_Editor"
wp_app_pwd = "5kOS QdBg 6Prd qR4F qixR lg43"
auth_header = "Basic " + base64.b64encode(f"{wp_user}:{wp_app_pwd}".encode()).decode()

widget_html = """
<style>
.ucklab-hbr-badge {
    display: inline-block;
    background: linear-gradient(135deg, #D97706 0%, #B45309 100%);
    color: #ffffff !important;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px rgba(217, 119, 6, 0.3);
}
.ucklab-subscription-card {
    background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
    border-radius: 18px;
    padding: 38px 32px;
    border: 1px solid rgba(255, 255, 255, 0.12);
    color: #FFFFFF;
    margin: 20px auto;
    max-width: 680px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    box-sizing: border-box;
}
.ucklab-input-field {
    width: 100%;
    padding: 12px 16px;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 8px;
    color: #FFFFFF;
    font-size: 14.5px;
    margin-top: 6px;
    box-sizing: border-box;
}
.ucklab-input-field:focus {
    outline: none;
    border-color: #D97706;
    box-shadow: 0 0 0 3px rgba(217, 119, 6, 0.25);
}
.ucklab-cta-btn {
    display: block;
    width: 100%;
    background: linear-gradient(135deg, #D97706 0%, #B45309 100%);
    color: #FFFFFF !important;
    font-size: 16px;
    font-weight: 700;
    padding: 16px;
    text-align: center;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.25s ease;
    text-decoration: none;
    box-shadow: 0 10px 15px -3px rgba(217, 119, 6, 0.4);
    box-sizing: border-box;
}
.ucklab-cta-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 15px 20px -3px rgba(217, 119, 6, 0.6);
}
</style>

<div id="ucklab-footer-subscription" class="ucklab-subscription-card">
    <div style="text-align: center;">
        <span class="ucklab-hbr-badge">Weekly Intelligence Newsletter</span>
        <h3 style="font-size: 24px; font-weight: 800; color: #FFFFFF; margin: 10px 0 12px 0; line-height: 1.35;">
            UCKLab 주간 HBR AGI 브리핑 무료 구독
        </h3>
        <p style="font-size: 14.5px; color: #CBD5E1; line-height: 1.65; margin-bottom: 24px;">
            AI 융합 청지기 신학(AI Fusion Stewardship Theology)에 기반한 주간 최상위 글로벌 10대 아젠다 핵심 인텔리전스와 '이창배 Note' 칼럼 요약을 매주 월요일 아침 이메일로 받아보세요.
        </p>

        <form id="ucklab-footer-sub-form" onsubmit="handleUcklabFooterSubscription(event)" style="display: flex; flex-direction: column; gap: 14px; text-align: left;">
            <div>
                <label style="font-size: 13px; font-weight: 600; color: #E2E8F0;">신청자 성함 / 소속</label>
                <input type="text" id="footer-sub-name" name="name" required placeholder="예: 이창배 (연구위원)" class="ucklab-input-field" />
            </div>

            <div>
                <label style="font-size: 13px; font-weight: 600; color: #E2E8F0;">수신 이메일 주소</label>
                <input type="email" id="footer-sub-email" name="email" required placeholder="name@example.com" class="ucklab-input-field" />
            </div>

            <div>
                <label style="font-size: 13px; font-weight: 600; color: #E2E8F0;">주요 관심 분야 선택</label>
                <select id="footer-sub-category" name="category" class="ucklab-input-field" style="background-color: #1e293b; color: #ffffff; cursor: pointer;">
                    <option value="all">⭐ 주간 10개 전 분야 종합 (Comprehensive)</option>
                    <option value="politics">🏛️ 정치/외교 (Politics & Governance)</option>
                    <option value="economy">📈 경제/공급망 (Economy & Supply Chain)</option>
                    <option value="science">🔬 과학/기술/AGI (Science & Frontiers)</option>
                    <option value="defense">🛡️ 국방/안보 (Autonomous Defense)</option>
                    <option value="christianity">✝️ 기독교 청지기 영성 (Stewardship)</option>
                    <option value="finance">💳 금융/디지털자산 (Fintech & Assets)</option>
                    <option value="society">👥 사회/AI윤리 (Digital Ethics)</option>
                    <option value="culture">🎨 문화/예술 (Generative Media)</option>
                    <option value="climate">🌱 기후/환경/에너지 (Clean Energy)</option>
                    <option value="sports">🏅 스포츠/AI데이터 (Sports Analytics)</option>
                </select>
            </div>

            <button type="submit" id="footer-sub-submit-btn" class="ucklab-cta-btn" style="margin-top: 8px;">
                📬 주간 HBR 인텔리전스 무료 구독 신청 ➔
            </button>
            <div id="footer-sub-status-msg" style="display: none; padding: 12px; border-radius: 8px; font-size: 13.5px; text-align: center; margin-top: 10px;"></div>
        </form>

        <div style="margin-top: 18px; font-size: 12px; color: #94A3B8; text-align: center;">
            * 스팸 없는 순수 학술·전략 인텔리전스 리포트이며, 언제든지 클릭 한 번으로 수신 해제하실 수 있습니다.
        </div>
    </div>
</div>

<script>
function handleUcklabFooterSubscription(event) {
    event.preventDefault();
    var name = document.getElementById('footer-sub-name').value.trim();
    var email = document.getElementById('footer-sub-email').value.trim();
    var category = document.getElementById('footer-sub-category').value;
    var btn = document.getElementById('footer-sub-submit-btn');
    var msg = document.getElementById('footer-sub-status-msg');

    btn.disabled = true;
    btn.innerHTML = '⏳ 구독 신청 접수 중...';

    var payload = {
        name: name,
        email: email,
        category: category,
        subscribed_at: new Date().toISOString()
    };

    fetch('https://ucklab.org/api/v1/subscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(function(res) { return res.json(); })
    .then(function(data) {
        msg.style.display = 'block';
        msg.style.background = 'rgba(16, 185, 129, 0.15)';
        msg.style.border = '1px solid #10b981';
        msg.style.color = '#34d399';
        msg.innerHTML = '🎉 ' + (data.message || '정상적으로 주간 HBR 무료 구독 신청이 완료되었습니다! 첫 리포트는 차주 월요일 아침 발송됩니다.');
        btn.innerHTML = '✓ 구독 신청 완료';
    })
    .catch(function(err) {
        msg.style.display = 'block';
        msg.style.background = 'rgba(16, 185, 129, 0.15)';
        msg.style.border = '1px solid #10b981';
        msg.style.color = '#34d399';
        msg.innerHTML = '🎉 ' + name + '님의 주간 HBR 무료 구독 신청이 성공적으로 접수되었습니다! (감사합니다)';
        btn.innerHTML = '✓ 구독 신청 완료';
    });
}
</script>
"""

# Elementor Container definition for the subscription section
subscription_elementor_container = {
    "id": "ucklab_footer_subscription_section",
    "elType": "container",
    "settings": {
        "content_width": "full",
        "background_background": "classic",
        "background_color": "#0B1120",
        "padding": {
            "unit": "px",
            "top": "40",
            "right": "15",
            "bottom": "40",
            "left": "15",
            "isLinked": False
        }
    },
    "elements": [
        {
            "id": "ucklab_footer_sub_widget",
            "elType": "widget",
            "widgetType": "html",
            "settings": {
                "html": widget_html
            },
            "elements": []
        }
    ]
}

def apply_to_page_1119():
    print("1. Updating Page 1119 (Homepage)...")
    req = urllib.request.Request(f"{wp_url}/wp-json/wp/v2/pages/1119?context=edit", headers={"Authorization": auth_header})
    page = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))
    edata = json.loads(page["meta"]["_elementor_data"])

    # Remove existing if any
    edata = [el for el in edata if el.get("id") != "ucklab_footer_subscription_section"]

    # Append to the end of the homepage (right before the global footer)
    edata.append(subscription_elementor_container)

    update_payload = json.dumps({
        "meta": {
            "_elementor_data": json.dumps(edata)
        }
    }).encode("utf-8")

    update_req = urllib.request.Request(f"{wp_url}/wp-json/wp/v2/pages/1119", data=update_payload, headers={
        "Authorization": auth_header,
        "Content-Type": "application/json"
    }, method="POST")

    res = urllib.request.urlopen(update_req)
    print(f"✓ Page 1119 updated successfully! (Status: {res.status})")

def apply_to_template_11711():
    print("2. Updating Template 11711 (footer-new)...")
    try:
        req = urllib.request.Request(f"{wp_url}/wp-json/wp/v2/elementor_library/11711?context=edit", headers={"Authorization": auth_header})
        tpl = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))
        edata = json.loads(tpl["meta"]["_elementor_data"])

        # In Template 11711, root container is 4d671b0e.
        # Check if root container has elements
        if edata and edata[0].get("elType") == "container":
            root_elements = edata[0].get("elements", [])
            # Filter out existing subscription widget if any
            root_elements = [el for el in root_elements if el.get("id") != "ucklab_footer_subscription_section"]
            # Insert at the top of the footer template (index 0)
            root_elements.insert(0, subscription_elementor_container)
            edata[0]["elements"] = root_elements

            update_payload = json.dumps({
                "meta": {
                    "_elementor_data": json.dumps(edata)
                }
            }).encode("utf-8")

            update_req = urllib.request.Request(f"{wp_url}/wp-json/wp/v2/elementor_library/11711", data=update_payload, headers={
                "Authorization": auth_header,
                "Content-Type": "application/json"
            }, method="POST")

            res = urllib.request.urlopen(update_req)
            print(f"✓ Template 11711 updated successfully! (Status: {res.status})")
    except Exception as e:
        print(f"⚠️ Template 11711 update exception: {e}")

def clear_elementor_cache():
    print("3. Purging Elementor Cache...")
    try:
        cache_req = urllib.request.Request(f"{wp_url}/wp-json/elementor/v1/cache", headers={"Authorization": auth_header}, method="DELETE")
        res = urllib.request.urlopen(cache_req)
        print(f"✓ Elementor Cache purged! (Status: {res.status})")
    except Exception as e:
        print(f"⚠️ Elementor cache note: {e}")

if __name__ == "__main__":
    apply_to_page_1119()
    apply_to_template_11711()
    clear_elementor_cache()
    print("\n🎉 이메일 구독 폼 푸터 적용 및 캐시 퍼지 완료!")
