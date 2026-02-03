import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# 앱 설정
st.set_page_config(page_title="2026 성수동 핫플", page_icon="🚀")
st.title("☕ 2026 성수동 커피 순번 & 팝업")

# 팀원 명단 및 데이터 초기화
members = ["규리", "조조", "은비", "까비"]
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'history_list' not in st.session_state: st.session_state.history_list = []

# --- [1. 커피 순번 섹션] ---
current_person = members[st.session_state.current_idx]
st.info(f"📍 **현재 순번: {current_person} 님**")

if st.button("✅ 결제 완료 & 다음 사람", use_container_width=True):
    now = datetime.now().strftime("%Y-%m-%d %H:%M") # 연도 포함 기록
    st.session_state.history_list.append({"날짜": now, "이름": current_person})
    st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
    st.rerun()

# --- [2. 기록 섹션 (최근 3개)] ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("📊 누적 통계")
    df = pd.DataFrame(st.session_state.history_list)
    stats = df['이름'].value_counts().reindex(members, fill_value=0).reset_index() if not df.empty else pd.DataFrame(members, columns=['이름']).assign(횟수=0)
    st.table(stats)

with col2:
    st.subheader("📜 최근 내역")
    recent_3 = st.session_state.history_list[-3:][::-1] if st.session_state.history_list else []
    st.table(pd.DataFrame(recent_3))

st.divider()

# --- [3. 2026년 실시간 성수동 팝업 검색] ---
current_year = "2026년"
st.subheader(f"🔍 {current_year} 성수동 실시간 팝업 정보")
st.write(f"과거 데이터 제외, **{current_year}년 최신 정보**만 필터링합니다.")

# 검색어에 2026년을 강제로 포함시켜 예전 정보 차단
search_queries = [
    {"title": "📅 2026년 2월 성수동 팝업 리스트", "query": f"{current_year} 2월 성수동 팝업스토어 최신"},
    {"title": "🔥 오늘 뜨는 2026 성수동 핫플", "query": f"{current_year} 성수동 오늘 팝업"},
    {"title": "📸 인스타 감성 2026 성수 전시회", "query": f"{current_year} 성수동 전시 팝업"}
]

for item in search_queries:
    # 검색 쿼리 인코딩
    encoded_query = urllib.parse.quote(item["query"])
    # 네이버 검색 시 '최신순' 옵션이 적용되도록 구성할 수도 있습니다.
    st.link_button(f"{item['title']} 확인하기", f"https://search.naver.com/search.naver?query={encoded_query}", use_container_width=True)

st.caption(f"⚠️ {current_year} 키워드가 포함된 검색 결과로 연결되어 예전 정보 노출을 최소화합니다.")

if st.button("🔄 기록 초기화"):
    st.session_state.current_idx = 0
    st.session_state.history_list = []
    st.rerun()
