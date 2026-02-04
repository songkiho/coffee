import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# 1. 앱 설정
st.set_page_config(page_title="커피당번", page_icon="☕", layout="centered")

# 2. 디자인 설정 (가시성 및 중첩 방지)
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    h1, h2, h3, p, span, div, label { 
        color: #1C1C1E !important; 
        font-family: 'Apple SD Gothic Neo', sans-serif !important; 
    }

    /* 메인 결제 버튼 (녹색) */
    .main-btn div.stButton > button {
        width: 100%;
        border-radius: 16px;
        height: 5rem;
        background-color: #28A745 !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 1.5rem !important;
    }
    
    /* 패스 버튼 (오렌지색) */
    .pass-btn div.stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 3.5rem;
        background-color: #FF9500 !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        border: none;
    }

    .winner-box {
        color: #007AFF !important;
        font-size: 3.8rem !important;
        font-weight: 900 !important;
        margin: 10px 0;
        text-align: center;
    }

    .admin-section {
        margin-top: 50px;
        padding: 20px;
        background-color: #F2F2F7;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 데이터 초기화 ---
members = ["규리", "조조", "은비", "까비"]

if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'history_list' not in st.session_state: st.session_state.history_list = []
if 'pass_list' not in st.session_state: st.session_state.pass_list = [] # 지각/휴가 기록용
if 'show_admin' not in st.session_state: st.session_state.show_admin = False

# --- 메인 화면 ---
st.markdown('# ☕ 커피당번')
st.markdown("---")
st.markdown("### 🚩 이번에 커피 쏠 사람")
current_name = members[st.session_state.current_idx]
st.markdown(f'<div class="winner-box">{current_name}</div>', unsafe_allow_html=True)

# [기능 1] 결제 완료 버튼
st.markdown('<div class="main-btn">', unsafe_allow_html=True)
if st.button("✅ 결제 완료 ! 다음 사람으로"):
    now = datetime.now().strftime("%m/%d %H:%M")
    st.session_state.history_list.append({"날짜": now, "이름": current_name})
    st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# [기능 2] PASS 버튼 (지각/휴가)
st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
col_late, col_vacation = st.columns(2)

with col_late:
    st.markdown('<div class="pass-btn">', unsafe_allow_html=True)
    if st.button("⏰ 지각 PASS"):
        st.session_state.pass_list.append({"이름": current_name, "사유": "지각"})
        st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col_vacation:
    st.markdown('<div class="pass-btn">', unsafe_allow_html=True)
    if st.button("🌴 휴가 PASS"):
        st.session_state.pass_list.append({"이름": current_name, "사유": "휴가"})
        st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# --- 통계 섹션 ---
st.markdown("### 📊 구입 현황")
df_hist = pd.DataFrame(st.session_state.history_list)
stats = df_hist['이름'].value_counts().reindex(members, fill_value=0).reset_index() if not df_hist.empty else pd.DataFrame(members, columns=['이름']).assign(count=0)
stats.columns = ['이름', '커피 구매 횟수']
st.table(stats)

# [기능 3] 지각/휴가 차트 (PASS 카운트)
st.markdown("### 🚫 지각/휴가 현황 (PASS)")
df_pass = pd.DataFrame(st.session_state.pass_list)
if not df_pass.empty:
    # 사유별로 카운트하여 표로 표시
    pass_stats = df_pass.groupby(['이름', '사유']).size().unstack(fill_value=0).reindex(members, fill_value=0).reset_index()
    st.table(pass_stats)
else:
    st.write("깨끗합니다! 아직 지각/휴가자가 없네요.")

st.markdown("---")

# --- 퀵 링크 ---
col_menu, col_pop = st.columns(2)
with col_menu:
    st.link_button("🍱 오늘 메뉴", "https://pf.kakao.com/_jxcvzn/posts", use_container_width=True)
with col_pop:
    popup_q = urllib.parse.quote("2026년 성수동 팝업스토어 최신")
    st.link_button("🔥 2026 팝업", f"https://search.naver.com/search.naver?query={popup_q}", use_container_width=True)

# --- 관리자 리셋 ---
st.markdown('<div class="admin-section">', unsafe_allow_html=True)
if not st.session_state.show_admin:
    if st.button("🛠️ 데이터 관리"):
        st.session_state.show_admin = True
        st.rerun()
else:
    pw = st.text_input("비밀번호", type="password")
    if st.button("🔄 모든 기록 초기화"):
        if pw == "123qwe..":
            st.session_state.current_idx = 0
            st.session_state.history_list = []
            st.session_state.pass_list = []
            st.session_state.show_admin = False
            st.success("리셋 완료")
            st.rerun()
        else:
            st.error("비번 틀림")
    if st.button("닫기"):
        st.session_state.show_admin = False
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
