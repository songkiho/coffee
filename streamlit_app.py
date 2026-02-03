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

# --- [STEP 1: 온누리상품권 가맹점 찾기] ---
st.subheader("💳 내 주변 온누리상품권 가맹점")
st.write("현재 위치 근처의 온누리상품권 사용 가능 식당과 카페를 확인하세요.")

col_on1, col_on2 = st.columns(2)
with col_on1:
    # 네이버 지도로 연결되는 링크 (모바일 환경에서 유용)
    onnuri_food = urllib.parse.quote("내 주변 온누리상품권 가맹 식당")
    st.link_button("🍜 주변 가맹 식당 찾기", f"https://m.map.naver.com/search2/search.naver?query={onnuri_food}", use_container_width=True)
with col_on2:
    onnuri_cafe = urllib.parse.quote("내 주변 온누리상품권 가맹 카페")
    st.link_button("☕ 주변 가맹 카페 찾기", f"https://m.map.naver.com/search2/search.naver?query={onnuri_cafe}", use_container_width=True)

st.caption("※ 네이버 지도 앱으로 연결되어 현재 위치 기반의 실시간 가맹점 정보를 보여줍니다.")
st.divider()

# --- [STEP 2: 커피 순번 시스템] ---
current_person = members[st.session_state.current_idx]
st.info(f"🚩 **현재 커피 당번: {current_person} 님**")

if st.button("✅ 결제 완료 & 다음 순번", use_container_width=True):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    st.session_state.history_list.append({"날짜": now, "이름": current_person})
    st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
    st.rerun()

# 누적 기록 및 최근 내역
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
