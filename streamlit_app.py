import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# 1. 앱 설정 및 고대비 테마 고정
st.set_page_config(page_title="커피당번", page_icon="☕", layout="centered")

st.markdown("""
    <style>
    /* 배경을 밝은 흰색으로 강제 고정하여 다크모드 간섭 방지 */
    .stApp { background-color: #FFFFFF !important; }
    
    /* 모든 텍스트 기본색을 진한 검정으로 설정 */
    h1, h2, h3, p, span, div, label { 
        color: #1C1C1E !important; 
        font-family: 'Apple SD Gothic Neo', sans-serif !important; 
    }

    /* [요청] 메인 버튼: 녹색 배경 + 흰색 글자 */
    div.stButton > button {
        width: 100%;
        border-radius: 16px;
        height: 5rem;
        background-color: #28A745 !important; /* 선명한 녹색 */
        color: #FFFFFF !important; /* 순백색 */
        font-weight: 800 !important;
        font-size: 1.5rem !important;
        border: none;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
        margin-top: 10px;
    }
    
    /* 당번 이름 강조 (파란색) */
    .winner-box {
        color: #007AFF !important;
        font-size: 3.8rem !important;
        font-weight: 900 !important;
        margin: 10px 0;
    }

    /* 표(구입 현황) 가시성 강화 */
    .stTable { 
        background-color: #FFFFFF !important; 
        border: 1px solid #E5E5EA !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    .stTable td { 
        font-size: 1.2rem !important; 
        color: #1C1C1E !important; 
        padding: 15px !important;
    }

    /* 하단 링크 버튼 (연한 회색 배경) */
    .link-section div.stButton > button {
        background-color: #F2F2F7 !important;
        color: #007AFF !important;
        border: 1px solid #D1D1D6 !important;
        height: 3.8rem;
        font-size: 1.1rem !important;
        box-shadow: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 상단 타이틀 ---
st.markdown('# ☕ 커피당번')
st.markdown(f"📅 **{datetime.now().strftime('%Y년 %m월 %d일')}**")

# --- 당번 확인 섹션 ---
members = ["규리", "조조", "은비", "까비"]
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'history_list' not in st.session_state: st.session_state.history_list = []

st.markdown("---")
st.markdown("### 🚩 이번에 커피 쏠 사람")
current_name = members[st.session_state.current_idx]
st.markdown(f'<div class="winner-box">{current_name}</div>', unsafe_allow_html=True)

# 메인 녹색 버튼
if st.button("✅ 결제 완료 ! 다음 사람으로"):
    now = datetime.now().strftime("%m/%d %H:%M")
    st.session_state.history_list.append({"날짜": now, "이름": current_name})
    st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
    st.rerun()

st.markdown("---")

# --- 데이터 통계 섹션 ---
st.markdown("### 📊 구입 현황")

df = pd.DataFrame(st.session_state.history_list)
# 누적 횟수 계산 (행 번호 없이 깔끔하게 표시하기 위해 스타일 조정)
stats = df['이름'].value_counts().reindex(members, fill_value=0).reset_index() if not df.empty else pd.DataFrame(members, columns=['이름']).assign(count=0)
stats.columns = ['이름', '횟수']

# [개선] 인덱스(0,1,2,3)를 제거하고 표만 출력
st.table(stats)

if not df.empty:
    st.markdown("**🕒 최근 기록 (최신순 3건)**")
    st.table(df.iloc[::-1].head(3))

st.markdown("---")

# --- 하단 링크 섹션 ---
st.markdown('<div class="link-section">', unsafe_allow_html=True)
st.link_button("🍱 오늘 메뉴 확인 (카카오 채널)", "https://pf.kakao.com/_jxcvzn/posts", use_container_width=True)
popup_q = urllib.parse.quote("2026년 성수동 팝업스토어 최신")
st.link_button("🔥 2026 성수 팝업 실시간 검색", f"https://search.naver.com/search.naver?query={popup_q}", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# 초기화 기능
with st.expander("🛠️ 데이터 초기화"):
    if st.button("🔄 기록 리셋"):
        st.session_state.current_idx = 0
        st.session_state.history_list = []
        st.rerun()
