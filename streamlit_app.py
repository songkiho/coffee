import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
import streamlit.components.v1 as components

# 1. 앱 설정
st.set_page_config(page_title="커피당번", page_icon="☕", layout="centered")

# 2. 디자인 설정 (녹색 테마 + 검정 글씨)
st.markdown("""
    <style>
    /* 기본 폰트 및 색상 */
    .stApp { background-color: #FFFFFF !important; }
    h1, h2, h3, p, div, span, label, li, input { 
        font-family: 'Apple SD Gothic Neo', sans-serif !important; 
        color: #1C1C1E !important; 
    }

    /* 버튼 스타일 통일 (녹색 배경 + 검정 글씨) */
    .stButton > button, .stLinkButton > a {
        background-color: #28A745 !important; 
        color: #000000 !important;       
        border: 1px solid #1E7E34 !important; 
        border-radius: 12px !important;
        font-weight: 900 !important;     
        font-size: 1rem !important;
        height: 3.5rem !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-decoration: none !important;
    }
    
    .stButton > button:hover, .stLinkButton > a:hover {
        background-color: #218838 !important;
        color: #000000 !important;
        border-color: #1C7430 !important;
    }

    /* 메뉴 박스 디자인 */
    .menu-box {
        background-color: #F8F9FA;
        border: 2px solid #28A745;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }

    /* 메인 결제 버튼 (크게) */
    .buy-btn div.stButton > button {
        height: 5.5rem !important;
        font-size: 1.6rem !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    /* 당번 카드 */
    .info-card {
        background-color: #F2F2F7;
        padding: 30px 20px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 20px;
        border: 1px solid #E5E5EA;
    }
    .winner-name { color: #000000 !important; font-size: 4rem !important; font-weight: 900 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 데이터 초기화 ---
members = ["기호", "인식", "성민", "현석"]
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'history_list' not in st.session_state: st.session_state.history_list = []
if 'pass_list' not in st.session_state: st.session_state.pass_list = []
if 'view_state' not in st.session_state: st.session_state.view_state = None
if 'confirm_reset' not in st.session_state: st.session_state.confirm_reset = False
if 'menu_open' not in st.session_state: st.session_state.menu_open = False

# --- 상단 타이틀 ---
st.markdown("# ☕ 커피당번")

# --- ☰ 메뉴 토글 버튼 ---
menu_label = "🔼 메뉴 닫기" if st.session_state.menu_open else "☰ 메뉴 및 통계 열기"

if st.button(menu_label, use_container_width=True):
    st.session_state.menu_open = not st.session_state.menu_open
    # 메뉴를 닫을 때 초기화 상태도 리셋하여 깔끔하게
    if not st.session_state.menu_open:
        st.session_state.confirm_reset = False
    st.rerun()

# --- 메뉴 내부 화면 ---
if st.session_state.menu_open:
    st.markdown('<div class="menu-box">', unsafe_allow_html=True)
    st.markdown("### 📊 통계 센터")
    
    # 1. 누적 구입
    st.markdown("**💰 누적 커피**")
    df_h = pd.DataFrame(st.session_state.history_list)
    stats = df_h['이름'].value_counts().reindex(members, fill_value=0).reset_index() if not df_h.empty else pd.DataFrame(members, columns=['이름']).assign(count=0)
    stats.columns = ['이름', '횟수']
    st.table(stats)
    
    # 2. 패스 기록
    st.markdown("**🚫 패스 기록**")
    df_p = pd.DataFrame(st.session_state.pass_list)
    if not df_p.empty:
        p_stats = df_p.groupby(['이름', '사유']).size().unstack(fill_value=0).reindex(members, fill_value=0).reset_index()
        st.table(p_stats)
    else:
        st.caption("패스 기록 없음")
        
    st.divider()
    
    # 3. [보안 강화] 비밀번호 입력 후 초기화
    st.markdown("### ⚙️ 설정")
    
    # 초기화 버튼을 아직 안 눌렀다면 -> 버튼 표시
    if not st.session_state.confirm_reset:
        if st.button("🗑️ 기록 초기화", key="reset_trigger"):
            st.session_state.confirm_reset = True
            st.rerun()
    
    # 초기화 버튼을 눌렀다면 -> 비밀번호 입력창 표시
    else:
        st.warning("⚠️ 초기화하려면 비밀번호를 입력하세요.", icon="🔒")
        
        # 비밀번호 입력 필드
        input_pw = st.text_input("비밀번호 4자리", type="password", key="reset_pw_input")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("네 (삭제)", key="reset_yes"):
                if input_pw == "1111":
                    st.session_state.current_idx = 0
                    st.session_state.history_list = []
                    st.session_state.pass_list = []
                    st.session_state.confirm_reset = False
                    st.success("모든 기록이 초기화되었습니다!")
                    st.rerun()
                else:
                    st.error("비밀번호가 틀렸습니다.")
        with c2:
            if st.button("취소", key="reset_no"):
                st.session_state.confirm_reset = False
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- 메인 화면 (당번 확인) ---
st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
current_name = members[st.session_state.current_idx]

st.markdown(f"""
    <div class="info-card">
        <p style='color:#555555 !important; font-size:1.1rem; margin-bottom:5px; font-weight:bold;'>오늘 커피 주인공</p>
        <div class="winner-name">{current_name}</div>
    </div>
    """, unsafe_allow_html=True)

# 결제 버튼
st.markdown('<div class="buy-btn">', unsafe_allow_html=True)
if st.button("✅ 오늘 결제 완료"):
    now = datetime.now().strftime("%m/%d %H:%M")
    st.session_state.history_list.append({"날짜": now, "이름": current_name})
    st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members)
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# 패스 버튼
st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
col_l, col_r = st.columns(2)
with col_l:
    if st.button("⏰ 지각 PASS"):
        st.session_state.pass_list.append({"이름": current_name, "사유": "지각"})
        st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members); st.rerun()
with col_r:
    if st.button("🌴 휴가 PASS"):
        st.session_state.pass_list.append({"이름": current_name, "사유": "휴가"})
        st.session_state.current_idx = (st.session_state.current_idx + 1) % len(members); st.rerun()

st.divider()

# --- 하단 링크 ---
st.subheader("🔗 성수동 정보")
b1, b2 = st.columns(2)
with b1:
    if st.button("🍱 오늘 메뉴 보기"):
        st.session_state.view_state = 'menu' if st.session_state.view_state != 'menu' else None
with b2:
    query = urllib.parse.quote("2026년 성수동 팝업스토어")
    st.link_button("🔥 성수 팝업 검색 (새창)", f"https://search.naver.com/search.naver?query={query}")

if st.session_state.view_state == 'menu':
    st.info("💡 화면이 안 보이면 아래 버튼을 눌러주세요.")
    components.iframe("https://pf.kakao.com/_jxcvzn/posts", height=500, scrolling=True)
    st.link_button("🌐 새창으로 메뉴 보기", "https://pf.kakao.com/_jxcvzn/posts")
