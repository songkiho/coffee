import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# 1. 앱 설정
st.set_page_config(page_title="커피당번", page_icon="☕", layout="centered")

# 2. 디자인 보정 (시인성 및 레이아웃 최적화)
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

    /* 초기화 영역 디자인 */
    .reset-section {
        margin-top: 50px;
        padding: 20px;
        border-top: 1px solid #E5E5EA;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 기본 데이터 설정 ---
members = ["규리", "조조", "은비", "까비"]
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'history_list' not in st.session_state: st.session_state.history_list = []

# --- 상단 타이틀 및 당번 ---
st.markdown('# ☕ 커피당번')
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
st.table(stats)

# --- 퀵 링크 ---
st.markdown('<div class="link-section">', unsafe_allow_html=True)
st.link_button("🍱 오늘 메뉴 확인 (카카오 채널)", "https://pf.kakao.com/_jxcvzn/posts", use_container_width=True)
popup_q = urllib.parse.quote("2026년 성수동 팝업스토어 최신")
st.link_button("🔥 2026 성수 팝업 실시간 검색", f"https://search.naver.com/search.naver?query={popup_q}", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- 🔐 [추가] 관리자용 데이터 초기화 영역 ---
st.markdown('<div class="reset-section">', unsafe_allow_html=True)
with st.expander("🛠️ 데이터 초기화 (관리자전용)"):
    st.write("모든 기록을 삭제하려면 비밀번호를 입력하세요.")
    # 비밀번호 입력창 (type="password"로 별표 처리)
    input_pw = st.text_input("비밀번호 입력", type="password")
    
    if st.button("🔄 기록 리셋하기"):
        if input_pw == "123qwe..":
            st.session_state.current_idx = 0
            st.session_state.history_list = []
            st.success("모든 데이터가 초기화되었습니다.")
            st.rerun()
        else:
            st.error("비밀번호가 틀렸습니다.")
st.markdown('</div>', unsafe_allow_html=True)
