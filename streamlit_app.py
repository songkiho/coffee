import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# 1. 앱 설정
st.set_page_config(page_title="커피당번", page_icon="☕", layout="centered")

# 2. 고대비 디자인 (글자색 강제 설정)
st.markdown("""
    <style>
    /* 전체 배경을 밝은색으로 고정 */
    .stApp { background-color: #FFFFFF !important; }
    
    /* 모든 텍스트를 진한 검은색으로 고정 */
    h1, h2, h3, p, span, div, label { color: #000000 !important; font-family: 'Apple SD Gothic Neo', sans-serif !important; }

    /* 메인 버튼: 검정 배경 + 흰색 글자 (최고의 대조) */
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 4.5rem;
        background-color: #1C1C1E !important; /* 아주 진한 검정 */
        color: #FFFFFF !important; /* 순백색 */
        font-weight: 800 !important;
        font-size: 1.3rem !important;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    
    /* 구입 현황 표 스타일 보정 */
    .stTable { background-color: #FFFFFF !important; }
    .stTable td, .stTable th { 
        color: #000000 !important; 
        font-size: 1.1rem !important; 
        border-bottom: 1px solid #EEEEEE !important; 
    }

    /* 링크 버튼 (오늘 메뉴 등) */
    .link-btn div.stButton > button {
        background-color: #F2F2F7 !important;
        color: #007AFF !important;
        border: 1px solid #D1D1D6 !important;
        height: 3.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 상단 헤더
st.markdown('# ☕ 커피당번')
st.markdown(f"**{datetime.now().strftime('%Y년 %m월 %d일')}**")

# --- 당번 섹션 ---
members = ["규리", "조조", "은비", "까비"]
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'history_list' not in st.session_state: st.session_state.history_list = []

st.markdown(f"### 🚩 오늘의 당번")
st.markdown(f"<h1 style='color: #007AFF !important; font-size: 3.5rem;'>{members[st.session_state.current_idx]}</h1>", unsafe_allow_html=True)

if st.button("✅ 결제 완료 ! 다음 순번으로"):
    now = datetime.now().strftime("%m/%d %H:%M")
    st.session_state.history_list.append({"날짜": now, "이름": members[st.session_state.current_idx]})
    st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
    st.rerun()

st.divider()

# --- 구입 현황 섹션 ---
st.markdown("### 📊 구입 현황")
df = pd.DataFrame(st.session_state.history_list)
stats = df['이름'].value_counts().reindex(members, fill_value=0).reset_index() if not df.empty else pd.DataFrame(members, columns=['이름']).assign(count=0)
stats.columns = ['이름', '횟수']

# 표 출력 (index 없이 깨끗하게)
st.table(stats)

if not df.empty:
    st.markdown("**🕒 최근 기록**")
    st.table(df.iloc[::-1].head(3))

st.divider()

# --- 하단 링크 ---
st.markdown('<div class="link-btn">', unsafe_allow_html=True)
st.link_button("🍱 오늘 메뉴 확인 (카카오 채널)", "https://pf.kakao.com/_jxcvzn/posts", use_container_width=True)
popup_q = urllib.parse.quote("2026년 성수동 팝업스토어 최신")
st.link_button("🔥 2026 성수 팝업 검색", f"https://search.naver.com/search.naver?query={popup_q}", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

with st.expander("🛠️ 초기화"):
    if st.button("🔄 기록 리셋"):
        st.session_state.current_idx = 0
        st.session_state.history_list = []
        st.rerun()
