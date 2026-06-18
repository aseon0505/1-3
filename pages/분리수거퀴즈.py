import streamlit as st
import random

st.set_page_config(
    page_title="에코 리워드 챌린지",
    page_icon="♻️",
    layout="wide"
)

# -------------------
# 문제 생성
# -------------------

base_questions = [
    {
        "question": "페트병은 라벨을 제거하고 버려야 한다.",
        "type": "OX",
        "answer": "O",
        "explanation": "라벨과 뚜껑을 제거하면 재활용 효율이 높아집니다."
    },
    {
        "question": "깨진 유리는 일반 유리수거함에 버린다.",
        "type": "OX",
        "answer": "X",
        "explanation": "깨진 유리는 신문지로 감싸 종량제 봉투에 버립니다."
    },
    {
        "question": "우유팩은 어디에 버려야 할까요?",
        "type": "MCQ",
        "options": [
            "일반쓰레기",
            "종이팩 수거함",
            "플라스틱",
            "음식물쓰레기"
        ],
        "answer": "종이팩 수거함",
        "explanation": "우유팩은 일반 종이와 분리하여 종이팩 수거함에 버립니다."
    },
    {
        "question": "음식물이 묻은 종이는?",
        "type": "MCQ",
        "options": [
            "종이류",
            "플라스틱",
            "일반쓰레기",
            "유리"
        ],
        "answer": "일반쓰레기",
        "explanation": "오염된 종이는 재활용이 어렵습니다."
    }
]

questions = []

for i in range(25):
    for q in base_questions:
        questions.append(q.copy())

random.shuffle(questions)

# -------------------
# 세션
# -------------------

if "money" not in st.session_state:
    st.session_state.money = 0

if "used" not in st.session_state:
    st.session_state.used = []

if "inventory" not in st.session_state:
    st.session_state.inventory = []

# -------------------
# 문제 선택
# -------------------

available = [
    i for i in range(len(questions))
    if i not in st.session_state.used
]

if len(available) == 0:
    st.session_state.used = []
    available = list(range(len(questions)))

if "current" not in st.session_state:
    st.session_state.current = random.choice(available)

q = questions[st.session_state.current]

# -------------------
# 디자인
# -------------------

st.markdown("""
<style>
.money-box{
position:fixed;
bottom:20px;
right:20px;
background:#2ecc71;
padding:15px;
border-radius:15px;
color:white;
font-size:22px;
font-weight:bold;
z-index:9999;
box-shadow:0px 0px 10px rgba(0,0,0,0.3);
}
</style>
""", unsafe_allow_html=True)

st.markdown(
f"""
<div class="money-box">
💰 {st.session_state.money} 원
</div>
""",
unsafe_allow_html=True
)

st.title("♻️ 에코 리워드 분리수거 챌린지")

tab1, tab2 = st.tabs(["퀴즈", "상점"])

# -------------------
# 퀴즈
# -------------------

with tab1:

    st.subheader("오늘의 분리수거 문제")

    st.write(q["question"])

    if q["type"] == "OX":

        answer = st.radio(
            "선택",
            ["O", "X"],
            key=f"ox_{st.session_state.current}"
        )

    else:

        answer = st.radio(
            "선택",
            q["options"],
            key=f"mcq_{st.session_state.current}"
        )

    if st.button("정답 제출"):

        if answer == q["answer"]:

            st.session_state.money += 300

            st.success("정답! +300원")

        else:

            st.session_state.money = max(
                0,
                st.session_state.money - 100
            )

            st.error("오답! -100원")

        st.info("해설: " + q["explanation"])

        if st.session_state.current not in st.session_state.used:
            st.session_state.used.append(
                st.session_state.current
            )

    if st.button("다음 문제"):

        remain = [
            i for i in range(len(questions))
            if i not in st.session_state.used
        ]

        if len(remain) == 0:
            st.session_state.used = []
            remain = list(range(len(questions)))

        st.session_state.current = random.choice(remain)
        st.rerun()

# -------------------
# 상점
# -------------------

shop_items = [
    ("로지텍 G PRO X SUPERLIGHT 2",1000),
    ("우팅 80HE",2000),
    ("벤큐 24인치 모니터",3000),
    ("RTX5090",4000),
    ("2023 롤스로이스 팬텀",5000),
    ("챔피언스 리그 결승전 티켓",6000),
    ("NFL하프타임쇼 티켓",7000),
    ("젠슨 황 통장 80% 있는 통장",8000),
    ("강남",9000),
    ("고추바사삭 치킨",10000)
]

with tab2:

    st.subheader("🛒 친환경 상점")

    for item, price in shop_items:

        col1, col2 = st.columns([3,1])

        with col1:
            st.write(f"**{item}**")
            st.write(f"{price}원")

        with col2:

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

                    st.error("돈이 부족합니다.")

    st.divider()

    st.subheader("🎁 내 아이템")

    if st.session_state.inventory:

        for item in st.session_state.inventory:
            st.write("✅", item)

    else:
        st.write("아직 구매한 아이템이 없습니다.")
