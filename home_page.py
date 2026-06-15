import streamlit as st
import json
import os

def load_home_css():
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
        padding-top: 28px;
    }

    label, p, span, h1, h2, h3 {
        color: #f5e8c7 !important;
    }
    </style>
    """, unsafe_allow_html=True)

LETTER_FILE = "letters.json"


def load_letters():
    if not os.path.exists(LETTER_FILE):
        return []

    with open(LETTER_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def show_home_page():
    load_home_css()
    letters = load_letters()

    st.title("📮 Slow Letter")

    st.markdown(
        """
### 기다림은 더 큰 선물로 돌아옵니다.

빠르게 소비되는 메시지가 아니라,

시간이 지나 더욱 깊어지는 마음을 전합니다.
"""
    )

    st.divider()

    st.subheader("💌 이런 편지를 보낼 수 있어요")

    st.write("✉ 미래의 나에게")
    st.write("❤️ 사랑하는 사람에게")
    st.write("🎂 생일에 열리는 편지")
    st.write("👨‍👩‍👧 가족에게 남기는 마음")

    st.divider()

    st.subheader("📬 현재 보관 중")

    st.metric(
        "총 편지 수",
        len(letters)
    )

    st.divider()

    st.info(
        """
기다림은 단순한 시간이 아니라,

더 큰 선물이 되어 돌아옵니다.
"""
    )