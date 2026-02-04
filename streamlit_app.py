import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
import streamlit.components.v1 as components

# 1. 앱 설정
st.set_page_config(page_title="커피당번", page_icon="☕", layout="wide")

# 2. 디자인 설정 (녹색 테마 유지)
st.markdown("""
    <style>
    /* 기본 설정 */
    .stApp { background-color: #FFFFFF !important; }
    h1, h2, h3, p, div, span, label { 
        font-family: 'Apple SD Gothic Neo', sans-serif !important; 
        color: #1C1C1E !important; 
    }

    /* 사이드바 스타일 */
    [data-testid="stSidebar"] { background-color: #F8F9FA !important; border-right: 1px solid #E5E5EA; }
    [data-testid="stSidebar"] svg, [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p { display: none !important; } 
    
    /* 버튼/링크버튼 스타일 통일 (녹색 배경 + 검정 글씨) */
    .stButton > button, .stLinkButton > a {
        background-color: #28A745 !important; 
        color: #000000 !important;       
        border: 1px solid #1E7E34 !important; 
        border-radius: 12px !important;
        font-weight: 900 !important;     
        font-size: 1rem !important;
        height: 3.5rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-decoration: none !important;
    }
    .stButton > button:hover, .stLinkButton > a:hover {
        background-color: #218838 !important;
        border-color: #1C7430 !important;
        color: #000000 !important;
    }

    /* 메인 결제 버튼 (크게) */
    .buy-btn div.stButton > button {
        height: 6rem !important;
        font-size: 1.8rem !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    /* 메인 카드 */
    .info-card {
        background-color: #F2F2F7;
        padding: 40px 20px;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 25px;
        border: 1px solid #E5E5EA;
    }
    .winner-name { color: #000000 !important; font-size: 4.5rem !important; font-weight: 900 !important; }
    
    /* 확인 팝업 박스 스타일 */
    [data-testid="stStatusWidget"] { display: none; } /* 로딩 숨김 */
    </style>
    """, unsafe_allow_html=True)

# --- 데이터 및 상태 초기화 ---
members = ["규리", "조조", "은비", "까비"]
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'history_list' not in st.session_state: st.session_state.history_list = []
if 'pass_list' not in st.session_state: st.session_state.pass_list = []
if 'view_state' not in st.session_state: st.session_state.view_state = None
if 'confirm_reset' not in st.session_state: st.session_state.confirm_reset = False # 초기화 확인창 상태

# --- ⬅️ 좌측 사이드바 ---
with st.sidebar:
    st.title("📊 리포트")
    
    # 1. 누적 구입
    st.markdown("### 💰 누적 커피")
    df_h = pd.DataFrame(st.session_state.history_list)
    stats = df_h['이름'].value_counts().reindex(members, fill_value=0).reset_index() if not df_h.empty else pd.DataFrame(members, columns=['이름']).assign(count=0)
    stats.columns = ['이름', '횟수']
    st.table(stats)
    
    # 2. 패스 기록
    st.markdown("### 🚫 패스 기록")
    df_p = pd.DataFrame(st.session_state.pass_list)
    if not df_p.empty:
        p_stats = df_p.groupby(['이름', '사유']).size().unstack(fill_value=0).reindex(members, fill_value=0).reset_index()
        st.table(p_stats)
    else:
        st.caption("패스 기록 없음")
    
    st.markdown("---")
    
    # 3. [변경] 기록 초기화 버튼 & 확인 팝업
    st.markdown("### ⚙️ 관리")
    
    # 초기화 버튼을 누르면 -> 확인창 상태(True)로 변경
    if st.button("🗑️ 기록 초기화", use_container_width=True):
        st.session_state.confirm_reset = True
        st.rerun()

    # 확인창이 켜져있으면 경고 박스 표시
    if st.session_state.confirm_reset:
        st.warning("⚠️ 정말로 모든 기록을 삭제하시겠습니까?", icon="⚠️")
        col_yes, col_no = st.columns(2)
        with col_yes:
            if st.button("네", use_container_width=True):
                # 데이터 초기화 실행
                st.session_state.current_idx = 0
                st.session_state.history_list = []
                st.session_state.pass_list = []
                st.session_state.confirm_reset = False
                st.success("초기화 완료!")
                st.rerun()
        with col_no:
            if st.button("아니오", use_container_width=True):
                # 취소
                st.session_state.confirm_reset = False
                st.rerun()

# --- ➡️ 우측 메인 화면 ---
st.markdown("# ☕ 커피당번")
current_name = members[st.session_state.current_idx]

st.markdown(f"""
    <div class="info-card">
        <p style='color:#555555 !important; font-size:1.2rem; margin-bottom:5px; font-weight:bold;'>오늘 커피 주인공</p>
        <div class="winner-name">{current_name}</div>
    </div>
    """, unsafe_allow_html=True)

# 메인 결제 버튼
st.markdown('<div class="buy-btn">', unsafe_allow_html=True)
if st.button("✅ 오늘 결제 완료"):
    now = datetime.now().strftime("%m/%d %H:%M")
    st.session_state.history_list.append({"날짜": now, "이름": current_name})
    st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# 패스 버튼
st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    if st.button("⏰ 지각 PASS", use_container_width=True):
        st.session_state.pass_list.append({"이름": current_name, "사유": "지각"})
        st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members); st.rerun()
with c2:
    if st.button("🌴 휴가 PASS", use_container_width=True):
        st.session_state.pass_list.append({"이름": current_name, "사유": "휴가"})
        st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members); st.rerun()

st.divider()

# --- 하단 실시간 정보 ---
st.subheader("🔗 성수동 정보")
b1, b2 = st.columns(2)

with b1:
    if st.button("🍱 오늘 메뉴 보기", use_container_width=True):
        st.session_state.view_state = 'menu' if st.session_state.view_state != 'menu' else None

with b2:
    query = urllib.parse.quote("2026년 성수동 팝업스토어")
    st.link_button("🔥 성수 팝업 검색 (새창)", f"https://search.naver.com/search.naver?query={query}", use_container_width=True)

if st.session_state.view_state == 'menu':
    st.info("💡 화면이 안 보이면 아래 버튼을 눌러주세요.")
    components.iframe("https://pf.kakao.com/_jxcvzn/posts", height=600, scrolling=True)
    st.link_button("🌐 새창으로 메뉴 보기", "https://pf.kakao.com/_jxcvzn/posts", use_container_width=True)
