import streamlit as st

st.set_page_config(
    page_title="Eco Money Quiz",
    page_icon="♻️",
    layout="wide"
)

# -----------------------
# 스타일
# -----------------------
st.markdown("""
<style>
.money-box{
    position:fixed;
    right:20px;
    bottom:20px;
    background:#1e8e3e;
    color:white;
    padding:15px;
    border-radius:15px;
    font-size:22px;
    font-weight:bold;
    z-index:9999;
    box-shadow:0 0 10px rgba(0,0,0,0.3);
}
.quiz-card{
    padding:20px;
    border-radius:15px;
    border:1px solid #ddd;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# 문제 데이터
# -----------------------
questions = [
    {
        "type":"OX",
        "question":"페트병은 라벨을 제거하고 배출해야 한다.",
        "answer":"O",
        "explanation":"페트병은 라벨과 뚜껑을 제거해야 재활용 효율이 높아집니다."
    },
    {
        "type":"OX",
        "question":"음식물이 묻은 종이는 종이류로 재활용할 수 있다.",
        "answer":"X",
        "explanation":"오염된 종이는 재활용이 어렵기 때문에 일반쓰레기로 배출합니다."
    },
    {
        "type":"MCQ",
        "question":"깨끗이 씻은 우유팩은 어디에 버려야 할까요?",
        "options":["일반쓰레기","종이팩 수거함","플라스틱","캔류"],
        "answer":"종이팩 수거함",
        "explanation":"우유팩은 일반 종이와 달라 별도 수거함에 배출합니다."
    },
    {
        "type":"MCQ",
        "question":"투명 페트병은 어떻게 배출해야 할까요?",
        "options":["내용물 제거 후 별도 배출",
                   "일반 플라스틱과 섞기",
                   "종량제 봉투",
                   "캔 수거함"],
        "answer":"내용물 제거 후 별도 배출",
        "explanation":"투명 페트병은 깨끗하게 비우고 별도 배출하는 것이 원칙입니다."
    },
    {
        "type":"OX",
        "question":"배터리는 전용 수거함에 버려야 한다.",
        "answer":"O",
        "explanation":"배터리는 유해물질이 있어 전용 수거함을 이용해야 합니다."
    },
    {
        "type":"MCQ",
        "question":"깨진 유리는 어디에 버려야 할까요?",
        "options":["유리병 수거함","일반쓰레기","플라스틱","캔류"],
        "answer":"일반쓰레기",
        "explanation":"깨진 유리는 재활용되지 않으며 안전하게 포장 후 일반쓰레기로 배출합니다."
    }
]

# -----------------------
# 세션 상태
# -----------------------
if "current" not in st.session_state:
    st.session_state.current = 0

if "money" not in st.session_state:
    st.session_state.money = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "answered" not in st.session_state:
    st.session_state.answered = False

# -----------------------
# 오른쪽 하단 통장
# -----------------------
st.markdown(
    f"""
    <div class="money-box">
    💰 환경 통장<br>
    {st.session_state.money:,}원
    </div>
    """,
    unsafe_allow_html=True
)

st.title("♻️ Eco Money Quiz")
st.subheader("분리수거를 배우고 환경 포인트를 모아보세요!")

progress = st.session_state.current / len(questions)
st.progress(progress)

# -----------------------
# 퀴즈 종료
# -----------------------
if st.session_state.current >= len(questions):

    st.success("🎉 모든 문제를 완료했습니다!")

    if st.session_state.score >= 5:
        grade = "🌳 환경 지킴이"
    elif st.session_state.score >= 3:
        grade = "🌱 환경 새싹"
    else:
        grade = "🌎 환경 입문자"

    st.metric("정답 수", f"{st.session_state.score}/{len(questions)}")
    st.metric("획득 금액", f"{st.session_state.money:,}원")

    st.markdown(f"## {grade}")

    if st.button("다시 시작"):
        st.session_state.current = 0
        st.session_state.money = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.rerun()

else:

    q = questions[st.session_state.current]

    st.markdown("### 문제")

    with st.container():

        st.markdown(f"#### {q['question']}")

        if q["type"] == "OX":

            answer = st.radio(
                "선택하세요",
                ["O", "X"],
                key=f"radio_{st.session_state.current}"
            )

        else:

            answer = st.radio(
                "선택하세요",
                q["options"],
                key=f"radio_{st.session_state.current}"
            )

        if not st.session_state.answered:

            if st.button("정답 확인"):

                st.session_state.answered = True

                if answer == q["answer"]:

                    st.session_state.money += 100
                    st.session_state.score += 1

                    st.success("✅ 정답입니다!")
                    st.balloons()

                else:

                    st.error("❌ 틀렸습니다.")
                    st.info(q["explanation"])

                st.rerun()

        else:

            correct = answer == q["answer"]

            if correct:
                st.success("✅ 정답입니다!")
            else:
                st.error("❌ 틀렸습니다.")
                st.info(q["explanation"])

            if st.button("다음 문제"):

                st.session_state.current += 1
                st.session_state.answered = False
                st.rerun()

# -----------------------
# 사이드바
# -----------------------
with st.sidebar:

    st.header("📊 학습 현황")

    st.metric(
        "획득 금액",
        f"{st.session_state.money:,}원"
    )

    st.metric(
        "정답 수",
        st.session_state.score
    )

    st.write("""
    ### ♻️ 분리수거 팁

    - 페트병 라벨 제거
    - 내용물 비우기
    - 캔은 헹군 후 배출
    - 배터리는 전용 수거함
    - 우유팩은 별도 수거
    """)
