import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="EcoSort Guide",
    page_icon="♻️",
    layout="wide"
)

# 분리수거 데이터
recycle_info = {
    "플라스틱": """
    - 내용물을 비우고 헹군 후 배출
    - 라벨은 제거 후 배출
    - 이물질이 많으면 일반쓰레기
    """,
    "종이": """
    - 물기에 젖지 않게 배출
    - 테이프, 스프링 제거
    - 영수증은 일반쓰레기
    """,
    "캔": """
    - 내용물을 비우고 헹군 후 배출
    - 압축 가능하면 눌러서 배출
    """,
    "유리병": """
    - 내용물을 제거 후 배출
    - 깨진 유리는 일반쓰레기
    """,
    "음식물 쓰레기": """
    - 동물이 먹을 수 있는 것 위주
    - 조개껍데기, 뼈는 일반쓰레기
    """
}

quiz_questions = [
    {
        "question": "플라스틱 용기는 내용물을 비우고 배출해야 한다.",
        "answer": "O"
    },
    {
        "question": "깨진 유리병은 재활용함에 넣는다.",
        "answer": "X"
    },
    {
        "question": "종이는 젖지 않게 배출하는 것이 좋다.",
        "answer": "O"
    }
]

# 제목
st.title("♻️ EcoSort Guide")
st.subheader("무분별한 쓰레기 배출 문제와 올바른 분리수거 안내")

# 사이드바
menu = st.sidebar.radio(
    "메뉴 선택",
    [
        "홈",
        "왜 분리수거가 중요할까?",
        "분리수거 가이드",
        "분리수거 퀴즈",
        "실천 다짐"
    ]
)

# 홈
if menu == "홈":
    st.header("🏠 앱 소개")

    st.write("""
    이 앱은 무분별한 쓰레기 배출로 인한 환경 문제를 알리고,
    올바른 분리수거 방법을 쉽게 배울 수 있도록 제작되었습니다.
    """)

    st.info("""
    사용 방법
    1. 분리수거의 중요성을 알아봅니다.
    2. 분리수거 가이드에서 배출 방법을 확인합니다.
    3. 퀴즈를 통해 지식을 점검합니다.
    4. 실천 다짐을 작성해 봅니다.
    """)

    st.success("왼쪽 메뉴를 선택하여 원하는 기능으로 이동하세요.")

# 중요성
elif menu == "왜 분리수거가 중요할까?":
    st.header("🌍 왜 분리수거가 중요할까?")

    st.write("""
    무분별한 쓰레기 배출은 토양 오염, 수질 오염,
    해양 생태계 파괴 등의 문제를 일으킵니다.
    """)

    st.write("""
    올바른 분리수거는 재활용률을 높이고
    자원 낭비를 줄이는 데 큰 도움이 됩니다.
    """)

    st.metric("플라스틱 분해 예상 기간", "약 500년")
    st.metric("유리병 분해 예상 기간", "1,000년 이상")

    st.warning("작은 실천이 환경을 지키는 큰 힘이 됩니다.")

# 가이드
elif menu == "분리수거 가이드":
    st.header("📦 분리수거 가이드")

    item = st.selectbox(
        "배출 방법이 궁금한 품목을 선택하세요.",
        list(recycle_info.keys())
    )

    st.success(recycle_info[item])

# 퀴즈
elif menu == "분리수거 퀴즈":
    st.header("🧠 분리수거 퀴즈")

    score = 0

    for idx, q in enumerate(quiz_questions):
        answer = st.radio(
            q["question"],
            ["O", "X"],
            key=f"quiz_{idx}"
        )

        if answer == q["answer"]:
            score += 1

    if st.button("결과 확인"):
        st.success(f"점수: {score} / {len(quiz_questions)}")

        if score == len(quiz_questions):
            st.balloons()
            st.success("훌륭합니다! 분리수거를 잘 알고 있네요.")
        elif score >= 2:
            st.info("좋아요! 조금만 더 공부해 보세요.")
        else:
            st.warning("가이드를 다시 읽어보면 도움이 될 거예요.")

# 실천 다짐
elif menu == "실천 다짐":
    st.header("✍️ 환경 보호 실천 다짐")

    promise = st.text_area(
        "내가 실천할 환경 보호 행동을 적어보세요."
    )

    if st.button("저장하기"):
        if promise.strip():
            st.success("좋은 다짐입니다!")
            st.write(f"🌱 나의 다짐: {promise}")
        else:
            st.error("내용을 입력해주세요.")
