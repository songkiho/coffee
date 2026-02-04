import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# 1. 앱 설정 및 고대비 디자인
st.set_page_config(page_title="커피당번", page_icon="☕", layout="centered")

st.markdown("""
    <style>
    /* 배경 및 기본 폰트 설정 */
    .stApp { background-color: #FFFFFF !important; }
    h1, h2, h3, p, span, div, label { 
        color: #1C1C1E !important; 
        font-family: 'Apple SD Gothic Neo', sans-serif !important; 
    }

    /* 메인 카드 박스 디자인 */
    .info-card {
        background-color: #F2F2F7;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #E5E5EA;
        text-align: center;
        margin-bottom: 20px;
    }

    /* 당번 이름 강조 */
    .winner-name {
        color: #007AFF !important;
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        margin: 10px 0;
    }

    /* 버튼 스타일링 */
    div.stButton > button {
        width: 100%;
        border-radius: 15px;
        font-weight: 800 !important;
        border: none !important;
    }

    /* 결제 버튼 (녹색) */
    .buy-btn div.stButton > button {
        height: 5.5rem;
        background-color: #28A745 !important;
        color: white !important;
        font-size: 1.5rem !important;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
    }

    /* 패스 버튼 (주황색) */
    .pass-btn div.stButton > button {
        height: 3.5rem;
        background-color: #FF9500 !important;
        color: white !important;
        font-size: 1.1rem !important;
    }

    /* 링크 버튼 (연회색) */
    .link-btn div.stButton > button {
        height: 3.5rem;
        background-color: #E5E5EA !important;
        color: #007AFF !important;
        font-size: 1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 데이터 초기화 ---
members = ["규리", "조조", "은비", "까비"]
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'history_list' not in st.session_state: st.session_state.history_list = []
if 'pass_list' not in st.session_state: st.session_state.pass_list = []
if 'show_admin' not in st.session_state: st.session_state.show_admin = False

# --- 메인 화면 ---
st.markdown('# ☕ 커피당번')
current_name = members[st.session_state.current_idx]

st.markdown(f"""
    <div class="info-card">
        <p style='margin-bottom:0px;'>오늘 커피 쏠 사람은?</p>
        <div class="winner-name">{current_name}</div>
    </div>
    """, unsafe_allow_html=True)

# 결제 완료 버튼
st.markdown('<div class="buy-btn">', unsafe_allow_html=True)
if st.button("✅ 결제 완료 ! 다음 사람으로"):
    now = datetime.now().strftime("%m/%d %H:%M")
    st.session_state.history_list.append({"날짜": now, "이름": current_name})
    st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# 패스 버튼 섹션 (지각/휴가)
st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
col_l, col_v = st.columns(2)
with col_l:
    st.markdown('<div class="pass-btn">', unsafe_allow_html=True)
    if st.button("⏰ 지각 PASS"):
        st.session_state.pass_list.append({"이름": current_name, "사유": "지각"})
        st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
with col_v:
    st.markdown('<div class="pass-btn">', unsafe_allow_html=True)
    if st.button("🌴 휴가 PASS"):
        st.session_state.pass_list.append({"이름": current_name, "사유": "휴가"})
        st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# --- 통계 섹션 ---
st.markdown("### 📊 구입 및 패스 현황")
df_h = pd.DataFrame(st.session_state.history_list)
stats = df_h['이름'].value_counts().reindex(members, fill_value=0).reset_index() if not df_h.empty else pd.DataFrame(members, columns=['이름']).assign(count=0)
stats.columns = ['이름', '커피 구매 횟수']
st.table(stats)

df_p = pd.DataFrame(st.session_state.pass_list)
if not df_p.empty:
    st.markdown("**🚫 지각/휴가 현황 (PASS)**")
    p_stats = df_p.groupby(['이름', '사유']).size().unstack(fill_value=0).reindex(members, fill_value=0).reset_index()
    st.table(p_stats)

# --- 퀵 링크 ---
st.markdown('<div class="link-btn">', unsafe_allow_html=True)
col_m, col_p = st.columns(2)
with col_m:
    st.link_button("🍱 오늘 메뉴", "https://pf.kakao.com/_jxcvzn/posts", use_container_width=True)
with col_p:
    p_query = urllib.parse.quote("2026년 성수동 팝업스토어")
    st.link_button("🔥 성수 팝업", f"https://search.naver.com/search.naver?query={p_query}", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- 관리자 비밀번호 리셋 ---
st.markdown("<div style='margin-top:50px;'></div>", unsafe_allow_html=True)
if not st.session_state.show_admin:
    if st.button("🛠️ 데이터 관리"):
        st.session_state.show_admin = True
        st.rerun()
else:
    pw = st.text_input("비밀번호 입력", type="password")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔄 기록 리셋"):
            if pw == "123qwe..":
                st.session_state.current_idx = 0
                st.session_state.history_list = []
                st.session_state.pass_list = []
                st.session_state.show_admin = False
                st.rerun()
            else: st.error("비번 오류")
    with c2:
        if st.button("취소"):
            st.session_state.show_admin = False
            st.rerun()
