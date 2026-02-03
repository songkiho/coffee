import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# 1. 앱 설정
st.set_page_config(page_title="커피당번", page_icon="☕", layout="centered")

# 2. 카카오톡 탈출을 위한 고대비 디자인
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    * { font-family: 'Apple SD Gothic Neo', sans-serif; color: #1C1C1E; }
    
    /* 탈출용 비상 버튼 디자인 (노란색) */
    .exit-btn div.stButton > button {
        background-color: #FEE500 !important; /* 카카오 노란색 */
        color: #191919 !important;
        border: 1px solid #FEE500;
        height: 4rem;
        font-size: 1.2rem;
        margin-bottom: 20px;
    }

    .main-card {
        background-color: #F2F2F7;
        padding: 30px 20px;
        border-radius: 20px;
        margin-bottom: 25px;
        border: 1px solid #E5E5EA;
        text-align: center;
    }
    
    .winner-name {
        color: #007AFF;
        font-size: 3.2rem;
        font-weight: 900;
        margin: 15px 0;
    }

    /* 메인 버튼 */
    .primary-btn div.stButton > button {
        width: 100%;
        border-radius: 15px;
        height: 5rem;
        background-color: #007AFF;
        color: #FFFFFF !important;
        font-weight: 800;
        font-size: 1.5rem;
    }
    
    .link-btn div.stButton > button {
        height: 3.8rem;
        background-color: #FFFFFF;
        color: #007AFF !important;
        border: 2px solid #007AFF;
    }
    </style>
    """, unsafe_allow_html=True)

# --- [비상 탈출 섹션: 카카오톡 내부 브라우저 감지 시 노출] ---
# 실제 배포 후 URL이 확정되면 아래 'your-app-url' 자리에 주소를 넣으세요.
current_url = "https://coffee-dangbun.streamlit.app" # 예시 주소

st.markdown('<div class="exit-btn">', unsafe_allow_html=True)
if st.button("🚀 (아이폰 전용) Safari 브라우저로 열기"):
    # 카카오톡 외부브라우저 호출 스키마
    out_link = f"kakaotalk://web/openExternal?url={urllib.parse.quote(current_url)}"
    st.markdown(f'<meta http-equiv="refresh" content="0;url={out_link}">', unsafe_allow_html=True)
    st.write("잠시만 기다려주세요... Safari로 이동합니다.")
st.markdown('</div>', unsafe_allow_html=True)

st.caption("⚠️ 위 버튼이 안 된다면? 오른쪽 아래 [···] → [다른 브라우저로 열기] 클릭!")
st.divider()

# --- [메인 기능: 커피당번] ---
st.markdown('# ☕ 커피당번')

members = ["규리", "조조", "은비", "까비"]
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'history_list' not in st.session_state: st.session_state.history_list = []

st.markdown('<div class="main-card">', unsafe_allow_html=True)
current_person = members[st.session_state.current_idx]
st.markdown(f"오늘 커피 쏠 사람은?", unsafe_allow_html=True)
st.markdown(f'<div class="winner-name">{current_person}</div>', unsafe_allow_html=True)

st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
if st.button("✅ 결제 완료! 다음 순번으로"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    st.session_state.history_list.append({"날짜": now, "이름": current_person})
    st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
    st.rerun()
st.markdown('</div></div>', unsafe_allow_html=True)

# --- [통계 섹션] ---
st.markdown("### 📊 구입 현황")
df = pd.DataFrame(st.session_state.history_list)
stats = df['이름'].value_counts().reindex(members, fill_value=0).reset_index() if not df.empty else pd.DataFrame(members, columns=['이름']).assign(count=0)
stats.columns = ['이름', '횟수']
st.table(stats)

# --- [실시간 정보] ---
st.markdown('<div class="link-btn">', unsafe_allow_html=True)
st.link_button("🍱 오늘 메뉴 확인", "https://pf.kakao.com/_jxcvzn/posts", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

with st.expander("🛠️ 초기화"):
    if st.button("🔄 기록 리셋"):
        st.session_state.current_idx = 0
        st.session_state.history_list = []
        st.rerun()
