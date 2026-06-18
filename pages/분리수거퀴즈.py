import streamlit as st
import random

st.set_page_config(
page_title="🌎 쓰레기 부자",
page_icon="♻️",
layout="wide"
)

# -----------------------------

# CSS

# -----------------------------

st.markdown("""

<style>

.hero{
background:linear-gradient(135deg,#43a047,#66bb6a);
padding:25px;
border-radius:20px;
color:white;
text-align:center;
margin-bottom:20px;
}

.wallet{
position:fixed;
bottom:20px;
right:20px;
background:#1b5e20;
color:white;
padding:15px 20px;
border-radius:15px;
font-size:22px;
font-weight:bold;
z-index:9999;
box-shadow:0px 0px 15px rgba(0,0,0,0.3);
}

.shop-card{
padding:15px;
border-radius:15px;
border:2px solid #ddd;
margin-bottom:10px;
}

</style>

""", unsafe_allow_html=True)

# -----------------------------

# 문제 생성

# -----------------------------

def make_questions():

```
questions=[]

ox_templates = [
    ("페트병은 내용물을 비우고 버려야 한다.", "O",
     "내용물을 비운 후 배출해야 재활용됩니다."),
    ("음식물이 묻은 종이는 재활용 가능하다.", "X",
     "오염된 종이는 일반쓰레기입니다."),
    ("유리병 뚜껑은 분리해서 버린다.", "O",
     "재질이 다르므로 분리배출합니다."),
    ("건전지는 일반쓰레기다.", "X",
     "건전지 수거함에 배출해야 합니다."),
    ("종이컵은 깨끗하면 재활용 가능하다.", "O",
     "깨끗이 비운 후 배출 가능합니다.")
]

for i in range(50):
    q = ox_templates[i % len(ox_templates)]
    questions.append({
        "type":"OX",
        "question":f"{i+1}. {q[0]}",
        "answer":q[1],
        "explanation":q[2]
    })

mcq_templates = [
    {
        "question":"재활용 가능한 것은?",
        "options":["깨끗한 종이","음식물 묻은 종이","휴지","기름 묻은 종이"],
        "answer":"깨끗한 종이",
        "explanation":"깨끗한 종이만 재활용 가능합니다."
    },
    {
        "question":"건전지는 어디에 버려야 할까요?",
        "options":["건전지 수거함","일반쓰레기","플라스틱","종이류"],
        "answer":"건전지 수거함",
        "explanation":"건전지는 별도 수거해야 합니다."
    },
    {
        "question":"페트병 배출 전 해야 할 일은?",
        "options":["비우기","물 채우기","자르기","태우기"],
        "answer":"비우기",
        "explanation":"내용물을 비운 후 배출합니다."
    },
    {
        "question":"유리병은 어떻게 배출할까요?",
        "options":["내용물 제거 후","음식물과 함께","태워서","그냥 버리기"],
        "answer":"내용물 제거 후",
        "explanation":"깨끗하게 비운 후 배출합니다."
    },
    {
        "question":"종이상자는 어떻게 버릴까요?",
        "options":["펼쳐서","물에 적셔서","잘게 찢어서","태워서"],
        "answer":"펼쳐서",
        "explanation":"상자는 펼쳐서 배출합니다."
    }
]

for i in range(50):
    q = mcq_templates[i % len(mcq_templates)]

    questions.append({
        "type":"MCQ",
        "question":f"{i+51}. {q['question']}",
        "options":q["options"],
        "answer":q["answer"],
        "explanation":q["explanation"]
    })

random.shuffle(questions)
return questions
```

# -----------------------------

# Session

# -----------------------------

if "money" not in st.session_state:
st.session_state.money = 0

if "inventory" not in st.session_state:
st.session_state.inventory = []

if "questions" not in st.session_state:
st.session_state.questions = make_questions()

if "current" not in st.session_state:
st.session_state.current = None

# -----------------------------

# 레벨

# -----------------------------

money = st.session_state.money

if money < 3000:
level="🌱 새싹"
elif money < 6000:
level="♻️ 환경지킴이"
elif money < 9000:
level="🌍 재활용 마스터"
else:
level="🏆 지구 영웅"

# -----------------------------

# 지갑

# -----------------------------

st.markdown(
f"""

<div class="wallet">
💰 {money:,}원
</div>
""",
unsafe_allow_html=True
)

# -----------------------------

# 메뉴

# -----------------------------

menu = st.sidebar.radio(
"메뉴",
["홈","퀴즈","상점","인벤토리"]
)

# -----------------------------

# 홈

# -----------------------------

if menu=="홈":

```
st.markdown("""
<div class="hero">
<h1>🌎 쓰레기 부자</h1>
<h3>분리수거를 배우고 돈을 모아보세요!</h3>
</div>
""", unsafe_allow_html=True)

solved = 100 - len(st.session_state.questions)

st.metric("현재 레벨", level)
st.metric("푼 문제", f"{solved}/100")

st.progress(solved/100)
```

# -----------------------------

# 퀴즈

# -----------------------------

elif menu=="퀴즈":

```
if len(st.session_state.questions)==0:
    st.success("🎉 모든 문제를 완료했습니다!")
    st.balloons()

else:

    if st.session_state.current is None:
        st.session_state.current = st.session_state.questions.pop()

    q = st.session_state.current

    st.subheader(q["question"])

    if q["type"]=="OX":

        answer = st.radio(
            "선택",
            ["O","X"]
        )

    else:

        answer = st.radio(
            "선택",
            q["options"]
        )

    if st.button("정답 제출"):

        if answer == q["answer"]:

            st.success("💰 +300원 획득!")
            st.session_state.money += 300

        else:

            st.error("❌ -100원")
            st.session_state.money = max(
                0,
                st.session_state.money - 100
            )

        st.info(q["explanation"])

        st.session_state.current = None
        st.rerun()
```

# -----------------------------

# 상점

# -----------------------------

elif menu=="상점":

```
items = [
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

st.header("🛒 친환경 상점")

for item,price in items:

    c1,c2=st.columns([3,1])

    with c1:
        st.markdown(
            f"""
            <div class="shop-card">
            <h4>{item}</h4>
            <p>{price:,}원</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        if st.button(
            f"구매-{item}"
        ):

            if st.session_state.money >= price:

                st.session_state.money -= price
                st.session_state.inventory.append(item)
                st.success("구매 완료!")

            else:
                st.error("돈이 부족합니다.")
```

# -----------------------------

# 인벤토리

# -----------------------------

elif menu=="인벤토리":

```
st.header("🎒 내가 구매한 물건")

if len(st.session_state.inventory)==0:

    st.info("구매한 물건이 없습니다.")

else:

    for item in st.session_state.inventory:
        st.write("✅", item)
```
