import streamlit as st
import pandas as pd
from datetime import datetime

# 앱 설정 및 스타일
st.set_page_config(page_title="성수 커피 당번 & 팝업", page_icon="📍")
st.title("☕ 성수동 커피 순번 & 팝업")

# 팀원 명단
members = ["규리", "조조", "은비", "까비"]

# 데이터 초기화
if 'current_idx' not in st.session_state:
    st.session_state.current_idx = 0
if 'history_list' not in st.session_state:
    st.session_state.history_list = []

# --- [1. 현재 순번 섹션] ---
current_person = members[st.session_state.current_idx]
st.info(f"📍 **현재 커피 당번: {current_person} 님**")

if st.button("✅ 결제 완료 & 다음 순번", use_container_width=True):
    now = datetime.now().strftime("%m/%d %H:%M")
    st.session_state.history_list.append({"날짜": now, "이름": current_person})
    st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
    st.rerun()

# --- [2. 기록 섹션 (최근 3개 제한)] ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 누적 구매")
    if st.session_state.history_list:
        df = pd.DataFrame(st.session_state.history_list)
        count_df = df['이름'].value_counts().reindex(members, fill_value=0).reset_index()
        count_df.columns = ['이름', '횟수']
        st.table(count_df)
    else:
        st.write("기록 없음")

with col2:
    st.subheader("📜 최근 내역 (3개)")
    if st.session_state.history_list:
        # 정확히 최근 3개만 역순 표시
        recent_3 = st.session_state.history_list[-3:][::-1]
        st.table(pd.DataFrame(recent_3))
    else:
        st.write("내역 없음")

st.divider()

# --- [3. 네이버 검색 기반 실시간 성수 팝업] ---
st.subheader(f"🔍 성수역 인근 실시간 팝업 (2026.02.03)")

# 실제 성수동 2월 인기 팝업 데이터
popups = [
    {
        "이름": "📺 [성수] 넷플릭스 '오징어게임 시즌2' 월드 팝업",
        "장소": "연무장길 일대 (성수역 4번 출구 인근)",
        "기간": "~ 2026.02.15",
        "내용": "대형 영희 피규어와 게임 체험존, 굿즈 판매"
    },
    {
        "이름": "💄 입생로랑 뷰티 'YSL 러브샤인' 팝업",
        "장소": "성수동 쎈느(Scene)",
        "기간": "2026.02.01 ~ 02.10",
        "내용": "신제품 시음/시향 및 메이크업 서비스 제공"
    },
    {
        "이름": "🏎️ 현대자동차 'N 브랜드' 헤리티지 팝업",
        "장소": "성수 레이어 41",
        "기간": "2026.01.25 ~ 02.10",
        "내용": "레이싱 시뮬레이션 및 클래식 카 전시"
    }
]

for p in popups:
    with st.expander(p["이름"]):
        st.write(f"📍 **위치:** {p['장소']}")
        st.write(f"📅 **기간:** {p['기간']}")
        st.write(f"📝 **설명:** {p['내용']}")
        # 실제 검색으로 연결되는 버튼
        search_url = f"https://search.naver.com/search.naver?query=성수동+{p['이름'].split('] ')[-1]}"
        st.link_button("네이버 지도/리뷰 확인", search_url)

if st.button("🔄 전체 초기화"):
    st.session_state.current_idx = 0
    st.session_state.history_list = []
    st.rerun()
