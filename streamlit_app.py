import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# 앱 설정
st.set_page_config(page_title="성수동 실시간 핫플", page_icon="🔥")
st.title("☕ 성수동 커피 순번 & 실시간 팝업")

# 팀원 명단 및 데이터 초기화 (기존과 동일)
members = ["규리", "조조", "은비", "까비"]
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'history_list' not in st.session_state: st.session_state.history_list = []

# --- [1. 커피 순번 섹션] ---
current_person = members[st.session_state.current_idx]
st.info(f"📍 **현재 순번: {current_person} 님**")

if st.button("✅ 결제 완료 & 다음 사람", use_container_width=True):
    now = datetime.now().strftime("%m/%d %H:%M")
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

# --- [3. 매일 갱신되는 실시간 팝업 섹션] ---
st.subheader(f"📅 오늘({datetime.now().strftime('%m/%d')}) 성수동 팝업 소식")
st.write("네이버 블로그와 지도의 최신 데이터를 실시간으로 확인하세요.")

# 검색어 설정
search_queries = [
    {"title": "📱 이번주 성수동 팝업 총정리", "query": "성수동 팝업스토어 2월"},
    {"title": "📍 지금 바로 가볼만한 성수 핫플", "query": "성수동 오늘 팝업"},
    {"title": "🍰 성수동 디저트/카페 팝업", "query": "성수동 카페 팝업스토어"}
]

# 버튼 클릭 시 네이버 실시간 검색 결과로 연결
for item in search_queries:
    encoded_query = urllib.parse.quote(item["query"])
    st.link_button(f"{item['title']} 확인하기", f"https://search.naver.com/search.naver?query={encoded_query}", use_container_width=True)

st.caption("위 버튼을 누르면 오늘 날짜 기준으로 작성된 네이버 블로그/뉴스 검색 결과로 바로 연결됩니다.")

if st.button("🔄 기록 초기화"):
    st.session_state.current_idx = 0
    st.session_state.history_list = []
    st.rerun()
