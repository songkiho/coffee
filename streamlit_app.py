import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# 1. 앱 설정
st.set_page_config(page_title="커피당번", page_icon="☕", layout="centered")

# 2. 카카오톡 외부 브라우저 호출 스크립트 (모바일 최적화)
# 카카오톡 브라우저로 접속 시 자동으로 Safari 등을 호출하거나 안내합니다.
st.markdown("""
    <script>
    var userAgent = navigator.userAgent.toLowerCase();
    var targetUrl = location.href;

    if (userAgent.match(/kakaotalk/i)) {
        // 카카오톡 외부브라우저 강제 호출 주소 (아이폰용)
        location.href = 'kakaotalk://web/openExternal?url=' + encodeURIComponent(targetUrl);
    }
    </script>
    
    <style>
    .stApp { background-color: #FFFFFF; }
    * { font-family: 'Apple SD Gothic Neo', sans-serif; color: #1C1C1E; }
    
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

    div.stButton > button {
        width: 100%;
        border-radius: 15px;
        height: 5rem;
        background-color: #007AFF;
        color: #FFFFFF !important;
        font-weight: 800;
        font-size: 1.5rem;
        border: none;
        box-shadow: 0 4px 15px rgba(0,122,255,0.3);
    }
    
    .link-btn div.stButton > button {
        height: 4rem;
        background-color: #FFFFFF;
        color: #007AFF !important;
        border: 2px solid #007AFF;
        font-size: 1.2rem;
        box-shadow: none;
        margin-bottom: 10px;
    }

    .stTable { background-color: white; border-radius: 12px; overflow: hidden; border: 1px solid #E5E5EA; }
    </style>
    """, unsafe_allow_html=True)

# 카카오톡 사용자에게 한 번 더 안내 (스크립트가 차단될 경우 대비)
if "Kakaotalk" in st.query_params.get("user-agent", ""):
    st.warning("⚠️ 카카오톡 브라우저에서는 '홈 화면 추가'가 어렵습니다. 오른쪽 하단 '···' 버튼을 눌러 '다른 브라우저로 열기'를 선택해주세요.")

# --- [상단 헤더] ---
st.markdown('# ☕ 커피당번')
st.markdown(f"**{datetime.now().strftime('%Y년 %m월 %d일')}**")

# --- [당번 안내 섹션] ---
members = ["규리", "조조", "은비", "까비"]
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'history_list' not in st.session_state: st.session_state.history_list = []

st.markdown('<div class="main-card">', unsafe_allow_html=True)
current_person = members[st.session_state.current_idx]
st.markdown(f"**오늘 커피 쏠 사람은?**", unsafe_allow_html=True)
st.markdown(f'<div class="winner-name">{current_person}</div>', unsafe_allow_html=True)

if st.button("✅ 결제 완료! 다음 순번으로"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    st.session_state.history_list.append({"날짜": now, "이름": current_person})
    st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- [구입 현황 섹션] ---
st.markdown("### 📊 구입 현황")
df = pd.DataFrame(st.session_state.history_list)

st.markdown("##### 🏆 멤버별 누적 횟수")
stats = df['이름'].value_counts().reindex(members, fill_value=0).reset_index() if not df.empty else pd.DataFrame(members, columns=['이름']).assign(count=0)
stats.columns = ['이름', '구입 횟수']
st.table(stats)

st.markdown("##### 🕒 최근 기록 (3회)")
if not df.empty:
    st.table(df.iloc[::-1].head(3))
else:
    st.info("아직 결제 내역이 없습니다.")

st.divider()

# --- [실시간 정보 섹션] ---
st.markdown("### 🔗 성수동 실시간 정보")
st.markdown('<div class="link-btn">', unsafe_allow_html=True)
st.link_button("🍱 오늘 메뉴 (카카오 채널)", "https://pf.kakao.com/_jxcvzn/posts", use_container_width=True)
popup_q = urllib.parse.quote("2026년 성수동 팝업스토어 최신")
st.link_button("🔥 2026 성수 팝업 검색", f"https://search.naver.com/search.naver?query={popup_q}", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

with st.expander("🛠️ 설정"):
    if st.button("🔄 기록 리셋"):
        st.session_state.current_idx = 0
        st.session_state.history_list = []
        st.rerun()
