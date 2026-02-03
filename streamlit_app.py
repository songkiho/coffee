import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# 1. 모바일 최적화 및 앱 이름 설정
st.set_page_config(
    page_title="커피당번", 
    page_icon="☕", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 고대비 모바일 전용 디자인
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    * { font-family: 'Apple SD Gothic Neo', sans-serif; color: #1C1C1E; }
    
    /* 메인 카드 박스 */
    .main-card {
        background-color: #F2F2F7;
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 20px;
        border: 1px solid #E5E5EA;
        text-align: center;
    }
    
    /* 당번 이름 강조 */
    .winner-name {
        color: #007AFF;
        font-size: 2.8rem;
        font-weight: 900;
        margin: 10px 0;
    }

    /* 메인 동작 버튼 (파란색) */
    div.stButton > button {
        width: 100%;
        border-radius: 15px;
        height: 4.8rem;
        background-color: #007AFF;
        color: #FFFFFF !important;
        font-weight: 800;
        font-size: 1.4rem;
        border: none;
        box-shadow: 0 4px 12px rgba(0,122,255,0.3);
    }
    
    /* 보조 링크 버튼 (흰색 배경) */
    .link-btn div.stButton > button {
        height: 3.8rem;
        background-color: #FFFFFF;
        color: #007AFF !important;
        border: 2px solid #007AFF;
        font-size: 1.1rem;
        box-shadow: none;
    }

    /* 테이블 가독성 */
    .stTable { background-color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- [상단 헤더] ---
st.markdown('# ☕ 커피당번')
st.markdown(f"**{datetime.now().strftime('%Y년 %m월 %d일')}**")

# --- [당번 안내 섹션] ---
members = ["규리", "조조", "은비", "까비"]
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'history_list' not in st.session_state: st.session_state.history_list = []

st.markdown('<div class="main-card">', unsafe_allow_html=True)
current_person = members[st.session_state.current_idx]
st.markdown(f"오늘 커피 쏠 사람은?", unsafe_allow_html=True)
st.markdown(f'<div class="winner-name">{current_person}</div>', unsafe_allow_html=True)

if st.button("✅ 결제 완료! 다음 순번으로"):
    now = datetime.now().strftime("%m/%d %H:%M")
    st.session_state.history_list.append({"날짜": now, "이름": current_person})
    st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- [주변 정보 섹션] ---
st.markdown("### 📍 주변 정보")

col1, col2 = st.columns(2)
with col1:
    loc_url = "https://m.map.naver.com/search2/search.naver?query=" + urllib.parse.quote("현재 내 위치")
    st.markdown('<div class="link-btn">', unsafe_allow_html=True)
    st.link_button("🔍 내 위치", loc_url, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    onnuri_url = "https://m.map.naver.com/search2/search.naver?query=" + urllib.parse.quote("내 주변 온누리 가맹 식당 카페")
    st.markdown('<div class="link-btn">', unsafe_allow_html=True)
    st.link_button("💳 온누리", onnuri_url, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="link-btn">', unsafe_allow_html=True)
st.link_button("🍱 오늘 메뉴 (카카오 채널)", "https://pf.kakao.com/_jxcvzn/posts", use_container_width=True)
popup_q = urllib.parse.quote("2026년 성수동 팝업스토어 최신")
st.link_button("🔥 2026 성수 팝업 실시간 검색", f"https://search.naver.com/search.naver?query={popup_q}", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- [데이터 관리] ---
with st.expander("📊 히스토리 및 통계"):
    if st.session_state.history_list:
        df = pd.DataFrame(st.session_state.history_list)
        stats = df['이름'].value_counts().reindex(members, fill_value=0).reset_index()
        stats.columns = ['이름', '구매횟수']
        st.table(stats)
        st.markdown("**최근 3회 내역**")
        st.table(pd.DataFrame(st.session_state.history_list[-3:][::-1]))
    else:
        st.write("기록이 없습니다.")

with st.expander("🛠️ 설정"):
    if st.button("🔄 기록 초기화"):
        st.session_state.current_idx = 0
        st.session_state.history_list = []
        st.rerun()
