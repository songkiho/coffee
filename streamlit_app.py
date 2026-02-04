import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
import streamlit.components.v1 as components

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
    
    /* 사이드바 중첩 방지 */
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
    
    /* 웹 뷰 박스 컨테이너 */
    .webview-container {
        border: 2px solid #E5E5EA;
        border-radius: 15px;
        overflow: hidden;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 데이터 초기화 ---
members = ["규리", "조조", "은비", "까비"]
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'history_list' not in st.session_state: st.session_state.history_list = []
if 'pass_list' not in st.session_state: st.session_state.pass_list = []
if 'admin_mode' not in st.session_state: st.session_state.admin_mode = False
# 화면 표시 상태 관리
if 'view_state' not in st.session_state: st.session_state.view_state = None 

# --- ⬅️ 좌측 사이드바 (통계 센터) ---
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

# --- 🔗 성수동 실시간 정보 (앱 내 보기) ---
st.subheader("🔗 성수동 실시간 정보")

btn_col1, btn_col2 = st.columns(2)

with btn_col1:
    if st.button("🍱 오늘 메뉴 보기", use_container_width=True):
        st.session_state.view_state = 'menu' if st.session_state.view_state != 'menu' else None

with btn_col2:
    if st.button("🔥 성수 팝업 검색", use_container_width=True):
        st.session_state.view_state = 'popup' if st.session_state.view_state != 'popup' else None

# 선택된 화면에 따른 iframe 표시
if st.session_state.view_state == 'menu':
    url = "https://pf.kakao.com/_jxcvzn/posts"
    st.markdown('**🍱 카카오 채널 메뉴판**')
    st.markdown('<div class="webview-container">', unsafe_allow_html=True)
    components.iframe(url, height=600, scrolling=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.link_button("🌐 외부 브라우저로 보기", url, use_container_width=True)

elif st.session_state.view_state == 'popup':
    query = urllib.parse.quote("2026년 성수동 팝업스토어")
    url = f"https://search.naver.com/search.naver?query={query}"
    st.markdown('**🔥 네이버 팝업 검색 결과**')
    st.info("💡 네이버는 보안상 앱 내 보기를 차단할 수 있습니다. 화면이 안 나오면 아래 버튼을 눌러주세요.")
    st.markdown('<div class="webview-container">', unsafe_allow_html=True)
    components.iframe(url, height=600, scrolling=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.link_button("🌐 외부 브라우저로 보기", url, use_container_width=True)
