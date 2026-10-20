<?php
/**
 * UCKLab ucdigin.net Master Front-Page (Self-Contained Critical Styles & Embedded Chatbot)
 * Eliminates all cache-delay and broken layouts with inline self-contained glassmorphism styles.
 */

get_header();
?>

<!-- ==========================================================================
     SELF-CONTAINED CRITICAL STYLES (캐시 충돌 및 레이아웃 깨짐 100% 원천 방지)
     ========================================================================== -->
<style id="ucklab-frontpage-master-styles">
:root {
    --deep-navy: #070B14;
    --navy-surface: #0F172A;
    --navy-card: rgba(15, 23, 42, 0.88);
    --warm-gold: #D97706;
    --warm-gold-light: #F59E0B;
    --warm-gold-bright: #FBBF24;
    --warm-gold-glow: #FDE047;
    --cyan-accent: #0284C7;
    --cyan-light: #38BDF8;
    --slate-text-bright: #F1F5F9;
    --slate-text: #E2E8F0;
    --muted-text: #CBD5E1;
}

body {
    background-color: var(--deep-navy) !important;
    color: var(--slate-text-bright) !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Pretendard', 'Noto Sans KR', 'Segoe UI', Roboto, sans-serif !important;
    margin: 0;
    padding: 0;
    line-height: 1.8;
}

/* 1. Header Navigation */
.header-nav {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    padding: 16px 40px !important;
    background: rgba(9, 13, 22, 0.95) !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.12) !important;
    position: sticky !important;
    top: 0 !important;
    z-index: 100 !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
}

.brand-logo {
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    text-decoration: none !important;
}

.brand-logo-img {
    transition: transform 0.25s ease, box-shadow 0.25s ease !important;
}

.brand-logo:hover .brand-logo-img {
    transform: scale(1.05) !important;
    box-shadow: 0 0 22px rgba(245, 158, 11, 0.75) !important;
}

.brand-badge {
    font-size: 11px !important;
    background: rgba(245, 158, 11, 0.22) !important;
    color: var(--warm-gold-bright) !important;
    border: 1px solid rgba(245, 158, 11, 0.5) !important;
    padding: 2px 8px !important;
    border-radius: 9999px !important;
    font-weight: 800 !important;
}

.nav-menu {
    display: flex !important;
    gap: 14px !important;
    list-style: none !important;
    margin: 0 !important;
    padding: 0 !important;
    align-items: center !important;
}

.nav-menu a {
    color: var(--slate-text-bright) !important;
    text-decoration: none !important;
    font-weight: 700 !important;
    font-size: 13.5px !important;
    padding: 6px 14px !important;
    border-radius: 9999px !important;
    transition: all 0.2s ease !important;
}

.nav-menu a:hover,
.nav-menu a.active {
    color: #FFFFFF !important;
    background: rgba(245, 158, 11, 0.22) !important;
    border: 1px solid rgba(245, 158, 11, 0.4) !important;
}

/* 1-1. Signature Hook Menu: [이창배 Note] 독립 메뉴 하이라이트 */
.nav-signature-hook {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.28) 0%, rgba(217, 119, 6, 0.18) 100%) !important;
    border: 1px solid rgba(245, 158, 11, 0.65) !important;
    color: #FDE047 !important;
    font-weight: 800 !important;
    box-shadow: 0 0 16px rgba(245, 158, 11, 0.3), inset 0 1px 1px rgba(255, 255, 255, 0.4) !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
    position: relative !important;
}

.nav-signature-hook:hover,
.nav-signature-hook.active {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.5) 0%, rgba(217, 119, 6, 0.4) 100%) !important;
    border-color: #FDE047 !important;
    color: #FFFFFF !important;
    box-shadow: 0 0 24px rgba(245, 158, 11, 0.65), inset 0 1px 2px #FFFFFF !important;
    transform: translateY(-1px) !important;
}

.hook-badge {
    font-size: 10px !important;
    background: linear-gradient(135deg, #D97706 0%, #B45309 100%) !important;
    color: #FFFFFF !important;
    padding: 1px 6px !important;
    border-radius: 9999px !important;
    font-weight: 900 !important;
    letter-spacing: -0.2px !important;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.4) !important;
}

/* 2. 3D Crystal Buttons */
.glass-pill-btn {
    position: relative !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 8px !important;
    padding: 12px 26px !important;
    font-size: 14px !important;
    font-weight: 800 !important;
    text-decoration: none !important;
    border-radius: 9999px !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.18) 0%, rgba(255, 255, 255, 0.05) 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.35) !important;
    backdrop-filter: blur(14px) !important;
    -webkit-backdrop-filter: blur(14px) !important;
    box-shadow: inset 0 1px 2px rgba(255, 255, 255, 0.6), 0 8px 24px -4px rgba(0, 0, 0, 0.5) !important;
    color: #FFFFFF !important;
}

.glass-pill-btn:hover {
    transform: translateY(-2px) !important;
    border-color: rgba(255, 255, 255, 0.65) !important;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.6) !important;
}

.glass-pill-btn-gold {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.95) 0%, rgba(217, 119, 6, 0.98) 100%) !important;
    border: 1px solid rgba(254, 215, 170, 0.75) !important;
    color: #FFFFFF !important;
    box-shadow: inset 0 2px 3px rgba(255, 255, 255, 0.75), 0 10px 28px rgba(217, 119, 6, 0.5) !important;
}

.glass-pill-btn-gold:hover {
    transform: translateY(-2px) !important;
    box-shadow: inset 0 2px 4px #FFFFFF, 0 14px 34px rgba(217, 119, 6, 0.7) !important;
}

.glass-pill-btn-blue {
    background: linear-gradient(135deg, rgba(56, 189, 248, 0.9) 0%, rgba(2, 132, 199, 0.96) 100%) !important;
    border: 1px solid rgba(186, 230, 253, 0.75) !important;
    color: #FFFFFF !important;
    box-shadow: inset 0 2px 3px rgba(255, 255, 255, 0.75), 0 10px 28px rgba(2, 132, 199, 0.5) !important;
}

.glass-pill-btn-small {
    padding: 6px 16px !important;
    font-size: 12.5px !important;
}

/* 3. 3D Crystal Cards */
.glass-card-3d {
    position: relative !important;
    background: linear-gradient(165deg, rgba(26, 38, 62, 0.82) 0%, rgba(13, 20, 36, 0.92) 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.18) !important;
    border-radius: 20px !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    box-shadow: 0 20px 48px -8px rgba(0, 0, 0, 0.6) !important;
    transition: all 0.3s ease !important;
}

