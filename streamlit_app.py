import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
import streamlit.components.v1 as components # 웹 페이지 삽입을 위한 모듈

# 1. 앱 설정
st.set_page_config(page_title="커피당번", page_icon="☕", layout="wide")

# 2. 디자인 보정
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    h1, h2, h3, p, span, div, label { 
        color: #1C1C1E !important; 
        font-family: 'Apple SD Gothic Neo', sans-serif !important; 
    }
    
    /* 사이드바 보정 */
    [data-testid="stSidebar"] { background-color: #F2F2F7 !important; }
    [data-testid="stSidebar"] span, [data-testid="stSidebar"] svg { display: none !important; }

    /* 메인 당번 카드 */
    .info-card {
        background-color: #F2F2F7;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 20px;
    }
    .winner-name {
        color: #007AFF !important;
        font-size: 4rem !important;
        font-weight: 900 !important;
    }

    /* 버튼 스타일 */
    .stButton > button { width: 100%; border-radius: 12px !important; font-weight: bold !important; }
    .buy-btn div.stButton > button {
        height: 5rem;
        background-color: #28A745 !important;
        color: white !important;
        font-size: 1.5rem !important;
    }
    
    /* 웹 뷰 박스 테두리 */
    .webview-container {
        border: 2px solid #E5E5EA;
        border-radius: 15px;
        overflow: hidden;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 데이터 초기화 ---
members = ["규리", "조조", "은비", "까비"]
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'history_list' not in st.session_state: st.session_state.history_list = []
if 'pass_list' not in st.session_state: st.session_state.pass_list = []
if 'admin_mode' not in st.session_state: st.session_state.admin_mode = False
if 'show_menu' not in st.session_state: st.session_state.show_menu = False # 메뉴 박스 노출 여부

# --- ⬅️ 좌측 사이드바 (통계) ---
with st.sidebar:
    st.markdown("### 📊 통계 센터")
    df_h = pd.DataFrame(st.session_state.history_list)
    stats = df_h['이름'].value_counts().reindex(members, fill_value=0).reset_index() if not df_h.empty else pd.DataFrame(members, columns=['이름']).assign(count=0)
    stats.columns = ['이름', '횟수']
    st.table(stats)
    
    st.divider()
    if not st.session_state.admin_mode:
        if st.button("🔐 관리자 모드"): st.session_state.admin_mode = True; st.rerun()
    else:
        pw = st.text_input("비번", type="password")
        if st.button("🧨 리셋"):
            if pw == "123qwe..":
                st.session_state.current_idx = 0
                st.session_state.history_list = []
                st.session_state.pass_list = []
                st.session_state.admin_mode = False
                st.rerun()
        if st.button("닫기"): st.session_state.admin_mode = False; st.rerun()

# --- ➡️ 우측 메인 화면 ---
st.markdown("# ☕ 커피당번")
current_name = members[st.session_state.current_idx]

st.markdown(f"""
    <div class="info-card">
        <p style='color:#8E8E93 !important;'>오늘 커피 쏠 사람</p>
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

# PASS 버튼
col1, col2 = st.columns(2)
with col1:
    if st.button("⏰ 지각 PASS"):
        st.session_state.pass_list.append({"이름": current_name, "사유": "지각"})
        st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members); st.rerun()
with col2:
    if st.button("🌴 휴가 PASS"):
        st.session_state.pass_list.append({"이름": current_name, "사유": "휴가"})
        st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members); st.rerun()

st.divider()

# --- 🍱 오늘의 메뉴 앱 내 보기 기능 ---
st.subheader("🍱 오늘의 메뉴")

if st.button("📱 메뉴 화면 열기 / 닫기", use_container_width=True):
    st.session_state.show_menu = not st.session_state.show_menu

if st.session_state.show_menu:
    st.info("💡 화면이 나오지 않는다면 해당 사이트에서 보안상 막아둔 것입니다. 이럴 땐 아래 '새창으로 보기'를 눌러주세요.")
    # iframe 삽입 (박스 형태로 표시)
    st.markdown('<div class="webview-container">', unsafe_allow_html=True)
    components.iframe("https://pf.kakao.com/_jxcvzn/posts", height=500, scrolling=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.link_button("🌐 외부 브라우저(새창)로 열기", "https://pf.kakao.com/_jxcvzn/posts", use_container_width=True)

st.divider()

# 팝업 검색 (이건 네이버가 막아둘 확률이 높아 버튼으로 유지)
popup_q = urllib.parse.quote("2026년 성수동 팝업스토어")
st.link_button("🔥 2026 성수 팝업 검색 (새창)", f"https://search.naver.com/search.naver?query={popup_q}", use_container_width=True)
