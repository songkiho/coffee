import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# 1. 앱 기본 설정
st.set_page_config(page_title="성수동 커피 대장", page_icon="🍱")

# 스타일 커스텀 (아이폰 가독성 최적화)
st.markdown("""
    <style>
    .main { background-color: #f9f9f9; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍱 성수동 커피 & 핫플 가이드")

# --- [STEP 1: 식사 메뉴 확인 (카카오 채널)] ---
st.subheader("🍴 오늘 뭐 먹지?")
kakao_url = "https://pf.kakao.com/_jxcvzn/posts"
st.link_button("📜 실시간 음식 메뉴 확인하기", kakao_url, type="primary")
st.caption("위 버튼을 누르면 카카오 채널의 최신 메뉴 포스트로 연결됩니다.")
st.divider()

# --- [STEP 2: 커피 순번 시스템] ---
members = ["규리", "조조", "은비", "까비"]

if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'history_list' not in st.session_state: st.session_state.history_list = []

current_person = members[st.session_state.current_idx]
st.subheader(f"☕ 커피 당번: {current_person} 님")

if st.button("✅ 결제 완료 & 다음 순번"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    st.session_state.history_list.append({"날짜": now, "이름": current_person})
    st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
    st.rerun()

# 기록 및 통계 (아이폰 가로 길이를 고려해 탭으로 분리)
tab1, tab2 = st.tabs(["📊 누적 통계", "📜 최근 내역(3개)"])
with tab1:
    df = pd.DataFrame(st.session_state.history_list)
    stats = df['이름'].value_counts().reindex(members, fill_value=0).reset_index() if not df.empty else pd.DataFrame(members, columns=['이름']).assign(횟수=0)
    stats.columns = ['이름', '구매 횟수']
    st.table(stats)

with tab2:
    recent_3 = st.session_state.history_list[-3:][::-1] if st.session_state.history_list else []
    if recent_3:
        st.table(pd.DataFrame(recent_3))
    else:
        st.write("아직 결제 내역이 없습니다.")

st.divider()

# --- [STEP 3: 2026년 실시간 성수동 팝업] ---
current_year = "2026년"
st.subheader(f"🔥 {current_year} 성수동 실시간 핫플")

search_queries = [
    {"title": "📅 2026년 2월 성수동 팝업 리스트", "query": f"{current_year} 2월 성수동 팝업스토어 최신"},
    {"title": "📸 지금 가장 핫한 성수동 오늘 팝업", "query": f"{current_year} 성수동 오늘 팝업"},
    {"title": "🧸 2026 성수동 전시/굿즈샵 정보", "query": f"{current_year} 성수동 전시 팝업"}
]

for item in search_queries:
    encoded_query = urllib.parse.quote(item["query"])
    st.link_button(item["title"], f"https://search.naver.com/search.naver?query={encoded_query}")

# --- [STEP 4: 초기화 및 하단 정보] ---
with st.expander("⚙️ 설정 및 초기화"):
    if st.button("🔄 모든 기록 리셋"):
        st.session_state.current_idx = 0
        st.session_state.history_list = []
        st.rerun()
st.caption(f"© 2026 성수동 팀장님 커스텀 앱 | 오늘 날짜: {datetime.now().strftime('%Y-%m-%d')}")