.glass-card-3d:hover {
    transform: translateY(-4px) !important;
    border-color: rgba(245, 158, 11, 0.5) !important;
}

.glass-card-gold {
    border-color: rgba(245, 158, 11, 0.45) !important;
    box-shadow: 0 20px 48px -8px rgba(0, 0, 0, 0.6), 0 0 24px rgba(217, 119, 6, 0.25) !important;
}

/* 4. Radar Animation */
.radar-pulse-dot {
    position: relative !important;
    display: inline-block !important;
    width: 10px !important;
    height: 10px !important;
    border-radius: 50% !important;
    background-color: #EF4444 !important;
}

.radar-pulse-dot::after {
    content: '' !important;
    position: absolute !important;
    top: -4px !important;
    left: -4px !important;
    width: 18px !important;
    height: 18px !important;
    border-radius: 50% !important;
    background-color: rgba(239, 68, 68, 0.6) !important;
    animation: radarPulse 1.8s infinite cubic-bezier(0, 0, 0.2, 1) !important;
}

@keyframes radarPulse {
    0% { transform: scale(0.6); opacity: 1; }
    100% { transform: scale(2.2); opacity: 0; }
}

@media (max-width: 768px) {
    .header-nav { padding: 12px 18px !important; flex-direction: column !important; gap: 10px !important; }
    .nav-menu { flex-wrap: wrap !important; justify-content: center !important; }
    .lee-note-hook-grid { grid-template-columns: 1fr !important; gap: 20px !important; }
    .lee-note-stamp-box { display: none !important; }
}
</style>

<!-- 1. HERO SECTION: 3D OSINT LIVE RADAR PANORAMA -->
<section class="hero-osint-wrapper" style="position:relative; width:100%; height:78vh; min-height:580px; overflow:hidden; background:#070B14;">
    
    <!-- Real-time 3D OSINT Map Iframe -->
    <iframe id="osintIframe" 
            class="osint-iframe" 
            src="https://www.worldmonitor.app/embed?layers=conflicts,military,finance" 
            title="World Monitor OSINT Radar"
            style="position:absolute; top:0; left:0; width:100%; height:100%; border:none; z-index:1; filter:contrast(1.1) brightness(0.85); transition:filter 0.3s ease;">
    </iframe>

    <!-- Map Interactive Shroud / HUD Overlay Container -->
    <div id="hudOverlay" class="hud-container" style="position:absolute; inset:0; z-index:10; pointer-events:none; display:flex; flex-direction:column; justify-content:space-between; padding:24px 32px;">
        
        <!-- Top Status Bar & Coordinates -->
        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:16px;">
            <div class="glass-pill-btn" style="pointer-events:auto; padding:7px 18px; font-size:13px; background:rgba(15, 23, 42, 0.92); border-color:rgba(245, 158, 11, 0.55); display:inline-flex; align-items:center; gap:8px;">
                <img src="<?php echo get_template_directory_uri(); ?>/images/icons/radar.png" alt="OSINT Radar" style="width:20px; height:20px; object-fit:contain;">
                <span class="radar-pulse-dot"></span>
                <span style="color:#FFFFFF !important; font-weight:800; text-shadow:0 1px 3px rgba(0,0,0,0.6);">LIVE OSINT CONFLICT &amp; GEOPOLITICAL INTELLIGENCE RADAR</span>
                <span style="margin:0 6px; color:rgba(255,255,255,0.4);">|</span>
                <span style="color:#FDE047 !important; font-size:12px; font-weight:800;">DEFCON-3 ELEVATED</span>
            </div>

            <div class="glass-pill-btn" style="pointer-events:auto; padding:6px 16px; font-size:12px; color:#E2E8F0 !important; background:rgba(15, 23, 42, 0.88);">
                <span style="color:#38BDF8 !important; font-weight:800;">TELEMETRY:</span> 24/7 REAL-TIME STREAMING
            </div>
        </div>

        <!-- 4 Global Conflict Hotspot HUD Widgets -->
        <div class="hotspot-grid" style="pointer-events:auto; display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:14px; max-width:1200px; width:100%; margin:0 auto;">
            
            <div class="glass-card-3d" style="padding:16px 20px; background:rgba(15, 23, 42, 0.88); border-color:rgba(239, 68, 68, 0.45);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <span style="font-size:13.5px; font-weight:900; color:#FFFFFF !important;">🇷🇺-🇺🇦 동유럽 전역</span>
                    <span style="font-size:11px; font-weight:900; color:#EF4444; background:rgba(239,68,68,0.25); padding:2px 8px; border-radius:9999px;">교전 8.7</span>
                </div>
                <div style="font-size:12.5px; color:#CBD5E1; font-weight:600;">미사일·드론 항적 탐지 | 전파 교란 최고조</div>
            </div>

            <div class="glass-card-3d" style="padding:16px 20px; background:rgba(15, 23, 42, 0.88); border-color:rgba(245, 158, 11, 0.45);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <span style="font-size:13.5px; font-weight:900; color:#FFFFFF !important;">🇮🇷-🇮🇱 호르무즈 해협</span>
                    <span style="font-size:11px; font-weight:900; color:#FDE047; background:rgba(245,158,11,0.25); padding:2px 8px; border-radius:9999px;">항행 경보</span>
                </div>
                <div style="font-size:12.5px; color:#CBD5E1; font-weight:600;">원유 수송선 호위 작전 | 유조선 통항 -34%</div>
            </div>

            <div class="glass-card-3d" style="padding:16px 20px; background:rgba(15, 23, 42, 0.88); border-color:rgba(56, 189, 248, 0.45);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <span style="font-size:13.5px; font-weight:900; color:#FFFFFF !important;">🇾🇪-🇸🇦 홍해 항로</span>
                    <span style="font-size:11px; font-weight:900; color:#38BDF8; background:rgba(56,189,248,0.25); padding:2px 8px; border-radius:9999px;">우회율 74%</span>
                </div>
                <div style="font-size:12.5px; color:#CBD5E1; font-weight:600;">희망봉 우회 운임 급등 | 글로벌 물류 쇼크</div>
            </div>

            <div class="glass-card-3d" style="padding:16px 20px; background:rgba(15, 23, 42, 0.88); border-color:rgba(16, 185, 129, 0.45);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <span style="font-size:13.5px; font-weight:900; color:#FFFFFF !important;">🇹🇼-🇨🇳 대만 해협</span>
                    <span style="font-size:11px; font-weight:900; color:#10B981; background:rgba(16,185,129,0.25); padding:2px 8px; border-radius:9999px;">감시 강화</span>
                </div>
                <div style="font-size:12.5px; color:#CBD5E1; font-weight:600;">방공식별구역 진입 42소티 | 반도체 공급망</div>
            </div>

        </div>

        <!-- Bottom Controls Bar -->
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; pointer-events:auto;">
            <div style="display:flex; gap:10px; flex-wrap:wrap;">
                <button type="button" onclick="toggleMapInteraction()" id="mapInteractiveToggle" class="glass-pill-btn glass-pill-btn-small glass-pill-btn-blue">
                    🗺️ 레이더 직접 탐색 (Interactive)
                </button>
                <button type="button" onclick="toggleHudVisibility()" class="glass-pill-btn glass-pill-btn-small">
                    👁️ HUD 오버레이 토글
                </button>
            </div>
            <div>
                <a href="#executive-review" class="glass-pill-btn glass-pill-btn-small glass-pill-btn-gold">
                    🏛️ 전략 제언 브리핑으로 이동 ↓
                </a>
            </div>
        </div>

    </div>
