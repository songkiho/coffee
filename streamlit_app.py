import streamlit as st

# 앱 설정
st.set_page_config(page_title="커피 순번 정하기", page_icon="☕")
st.title("☕ 이번엔 누구 차례?")

# 팀원 명단 (순서대로)
members = ["규리", "조조", "은비", "까비"]

# 세션 상태에 현재 순번(index) 저장
if 'current_idx' not in st.session_state:
    st.session_state.current_idx = 0

# 메인 화면 구성
current_person = members[st.session_state.current_idx]
next_person = members[(st.session_state.current_idx + 1) % len(members)]

st.info(f"📍 현재 순번: **{current_person}**")
st.write(f"⏭️ 다음 순번: {next_person}")

col1, col2 = st.columns(2)

with col1:
    if st.button("✅ 결제 완료 (다음 사람으로)", use_container_width=True):
        st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
        st.success(f"다음 차례는 {members[st.session_state.current_idx]} 님입니다!")
        st.rerun()

with col2:
    if st.button("🔄 순번 초기화", use_container_width=True):
        st.session_state.current_idx = 0
        st.warning("순번이 처음(규리)으로 돌아갔습니다.")
        st.rerun()

st.divider()

# 전체 순서도 보여주기
st.subheader("🏃 순번 리스트")
for i, name in enumerate(members):
    if i == st.session_state.current_idx:
        st.markdown(f"**👉 {i+1}번: {name} (Today)**")
    else:
        st.text(f"   {i+1}번: {name}")
