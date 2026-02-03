import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# 1. 모바일 최적화 설정
st.set_page_config(
    page_title="성수동 점심 대장", 
    page_icon="☕", 
    layout="centered", # 모바일은 중앙 집중형이 보기 좋습니다.
    initial_sidebar_state="collapsed"
)

# 2. 모바일 전용 고대비 디자인 (CSS)
st.markdown("""
    <style>
    /* 전체 배경 및 폰트 설정 */
    .stApp { background-color: #FFFFFF; }
    * { font-family: 'Apple SD Gothic Neo', sans-serif; color: #1C1C1E; }
    
    /* 카드 디자인: 모바일 꽉 찬 느낌 */
    .mobile-card {
        background-color: #F2F2F7;
        padding: 20px;
        border-radius: 18px;
        margin-bottom: 15px;
        border: 1px solid #E5E5EA;
    }
    
    /* 모바일용 왕 버튼 */
    div.stButton > button {
        width: 100%;
        border-radius: 15px;
        height: 4.5rem; /* 버튼을 더 크게 */
        background-color: #007AFF;
        color: #FFFFFF !important;
        font-weight: 800;
        font-size: 1.3rem;
        border: none;
        margin-top: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* 링크 버튼 커스텀 */
    div[data-testid="stHorizontalBlock"] div.stButton > button {
        height: 3.5rem;
        background-color: #FFFFFF;
        color: #007AFF !important;
        border: 2px solid #007AFF;
    }

    /* 표 가독성 */
    .stTable { font-size: 1.1rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [상단 헤더] ---
st.markdown('# ☕ 성수동 가이드')
st.markdown(f"**{datetime.now().strftime('%m월 %d일')} 점심시간**")

# --- [STEP 1: 당번 안내 (가장 중요)] ---
members = ["규리", "조조", "은비", "까비"]
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'history_list' not in st.session_state: st.session_state.history_list = []

st.markdown('<div class="mobile-card">', unsafe_allow_html=True)
current_person = members[st.session_state.current_idx]
st.markdown(f"### 🚩 오늘의 당번<br><span style='color:#007AFF; font-size:2.2rem;'>{current_person} 님</span>", unsafe_allow_html=True)

if st.button("✅ 결제 완료 & 순번 넘기기"):
    now = datetime.now().strftime("%m/%d %H:%M")
    st.session_state.history_list.append({"날짜": now, "이름": current_person})
    st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- [STEP 2: 위치 및 메뉴 (세로 배치)] ---
st.markdown("### 📍 주변 정보 확인")

# 모바일에서는 버튼을 나란히 두지 않고 하나씩 크게 배치하거나, 좁게 배치합니다.
col1, col2 = st.columns(2)
with col1:
    loc_url = "https://m.map.naver.com/search2/search.naver?query=" + urllib.parse.quote("현재 내 위치")
    st.link_button("🔍 내 위치", loc_url, use_container_width=True)
with col2:
    onnuri_url = "https://m.map.naver.com/search2/search.naver?query=" + urllib.parse.quote("내 주변 온누리 가맹 식당 카페")
    st.link_button("💳 온누리", onnuri_url, use_container_width=True)

st.link_button("🍱 오늘 메뉴 (카카오 채널)", "https://pf.kakao.com/_jxcvzn/posts", use_container_width=True)
popup_q = urllib.parse.quote("2026년 성수동 팝업스토어 최신")
st.link_button("🔥 실시간 성수 팝업 검색", f"https://search.naver.com/search.naver?query={popup_q}", use_container_width=True)

# --- [STEP 3: 기록 확인 (아래로 내려감)] ---
with st.expander("📊 누적 기록 및 통계 확인"):
    df = pd.DataFrame(st.session_state.history_list)
    if not df.empty:
        stats = df['이름'].value_counts().reindex(members, fill_value=0).reset_index()
        stats.columns = ['이름', '횟수']
        st.table(stats)
        
        st.markdown("**최근 결제 내역**")
        st.table(pd.DataFrame(st.session_state.history_list[-3:][::-1]))
    else:
        st.write("아직 데이터가 없습니다.")

# 관리용 초기화
with st.expander("🛠️ 설정"):
    if st.button("🔄 전체 기록 초기화"):
        st.session_state.current_idx = 0
        st.session_state.history_list = []
        st.rerun()
