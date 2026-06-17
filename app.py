if menu == "홈":

    st.markdown("""
    <div class="big-banner">
        <h1>♻️ EcoSort Guide</h1>
        <h3>무분별한 쓰레기 배출을 줄이고 지구를 지켜요!</h3>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card">
        <h3>🌍 앱의 목적</h3>
        <p>
        쓰레기 문제의 심각성을 이해하고
        올바른 분리수거 방법을 학습합니다.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
        <h3>📚 사용 방법</h3>
        <p>
        중요성 학습 → 분리수거 가이드 →
        퀴즈 → 실천 다짐
        </p>
        </div>
        """, unsafe_allow_html=True)

    st.success("👈 왼쪽 메뉴를 눌러 시작해보세요!")
