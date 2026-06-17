import streamlit as st
import google.generativeai as genai
import random

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="Re-Mind: 올바른 분리수거 도와주기",
    page_icon="♻️",
    layout="centered"
)

# 2. Gemini API 세팅 및 예외 처리
try:
    # Streamlit Cloud의 Secrets에서 API 키를 가져옵니다.
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # 가볍고 빠른 gemini-2.5-flash-lite 모델 지정
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
except Exception as e:
    st.error("⚠️ API 키 설정을 확인해주세요. Streamlit Cloud Secrets에 'GEMINI_API_KEY'가 필요합니다.")
    st.stop()

# 3. 앱 타이틀 및 소개
st.title("♻️ Re-Mind : 올바른 분리배출 가이드")
st.caption("헤매고 헷갈리는 분리수거, AI에게 물어보고 올바르게 실천해요!")

# --- 차별화 기능 1: 오늘의 환경 챌린지 ---
st.markdown("---")
challenges = [
    "🥤 페트병 비닐 라벨 완전히 뜯어서 버리기",
    "📦 택배 상자의 송장 스티커와 테이프 완벽히 제거하기",
    "☕ 배달 플라스틱 용기 깨끗이 씻어서 말린 후 배출하기",
    "🥛 우유팩 물에 씻어서 펼친 뒤 말려두기",
    "🔋 다 쓴 건전지 모아서 아파트/주민센터 수거함에 넣기"
]
st.info(f"💡 **오늘의 Mini 챌린지:** {random.choice(challenges)}")
st.markdown("---")

# 4. 메인 기능: AI 분리배출 검색기
st.subheader("🔍 무엇이든 물어보세요!")
search_query = st.text_input(
    "분리수거 방법이 궁금한 품목을 입력해주세요.",
    placeholder="예: 배달 떡볶이 용기, 깨진 접시, 컵라면 용기, 영수증 등"
)

if search_query:
    with st.spinner("🔄 올바른 분리배출 방법을 분석 중입니다..."):
        # AI에게 엄격한 형식을 요구하는 프롬프트 작성
        prompt = f"""
        사용자가 입력한 품목: '{search_query}'
        
        이 품목에 대한 올바른 분리배출 방법을 한국어로 친절하게 알려줘.
        반드시 다음 양식을 지켜서 답변해줘:
        
        ### 📌 분리배출 요약 테이블
        | 항목 | 내용 |
        | --- | --- |
        | **분류 카테고리** | (예: 플라스틱, 일반쓰레기, 대형폐기물 등) |
        | **라벨/이물질 제거 여부** | (예: 필수 제거, 해당 없음 등) |
        | **세척 필요 여부** | (예: 깨끗이 세척 필요, 세척 불가능 등) |
        
        ### ⚠️ 핵심 주의사항 및 팁
        - (내용 기술)
        - (내용 기술)
        """
        
        try:
            response = model.generate_content(prompt)
            st.success("✅ 분석 완료!")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"❌ AI 분석 중 오류가 발생했습니다: {e}")

# --- 차별화 기능 2: 자주 찾는 품목 퀵 가이드 ---
st.markdown("---")
st.subheader("📋 자주 찾는 품목 퀵 가이드")
st.write("검색하기 번거롭다면? 많은 분들이 헷갈려하는 대표 품목들을 모았어요.")

tab1, tab2, tab3, tab4 = st.tabs(["🥤 페트병", "📦 택배 박스", "🍜 컵라면 용기", "🥛 우유팩"])

with tab1:
    st.markdown("""
    **비닐 라벨은 떼고, 압착해서 플라스틱으로!**
    - **내용물:** 깨끗이 비우기
    - **라벨:** 비닐류로 따로 분리배출
    - **뚜껑:** 닫아서 배출해도 되나, 가급적 부피를 줄여 압착하기
    """)

with tab2:
    st.markdown("""
    **테이프와 송장은 무조건 쓰레기통으로!**
    - **종이 상자:** 송장 스티커, 박스 테이프를 완전히 제거한 뒤 접어서 종이로 배출
    - **아이스팩:** 젤 형태는 **일반쓰레기(종량제)**, 물 형태는 가위로 잘라 물을 버린 후 비닐로 배출
    """)

with tab3:
    st.markdown("""
    **오염이 심하면 일반쓰레기입니다!**
    - **하얀색 스티로폼 용기:** 국물 자국이 안 지워지면 **일반쓰레기**
    - **깨끗이 씻긴 용기:** 스티로폼(재활용)으로 배출
    """)

with tab4:
    st.markdown("""
    **일반 종이류와 섞이지 않게 따로!**
    - **방법:** 내용물을 비우고 물로 헹군 뒤, 펼쳐서 말리기
    - **배출:** 종이팩 전용 수거함에 배출 (없다면 종이류와 구분하여 묶어서 배출)
    """)

# 푸터 설정
st.markdown("---")
st.caption("Re-Mind App | Gemini 2.5 Flash-Lite 기반 스마트 분리수거 도우미")1
