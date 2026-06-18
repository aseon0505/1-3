import streamlit as st
import random

st.set_page_config(
    page_title="Eco Money Challenge",
    page_icon="🌎",
    layout="wide"
)

# ---------------------------
# 초기 상태
# ---------------------------
if "money" not in st.session_state:
    st.session_state.money = 0

if "answered" not in st.session_state:
    st.session_state.answered = False

if "current_question" not in st.session_state:
    st.session_state.current_question = None

if "remaining_questions" not in st.session_state:

    questions = []

    # ---------------------------
    # OX 문제 50개
    # ---------------------------
    for i in range(1, 51):
        questions.append({
            "type": "OX",
            "question": f"플라스틱 병은 내용물을 비우고 버려야 한다. ({i})",
            "answer": "O",
            "explanation": "플라스틱 병은 내용물을 비우고 배출해야 재활용이 가능합니다."
        })

    # ---------------------------
    # 객관식 50개
    # ---------------------------
    for i in range(51, 101):
        questions.append({
            "type": "MCQ",
            "question": f"재활용이 가능한 것은 무엇일까요? ({i})",
            "options": [
                "깨끗한 종이",
                "음식물 묻은 종이",
                "일반 쓰레기",
                "오염된 비닐"
            ],
            "answer": "깨끗한 종이",
            "explanation": "깨끗한 종이는 재활용 가능하지만 오염된 종이는 일반쓰레기입니다."
        })

    random.shuffle(questions)

    st.session_state.remaining_questions = questions

if "inventory" not in st.session_state:
    st.session_state.inventory = []

# ---------------------------
# 스타일
# ---------------------------

st.markdown("""
<style>

.main-title{
font-size:45px;
font-weight:bold;
color:#2e7d32;
text-align:center;
}

.money-box{
position:fixed;
bottom:20px;
right:20px;
background:#2e7d32;
color:white;
padding:15px;
border-radius:15px;
font-size:22px;
font-weight:bold;
z-index:9999;
}

.shop-card{
padding:15px;
border-radius:12px;
border:2px solid #ddd;
margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# 우측 하단 돈 표시
# ---------------------------

st.markdown(
f"""
<div class="money-box">
💰 {st.session_state.money:,} 원
</div>
""",
unsafe_allow_html=True
)

# ---------------------------
# 메뉴
# ---------------------------

menu = st.sidebar.radio(
    "메뉴",
    ["🏠 HOME", "📝 QUIZ", "🛒 SHOP", "🎒 MY ITEMS"]
)

# ---------------------------
# HOME
# ---------------------------

if menu == "🏠 HOME":

    st.markdown(
        '<p class="main-title">🌎 Eco Money Challenge 🌎</p>',
        unsafe_allow_html=True
    )

    st.image(
        "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=1200",
        use_container_width=True
    )

    st.success(
        "올바른 분리수거를 배우고 돈을 모아 친환경 아이템을 구매해보세요!"
    )

    total = 100
    solved = total - len(st.session_state.remaining_questions)

    st.progress(solved / total)

    st.write(f"진행도 : {solved} / {total}")

# ---------------------------
# QUIZ
# ---------------------------

elif menu == "📝 QUIZ":

    st.header("♻️ 분리수거 퀴즈")

    if len(st.session_state.remaining_questions) == 0:
        st.success("🎉 모든 문제를 완료했습니다!")
        st.balloons()

    else:

        if st.session_state.current_question is None:
            st.session_state.current_question = st.session_state.remaining_questions.pop()

        q = st.session_state.current_question

        st.subheader(q["question"])

        if q["type"] == "OX":

            answer = st.radio(
                "정답 선택",
                ["O", "X"],
                key=q["question"]
            )

        else:

            answer = st.radio(
                "정답 선택",
                q["options"],
                key=q["question"]
            )

        if st.button("제출"):

            if answer == q["answer"]:

                st.success("정답입니다! +300원")
                st.session_state.money += 300

            else:

                st.error("틀렸습니다! -100원")
                st.session_state.money = max(
                    0,
                    st.session_state.money - 100
                )

            st.info("해설")
            st.write(q["explanation"])

            st.session_state.current_question = None

# ---------------------------
# SHOP
# ---------------------------

elif menu == "🛒 SHOP":

    st.header("🛍️ 친환경 상점")

    items = [
        ("대나무 칫솔", 1000),
        ("에코 텀블러", 2000),
        ("재활용 노트", 3000),
        ("친환경 가방", 4000),
        ("태양광 랜턴", 5000),
        ("에코 도시락", 6000),
        ("업사이클 파우치", 7000),
        ("친환경 의자", 8000),
        ("미니 태양광 패널", 9000),
        ("환경 수호자 세트", 10000),
    ]

    for item, price in items:

        col1, col2 = st.columns([3,1])

        with col1:
            st.markdown(
                f"""
                <div class="shop-card">
                <h4>{item}</h4>
                <p>{price:,}원</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:

            if st.button(
                f"구매-{item}"
            ):

                if st.session_state.money >= price:

                    st.session_state.money -= price
                    st.session_state.inventory.append(item)

                    st.success("구매 완료!")

                else:
                    st.error("돈이 부족합니다.")

# ---------------------------
# MY ITEMS
# ---------------------------

elif menu == "🎒 MY ITEMS":

    st.header("🎁 내가 구매한 물건")

    if len(st.session_state.inventory) == 0:
        st.info("아직 구매한 물건이 없습니다.")

    else:

        for item in st.session_state.inventory:
            st.write("✅", item)
