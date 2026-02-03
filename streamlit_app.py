import streamlit as st
import random
import pandas as pd

# 앱 타이틀 및 설정
st.set_page_config(page_title="커피 당번 뽑기", page_icon="☕")
st.title("☕ 커피 당번 어플")

# 팀원 명단
members = ["규리", "조조", "은비", "까비"]

# 세션 상태 초기화 (당첨 횟수 저장용)
if 'history' not in st.session_state:
    st.session_state.history = {name: 0 for name in members}

# 메인 화면 구성
st.subheader("오늘의 운명은?")
if st.button("🔥 당번 추첨하기", use_container_width=True):
    winner = random.choice(members)
    st.session_state.history[winner] += 1
    st.balloons()
    st.success(f"🎊 오늘의 커피 당번은 **[{winner}]** 님입니다!")

st.divider()

# 누적 통계 보기
st.subheader("📊 누적 당첨 횟수")
df = pd.DataFrame(
    list(st.session_state.history.items()), 
    columns=['이름', '당첨 횟수']
)
st.table(df)

# 초기화 버튼
if st.button("기록 초기화"):
    st.session_state.history = {name: 0 for name in members}
    st.rerun()
