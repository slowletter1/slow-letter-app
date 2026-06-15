import streamlit as st
from datetime import date, datetime
import json
import os
import uuid


LETTER_FILE = "letters.json"


def load_letters():
    if not os.path.exists(LETTER_FILE):
        return []

    with open(LETTER_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_letters(letters):
    with open(LETTER_FILE, "w", encoding="utf-8") as f:
        json.dump(letters, f, ensure_ascii=False, indent=2)


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
    receiver = st.text_input("받는 사람", placeholder="미래의 나, 친구, 연인, 가족", key="receiver")
    receiver_contact = st.text_input(
    "받는 사람 연락처",
    placeholder="010-0000-0000"
)
    open_date = st.date_input("열리는 날짜", value=date.today(), key="open_date")
    title = st.text_input("편지 제목", placeholder="오늘의 마음을 한 줄로 적어보세요", key="title")
    content = st.text_area("편지 내용", placeholder="지금의 감정, 다짐, 고마움, 후회를 천천히 적어보세요.", key="content")
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
        f"http://localhost:8501/?letter_id=********"
    )

    st.info(
        f"✉ 개봉일 알림\n\n"
        f"{sender if sender else '000'}님이 보낸 편지를 열 수 있습니다.\n\n"
        f"제목\n"
        f"『{title if title else '제목 없음'}』\n\n"
        f"편지 ID/n"
        f"{preview_letter_id}"
        f"지금 앱에서 확인해 보세요."
        f"http://localhost:8501/?letter_id=********"
    )
    if st.button("📮 봉투에 담아 보내기"):
        if not sender or not receiver or not title or not content:
            st.warning("보내는 사람,받는 사람, 제목, 편지 내용을 모두 입력해주세요.")
        else:
            letters = load_letters()
            letter_id = str(uuid.uuid4())[:8]
            new_letter = {
                "sender": sender,
                "receiver": receiver,
                "receiver_contact": receiver_contact,

                "letter_id": letter_id,

                "open_date": str(open_date),
                "title": title,
                "content": content,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            letters.append(new_letter)
            save_letters(letters)
            
            st.success("편지가 잠긴 봉투에 보관되었습니다.")
           
            st.info(
                f"📮 공유용 편지 ID\n\n"
                f"{letter_id}\n\n"
                f"상대방에게 이 ID를 보내면, 편지 열기 화면에서 확인할 수 있습니다."
            )

            st.code(
                f"http://localhost:8501/?letter_id={letter_id}",
                language="text"
)
            st.link_button(
    st.info("카카오톡 공유 버튼은 실제 배포 도메인 연결 후 Kakao Developers 설정으로 붙일 예정입니다.")
)
            st.caption(
    "상대방에게 이 링크를 보내면 앱 없이도 편지를 확인할 수 있습니다."
)
            

    st.divider()

    st.subheader("🔒 잠긴 편지함")
    letters = load_letters()

    if not letters:
        st.caption("아직 보관된 편지가 없습니다.")
        return
    st.caption(f"총 {len(letters)}개의 편지가 보관되어 있습니다.")

    today = date.today()

    locked_letters = []
    opened_letters = []

    for letter in letters:
        open_day = datetime.strptime(letter["open_date"], "%Y-%m-%d").date()

        if open_day > today:
            locked_letters.append(letter)
        else:
            opened_letters.append(letter)
    if not locked_letters:
        st.caption("잠긴 편지가 없습니다.")

    for letter in reversed(locked_letters):
        open_day = datetime.strptime(letter["open_date"], "%Y-%m-%d").date()
        d_day = (open_day - today).days

        st.info(
            f"🔒 **{d_day}일 후 개봉**\n\n"
            f"To. {letter['receiver']}\n\n"
            f"제목: {letter['title']}\n\n"
            f"📅 {letter['open_date']}\n\n"
            f"기다림이 선물이 됩니다."
        )

    st.divider()

    st.subheader("✉ 열린 편지함")

    if not opened_letters:
        st.caption("아직 열린 편지가 없습니다.")

    for letter in reversed(opened_letters):
        with st.expander(f"✉ 개봉된 편지 · {letter['title']}"):
            st.write(f"To. {letter['receiver']}")
            st.write(f"작성일: {letter['created_at']}")
            st.divider()
            st.write(letter["content"])

if __name__ == "__main__":
    show_letter_page()