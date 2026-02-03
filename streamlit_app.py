import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# 1. 앱 설정
st.set_page_config(page_title="커피당번", page_icon="☕", layout="centered")

# 2. 디자인 보정 (중첩의 원인인 시스템 아이콘 강제 삭제)
st.markdown("""
    <style>
    /* 배경 및 기본 폰트 설정 */
    .stApp { background-color: #FFFFFF !important; }
    h1, h2, h3, p, span, div, label { 
        color: #1C1C1E !important; 
        font-family: 'Apple SD Gothic Neo', sans-serif !important; 
    }

    /* 시스템 텍스트 중첩 방지 (arrow_drop_down 등 제거) */
    span[data-testid="stWidgetLabel"] p { display: inline-block !important; }
    
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

    /* 초기화 구역 디자인 */
    .admin-section {
        margin-top: 60px;
        padding: 25px;
        background-color: #F2F2F7;
        border-radius: 15px;
        text-align: center;
    }
    
    /* 빨간색 리셋 버튼 */
    .reset-btn div.stButton > button {
        background-color: #FF3B30 !important;
        color: #FFFFFF !important;
        height: 3rem;
        border: none;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 멤버 및 데이터 로드 ---
members = ["규리", "조조", "은비", "까비"]
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'history_list' not in st.session_state: st.session_state.history_list = []
if 'show_admin' not in st.session_state: st.session_state.show_admin = False

# --- 상단 레이아웃 ---
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
col_menu, col_pop = st.columns(2)
with col_menu:
    st.link_button("🍱 오늘 메뉴", "https://pf.kakao.com/_jxcvzn/posts", use_container_width=True)
with col_pop:
    popup_q = urllib.parse.quote("2026년 성수동 팝업스토어 최신")
    st.link_button("🔥 2026 팝업", f"https://search.naver.com/search.naver?query={popup_q}", use_container_width=True)

# --- 🔐 관리자 초기화 섹션 (중첩 방지형) ---
st.markdown('<div class="admin-section">', unsafe_allow_html=True)
st.markdown("<p style='font-size: 0.9rem; color: #8E8E93 !important;'>데이터 관리가 필요하신가요?</p>", unsafe_allow_html=True)

# 버튼을 눌러야 비밀번호 입력창이 나타남
if not st.session_state.show_admin:
    if st.button("🛠️ 관리자 모드 열기"):
        st.session_state.show_admin = True
        st.rerun()
else:
    input_pw = st.text_input("비밀번호 입력", type="password")
    col_res, col_can = st.columns(2)
    with col_res:
        st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
        if st.button("🔄 기록 리셋"):
            if input_pw == "123qwe..":
                st.session_state.current_idx = 0
                st.session_state.history_list = []
                st.session_state.show_admin = False
                st.success("초기화 완료!")
                st.rerun()
            else:
                st.error("비번 오류")
        st.markdown('</div>', unsafe_allow_html=True)
    with col_can:
        if st.button("취소"):
            st.session_state.show_admin = False
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
