import streamlit as st
from home_page import show_home_page
from letter_page import show_letter_page
from open_letter_page import show_open_letter_page


st.set_page_config(
    page_title="Slow Letter",
    page_icon="📮",
    layout="centered"
)


def load_app_css():
    st.markdown("""
    <style>
    .stApp {
        background:
            radial-gradient(circle at top, rgba(184,134,11,0.15), transparent 35%),
            linear-gradient(180deg, #120c08 0%, #050403 100%);
        color: #f5e8c7;
    }

    .block-container {
        max-width: 480px;
        padding-top: 5rem;
    }

    label, p, span, h1, h2, h3 {
        color: #f5e8c7 !important;
    }

    div[data-testid="stTextInput"] input {
        background-color: #17100b !important;
        color: #f5e8c7 !important;
        border: 1px solid rgba(218,165,32,0.45) !important;
        border-radius: 14px !important;
    }
    </style>
    """, unsafe_allow_html=True)


load_app_css()


query_params = st.query_params
shared_letter_id = query_params.get("letter_id", None)


#if not st.user.is_logged_in:
   # st.title("📮 Slow Letter")
  #  st.write("Google 계정으로 로그인하세요.")

  #  if st.button("Google 로그인"):
   #     st.login()

  #  st.stop()


st.sidebar.title("📮 Slow Letter")
st.sidebar.success(f"{st.user.name}님 로그인 중")

if st.sidebar.button("로그아웃"):
    st.logout()


page = st.sidebar.radio(
    "메뉴",
    ["홈", "편지 쓰기", "편지 열기"]
)


if shared_letter_id:
    show_open_letter_page(shared_letter_id)

else:
    if page == "홈":
        show_home_page()

    elif page == "편지 쓰기":
        show_letter_page()

    elif page == "편지 열기":
        letter_id = st.text_input("편지 링크 ID를 입력하세요")

        if letter_id:
            show_open_letter_page(letter_id)
        else:
            st.info("카카오톡이나 문자로 받은 편지 ID를 입력하면 편지를 확인할 수 있습니다.")