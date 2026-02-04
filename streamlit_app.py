import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# 1. 앱 설정
st.set_page_config(page_title="커피당번", page_icon="☕", layout="centered")

# 2. HTML/CSS 직접 주입 (프론트엔드 효과)
st.markdown("""
    <style>
    /* 아이폰 감성 배경 */
    .stApp { background-color: #F2F2F7 !important; }
    
    /* 카드형 프론트엔드 디자인 */
    .info-card {
        background-color: white;
        padding: 30px;
        border-radius: 25px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        margin-bottom: 25px;
        text-align: center;
    }
    
    .winner-label { color: #8E8E93; font-size: 1.1rem; font-weight: bold; }
    .winner-name { color: #007AFF; font-size: 4rem; font-weight: 900; margin: 10px 0; }
    
    /* 버튼 스타일링 (녹색) */
    .stButton > button {
        width: 100%;
        border-radius: 18px !important;
        height: 5.5rem !important;
        background-color: #34C759 !important; /* iOS Green */
        color: white !important;
        font-size: 1.6rem !important;
        font-weight: 800 !important;
        border: none !important;
        box-shadow: 0 8px 15px rgba(52, 199, 89, 0.3) !important;
    }
    
    /* 테이블 디자인 고정 */
    .stTable { background-color: white; border-radius: 15px; border: none; }
    </style>
    """, unsafe_allow_html=True)

# 데이터 로직
members = ["규리", "조조", "은비", "까비"]
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'history_list' not in st.session_state: st.session_state.history_list = []
if 'pass_list' not in st.session_state: st.session_state.pass_list = []

# --- [HTML로 구성한 메인 화면] ---
current_name = members[st.session_state.current_idx]

st.markdown(f"""
    <div class="info-card">
        <div class="winner-label">오늘의 커피 주인공</div>
        <div class="winner-name">{current_name}</div>
    </div>
    """, unsafe_allow_html=True)

if st.button("✅ 결제 완료 ! 다음 순번"):
    now = datetime.now().strftime("%m/%d %H:%M")
    st.session_state.history_list.append({"날짜": now, "이름": current_name})
    st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
    st.rerun()

# --- [PASS 섹션] ---
st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
col_l, col_v = st.columns(2)
with col_l:
    if st.button("⏰ 지각 PASS"):
        st.session_state.pass_list.append({"이름": current_name, "사유": "지각"})
        st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
        st.rerun()
with col_v:
    if st.button("🌴 휴가 PASS"):
        st.session_state.pass_list.append({"이름": current_name, "사유": "휴가"})
        st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
        st.rerun()

# --- [통계 섹션] ---
st.markdown("### 📊 구입 및 패스 현황")
tab1, tab2 = st.tabs(["💰 커피 횟수", "🚫 패스 기록"])

with tab1:
    df_h = pd.DataFrame(st.session_state.history_list)
    stats = df_h['이름'].value_counts().reindex(members, fill_value=0).reset_index() if not df_h.empty else pd.DataFrame(members, columns=['이름']).assign(count=0)
    stats.columns = ['이름', '횟수']
    st.table(stats)

with tab2:
    df_p = pd.DataFrame(st.session_state.pass_list)
    if not df_p.empty:
        p_stats = df_p.groupby(['이름', '사유']).size().unstack(fill_value=0).reindex(members, fill_value=0).reset_index()
        st.table(p_stats)
    else:
        st.write("패스 기록이 없습니다.")
