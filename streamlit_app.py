import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# 1. 앱 설정 및 레이아웃 (전체 폭 사용)
st.set_page_config(page_title="커피당번", page_icon="☕", layout="wide")

# 2. 디자인 보정 (중첩 텍스트 강제 삭제 및 모바일 최적화)
st.markdown("""
    <style>
    /* 배경 및 기본 폰트 */
    .stApp { background-color: #FFFFFF !important; }
    h1, h2, h3, p, span, div, label { 
        color: #1C1C1E !important; 
        font-family: 'Apple SD Gothic Neo', sans-serif !important; 
    }
    
    /* [수정] 사이드바 내부의 화살표/아이콘 텍스트 중첩 강제 차단 */
    [data-testid="stSidebar"] span, [data-testid="stSidebar"] svg {
        display: none !important;
    }
    /* 사이드바 제목/텍스트는 보이게 허용 */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] b {
        display: block !important;
    }

    /* 사이드바 배경 및 구분선 */
    [data-testid="stSidebar"] {
        background-color: #F2F2F7 !important;
        border-right: 1px solid #E5E5EA;
    }

    /* 메인 당번 카드 */
    .info-card {
        background-color: #F2F2F7;
        padding: 40px 20px;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 25px;
    }
    .winner-name {
        color: #007AFF !important;
        font-size: 5rem !important;
        font-weight: 900 !important;
        margin: 10px 0;
    }

    /* 버튼 스타일 */
    .stButton > button { width: 100%; border-radius: 15px !important; font-weight: bold !important; }
    
    /* 결제 버튼 (녹색) */
    .buy-btn div.stButton > button {
        height: 6rem;
        background-color: #28A745 !important;
        color: white !important;
        font-size: 1.8rem !important;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
    }
    
    /* 패스 버튼 (주황색) */
    .pass-btn div.stButton > button {
        background-color: #FF9500 !important;
        color: white !important;
    }

    /* 초기화 버튼 (빨간색) */
    .reset-btn div.stButton > button {
        background-color: #FF3B30 !important;
        color: white !important;
        height: 3rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 데이터 세션 초기화 ---
members = ["규리", "조조", "은비", "까비"]
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'history_list' not in st.session_state: st.session_state.history_list = []
if 'pass_list' not in st.session_state: st.session_state.pass_list = []
if 'show_reset' not in st.session_state: st.session_state.show_reset = False

# --- ⬅️ 좌측 사이드바 (통계 및 관리) ---
with st.sidebar:
    st.markdown("### 📊 통계 센터")
    
    # 누적 구입 통계
    st.markdown("**💰 누적 커피 구매**")
    df_h = pd.DataFrame(st.session_state.history_list)
    stats = df_h['이름'].value_counts().reindex(members, fill_value=0).reset_index() if not df_h.empty else pd.DataFrame(members, columns=['이름']).assign(count=0)
    stats.columns = ['이름', '횟수']
    st.table(stats)
    
    # 패스 현황 (지각/휴가)
    st.markdown("**🚫 패스 현황**")
    df_p = pd.DataFrame(st.session_state.pass_list)
    if not df_p.empty:
        p_stats = df_p.groupby(['이름', '사유']).size().unstack(fill_value=0).reindex(members, fill_value=0).reset_index()
        st.table(p_stats)
    else:
        st.caption("패스 내역이 없습니다.")
    
    st.markdown("---")
    
    # 관리자 리셋 (중첩 방지를 위해 expander 제거)
    st.markdown("**🛠️ 시스템 관리**")
    if not st.session_state.show_reset:
        if st.button("데이터 리셋 열기"):
            st.session_state.show_reset = True
            st.rerun()
    else:
        pw = st.text_input("비밀번호", type="password", placeholder="비번입력")
        col_r, col_c = st.columns(2)
        with col_r:
            st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
            if st.button("리셋"):
                if pw == "123qwe..":
                    st.session_state.current_idx = 0
                    st.session_state.history_list = []
                    st.session_state.pass_list = []
                    st.session_state.show_reset = False
                    st.rerun()
                else: st.error("오류")
            st.markdown('</div>', unsafe_allow_html=True)
        with col_c:
            if st.button("취소"):
                st.session_state.show_reset = False
                st.rerun()

# --- ➡️ 우측 메인 화면 ---
st.markdown("# ☕ 커피당번")
current_name = members[st.session_state.current_idx]

st.markdown(f"""
    <div class="info-card">
        <p style='font-size:1.2rem; color:#8E8E93 !important;'>오늘 커피 쏠 사람</p>
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

st.markdown("---")

# 퀵 링크
st.markdown("### 🔗 성수동 실시간 정보")
cl1, cl2 = st.columns(2)
with cl1:
    st.link_button("🍱 오늘 메뉴", "https://pf.kakao.com/_jxcvzn/posts", use_container_width=True)
with cl2:
    p_q = urllib.parse.quote("2026년 성수동 팝업스토어")
    st.link_button("🔥 2026 팝업", f"https://search.naver.com/search.naver?query={p_q}", use_container_width=True)
