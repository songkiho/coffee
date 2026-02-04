import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
import streamlit.components.v1 as components

# 1. 앱 설정
st.set_page_config(page_title="커피당번", page_icon="☕", layout="wide")

# 2. 디자인 보정 (사이드바 버튼 글자 강제 노출)
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    
    /* 사이드바 전체 스타일 */
    [data-testid="stSidebar"] {
        background-color: #F2F2F7 !important;
        border-right: 1px solid #E5E5EA;
    }

    /* [해결] 사이드바 내 버튼 글자 안 보임 현상 수정 */
    [data-testid="stSidebar"] .stButton button {
        background-color: #FFFFFF !important;
        color: #007AFF !important; /* 글자색 파란색 강제 */
        border: 1px solid #D1D1D6 !important;
        border-radius: 10px !important;
        height: 3rem !important;
        font-weight: bold !important;
        font-size: 0.9rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    /* 리셋 버튼은 빨간색으로 */
    [data-testid="stSidebar"] .reset-btn button {
        background-color: #FF3B30 !important;
        color: white !important;
        border: none !important;
    }

    /* 메인 화면 당번 카드 */
    .info-card {
        background-color: #F2F2F7;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 20px;
    }
    .winner-name {
        color: #007AFF !important;
        font-size: 4rem !important;
        font-weight: 900 !important;
    }

    /* 메인 화면 큰 결제 버튼 */
    .buy-btn button {
        height: 5rem !important;
        background-color: #28A745 !important;
        color: white !important;
        font-size: 1.5rem !important;
        border-radius: 15px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 데이터 초기화 ---
members = ["규리", "조조", "은비", "까비"]
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'history_list' not in st.session_state: st.session_state.history_list = []
if 'pass_list' not in st.session_state: st.session_state.pass_list = []
if 'admin_mode' not in st.session_state: st.session_state.admin_mode = False
if 'view_state' not in st.session_state: st.session_state.view_state = None

# --- ⬅️ 좌측 사이드바 (글자 겹침 방지 처리) ---
with st.sidebar:
    st.markdown("### 📊 통계 센터")
    
    # 누적 구입
    st.markdown("**💰 누적 커피 구매**")
    df_h = pd.DataFrame(st.session_state.history_list)
    stats = df_h['이름'].value_counts().reindex(members, fill_value=0).reset_index() if not df_h.empty else pd.DataFrame(members, columns=['이름']).assign(count=0)
    stats.columns = ['이름', '횟수']
    st.table(stats)
    
    # 패스 현황
    st.markdown("**🚫 패스 현황**")
    df_p = pd.DataFrame(st.session_state.pass_list)
    if not df_p.empty:
        p_stats = df_p.groupby(['이름', '사유']).size().unstack(fill_value=0).reindex(members, fill_value=0).reset_index()
        st.table(p_stats)
    
    st.divider()
    
    # [수정] 시스템 관리 버튼 영역
    st.markdown("### 🛠️ 시스템 관리")
    if not st.session_state.admin_mode:
        if st.button("🔐 관리자 모드 열기"):
            st.session_state.admin_mode = True
            st.rerun()
    else:
        pw = st.text_input("비번입력", type="password")
        # 리셋 버튼만 별도 스타일(빨간색) 적용을 위해 div로 감쌈
        st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
        if st.button("🧨 전체 기록 리셋"):
            if pw == "123qwe..":
                st.session_state.current_idx = 0
                st.session_state.history_list = []
                st.session_state.pass_list = []
                st.session_state.admin_mode = False
                st.rerun()
            else: st.error("비번 오류")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("❌ 닫기"):
            st.session_state.admin_mode = False
            st.rerun()

# --- ➡️ 우측 메인 화면 ---
st.markdown("# ☕ 커피당번")
current_name = members[st.session_state.current_idx]

st.markdown(f"""
    <div class="info-card">
        <p style='color:#8E8E93 !important;'>오늘 커피 쏠 사람</p>
        <div class="winner-name">{current_name}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="buy-btn">', unsafe_allow_html=True)
if st.button("✅ 오늘 결제 완료"):
    now = datetime.now().strftime("%m/%d %H:%M")
    st.session_state.history_list.append({"날짜": now, "이름": current_name})
    st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# PASS 버튼
col1, col2 = st.columns(2)
with col1:
    if st.button("⏰ 지각 PASS"):
        st.session_state.pass_list.append({"이름": current_name, "사유": "지각"})
        st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members); st.rerun()
with col2:
    if st.button("🌴 휴가 PASS"):
        st.session_state.pass_list.append({"이름": current_name, "사유": "휴가"})
        st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members); st.rerun()

st.divider()

# --- 🍱 하단 웹뷰 영역 ---
st.subheader("🔗 성수동 실시간 정보")
b1, b2 = st.columns(2)
with b1:
    if st.button("🍱 오늘 메뉴 보기"):
        st.session_state.view_state = 'menu' if st.session_state.view_state != 'menu' else None
with b2:
    if st.button("🔥 성수 팝업 검색"):
        st.session_state.view_state = 'popup' if st.session_state.view_state != 'popup' else None

if st.session_state.view_state == 'menu':
    components.iframe("https://pf.kakao.com/_jxcvzn/posts", height=600, scrolling=True)
elif st.session_state.view_state == 'popup':
    query = urllib.parse.quote("2026년 성수동 팝업스토어")
    components.iframe(f"https://search.naver.com/search.naver?query={query}", height=600, scrolling=True)
