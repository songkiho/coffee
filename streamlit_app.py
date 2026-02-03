import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# 1. 앱 설정
st.set_page_config(page_title="성수동 마스터 앱", page_icon="📍")
st.title("☕ 성수동 커피 순번 & 온누리 지도")

# 2. 팀원 및 데이터 초기화
members = ["규리", "조조", "은비", "까비"]
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'history_list' not in st.session_state: st.session_state.history_list = []

# --- [STEP 1: 온누리상품권 가맹점 지도 (최적화 링크)] ---
st.subheader("🗺️ 온누리 가맹점 실시간 지도")
st.write("네이버 지도 앱을 통해 현재 위치 주변 가맹점을 바로 확인하세요.")

# 검색 정확도를 위해 '성수동'과 '온누리상품권 가맹점'을 조합한 딥링크
# 이 링크는 네이버 지도에서 바로 장소 핀(Pin)을 보여줍니다.
map_query = urllib.parse.quote("성수동 온누리상품권 가맹점")
map_url = f"https://m.map.naver.com/search2/search.naver?query={map_query}"

st.link_button("📍 내 주변 온누리 가맹점 지도로 보기", map_url, type="primary", use_container_width=True)
st.caption("💡 팁: 지도 앱이 열리면 상단의 '현위치' 버튼을 눌러 정확한 주변 식당을 확인하세요.")
st.divider()

# --- [STEP 2: 커피 순번 시스템] ---
current_person = members[st.session_state.current_idx]
st.success(f"### 🚩 이번 당번: **{current_person}** 님")

if st.button("✅ 결제 완료 & 다음 순번", use_container_width=True):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    st.session_state.history_list.append({"날짜": now, "이름": current_person})
    st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
    st.rerun()

# 기록 및 통계
col_stat, col_recent = st.columns(2)
with col_stat:
    st.subheader("📊 누적 통계")
    df = pd.DataFrame(st.session_state.history_list)
    stats = df['이름'].value_counts().reindex(members, fill_value=0).reset_index() if not df.empty else pd.DataFrame(members, columns=['이름']).assign(횟수=0)
    stats.columns = ['이름', '횟수']
    st.table(stats)
with col_recent:
    st.subheader("📜 최근 내역(3개)")
    recent_3 = st.session_state.history_list[-3:][::-1] if st.session_state.history_list else []
    st.table(pd.DataFrame(recent_3))

st.divider()

# --- [STEP 3: 2026 실시간 팝업 & 메뉴] ---
st.subheader("🔗 성수동 실시간 정보")

col_info1, col_info2 = st.columns(2)
with col_info1:
    st.link_button("🍱 오늘 메뉴 확인", "https://pf.kakao.com/_jxcvzn/posts", use_container_width=True)
with col_info2:
    popup_q = urllib.parse.quote("2026년 성수동 팝업스토어 최신")
    st.link_button("🔥 2026 팝업 검색", f"https://search.naver.com/search.naver?query={popup_q}", use_container_width=True)

# 초기화 버튼
with st.expander("설정 및 초기화"):
    if st.button("🔄 모든 데이터 리셋"):
        st.session_state.current_idx = 0
        st.session_state.history_list = []
        st.rerun()
