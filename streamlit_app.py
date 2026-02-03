import streamlit as st
import pandas as pd
from datetime import datetime

# 앱 설정
st.set_page_config(page_title="커피 순번 & 기록", page_icon="☕")
st.title("☕ 커피 순번 관리 시스템")

# 팀원 명단 (규리, 조조, 은비, 까비)
members = ["규리", "조조", "은비", "까비"]

# 데이터 초기화 (현재 순번 및 히스토리 저장)
if 'current_idx' not in st.session_state:
    st.session_state.current_idx = 0
if 'history_list' not in st.session_state:
    st.session_state.history_list = []

# 메인 화면: 현재 당번 안내
current_person = members[st.session_state.current_idx]
st.info(f"📅 **오늘의 커피 당번: {current_person}**")

if st.button("☕ 결제 완료 (기록 및 다음으로)", use_container_width=True):
    # 현재 날짜와 시간 기록
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 히스토리에 추가
    st.session_state.history_list.append({
        "날짜": now,
        "이름": current_person
    })
    
    # 다음 순번으로 이동
    st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
    st.success(f"기록 완료! 다음 차례는 {members[st.session_state.current_idx]} 님입니다.")
    st.rerun()

st.divider()

# 📊 통계 및 기록 섹션
col1, col2 = st.columns(2)

# 1. 인당 구매 횟수 통계
with col1:
    st.subheader("📊 누적 횟수")
    if st.session_state.history_list:
        df_history = pd.DataFrame(st.session_state.history_list)
        count_df = df_history['이름'].value_counts().reset_index()
        count_df.columns = ['이름', '횟수']
        # 모든 멤버 표시를 위해 병합
        full_stats = pd.DataFrame(members, columns=['이름'])
        full_stats = pd.merge(full_stats, count_df, on='이름', how='left').fillna(0)
        st.table(full_stats)
    else:
        st.write("아직 기록이 없습니다.")

# 2. 최근 결제 내역 (날짜 포함)
with col2:
    st.subheader("📜 최근 내역")
    if st.session_state.history_list:
        # 최신순으로 정렬하여 표시
        st.dataframe(pd.DataFrame(st.session_state.history_list).iloc[::-1], hide_index=True)
    else:
        st.write("내역 없음")

# 초기화 버튼
if st.button("🔄 전체 기록 초기화"):
    st.session_state.current_idx = 0
    st.session_state.history_list = []
    st.rerun()
