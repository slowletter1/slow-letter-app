import streamlit as st
from datetime import date, datetime
import uuid
from supabase import create_client
import streamlit.components.v1 as components


supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)


def save_letter_to_supabase(letter):
    supabase.table("letters").insert(letter).execute()


def load_letters_from_supabase():
    response = (
        supabase
        .table("letters")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )
    return response.data

def load_my_sent_letters():
    response = (
        supabase
        .table("letters")
        .select("*")
        .eq("sender_email", st.user.email)
        .order("created_at", desc=True)
        .execute()
    )

    return response.data

def load_letter_css():
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

    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea,
    div[data-testid="stDateInput"] input {
        background-color: #17100b !important;
        color: #f5e8c7 !important;
        border: 1px solid rgba(218,165,32,0.45) !important;
        border-radius: 14px !important;
    }

    div[data-testid="stTextArea"] textarea {
        min-height: 220px;
    }

    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #d4af37, #8a6420);
        color: #120c08;
        border: none;
        border-radius: 16px;
        padding: 0.85rem 1rem;
        font-weight: 900;
    }
    </style>
    """, unsafe_allow_html=True)


def show_letter_page():
    load_letter_css()

    st.caption("DARK SLOW POST OFFICE")
    st.title("📮 Slow Letter")

    st.write(
        "기다림이 선물이 되는 온라인 우체국.\n\n"
        "지금의 마음을 봉투에 담아 미래의 나 또는 소중한 사람에게 보내세요."
    )

    st.info(
        "🔒 이 편지는 정해진 날까지 잠겨 있습니다.\n\n"
        "빠르게 소비되는 메시지가 아니라, 시간이 지나 더 깊어지는 마음을 보관합니다."
    )

    st.divider()

    st.subheader("✉ 잠긴 편지 작성")

    sender = st.text_input("보내는 사람", placeholder="내 이름 또는 닉네임")
    receiver = st.text_input("받는 사람", placeholder="미래의 나, 친구, 연인, 가족")
    receiver_contact = st.text_input("받는 사람 연락처", placeholder="010-0000-0000")
    open_date = st.date_input("열리는 날짜", value=date.today())
    title = st.text_input("편지 제목", placeholder="오늘의 마음을 한 줄로 적어보세요")
    content = st.text_area(
        "편지 내용",
        placeholder="지금의 감정, 다짐, 고마움, 후회를 천천히 적어보세요."
    )

    st.info(
        f"📩 알림 미리보기\n\n"
        f"{sender if sender else '000'}님이 진심을 담은 편지를 보냈습니다.\n\n"
        f"제목: {title if title else '아직 제목이 없습니다'}\n\n"
        f"🔒 이 편지는 아직 잠겨 있습니다.\n\n"
        f"개봉일: {open_date}\n\n"
        f"앱에서 확인해 주세요."
    )

    st.divider()

    st.subheader("📱 카카오톡 알림 미리보기")
    preview_letter_id = "********"

    st.success(
        f"📩 편지 도착 알림\n\n"
        f"{sender if sender else '000'}님이 진심을 담은 편지를 보냈습니다.\n\n"
        f"제목\n"
        f"『{title if title else '제목 없음'}』\n\n"
        f"🔒 이 편지는 아직 잠겨 있습니다.\n\n"
        f"개봉일\n"
        f"{open_date}\n\n"
        f"편지 ID\n"
        f"{preview_letter_id}\n\n"
        f"앱에서 확인해 보세요.\n\n"
        f"http://slow-letter-app-cgw2dfczedxrtw7r3nocvz.streamlit.app/?letter_id=********"
    )

    st.info(
        f"✉ 개봉일 알림\n\n"
        f"{sender if sender else '000'}님이 보낸 편지를 열 수 있습니다.\n\n"
        f"제목\n"
        f"『{title if title else '제목 없음'}』\n\n"
        f"편지 ID\n"
        f"{preview_letter_id}\n\n"
        f"지금 앱에서 확인해 보세요.\n\n"
        f"http://slow-letter-app-cgw2dfczedxrtw7r3nocvz.streamlit.app/?letter_id=********"
    )

    if st.button("📮 봉투에 담아 보내기"):
        
        if not sender or not receiver or not title or not content:
            st.warning("보내는 사람, 받는 사람, 제목, 편지 내용을 모두 입력해주세요.")
        else:
            letter_id = str(uuid.uuid4())[:8]

            new_letter = {
                "sender": sender,
                "sender_email": st.user.email,
                "receiver": receiver,
                "receiver_contact": receiver_contact,
                "letter_id": letter_id,
                "open_date": str(open_date),
                "title": title,
                "content": content,
            }


            save_letter_to_supabase(new_letter)

            st.success("편지가 잠긴 봉투에 보관되었습니다.")

            st.info(
                f"📮 공유용 편지 ID\n\n"
                f"{letter_id}\n\n"
                f"상대방에게 이 ID를 보내면, 편지 열기 화면에서 확인할 수 있습니다."
            )

            st.code(
                f"https://slow-letter-app-cgw2dfczedxrtw7r3nocvz.streamlit.app/?letter_id={letter_id}",
                language="text"
            )

            st.caption("상대방에게 이 링크를 보내면 편지를 확인할 수 있습니다.")

    st.divider()

    st.subheader("📬 내가 보낸 편지")

    my_letters = load_my_sent_letters()

    if not my_letters:
        st.caption("아직 보낸 편지가 없습니다.")

    else:
        for letter in my_letters:
            st.info(
                f"✉ **{letter['title']}**\n\n"
                f"To. {letter['receiver']}\n\n"
                f"개봉일: {letter['open_date']}\n\n"
                f"편지 ID: {letter['letter_id']}"
            )

            share_url = f"https://slow-letter-app-cgw2dfczedxrtw7r3nocvz.streamlit.app/?letter_id={letter['letter_id']}"
        
            st.markdown("### 🔗 카카오톡 · 인스타그램으로 공유하기")

    st.caption(
        "아래 링크를 복사해서 카카오톡이나 인스타그램 DM으로 보내주세요."
    )

    st.link_button(
        "💬 공유 링크 열기",
        share_url
    )

    st.code(share_url, language="text")
if __name__ == "__main__":
    show_letter_page()