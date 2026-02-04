import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
import streamlit.components.v1 as components

# 1. 앱 설정
st.set_page_config(page_title="커피당번", page_icon="☕", layout="wide")

# 2. 디자인 설정 (녹색 배경 + 검정 글씨 강제 적용)
st.markdown("""
    <style>
    /* 기본 배경 및 폰트 */
    .stApp { background-color: #FFFFFF !important; }
    h1, h2, h3, p, div, span, label { 
        font-family: 'Apple SD Gothic Neo', sans-serif !important; 
        color: #1C1C1E !important; 
    }

    /* 사이드바 스타일 보정 */
    [data-testid="stSidebar"] { background-color: #F8F9FA !important; border-right: 1px solid #E5E5EA; }
    [data-testid="stSidebar"] svg, [data-testid="stSidebar"] .st-emotion-cache-15zrgzn { display: none !important; }
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p { display: none !important; } /* 시스템 텍스트 숨김 */
    
    /* [핵심] 모든 버튼 스타일: 녹색 배경 + 검정 글씨 */
    .stButton > button {
        background-color: #28A745 !important; /* 녹색 */
        color: #000000 !important;       /* 검정색 글씨 */
        border: 1px solid #1E7E34 !important; /* 테두리는 조금 더 진한 녹색 */
        border-radius: 12px !important;
        font-weight: 900 !important;     /* 글자 아주 굵게 */
        font-size: 1rem !important;
        height: 3.5rem !important;
    }
    
    /* 버튼 호버 효과 (마우스 올렸을 때) */
    .stButton > button:hover {
        background-color: #218838 !important;
        color: #000000 !important;
        border-color: #1C7430 !important;
    }

    /* 메인 '오늘 결제 완료' 버튼 (더 크고 웅장하게) */
    .buy-btn div.stButton > button {
        height: 6rem !important;
        font-size: 1.8rem !important;
        background-color: #28A745 !important;
        color: #000000 !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    /* 메인 카드 디자인 */
    .info-card {
        background-color: #F2F2F7;
        padding: 40px 20px;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 25px;
        border: 1px solid #E5E5EA;
    }
    .winner-name { color: #000000 !important; font-size: 4.5rem !important; font-weight: 900 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 데이터 초기화 ---
members = ["규리", "조조", "은비", "까비"]
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'history_list' not in st.session_state: st.session_state.history_list = []
if 'pass_list' not in st.session_state: st.session_state.pass_list = []
if 'view_state' not in st.session_state: st.session_state.view_state = None

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
    
    # 3. 시스템 관리 (체크박스 방식)
    st.markdown("### ⚙️ 설정")
    admin_toggle = st.checkbox("관리자 모드 (리셋)")
    
    if admin_toggle:
        pw = st.text_input("비밀번호", type="password", placeholder="비번 입력")
        if st.button("🧨 모든 기록 리셋"):
            if pw == "123qwe..":
                st.session_state.current_idx = 0
                st.session_state.history_list = []
                st.session_state.pass_list = []
                st.success("리셋 완료!")
                st.rerun()
            else:
                st.error("비번 불일치")

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
    if st.button("🔥 성수 팝업 검색", use_container_width=True):
        st.session_state.view_state = 'popup' if st.session_state.view_state != 'popup' else None

if st.session_state.view_state == 'menu':
    st.info("💡 카카오 보안 정책으로 인해 화면이 안 보이면 아래 버튼을 눌러주세요.")
    components.iframe("https://pf.kakao.com/_jxcvzn/posts", height=600, scrolling=True)
    st.link_button("🌐 새창으로 메뉴 보기", "https://pf.kakao.com/_jxcvzn/posts", use_container_width=True)

elif st.session_state.view_state == 'popup':
    query = urllib.parse.quote("2026년 성수동 팝업스토어")
    # 네이버는 iframe 불가하므로 버튼만 제공
    st.link_button("🌐 네이버 팝업 검색 (새창)", f"https://search.naver.com/search.naver?query={query}", use_container_width=True)
