import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# 1. 앱 설정
st.set_page_config(page_title="성수동 올인원 가이드", page_icon="💳")
st.title("☕ 성수동 커피 순번 & 온누리 찾기")

# 2. 데이터 초기화
members = ["규리", "조조", "은비", "까비"]
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'history_list' not in st.session_state: st.session_state.history_list = []

# --- [STEP 1: 온누리상품권 가맹점 찾기 (링크 보정)] ---
st.subheader("💳 내 주변 온누리상품권 가맹점")
st.write("버튼을 누르면 현재 위치 기반 가맹점 검색 결과로 연결됩니다.")

# 검색 쿼리 최적화: '성수동' 키워드를 기본 포함하여 검색 정확도를 높임
col_on1, col_on2 = st.columns(2)
with col_on1:
    # 네이버 검색 결과 페이지로 직접 연결 (지도가 안 뜰 경우 대비)
    q_food = urllib.parse.quote("성수동 온누리상품권 가맹 식당")
    st.link_button("🍜 성수 가맹 식당", f"https://search.naver.com/search.naver?query={q_food}", use_container_width=True)
with col_on2:
    q_cafe = urllib.parse.quote("성수동 온누리상품권 가맹 카페")
    st.link_button("☕ 성수 가맹 카페", f"https://search.naver.com/search.naver?query={q_cafe}", use_container_width=True)

st.info("💡 **팁:** 주로 '성수역 뚝도시장'이나 '성수전통시장' 인근 식당들이 온누리상품권 가맹점인 경우가 많습니다.")
st.divider()

# --- [STEP 2: 커피 순번 시스템] ---
current_person = members[st.session_state.current_idx]
st.info(f"🚩 **현재 커피 당번: {current_person} 님**")

if st.button("✅ 결제 완료 & 다음 순번", use_container_width=True):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    st.session_state.history_list.append({"날짜": now, "이름": current_person})
    st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
    st.rerun()

# 기록 및 통계
tab1, tab2 = st.tabs(["📊 누적 통계", "📜 최근 내역(3개)"])
with tab1:
    df = pd.DataFrame(st.session_state.history_list)
    stats = df['이름'].value_counts().reindex(members, fill_value=0).reset_index() if not df.empty else pd.DataFrame(members, columns=['이름']).assign(횟수=0)
    stats.columns = ['이름', '횟수']
    st.table(stats)
with tab2:
    recent_3 = st.session_state.history_list[-3:][::-1] if st.session_state.history_list else []
    st.table(pd.DataFrame(recent_3))

st.divider()

# --- [STEP 3: 성수동 정보 & 메뉴] ---
st.subheader("🔗 성수동 실시간 정보")
st.link_button("🍱 오늘의 메뉴 확인 (카카오 채널)", "https://pf.kakao.com/_jxcvzn/posts", use_container_width=True)

# 2026년 팝업 검색
popup_query = urllib.parse.quote("2026년 성수동 팝업스토어 최신")
st.link_button("🔥 2026 성수 팝업 실시간 검색", f"https://search.naver.com/search.naver?query={popup_query}", use_container_width=True)

with st.expander("⚙️ 초기화"):
    if st.button("🔄 기록 리셋"):
        st.session_state.current_idx = 0
        st.session_state.history_list = []
        st.rerun()
