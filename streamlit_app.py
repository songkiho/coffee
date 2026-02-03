import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# 1. 앱 설정
st.set_page_config(page_title="커피당번", page_icon="☕", layout="centered")

# 2. 디자인 보정 (중첩 방지 및 가시성 강화)
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    h1, h2, h3, p, span, div, label { 
        color: #1C1C1E !important; 
        font-family: 'Apple SD Gothic Neo', sans-serif !important; 
    }

    /* 메인 녹색 버튼 */
    .main-btn div.stButton > button {
        width: 100%;
        border-radius: 16px;
        height: 5rem;
        background-color: #28A745 !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 1.5rem !important;
        border: none;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
    }
    
    /* 당번 이름 강조 */
    .winner-box {
        color: #007AFF !important;
        font-size: 3.8rem !important;
        font-weight: 900 !important;
        margin: 10px 0;
        text-align: center;
    }

    /* 하단 링크 버튼 */
    .link-section div.stButton > button {
        background-color: #F2F2F7 !important;
        color: #007AFF !important;
        border: 1px solid #D1D1D6 !important;
        height: 3.8rem;
        margin-bottom: 10px;
    }

    /* [수정] 초기화 버튼 구역 - 중첩 방지를 위해 테두리 및 여백 조정 */
    .reset-section {
        margin-top: 50px;
        padding: 20px;
        border-top: 1px solid #E5E5EA;
        text-align: center;
    }
    .reset-btn div.stButton > button {
        background-color: #FF3B30 !important; /* 경고의 빨간색 */
        color: #FFFFFF !important;
        height: 3rem;
        width: auto;
        padding: 0 30px;
        font-size: 1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 타이틀 및 당번 ---
st.markdown('# ☕ 커피당번')
members = ["규리", "조조", "은비", "까비"]
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'history_list' not in st.session_state: st.session_state.history_list = []

st.markdown("---")
st.markdown("### 🚩 이번에 커피 쏠 사람")
current_name = members[st.session_state.current_idx]
st.markdown(f'<div class="winner-box">{current_name}</div>', unsafe_allow_html=True)

st.markdown('<div class="main-btn">', unsafe_allow_html=True)
if st.button("✅ 결제 완료 ! 다음 사람으로"):
    now = datetime.now().strftime("%m/%d %H:%M")
    st.session_state.history_list.append({"날짜": now, "이름": current_name})
    st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- 통계 표 ---
st.markdown("### 📊 구입 현황")
df = pd.DataFrame(st.session_state.history_list)
stats = df['이름'].value_counts().reindex(members, fill_value=0).reset_index() if not df.empty else pd.DataFrame(members, columns=['이름']).assign(count=0)
stats.columns = ['이름', '횟수']
st.table(stats) # 인덱스 없이 깔끔하게 출력

# --- 퀵 링크 ---
st.markdown('<div class="link-section">', unsafe_allow_html=True)
st.link_button("🍱 오늘 메뉴 확인 (카카오 채널)", "https://pf.kakao.com/_jxcvzn/posts", use_container_width=True)
popup_q = urllib.parse.quote("2026년 성수동 팝업스토어 최신")
st.link_button("🔥 2026 성수 팝업 실시간 검색", f"https://search.naver.com/search.naver?query={popup_q}", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- [수정] 초기화 영역: 중첩 방지를 위해 expander 대신 일반 영역으로 분리 ---
st.markdown('<div class="reset-section">', unsafe_allow_html=True)
st.markdown("<p style='font-size: 0.9rem; color: #8E8E93 !important;'>데이터 관리가 필요하신가요?</p>", unsafe_allow_html=True)
st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
if st.button("🔄 전체 기록 리셋"):
    st.session_state.current_idx = 0
    st.session_state.history_list = []
    st.rerun()
st.markdown('</div></div>', unsafe_allow_html=True)
