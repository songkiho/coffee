import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# 1. 앱 설정 및 디자인
st.set_page_config(page_title="커피당번", page_icon="☕", layout="wide") # wide 모드로 분할 최적화

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    h1, h2, h3, p, span, div, label { 
        color: #1C1C1E !important; 
        font-family: 'Apple SD Gothic Neo', sans-serif !important; 
    }
    
    /* 사이드바 배경색 보정 */
    [data-testid="stSidebar"] {
        background-color: #F2F2F7 !important;
        border-right: 1px solid #E5E5EA;
    }

    /* 메인 카드 디자인 */
    .info-card {
        background-color: #F2F2F7;
        padding: 30px;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 25px;
    }

    .winner-name {
        color: #007AFF !important;
        font-size: 4.5rem !important;
        font-weight: 900 !important;
        margin: 15px 0;
    }

    /* 버튼 스타일 */
    .buy-btn div.stButton > button {
        width: 100%;
        border-radius: 20px;
        height: 6rem;
        background-color: #28A745 !important;
        color: white !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
    }
    
    .pass-btn div.stButton > button {
        height: 4rem;
        background-color: #FF9500 !important;
        color: white !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 데이터 로직 ---
members = ["규리", "조조", "은비", "까비"]
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'history_list' not in st.session_state: st.session_state.history_list = []
if 'pass_list' not in st.session_state: st.session_state.pass_list = []

# --- ⬅️ 좌측 사이드바 메뉴 ---
with st.sidebar:
    st.header("📊 통계 센터")
    
    # 1. 구입 횟수 통계
    df_h = pd.DataFrame(st.session_state.history_list)
    stats = df_h['이름'].value_counts().reindex(members, fill_value=0).reset_index() if not df_h.empty else pd.DataFrame(members, columns=['이름']).assign(count=0)
    stats.columns = ['이름', '커피 구매']
    st.subheader("💰 누적 구입")
    st.table(stats)
    
    # 2. PASS 현황 (지각/휴가)
    df_p = pd.DataFrame(st.session_state.pass_list)
    if not df_p.empty:
        st.subheader("🚫 패스 현황")
        p_stats = df_p.groupby(['이름', '사유']).size().unstack(fill_value=0).reindex(members, fill_value=0).reset_index()
        st.table(p_stats)
    
    st.divider()
    
    # 3. 데이터 초기화 (비번: 123qwe..)
    with st.expander("🛠️ 시스템 리셋"):
        pw = st.text_input("비밀번호", type="password")
        if st.button("🔄 전체 초기화"):
            if pw == "123qwe..":
                st.session_state.current_idx = 0
                st.session_state.history_list = []
                st.session_state.pass_list = []
                st.rerun()
            else: st.error("비번 틀림")

# --- ➡️ 우측 메인 화면 ---
st.title("☕ 커피당번")
current_name = members[st.session_state.current_idx]

st.markdown(f"""
    <div class="info-card">
        <p style='font-size:1.2rem; margin-bottom:0px;'>오늘 커피 주인공</p>
        <div class="winner-name">{current_name}</div>
    </div>
    """, unsafe_allow_html=True)

# 결제 및 패스 버튼
st.markdown('<div class="buy-btn">', unsafe_allow_html=True)
if st.button("✅ 오늘 결제 완료"):
    now = datetime.now().strftime("%m/%d %H:%M")
    st.session_state.history_list.append({"날짜": now, "이름": current_name})
    st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    st.markdown('<div class="pass-btn">', unsafe_allow_html=True)
    if st.button("⏰ 지각 PASS"):
        st.session_state.pass_list.append({"이름": current_name, "사유": "지각"})
        st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="pass-btn">', unsafe_allow_html=True)
    if st.button("🌴 휴가 PASS"):
        st.session_state.pass_list.append({"이름": current_name, "사유": "휴가"})
        st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# 퀵 링크
st.subheader("🔗 성수동 실시간 정보")
col_m, col_p = st.columns(2)
with col_m:
    st.link_button("🍱 오늘 메뉴 (카카오)", "https://pf.kakao.com/_jxcvzn/posts", use_container_width=True)
with col_p:
    p_q = urllib.parse.quote("2026년 성수동 팝업스토어")
    st.link_button("🔥 2026 성수 팝업", f"https://search.naver.com/search.naver?query={p_q}", use_container_width=True)
