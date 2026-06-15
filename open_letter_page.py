import streamlit as st
from datetime import date, datetime
from supabase import create_client


supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)


def find_letter_by_id(letter_id):
    response = (
        supabase
        .table("letters")
        .select("*")
        .eq("letter_id", letter_id)
        .execute()
    )

    if response.data:
        return response.data[0]

    return None


def load_open_letter_css():
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
    </style>
    """, unsafe_allow_html=True)


def show_open_letter_page(letter_id):
    load_open_letter_css()

    st.title("📮 Slow Letter")

    letter = find_letter_by_id(letter_id)

    if letter is None:
        st.error("존재하지 않는 편지입니다.")
        return

    today = date.today()
    open_day = datetime.strptime(letter["open_date"], "%Y-%m-%d").date()

    st.caption("잠긴 편지 도착")

    st.write(
        f"{letter.get('sender', '누군가')}님이 "
        f"{letter.get('receiver', '당신')}님에게 진심을 담은 편지를 보냈습니다."
    )

    st.subheader(f"『{letter['title']}』")

    if today < open_day:
        d_day = (open_day - today).days

        st.info(
            f"🔒 이 편지는 아직 잠겨 있습니다.\n\n"
            f"개봉일: {letter['open_date']}\n\n"
            f"⏳ {d_day}일 후 열 수 있습니다.\n\n"
            f"조금만 더 기다려 주세요."
        )
    else:
        st.success("✉ 편지를 열 수 있습니다.")

        st.write(f"From. {letter.get('sender', '알 수 없음')}")
        st.write(f"To. {letter.get('receiver', '알 수 없음')}")
        st.write(f"작성일: {letter.get('created_at', '알 수 없음')}")

        st.divider()

        st.write(letter["content"])


if __name__ == "__main__":
    test_id = st.text_input("테스트용 letter_id 입력")
    if test_id:
        show_open_letter_page(test_id)