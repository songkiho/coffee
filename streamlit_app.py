import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
import streamlit.components.v1 as components

# 1. 앱 설정
st.set_page_config(page_title="커피당번", page_icon="☕", layout="wide")

# 2. 디자인 보정 (사이드바 버튼 글자 및 배경 대비 강화)
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    
    /* 사이드바 스타일 및 시스템 아이콘 제거 */
    [data-testid="stSidebar"] { background-color: #F2F2F7 !important; border-right: 1px solid #E5E5EA; }
    [data-testid="stSidebar"] span, [data-testid="stSidebar"] svg { display: none !important; }

    /* 사이드바 버튼: 흰색 배경에 굵은 파란색 글자 */
    [data-testid="stSidebar"] .stButton button {
        background-color: #FFFFFF !important;
        color: #007AFF !important;
        border: 2px solid #007AFF !important;
        height: 3.2rem !important;
        font-weight: 800 !important;
        font-size: 1rem !important;
    }
    
    /* 관리자 리셋 버튼: 빨간색 */
    [data-testid="stSidebar"] .reset-btn button {
        background-color: #FF3B30 !important;
        color: #FFFFFF !important;
        border: none !important;
    }

    /* 메인 카드 및 버튼 */
    .info-card { background-color: #F2F2F7; padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 20px; }
    .winner-name { color: #007AFF !important; font-size: 4.5rem !important; font-weight: 900 !important; }
    .buy-btn button { height: 5.5rem !important; background-color: #28A745 !important; color: white !important; font-size: 1.6rem !important; border-radius: 15px !important; }
    </style>
    """, unsafe_allow_html=True)

# 데이터 초기화
members = ["규리", "조조", "은비", "까비"]
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'history_list' not in st.session_state: st.session_state.history_list = []
if 'pass_list' not in st.session_state: st.session_state.pass_list = []
if 'admin_mode' not in st.session_state: st.session_state.admin_mode = False
if 'show_menu_box' not in st.session_state: st.session_state.show_menu_box = False

# --- ⬅️ 좌측 사이드바 (통계 및 관리) ---
with st.sidebar:
    st.markdown("### 📊 통계 센터")
    df_h = pd.DataFrame(st.session_state.history_list)
    stats = df_h['이름'].value_counts().reindex(members, fill_value=0).reset_index() if not df_h.empty else pd.DataFrame(members, columns=['이름']).assign(count=0)
    stats.columns = ['이름', '횟수']
    st.table(stats)
    
    st.markdown("**🚫 패스 현황**")
    df_p = pd.DataFrame(st.session_state.pass_list)
    if not df_p.empty:
        p_stats = df_p.groupby(['이름', '사유']).size().unstack(fill_value=0).reindex(members, fill_value=0).reset_index()
        st.table(p_stats)

    st.divider()
    if not st.session_state.admin_mode:
        if st.button("🔐 관리자 모드 열기"):
            st.session_state.admin_mode = True
            st.rerun()
    else:
        pw = st.text_input("비밀번호", type="password")
        st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
        if st.button("🧨 전체 기록 리셋"):
            if pw == "123qwe..":
                st.session_state.current_idx = 0
                st.session_state.history_list = []
                st.session_state.pass_list = []
                st.session_state.admin_mode = False
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("❌ 닫기"):
            st.session_state.admin_mode = False
            st.rerun()

# --- ➡️ 우측 메인 화면 ---
st.markdown("# ☕ 커피당번")
current_name = members[st.session_state.current_idx]

st.markdown(f"""
    <div class="info-card">
        <p style='color:#8E8E93 !important; font-size:1.2rem;'>오늘 커피 주인공</p>
        <div class="winner-name">{current_name}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="buy-btn">', unsafe_allow_html=True)
if st.button("✅ 오늘 결제 완료"):
    now = datetime.now().strftime("%m/%d %H:%M")
    st.session_state.history_list.append({"날짜": now, "이름": current_name})
    st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    if st.button("⏰ 지각 PASS"):
        st.session_state.pass_list.append({"이름": current_name, "사유": "지각"})
        st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members); st.rerun()
with col2:
    if st.button("🌴 휴가 PASS"):
        st.session_state.pass_list.append({"이름": current_name, "사유": "휴가"})
        st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members); st.rerun()

st.divider()

# --- 하단 정보 (보안을 고려한 연결) ---
st.subheader("🔗 성수동 실시간 정보")

# 1. 메뉴 확인 (선택적 박스 노출)
if st.button("🍱 오늘 메뉴 내부 박스로 보기", use_container_width=True):
    st.session_state.show_menu_box = not st.session_state.show_menu_box

if st.session_state.show_menu_box:
    st.info("💡 카카오 채널도 보안 정책에 따라 빈 화면이 나올 수 있습니다.")
    components.iframe("https://pf.kakao.com/_jxcvzn/posts", height=500, scrolling=True)

st.link_button("🌐 오늘 메뉴 새창으로 열기 (추천)", "https://pf.kakao.com/_jxcvzn/posts", use_container_width=True)

# 2. 네이버 팝업 검색 (보안상 100% 차단되므로 새창 버튼만 배치)
p_query = urllib.parse.quote("2026년 성수동 팝업스토어")
st.link_button("🔥 2026 성수 팝업 실시간 검색 (새창)", f"https://search.naver.com/search.naver?query={p_query}", use_container_width=True)
