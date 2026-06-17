import streamlit as st
import random

st.set_page_config(
    page_title="Eco Money",
    page_icon="♻️",
    layout="wide"
)

# ----------------------
# 초기 데이터
# ----------------------

quiz_data = [
    {
        "type": "OX",
        "question": "깨끗이 씻은 페트병은 재활용이 가능하다.",
        "answer": "O",
        "explanation": "페트병은 내용물을 비우고 씻은 후 배출해야 재활용이 가능합니다."
    },
    {
        "type": "OX",
        "question": "음식물이 묻은 종이는 종이류로 재활용할 수 있다.",
        "answer": "X",
        "explanation": "오염된 종이는 일반 쓰레기로 버려야 합니다."
    },
    {
        "type": "MC",
        "question": "우유팩은 어디에 버려야 할까요?",
        "options": [
            "일반 쓰레기",
            "종이팩 수거함",
            "플라스틱",
            "캔류"
        ],
        "answer": "종이팩 수거함",
        "explanation": "우유팩은 일반 종이와 분리하여 종이팩 수거함에 배출합니다."
    },
    {
        "type": "MC",
        "question": "배터리는 어떻게 버려야 할까요?",
        "options": [
            "일반 쓰레기",
            "음식물 쓰레기",
            "폐건전지 수거함",
            "플라스틱"
        ],
        "answer": "폐건전지 수거함",
        "explanation": "배터리는 전용 수거함에 배출해야 합니다."
    },
    {
        "type": "OX",
        "question": "캔은 내용물을 비우고 버려야 한다.",
        "answer": "O",
        "explanation": "내용물을 비우고 헹군 후 배출하는 것이 좋습니다."
    },
    {
        "type": "MC",
        "question": "깨진 유리는 어디에 버려야 할까요?",
        "options": [
            "유리병 수거함",
            "일반 쓰레기",
            "플라스틱",
            "종이류"
        ],
        "answer": "일반 쓰레기",
        "explanation": "깨진 유리는 재활용되지 않으므로 일반 쓰레기로 배출합니다."
    }
]

shop_items = [
    ("에코 스티커", 1000),
    ("재활용 배지", 2000),
    ("친환경 텀블러", 3000),
    ("에코 노트", 4000),
    ("대나무 칫솔 세트", 5000),
    ("재사용 장바구니", 6000),
    ("에코 키링", 7000),
    ("친환경 물병", 8000),
    ("태양광 손전등", 9000),
    ("친환경 선물 상자", 10000),
]

# ----------------------
# 세션 상태
# ----------------------

if "money" not in st.session_state:
    st.session_state.money = 0

if "inventory" not in st.session_state:
    st.session_state.inventory = []

if "current_quiz" not in st.session_state:
    st.session_state.current_quiz = random.choice(quiz_data)

# ----------------------
# 제목
# ----------------------

st.title("♻️ Eco Money")
st.subheader("올바른 분리수거를 배우고 돈을 모아보세요!")

# ----------------------
# 퀴즈
# ----------------------

quiz = st.session_state.current_quiz

st.markdown("---")
st.header("🧠 분리수거 퀴즈")

st.write(f"### {quiz['question']}")

if quiz["type"] == "OX":

    answer = st.radio(
        "정답 선택",
        ["O", "X"],
        key="quiz_answer"
    )

else:

    answer = st.radio(
        "정답 선택",
        quiz["options"],
        key="quiz_answer"
    )

if st.button("제출하기"):

    try:

        if answer == quiz["answer"]:

            st.session_state.money += 300

            st.success("정답입니다! +300원")

        else:

            st.session_state.money = max(
                0,
                st.session_state.money - 100
            )

            st.error("오답입니다! -100원")
            st.info(f"해설: {quiz['explanation']}")

        st.session_state.current_quiz = random.choice(
            quiz_data
        )

        st.rerun()

    except Exception as e:
        st.error(f"오류 발생: {e}")

# ----------------------
# 상점
# ----------------------

st.markdown("---")
st.header("🛒 친환경 상점")

for item, price in shop_items:

    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        st.write(item)

    with col2:
        st.write(f"{price}원")

    with col3:

        if st.button(
            f"구매",
            key=item
        ):

            if st.session_state.money >= price:

                st.session_state.money -= price

                st.session_state.inventory.append(
                    item
                )

                st.success(
                    f"{item} 구매 완료!"
                )

            else:

                st.warning(
                    "돈이 부족합니다."
                )

# ----------------------
# 인벤토리
# ----------------------

st.markdown("---")
st.header("🎁 구매한 물건")

if st.session_state.inventory:

    for item in st.session_state.inventory:
        st.write("✅", item)

else:
    st.write("아직 구매한 물건이 없습니다.")

# ----------------------
# 우측 하단 돈 표시
# ----------------------

st.markdown(
    f"""
    <div style="
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: gold;
        color: black;
        padding: 15px;
        border-radius: 15px;
        font-size: 24px;
        font-weight: bold;
        z-index:9999;
        box-shadow: 2px 2px 10px gray;
    ">
        💰 {st.session_state.money}원
    </div>
    """,
    unsafe_allow_html=True
)