</section>

<!-- ==========================================================================
     INTERACTIVE EMBED CHATBOT BAR (Directly below Hero Section)
     Jev Router $0 Guardrail + Auto-Fallback AI Mascot Character (Zero Broken Box)
     ========================================================================== -->
<section id="ucklab-chatbot-section" style="max-width:1180px; margin:28px auto 0 auto; padding:0 24px; position:relative; z-index:20;">
    <div class="glass-card-3d" style="padding:24px 28px; background:linear-gradient(135deg, rgba(15, 23, 42, 0.94) 0%, rgba(9, 13, 22, 0.98) 100%); border:1px solid rgba(245, 158, 11, 0.5); box-shadow:0 16px 40px rgba(0,0,0,0.6), 0 0 20px rgba(245,158,11,0.2);">
        
        <!-- Chatbot Header Bar -->
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:18px; flex-wrap:wrap; gap:12px; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:14px;">
            <div style="display:flex; align-items:center; gap:14px;">
                <!-- 3D Gold Stewardship AI Mascot Badge -->
                <div style="position:relative; width:48px; height:48px; flex-shrink:0;">
                    <img src="<?php echo get_template_directory_uri(); ?>/images/icons/ai_assistant.png" 
                         alt="Stewardship AI" 
                         style="width:48px; height:48px; border-radius:14px; border:1.5px solid #FDE047; box-shadow:0 0 18px rgba(245,158,11,0.6); object-fit:contain; background:rgba(15,23,42,0.85); padding:4px; display:block;">
                    <span style="position:absolute; bottom:-2px; right:-2px; width:12px; height:12px; background:#10B981; border:2px solid #070B14; border-radius:50%; box-shadow:0 0 6px #10B981;"></span>
                </div>
                <div>
                    <div style="font-size:16.5px; font-weight:900; color:#FFFFFF !important; display:flex; align-items:center; gap:8px;">
                        UCKLab OSINT &amp; Research AI Assistant
                        <span style="font-size:11px; background:rgba(56,189,248,0.2); color:#38BDF8; border:1px solid rgba(56,189,248,0.5); padding:1px 8px; border-radius:9999px; font-weight:800;">Stewardship AI</span>
                    </div>
                    <div style="font-size:12px; color:#94A3B8; margin-top:2px;">
                        World Monitor 지정학 분석 • AGI 문명 전환 패러다임 • Monograph™ 학술 저널 발급 지원
                    </div>
                </div>
            </div>
            
            <div style="display:flex; align-items:center; gap:8px;">
                <span class="glass-pill-btn glass-pill-btn-small" style="font-size:11.5px; padding:4px 12px; background:rgba(16,185,129,0.15); border-color:rgba(16,185,129,0.5); color:#6EE7B7 !important;">
                    🛡️ Jev Router $0 Guardrail Enabled
                </span>
            </div>
        </div>

        <!-- Chat Conversation Display Pane -->
        <div id="chatMessagePane" style="background:rgba(5, 8, 17, 0.75); border:1px solid rgba(255,255,255,0.08); border-radius:14px; padding:16px 20px; min-height:85px; max-height:260px; overflow-y:auto; margin-bottom:14px;">
            <div style="display:flex; gap:12px; align-items:flex-start;">
                <img src="<?php echo get_template_directory_uri(); ?>/images/icons/ai_assistant.png" alt="AI 도우미" style="width:26px; height:26px; object-fit:contain; margin-top:2px;">
                <div style="font-size:14px; line-height:1.75; color:#E2E8F0;">
                    <b>상황실 도우미:</b> 안녕하세요! World Monitor 기반 실시간 OSINT 데이터, 당주 AGI 10대 분야 분석, 또는 <span style="color:#FDE047; font-weight:800;">UCKLab Monograph™ (2,500단어 PDF)</span> 발급에 대해 궁금한 점을 질문해 주세요.
                </div>
            </div>
        </div>

        <!-- Guardrail Filter Notification Pill (0.7s Jev Warning) -->
        <div id="guardrailWarning" style="display:none; background:rgba(239, 68, 68, 0.15); border:1px solid rgba(239, 68, 68, 0.4); border-radius:10px; padding:8px 14px; margin-bottom:12px; font-size:12.5px; color:#FCA5A5;">
            ⚡ <b>Jev Router 0.7s 필터 작동:</b> UCKLab 연구 분야(OSINT, 지정학, AGI 청지기 신학, 학술 저널) 질문으로 가이드합니다.
        </div>

        <!-- Input Bar with Send Button -->
        <div style="display:flex; gap:10px; align-items:center;">
            <input type="text" 
                   id="chatbotUserInput" 
                   placeholder="OSINT 레이더 분석, AGI 청지기 신학, Monograph 발급 등에 대해 물어보세요..." 
                   onkeypress="if(event.key === 'Enter') executeChatbotQuery();"
                   style="flex:1; background:rgba(15, 23, 42, 0.95); border:1px solid rgba(255,255,255,0.22); border-radius:9999px; padding:12px 22px; font-size:14px; color:#FFFFFF; outline:none; transition:border-color 0.2s;"
                   onfocus="this.style.borderColor='#F59E0B';" 
                   onblur="this.style.borderColor='rgba(255,255,255,0.22)';">
            <button type="button" 
                    onclick="executeChatbotQuery()" 
                    class="glass-pill-btn glass-pill-btn-gold" 
                    style="padding:11px 26px; font-size:14px; white-space:nowrap; flex-shrink:0;">
                🚀 질문 전송
            </button>
        </div>

        <!-- Quick Recommend Tag Chips -->
        <div style="display:flex; gap:8px; margin-top:14px; flex-wrap:wrap; font-size:12px;">
            <span style="color:#94A3B8; font-weight:700; align-self:center; margin-right:4px;">추천 질의:</span>
            <button type="button" onclick="setQuickQuestion('Argos Atlas에서 전 세계 실시간 라이브 카메라 및 항공/선박 트랙을 탐색하는 방법 알려줘')" class="glass-pill-btn glass-pill-btn-small" style="font-size:12px; padding:4px 12px; background:rgba(56,189,248,0.12); border-color:rgba(56,189,248,0.45); color:#38BDF8 !important;">
                # 🌐 Argos Atlas 실시간 카메라 탐색
            </button>
            <button type="button" onclick="setQuickQuestion('OSINT 레이더 보는 법')" class="glass-pill-btn glass-pill-btn-small" style="font-size:12px; padding:4px 12px; background:rgba(255,255,255,0.06);">
                # OSINT 레이더 보는 법
            </button>
            <button type="button" onclick="setQuickQuestion('Monograph PDF 발급 안내')" class="glass-pill-btn glass-pill-btn-small" style="font-size:12px; padding:4px 12px; background:rgba(255,255,255,0.06);">
                # Monograph PDF 발급 안내
            </button>
            <button type="button" onclick="setQuickQuestion('이창배 NOTE 칼럼 소개')" class="glass-pill-btn glass-pill-btn-small" style="font-size:12px; padding:4px 12px; background:rgba(255,255,255,0.06);">
                # 이창배 NOTE 칼럼 소개
            </button>
        </div>

    </div>
