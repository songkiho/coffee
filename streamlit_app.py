import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# 1. 앱 설정 및 커스텀 CSS (아이폰 감성 디자인)
st.set_page_config(page_title="Seongsu Coffee", page_icon="☕", layout="centered")

st.markdown("""
    <style>
    /* 메인 배경색 */
    .stApp { background-color: #F2F2F7; }
    
    /* 버튼 디자인 */
    div.stButton > button {
        width: 100%;
        border-radius: 15px;
        border: none;
        height: 3.5rem;
        background-color: #007AFF; /* Apple Blue */
        color: white;
        font-weight: bold;
        font-size: 1.1rem;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        transition: all 0.2s;
    }
    div.stButton > button:hover { background-color: #0051A8; transform: scale(1.02); }
    
    /* 카드형 섹션 디자인 */
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0px 2px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    
    /* 텍스트 스타일링 */
    h1, h2, h3 { color: #1C1C1E; font-family: 'Apple SD Gothic Neo', sans-serif; }
    .stMarkdown { font-family: 'Apple SD Gothic Neo', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# 2. 상단 헤더
st.title("☕ 성수동 점심 가이드")
st.caption(f"Today: {datetime.now().strftime('%Y년 %m월 %d일')}")

# --- [STEP 1: 위치 및 온누리 지도 카드] ---
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📍 내 주변 핫플 & 가맹점")
col_loc1, col_loc2 = st.columns(2)

with col_loc1:
    loc_url = "https://m.map.naver.com/search2/search.naver?query=" + urllib.parse.quote("현재 내 위치")
    st.link_button("🔍 내 위치 확인", loc_url)
with col_loc2:
    onnuri_url = "https://m.map.naver.com/search2/search.naver?query=" + urllib.parse.quote("내 주변 온누리 가맹 식당 카페")
    st.link_button("💳 온누리 가맹점", onnuri_url)
st.markdown('</div>', unsafe_allow_html=True)

# --- [STEP 2: 커피 순번 카드] ---
members = ["규리", "조조", "은비", "까비"]
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'history_list' not in st.session_state: st.session_state.history_list = []

st.markdown('<div class="card">', unsafe_allow_html=True)
current_person = members[st.session_state.current_idx]
st.markdown(f"### 🚩 오늘의 당번: <span style='color:#007AFF;'>{current_person}</span> 님", unsafe_allow_html=True)

if st.button("✅ 결제 완료 (다음 순번으로)"):
    now = datetime.now().strftime("%m/%d %H:%M")
    st.session_state.history_list.append({"날짜": now, "이름": current_person})
    st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
    st.rerun()

# 누적 기록을 깔끔하게 표시
tab1, tab2 = st.tabs(["📊 통계", "📜 기록"])
with tab1:
    df = pd.DataFrame(st.session_state.history_list)
    stats = df['이름'].value_counts().reindex(members, fill_value=0).reset_index() if not df.empty else pd.DataFrame(members, columns=['이름']).assign(횟수=0)
    stats.columns = ['이름', '구매회수']
    st.dataframe(stats, use_container_width=True, hide_index=True)
with tab2:
    recent_3 = st.session_state.history_list[-3:][::-1] if st.session_state.history_list else []
    st.dataframe(pd.DataFrame(recent_3), use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- [STEP 3: 실시간 정보 링크] ---
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🔗 퀵 링크")
col_link1, col_link2 = st.columns(2)

with col_link1:
    st.link_button("🍱 메뉴 확인", "https://pf.kakao.com/_jxcvzn/posts")
with col_link2:
    popup_q = urllib.parse.quote("2026년 성수동 팝업스토어")
    st.link_button("🔥 2026 팝업", f"https://search.naver.com/search.naver?query={popup_q}")
st.markdown('</div>', unsafe_allow_html=True)

# --- [하단 관리 기능] ---
with st.expander("🛠️ 시스템 설정"):
    if st.button("🔄 모든 데이터 리셋"):
        st.session_state.current_idx = 0
        st.session_state.history_list = []
        st.rerun()
