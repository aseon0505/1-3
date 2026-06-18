import streamlit as st
import random

st.set_page_config(
page_title="🌎 쓰레기 부자",
page_icon="♻️",
layout="wide"
)

# -------------------

# 스타일

# -------------------

st.markdown("""

<style>
.wallet{
    position:fixed;
    bottom:20px;
    right:20px;
    background:#1b5e20;
    color:white;
    padding:15px;
    border-radius:12px;
    font-size:22px;
    font-weight:bold;
    z-index:9999;
}
</style>

""", unsafe_allow_html=True)

# -------------------

# 문제 생성

# -------------------

def create_questions():
questions = []

```
for i in range(50):
    questions.append({
        "type": "OX",
        "question": f"{i+1}. 페트병은 내용물을 비우고 버려야 한다.",
        "answer": "O",
        "explanation": "페트병은 내용물을 비우고 배출해야 재활용됩니다."
    })

for i in range(50):
    questions.append({
        "type": "MCQ",
        "question": f"{i+51}. 재활용 가능한 것은?",
        "options": [
            "깨끗한 종이",
            "음식물 묻은 종이",
            "오염된 비닐",
            "일반쓰레기"
        ],
        "answer": "깨끗한 종이",
        "explanation": "깨끗한 종이는 재활용 가능합니다."
    })

random.shuffle(questions)
return questions
```

# -------------------

# 세션 상태

# -------------------

if "money" not in st.session_state:
st.session_state.money = 0

if "inventory" not in st.session_state:
st.session_state.inventory = []

if "questions" not in st.session_state:
st.session_state.questions = create_questions()

if "current_question" not in st.session_state:
st.session_state.current_question = None

# -------------------

# 지갑 표시

# -------------------

st.markdown(
f""" <div class="wallet">
💰 {st.session_state.money:,}원 </div>
""",
unsafe_allow_html=True
)

# -------------------

# 메뉴

# -------------------

menu = st.sidebar.radio(
"메뉴",
["홈", "퀴즈", "상점", "인벤토리"]
)

# -------------------

# 홈

# -------------------

if menu == "홈":

```
st.title("🌎 쓰레기 부자")
st.subheader("분리수거를 배우고 돈을 모아보세요!")

solved = 100 - len(st.session_state.questions)

st.metric("보유 금액", f"{st.session_state.money:,}원")
st.metric("푼 문제", f"{solved}/100")

st.progress(solved / 100)
```

# -------------------

# 퀴즈

# -------------------

elif menu == "퀴즈":

```
if len(st.session_state.questions) == 0:
    st.success("🎉 모든 문제를 완료했습니다!")
    st.stop()

if st.session_state.current_question is None:
    st.session_state.current_question = st.session_state.questions.pop()

q = st.session_state.current_question

st.subheader(q["question"])

if q["type"] == "OX":
    answer = st.radio("정답 선택", ["O", "X"])
else:
    answer = st.radio("정답 선택", q["options"])

if st.button("제출"):

    if answer == q["answer"]:
        st.session_state.money += 300
        st.success("정답! +300원")
    else:
        st.session_state.money = max(
            0,
            st.session_state.money - 100
        )
        st.error("오답! -100원")

    st.info(q["explanation"])

    st.session_state.current_question = None
```

# -------------------

# 상점

# -------------------

elif menu == "상점":

```
st.header("🛒 친환경 상점")

shop_items = [
    ("대나무 칫솔",1000),
    ("텀블러",2000),
    ("재활용 노트",3000),
    ("에코백",4000),
    ("친환경 물병",5000),
    ("태양광 랜턴",6000),
    ("업사이클 파우치",7000),
    ("친환경 스피커",8000),
    ("미니 태양광 패널",9000),
    ("환경 지킴이 세트",10000)
]

for item, price in shop_items:

    col1, col2 = st.columns([3,1])

    with col1:
        st.write(f"### {item}")
        st.write(f"{price:,}원")

    with col2:

        if st.button(
            f"구매-{item}",
            key=item
        ):

            if st.session_state.money >= price:

                st.session_state.money -= price
                st.session_state.inventory.append(item)

                st.success("구매 완료!")

            else:
                st.error("돈이 부족합니다.")
```

# -------------------

# 인벤토리

# -------------------

elif menu == "인벤토리":

```
st.header("🎒 구매한 물건")

if len(st.session_state.inventory) == 0:
    st.info("구매한 물건이 없습니다.")
else:
    for item in st.session_state.inventory:
        st.write("✅", item)
```