</section>

<!-- Chatbot Guardrail & Execution Script -->
<script>
// Argos Atlas 좌표 및 실시간 카메라 뷰 연동 함수
function focusArgosLocation(lat, lng, zoom, regionName) {
    const iframe = document.getElementById('osintIframe');
    const btn = document.getElementById('osintToggleBtn') || document.getElementById('mapInteractiveToggle');
    const card = document.getElementById('heroOverlayCard') || document.querySelector('.hotspot-grid');
    const chatBox = document.getElementById('ucklabChatBox') || document.getElementById('chatMessagePane');

    // 1. 지도 터치/조작 모드 활성화 (pointer-events: auto)
    if (iframe) {
        iframe.style.pointerEvents = 'auto';
        iframe.style.filter = 'brightness(0.9) contrast(1.0)';
        iframe.style.zIndex = '15';
    }
    if (card) card.style.opacity = '0.35'; // 맵 집중 모드
    if (btn) {
        btn.innerHTML = '🔒 일반 스크롤 모드로 전환';
        btn.style.background = '#D97706';
        btn.style.color = '#ffffff';
    }

    // 2. Argos Atlas URL 파라미터 업데이트를 통한 위치 Zoom-in
    const baseUrl = 'https://argosatlas.com'; // 또는 지정된 Argos Atlas Embed URL
    if (iframe) {
        iframe.src = `${baseUrl}/#lat=${lat}&lng=${lng}&zoom=${zoom}`;
    }

    // 3. 챗봇 메시지 자동 안내
    if (chatBox) {
        chatBox.innerHTML += `<p style="margin:8px 0; font-size:13.5px; color:#38BDF8;">🌐 <b>Argos Atlas 레이더:</b> ${regionName} 실시간 카메라 &amp; 모니터링 레이어로 지도가 이동되었습니다.</p>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}

// Quick Tag 클릭 핸들러
function setQuickQuestion(q) {
    const input = document.getElementById('chatInput') || document.getElementById('chatbotUserInput');
    if (input) input.value = q;

    if (q.includes('Argos Atlas') || q.includes('카메라')) {
        // 기본 주요 교차로/분쟁 지역 뷰로 자동 Zoom-in (예: 동유럽/중동 분쟁 레이어 또는 글로벌 허브)
        focusArgosLocation(50.4501, 30.5234, 6, '글로벌 핫스팟 및 주요 교통 카메라 뷰');
        sendUcklabChat();
    } else {
        sendUcklabChat();
    }
}

function setQuickQuery(text) {
    setQuickQuestion(text);
}

function sendUcklabChat() {
    executeChatbotQuery();
}

function executeChatbotQuery() {
    const input = document.getElementById('chatInput') || document.getElementById('chatbotUserInput');
    const query = input.value.trim();
    if (!query) return;

    const pane = document.getElementById('ucklabChatBox') || document.getElementById('chatMessagePane');
    const warn = document.getElementById('guardrailWarning');
    warn.style.display = 'none';

    // 1. 사용자 질문 렌더링
    pane.innerHTML += `
        <div style="display:flex; justify-content:flex-end; margin-bottom:12px; margin-top:8px;">
            <div style="background:rgba(245,158,11,0.22); border:1px solid rgba(245,158,11,0.5); color:#FEF08A; padding:8px 16px; border-radius:14px 14px 2px 14px; font-size:13.5px; max-width:80%;">
                👤 <b>사용자:</b> ${escapeHtml(query)}
            </div>
        </div>
        <div id="aiResponsePending" style="display:flex; gap:10px; align-items:center; color:#38BDF8; font-size:13px;">
            <span class="radar-pulse-dot"></span> Jev Router $0 Guardrail 범위 판별 중 (0.7초)...
        </div>
    `;
    input.value = '';

    // 2. 0.7초 Jev Router Guardrail 검증 로직 ($0 판별)
    setTimeout(() => {
        const allowedKeywords = [
            'argos', 'atlas', '아르고스', '카메라', '라이브', '항공', '선박', '위성', '트랙', '탐색', '조종',
            'osint', '오신트', '레이더', '지정학', '분쟁', '전쟁', '군사', '호르무즈', '홍해', '대만', '우크라이나',
            'agi', 'ai', '인공지능', '신학', '청지기', '이창배', 'note', '칼럼',
            'monograph', '모노그래프', '저널', '학술', 'pdf', 'top10', '뉴스', '리뷰', '발급', '연구소', 'ucklab'
        ];

        const lowerQuery = query.toLowerCase();
        const isInScope = allowedKeywords.some(keyword => lowerQuery.includes(keyword));

        const pending = document.getElementById('aiResponsePending');
        if (!isInScope) {
            // [범위 벗어남: Out of Scope - 즉시 차단 및 $0 안내]
            warn.style.display = 'block';
            pane.innerHTML += `
                <div style="display:flex; gap:12px; align-items:flex-start; margin-top:8px;">
                    <span style="font-size:20px;">🛡️</span>
                    <div style="font-size:13.5px; line-height:1.8; color:#CBD5E1; background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.3); border-radius:12px; padding:12px 16px;">
                        <b style="color:#F87171;">Jev Router 가드레일 안내:</b><br>
                        죄송합니다. 저는 <b>UCKLab 연구소의 OSINT 지정학 분석 및 AGI 청지기 신학 전용 AI 도우미</b>입니다.<br>
                        일반 일상 대화보다는 연구소 연구 분야에 대해 질문해 주시면 500단어 요약 및 Monograph 저널 발급 안내를 도와드립니다.<br>
                        <span style="color:#FDE047; font-weight:800;">💡 추천: '# 🌐 Argos Atlas 실시간 카메라 탐색', '# OSINT 레이더 보는 법', '# Monograph PDF 발급 안내'</span> 태그를 눌러보세요.
                    </div>
                </div>
            `;
        } else {
            // [범위 내: In Scope - 인텔리전스 응답 및 저널 연동]
            let answer = "";
            let actionButtons = `
                <div style="margin-top:10px; display:flex; gap:8px; flex-wrap:wrap;">
                    <a href="/category/lee-note/" class="glass-pill-btn glass-pill-btn-small glass-pill-btn-gold" style="font-size:11.5px; padding:3px 12px;">
                        ✒️ 이창배 Note 바로 읽기 ➔
                    </a>
                    <a href="https://ucklab.org/research" class="glass-pill-btn glass-pill-btn-small" style="font-size:11.5px; padding:3px 12px;">
                        🎓 Monograph™ 저널 발급 ➔
                    </a>
                </div>
            `;

            if (lowerQuery.includes('argos') || lowerQuery.includes('atlas') || lowerQuery.includes('아르고스') || lowerQuery.includes('카메라') || lowerQuery.includes('항공') || lowerQuery.includes('선박') || lowerQuery.includes('트랙')) {
                answer = "<b>[🌐 Argos Atlas 실시간 카메라 &amp; 항공/선박/위성 레이어 탐색 안내]</b><br><b>Argos Atlas</b>는 전 세계 <b>200,000개 이상의 실시간 라이브 카메라(CCTV/웹캠)</b>와 글로벌 <b>항공(Flight)·선박(Ship)·위성(Satellite) 실시간 트랙 레이어</b>를 통합 관제하는 OSINT 지리공간 플랫폼입니다.<br>상단 Hero 섹션에서 <b>\"🌐 실시간 OSINT 조종 모드\"</b> 버튼을 토글(활성화)하시면, Argos Atlas 라이브 피드와 3D 지구본 상의 실시간 항공·선박 항적 및 카메라 비콘을 직접 확대·회전하며 탐색하실 수 있습니다.";
            } else if (lowerQuery.includes('osint') || lowerQuery.includes('레이더')) {
                answer = "World Monitor 실시간 레이더는 전 세계 4대 분쟁 축(동유럽, 호르무즈, 홍해, 대만해협)의 군사 항적과 금융 통화 위협 지수를 24/7 실시간 집계합니다. 상단의 <b>'🗺️ 레이더 직접 탐색'</b> 버튼을 누르시면 지도를 자유롭게 확대/회전하실 수 있습니다.";
            } else if (lowerQuery.includes('이창배') || lowerQuery.includes('note') || lowerQuery.includes('노트') || lowerQuery.includes('칼럼')) {
                answer = "<b>[이창배 Note]</b>는 UCKLab 소장 이창배 박사의 심층 통찰 칼럼입니다. 기술적 초지능(AGI) 가속화와 글로벌 지정학 격변기 속에서 '성경적 청지기 도덕 주권'과 국가·기업의 전략적 나침반을 제시합니다. 상단 내비게이션 메뉴 및 아래 버튼을 통해 7편의 정론 아카이브를 지금 바로 열람하실 수 있습니다.";
            } else if (lowerQuery.includes('monograph') || lowerQuery.includes('저널') || lowerQuery.includes('pdf')) {
                answer = "<b>UCKLab Monograph™</b>는 2,500단어 분량의 APA 7th 학술 규격 저널 PDF입니다. 엄밀한 연구방법론과 참고문헌을 포함하여 생성되며, 아래 [학술 저널 발급] 버튼을 통해 즉시 발급받으실 수 있습니다.";
            } else if (lowerQuery.includes('신학') || lowerQuery.includes('청지기') || lowerQuery.includes('agi')) {
                answer = "<b>AGI 융합 청지기 신학(Stewardship Theology)</b>은 급변하는 초지능 가속 시대에 인류가 견지해야 할 윤리적 분별력과 시사적 통찰을 제시하는 UCKLab 고유의 정론 프레임워크입니다.";
            } else {
                answer = "UCKLab AI 싱크탱크 분석에 따르면, 당주 핵심 이슈는 지정학적 공급망 리스크와 자율 금융 인프라의 격변입니다. 상세한 500단어 브리핑은 아래 <b>'이창배 Note'</b> 및 <b>'Executive Note'</b> 섹션에서 바로 확인하실 수 있습니다.";
            }

            pane.innerHTML += `
                <div style="display:flex; gap:12px; align-items:flex-start; margin-top:8px;">
                    <img src="<?php echo get_template_directory_uri(); ?>/images/icons/ai_assistant.png" alt="AI Assistant" style="width:26px; height:26px; object-fit:contain; margin-top:2px; filter:drop-shadow(0 0 6px rgba(56,189,248,0.6));">
                    <div style="font-size:13.5px; line-height:1.8; color:#F1F5F9; background:rgba(15,23,42,0.85); border:1px solid rgba(245,158,11,0.4); border-radius:12px; padding:12px 16px;">
                        <b style="color:#FBBF24;">상황실 AI 인텔리전스 브리핑:</b><br>
                        ${answer}
                        ${actionButtons}
                    </div>
                </div>
            `;
        }
        if (pending) pending.remove();
        pane.scrollTop = pane.scrollHeight;
    }, 700);
}

function escapeHtml(text) {
    const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}
</script>

<!-- ==========================================================================
     FRONT-PAGE FEATURED HOOK: [이창배 Note] 소장 정론 권두 칼럼 쇼케이스
     사용자 유입 시 강력한 시선 흡입 및 학술적 권위 확립을 위한 3D 골드 글래스모피즘 Hook
     ========================================================================== -->
<section id="lee-chang-bae-note-hook" style="max-width:1180px; margin:46px auto 0 auto; padding:0 24px; position:relative; z-index:20;">
    <div class="glass-card-3d" style="padding:36px 38px; background:linear-gradient(145deg, rgba(26, 36, 60, 0.95) 0%, rgba(11, 16, 30, 0.98) 100%); border:1px solid rgba(245, 158, 11, 0.65); box-shadow:0 22px 50px -10px rgba(0,0,0,0.7), 0 0 30px rgba(245, 158, 11, 0.22); border-left:6px solid #F59E0B;">
        
        <!-- Header Meta Line -->
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:20px; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:14px;">
            <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
                <span class="glass-pill-btn glass-pill-btn-small" style="background:linear-gradient(135deg, rgba(245,158,11,0.95) 0%, rgba(217,119,6,0.98) 100%); border:none; color:#FFFFFF !important; font-weight:900; font-size:12px; box-shadow:0 2px 10px rgba(217,119,6,0.45);">
                    ✒️ DIRECTOR'S SIGNATURE NOTE
                </span>
                <span style="background:rgba(245, 158, 11, 0.15); border:1px solid rgba(245, 158, 11, 0.4); color:#FDE047; font-size:12px; font-weight:800; padding:2px 10px; border-radius:9999px;">
                    소장 정론 권두 칼럼
                </span>
                <span style="color:#94A3B8; font-size:12.5px; font-weight:600;">
                    Vol. 39 최신 기고
                </span>
            </div>
            
            <a href="/category/lee-note/" class="glass-pill-btn glass-pill-btn-small" style="font-size:12.5px; padding:4px 14px; background:rgba(255,255,255,0.06); border-color:rgba(245,158,11,0.45); color:#FDE047 !important;">
                이창배 Note 아카이브 전체보기 (7편) ➔
            </a>
        </div>

        <!-- 2-Column Responsive Body Layout -->
        <div style="display:grid; grid-template-columns:minmax(0, 1fr) auto; gap:32px; align-items:center;" class="lee-note-hook-grid">
            
            <!-- Left Column: Title, Quote Hook, Author Profile -->
            <div>
                <!-- Author Byline -->
                <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
                    <img src="<?php echo get_template_directory_uri(); ?>/images/icons/dr_lee_avatar.png" 
                         alt="이창배 박사" 
                         style="width:42px; height:42px; border-radius:12px; border:1.5px solid #FDE047; box-shadow:0 0 14px rgba(245,158,11,0.5); object-fit:contain; flex-shrink:0; background:rgba(15,23,42,0.85); padding:2px;">
                    <div>
                        <div style="font-size:14.5px; font-weight:900; color:#FFFFFF !important; line-height:1.2;">
                            이창배 박사 <span style="font-size:12px; font-weight:700; color:#FBBF24;">(Dr. Lee Chang-bae)</span>
                        </div>
                        <div style="font-size:11.5px; color:#CBD5E1;">
                            UCKLab 소장 / 신학박사 · AI Fusion Stewardship Specialist
                        </div>
                    </div>
                </div>

                <!-- Main Hook Headline -->
                <h2 style="font-size:24px; font-weight:900; color:#FFFFFF !important; margin:0 0 14px 0; line-height:1.4; letter-spacing:-0.5px; text-shadow:0 2px 6px rgba(0,0,0,0.8); word-break:keep-all;">
                    <a href="/category/lee-note/" style="color:#FFFFFF !important; text-decoration:none;" onmouseover="this.style.color='#FBBF24';" onmouseout="this.style.color='#FFFFFF';">
                        "AGI 문명 대전환과 성경적 청지기 도덕 주권: 우리는 무엇을 지켜낼 것인가?"
                    </a>
                </h2>

                <!-- Blockquote Hook -->
                <div style="background:rgba(15, 23, 42, 0.75); border-left:4px solid #F59E0B; border-radius:0 10px 10px 0; padding:14px 18px; margin-bottom:18px;">
                    <p style="font-size:14.5px; line-height:1.8; color:#E2E8F0 !important; margin:0; word-break:keep-all;">
                        “인공지능은 숭배나 두려움의 대상이 아닌, 하나님께서 위임하신 거룩한 관리와 돌봄의 도구입니다. 단일 글로벌 빅테크의 알고리즘 종속을 넘어, 기술 주권과 청지기 신학이 결합된 독자적 규범을 확립해야 합니다.”
                    </p>
                </div>

                <!-- Strategic Keywords & CTA Buttons -->
                <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:14px;">
                    <div style="display:flex; gap:6px; flex-wrap:wrap;">
                        <span style="font-size:11px; background:rgba(255,255,255,0.06); color:#CBD5E1; padding:2px 8px; border-radius:6px; font-weight:600;">#AGI문명전환</span>
                        <span style="font-size:11px; background:rgba(245,158,11,0.12); color:#FDE047; padding:2px 8px; border-radius:6px; font-weight:600;">#청지기신학</span>
                        <span style="font-size:11px; background:rgba(56,189,248,0.12); color:#38BDF8; padding:2px 8px; border-radius:6px; font-weight:600;">#지식주권</span>
                        <span style="font-size:11px; background:rgba(16,185,129,0.12); color:#34D399; padding:2px 8px; border-radius:6px; font-weight:600;">#소장직필</span>
                    </div>

                    <div style="display:flex; gap:10px; flex-wrap:wrap;">
                        <a href="/category/lee-note/" class="glass-pill-btn glass-pill-btn-small glass-pill-btn-gold" style="font-weight:900;">
                            ✒️ 이창배 Note 전문 읽기 ➔
                        </a>
                        <a href="https://ucklab.org/research" class="glass-pill-btn glass-pill-btn-small">
                            🎓 학술 Monograph 발급
                        </a>
                    </div>
                </div>

            </div>

            <!-- Right Column: Visual Stamp Card / Seal -->
            <div style="text-align:center; min-width:200px; padding:20px; background:rgba(15,23,42,0.65); border:1px dashed rgba(245,158,11,0.5); border-radius:16px;" class="lee-note-stamp-box">
                <img src="<?php echo get_template_directory_uri(); ?>/images/icons/dispatch_seal.png" 
                     alt="UCK Lab Official Seal" 
                     style="width:52px; height:52px; margin:0 auto 10px auto; display:block; object-fit:contain; filter:drop-shadow(0 0 12px rgba(245,158,11,0.5));">
                <div style="font-size:13px; font-weight:900; color:#FDE047; letter-spacing:1px; text-transform:uppercase;">
                    OFFICIAL DISPATCH
                </div>
                <div style="font-size:11.5px; color:#94A3B8; margin:4px 0 12px 0;">
                    UCKLab Research Directorate
                </div>
                <div style="font-size:12px; color:#E2E8F0; line-height:1.6; border-top:1px solid rgba(255,255,255,0.1); padding-top:10px;">
                    주간 심층 오피니언<br>
                    <b style="color:#FBBF24;">7개 정론 아카이브</b>
                </div>
                <a href="/category/lee-note/" class="glass-pill-btn glass-pill-btn-small" style="font-size:11.5px; padding:4px 12px; margin-top:12px; width:100%; border-color:#F59E0B;">
                    열람하기 ↓
                </a>
            </div>

        </div>

    </div>
</section>

<!-- 2. RELOCATED STRATEGIC REVIEW EXECUTIVE BANNER (Directly above #top10-grid) -->
<section id="executive-review" style="max-width:1180px; margin:50px auto 0 auto; padding:0 24px;">
    <div class="glass-card-3d glass-card-gold" style="padding:48px 40px; text-align:center; position:relative;">
        
        <!-- Top Status Pill -->
        <div style="display:inline-flex; align-items:center; gap:8px; margin-bottom:20px;">
            <span class="glass-pill-btn glass-pill-btn-small" style="background:rgba(217,119,6,0.25); border-color:#F59E0B; color:#FDE047 !important; font-weight:800; display:inline-flex; align-items:center; gap:8px;">
                <img src="<?php echo get_template_directory_uri(); ?>/images/icons/strategy_review.png" alt="Strategic Review" style="width:18px; height:18px; object-fit:contain;">
                UCKLab Strategic Review™ | Vol. 39 총괄 제언
            </span>
        </div>

        <!-- Main Title -->
        <h1 style="font-size:32px; font-weight:900; color:#FFFFFF !important; margin:0 0 16px 0; line-height:1.35; letter-spacing:-0.5px; word-break:keep-all; text-shadow:0 2px 8px rgba(0,0,0,0.85);">
            AGI 문명적 대전환과 지정학적 금융·안보 패러다임의 미래 전망
        </h1>

        <!-- Subtitle -->
        <p style="font-size:16.5px; color:#E2E8F0 !important; max-width:860px; margin:0 auto 36px auto; line-height:1.8; word-break:keep-all;">
            World Monitor 실시간 군사·분쟁 지능 망 x AI 융합 청지기 신학(Stewardship Theology) 정론 브리핑.<br>
            글로벌 패권 갈등과 자율 알고리즘 금융 통화 질서의 격변 속에서 국가와 기업이 견지해야 할 최고위 전략 프레임워크를 제시합니다.
        </p>

        <!-- 3 Executive Telemetry Metric Boxes -->
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:20px; max-width:920px; margin:0 auto 36px auto; text-align:center;">
            
            <div style="background:rgba(15, 23, 42, 0.7); border:1px solid rgba(255,255,255,0.14); border-radius:14px; padding:20px 16px;">
                <div style="font-size:26px; font-weight:900; color:#FBBF24; margin-bottom:4px; text-shadow:0 2px 6px rgba(245,158,11,0.4);">10대 분야</div>
                <div style="font-size:13.5px; font-weight:800; color:#FFFFFF !important; margin-bottom:6px;">핵심 카테고리 심층 분석</div>
                <div style="font-size:12.5px; color:#CBD5E1; font-weight:600;">정치·금융·국방·과학·사회 모니터링</div>
            </div>

            <div style="background:rgba(15, 23, 42, 0.7); border:1px solid rgba(255,255,255,0.14); border-radius:14px; padding:20px 16px;">
                <div style="font-size:26px; font-weight:900; color:#38BDF8; margin-bottom:4px; text-shadow:0 2px 6px rgba(56,189,248,0.4);">24 / 7</div>
                <div style="font-size:13.5px; font-weight:800; color:#FFFFFF !important; margin-bottom:6px;">실시간 OSINT 지능 망</div>
                <div style="font-size:12.5px; color:#CBD5E1; font-weight:600;">전 세계 분쟁 위협·위성 궤도 추적</div>
            </div>

            <div style="background:rgba(15, 23, 42, 0.7); border:1px solid rgba(255,255,255,0.14); border-radius:14px; padding:20px 16px;">
                <div style="font-size:26px; font-weight:900; color:#10B981; margin-bottom:4px; text-shadow:0 2px 6px rgba(16,185,129,0.4);">2,500 단어</div>
                <div style="font-size:13.5px; font-weight:800; color:#FFFFFF !important; margin-bottom:6px;">APA 7th 학술 저널 PDF</div>
                <div style="font-size:12.5px; color:#CBD5E1; font-weight:600;">연구 방법론·실증 통계·공인 참고문헌</div>
            </div>

        </div>

        <!-- 3D Glass Pill Action CTA Buttons -->
        <div style="display:flex; justify-content:center; gap:16px; flex-wrap:wrap;">
            <a href="#top10-grid" class="glass-pill-btn" style="padding:14px 30px; font-size:15px;">
                📖 UCKLab Executive Note™ (500단어 요약 보기)
            </a>
            <a href="https://ucklab.org/api/v1/academic/upgrade?topic=AGI_Monograph_Vol39" class="glass-pill-btn glass-pill-btn-gold" style="padding:14px 34px; font-size:15px;">
                🎓 UCKLab Monograph™ 학술 저널 발급 ➔
            </a>
        </div>

    </div>
</section>

<!-- 3. BOTTOM 3-COLUMN FOCUS CARDS BLOCK -->
<main id="top10-grid" style="max-width:1180px; margin:40px auto 60px auto; padding:0 24px;">
    
    <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:28px; flex-wrap:wrap; gap:14px;">
        <div>
            <div style="font-size:12.5px; font-weight:800; color:#F59E0B; letter-spacing:1px; text-transform:uppercase; margin-bottom:6px; display:flex; align-items:center; gap:8px;">
                <img src="<?php echo get_template_directory_uri(); ?>/images/icons/pillars_core.png" alt="Core Pillars" style="width:18px; height:18px; object-fit:contain;">
                THREE CORE PILLARS OF UCKLAB INTELLIGENCE
            </div>
            <h2 style="font-size:26px; font-weight:900; color:#FFFFFF !important; margin:0; text-shadow:0 2px 6px rgba(0,0,0,0.8);">
                주간 정론 인텔리전스 3대 축 (Core Focus Grid)
            </h2>
        </div>
        <div>
            <a href="/category/news-top10/" class="glass-pill-btn glass-pill-btn-small" style="font-size:13px;">
                10대 카테고리 전체 탐색 ➔
            </a>
        </div>
    </div>

    <!-- 3-Column Glass Card Grid -->
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:24px;">
        
        <!-- Card 1: Executive Note (500단어 브리핑) -->
        <div class="glass-card-3d" style="padding:32px 28px; display:flex; flex-direction:column; justify-content:space-between;">
            <div>
                <div style="width:52px; height:52px; border-radius:14px; background:linear-gradient(135deg, rgba(56,189,248,0.2) 0%, rgba(2,132,199,0.3) 100%); border:1px solid rgba(56,189,248,0.5); display:flex; align-items:center; justify-content:center; margin-bottom:20px; box-shadow:0 8px 20px rgba(56,189,248,0.25);">
                    <img src="<?php echo get_template_directory_uri(); ?>/images/icons/weekly_briefing.png" alt="Weekly Briefing" style="width:36px; height:36px; object-fit:contain; filter:drop-shadow(0 4px 8px rgba(0,0,0,0.4));">
                </div>
                <div style="font-size:12px; font-weight:800; color:#38BDF8; letter-spacing:0.5px; margin-bottom:8px;">STAGE 1 • WEEKLY BRIEFING</div>
                <h3 style="font-size:21px; font-weight:900; color:#FFFFFF !important; margin:0 0 12px 0; line-height:1.35; text-shadow:0 1px 3px rgba(0,0,0,0.7);">
                    UCKLab Executive Note™
                </h3>
                <p style="font-size:15px; color:#E2E8F0 !important; line-height:1.8; margin-bottom:24px;">
                    당주 가장 파급력이 큰 10대 카테고리 핵심 이슈와 U-Radar 지수를 500단어 요약과 정론 칼럼으로 전달합니다.
                </p>
            </div>
            <div>
                <a href="/category/news-top10/" class="glass-pill-btn glass-pill-btn-blue glass-pill-btn-small" style="width:100%;">
                    리뷰 전체 보기 (200자 요약) ➔
                </a>
            </div>
        </div>

        <!-- Card 2: Editorial Column (이창배 Note) -->
        <div class="glass-card-3d" style="padding:32px 28px; display:flex; flex-direction:column; justify-content:space-between; border-color:rgba(245,158,11,0.5); box-shadow:0 20px 48px -8px rgba(0,0,0,0.6), 0 0 20px rgba(245,158,11,0.2);">
            <div>
                <div style="width:52px; height:52px; border-radius:14px; background:linear-gradient(135deg, rgba(245,158,11,0.3) 0%, rgba(217,119,6,0.4) 100%); border:1px solid rgba(245,158,11,0.7); display:flex; align-items:center; justify-content:center; margin-bottom:20px; box-shadow:0 8px 20px rgba(245,158,11,0.35);">
                    <img src="<?php echo get_template_directory_uri(); ?>/images/icons/quill_column.png" alt="Editorial Column" style="width:36px; height:36px; object-fit:contain; filter:drop-shadow(0 4px 8px rgba(0,0,0,0.4));">
                </div>
                <div style="font-size:12px; font-weight:800; color:#FBBF24; letter-spacing:0.5px; margin-bottom:8px;">STAGE 2 • SIGNATURE COLUMN</div>
                <h3 style="font-size:21px; font-weight:900; color:#FFFFFF !important; margin:0 0 12px 0; line-height:1.35; text-shadow:0 1px 3px rgba(0,0,0,0.7);">
                    이창배 Note™ 소장 칼럼
                </h3>
                <p style="font-size:15px; color:#E2E8F0 !important; line-height:1.8; margin-bottom:24px;">
                    기술 가속도 속에서 흔들리지 않는 청지기적 분별력과 글로벌 지정학 리스크에 대한 깊이 있는 시사 분석을 제시합니다.
                </p>
            </div>
            <div>
                <a href="/category/lee-note/" class="glass-pill-btn glass-pill-btn-gold glass-pill-btn-small" style="width:100%;">
                    칼럼 아카이브 전체 읽기 (7편) ➔
                </a>
            </div>
        </div>

        <!-- Card 3: Monograph (2,500단어 APA 7th 저널) -->
        <div class="glass-card-3d glass-card-gold" style="padding:32px 28px; display:flex; flex-direction:column; justify-content:space-between;">
            <div>
                <div style="width:52px; height:52px; border-radius:14px; background:linear-gradient(135deg, rgba(245,158,11,0.3) 0%, rgba(217,119,6,0.4) 100%); border:1px solid rgba(245,158,11,0.7); display:flex; align-items:center; justify-content:center; margin-bottom:20px; box-shadow:0 8px 20px rgba(217,119,6,0.35);">
                    <img src="<?php echo get_template_directory_uri(); ?>/images/icons/academic_monograph.png" alt="Academic Monograph" style="width:36px; height:36px; object-fit:contain; filter:drop-shadow(0 4px 8px rgba(0,0,0,0.4));">
                </div>
                <div style="font-size:12px; font-weight:800; color:#FDE047; letter-spacing:0.5px; margin-bottom:8px;">STAGE 3 • ACADEMIC JOURNAL</div>
                <h3 style="font-size:21px; font-weight:900; color:#FFFFFF !important; margin:0 0 12px 0; line-height:1.35; text-shadow:0 1px 3px rgba(0,0,0,0.7);">
                    UCKLab Monograph™
                </h3>
                <p style="font-size:15px; color:#E2E8F0 !important; line-height:1.8; margin-bottom:24px;">
                    2,500단어 APA 7th 규격의 한국어 학술 저널 PDF를 실시간 생성하여 신뢰할 수 있는 학술 연구 논거를 제공합니다.
                </p>
            </div>
            <div>
                <a href="https://ucklab.org/research" class="glass-pill-btn glass-pill-btn-gold glass-pill-btn-small" style="width:100%;">
                    저널 PDF 발급 받기 (9,900원) ➔
                </a>
            </div>
        </div>

    </div>

</main>

<script>
let isMapInteractive = false;
let isHudVisible = true;

function toggleMapInteraction() {
    const iframe = document.getElementById('osintIframe');
    const btn = document.getElementById('mapInteractiveToggle');

    isMapInteractive = !isMapInteractive;
    if (isMapInteractive) {
        iframe.style.filter = 'none';
        iframe.style.zIndex = '15';
        btn.innerHTML = '🔒 HUD 고정 모드로 복귀';
        btn.classList.remove('glass-pill-btn-blue');
        btn.classList.add('glass-pill-btn-gold');
    } else {
        iframe.style.filter = 'contrast(1.1) brightness(0.85)';
        iframe.style.zIndex = '1';
        btn.innerHTML = '🗺️ 레이더 직접 탐색 (Interactive)';
        btn.classList.remove('glass-pill-btn-gold');
        btn.classList.add('glass-pill-btn-blue');
    }
}

function toggleHudVisibility() {
    const hudWidgets = document.querySelector('.hotspot-grid');
    isHudVisible = !isHudVisible;
    hudWidgets.style.display = isHudVisible ? 'grid' : 'none';
}
</script>

<?php get_footer(); ?>
