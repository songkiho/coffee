import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
import streamlit.components.v1 as components

# 1. 앱 설정
st.set_page_config(page_title="커피당번", page_icon="☕", layout="wide")

# 2. 강력한 사이드바 UI 보정 (중첩 및 잔상 제거)
st.markdown("""
    <style>
    /* 기본 배경 및 폰트 */
    .stApp { background-color: #FFFFFF !important; }
    h1, h2, h3, p, div, span { font-family: 'Apple SD Gothic Neo', sans-serif !important; color: #1C1C1E !important; }

    /* 사이드바 내부 시스템 아이콘/화살표 완전 박멸 */
    [data-testid="stSidebar"] svg, [data-testid="stSidebar"] .st-emotion-cache-15zrgzn { display: none !important; }
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p { display: none !important; }

    /* 사이드바 배경 및 텍스트 가독성 */
    [data-testid="stSidebar"] { background-color: #F8F9FA !important; border-right: 1px solid #E5E5EA; }
    
    /* 사이드바 테이블 가독성 강화 */
    [data-testid="stSidebar"] .stTable td { font-size: 1rem !important; padding: 10px 5px !important; }

    /* 메인 카드 디자인 */
    .info-card {
        background-color: #F2F2F7;
        padding: 40px 20px;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 25px;
        border: 1px solid #E5E5EA;
    }
    .winner-name { color: #007AFF !important; font-size: 4.5rem !important; font-weight: 900 !important; }

    /* 메인 버튼 스타일 */
    .buy-btn div.stButton > button {
        height: 6rem;
        background-color: #28A745 !important;
        color: white !important;
        font-size: 1.8rem !important;
        border-radius: 20px !important;
        font-weight: 800 !important;
    }
    
    /* 사이드바 리셋 버튼 전용 스타일 (중첩 방지를 위해 단순화) */
    .sidebar-reset-btn button {
        background-color: #FF3B30 !important;
        color: white !important;
        height: 3rem !important;
        font-size: 1rem !important;
        width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 데이터 초기화 ---
members = ["규리", "조조", "은비", "까비"]
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'history_list' not in st.session_state: st.session_state.history_list = []
if 'pass_list' not in st.session_state: st.session_state.pass_list = []
if 'admin_open' not in st.session_state: st.session_state.admin_open = False
if 'view_state' not in st.session_state: st.session_state.view_state = None

# --- ⬅️ 좌측 사이드바 (구조 혁신) ---
with st.sidebar:
    st.title("📊 리포트")
    
    # 1. 누적 구입 (표 형식 유지하되 간결하게)
    st.markdown("### 💰 누적 커피")
    df_h = pd.DataFrame(st.session_state.history_list)
    stats = df_h['이름'].value_counts().reindex(members, fill_value=0).reset_index() if not df_h.empty else pd.DataFrame(members, columns=['이름']).assign(count=0)
    stats.columns = ['이름', '횟수']
    st.table(stats)
    
    # 2. 패스 기록
    st.markdown("### 🚫 패스 기록")
    df_p = pd.DataFrame(st.session_state.pass_list)
    if not df_p.empty:
        p_stats = df_p.groupby(['이름', '사유']).size().unstack(fill_value=0).reindex(members, fill_value=0).reset_index()
        st.table(p_stats)
    else:
        st.caption("패스 기록이 없습니다.")
    
    st.markdown("---")
    
    # 3. 시스템 관리 (버튼 대신 가벼운 토글 방식)
    st.markdown("### ⚙️ 설정")
    admin_toggle = st.checkbox("관리자 모드 활성화")
    
    if admin_toggle:
        pw = st.text_input("비밀번호", type="password", placeholder="비번 입력")
        st.markdown('<div class="sidebar-reset-btn">', unsafe_allow_html=True)
        if st.button("🧨 모든 기록 리셋"):
            if pw == "123qwe..":
                st.session_state.current_idx = 0
                st.session_state.history_list = []
                st.session_state.pass_list = []
                st.success("리셋 완료!")
                st.rerun()
            else:
                st.error("비번이 틀렸습니다.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- ➡️ 우측 메인 화면 ---
st.markdown("# ☕ 커피당번")
current_name = members[st.session_state.current_idx]

st.markdown(f"""
    <div class="info-card">
        <p style='color:#8E8E93 !important; font-size:1.2rem; margin-bottom:5px;'>오늘 커피 주인공</p>
        <div class="winner-name">{current_name}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="buy-btn">', unsafe_allow_html=True)
if st.button("✅ 오늘 결제 완료"):
    now = datetime.now().strftime("%m/%d %H:%M")
    st.session_state.history_list.append({"날짜": now, "이름": current_name})
    st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# 패스 버튼
st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    if st.button("⏰ 지각 PASS", use_container_width=True):
        st.session_state.pass_list.append({"이름": current_name, "사유": "지각"})
        st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members); st.rerun()
with c2:
    if st.button("🌴 휴가 PASS", use_container_width=True):
        st.session_state.pass_list.append({"이름": current_name, "사유": "휴가"})
        st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members); st.rerun()

st.divider()

# --- 하단 실시간 정보 ---
st.subheader("🔗 성수동 정보")
b1, b2 = st.columns(2)
with b1:
    if st.button("🍱 오늘 메뉴 보기", use_container_width=True):
        st.session_state.view_state = 'menu' if st.session_state.view_state != 'menu' else None
with b2:
    if st.button("🔥 성수 팝업 검색", use_container_width=True):
        st.session_state.view_state = 'popup' if st.session_state.view_state != 'popup' else None

if st.session_state.view_state == 'menu':
    st.info("💡 카카오 채널은 보안상 빈 화면이 나올 수 있습니다. (새창 버튼 이용 권장)")
    components.iframe("https://pf.kakao.com/_jxcvzn/posts", height=600, scrolling=True)
    st.link_button("🌐 외부 브라우저로 메뉴 보기", "https://pf.kakao.com/_jxcvzn/posts", use_container_width=True)
elif st.session_state.view_state == 'popup':
    query = urllib.parse.quote("2026년 성수동 팝업스토어")
    st.link_button("🌐 네이버 팝업 검색결과 새창으로 열기", f"https://search.naver.com/search.naver?query={query}", use_container_width=True)
