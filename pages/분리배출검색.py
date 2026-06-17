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
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
except Exception as e:
    st.error("⚠️ API 키 설정을 확인해주세요. Streamlit Cloud Secrets에 'GEMINI_API_KEY'가 필요합니다.")
    st.stop()

# 3. 앱 타이틀 및 소개
st.title("♻️ Re-Mind : 올바른 분리배출 가이드")
st.caption("헤매고 헷갈리는 분리수거, AI에게 물어보고 올바르게 실천해요!")

# 4. 오늘의 환경 챌린지
st.markdown("---")
challenges = [
    "🥤 페트병 비닐 라벨 완전히 뜯어서 버리기",
    "📦 택배 상자의 송장 스티커와 테이프 완벽히 제거하기",
    "☕ 배달 플라스틱 용기 깨끗이 씻어서 말린 후 배출하기",
    "🥛 우유팩 물에 씻어서 펼친 뒤 말려두기",
    "🔋 다 쓴 건전지 모아서 아파트/주민센터 수거함에 넣기"
]
# 앱이 리로드될 때 매번 바뀌지 않도록 세션 상태 활용
if "today_challenge" not in st.session_state:
    st.session_state.today_challenge = random.choice(challenges)

st.info(f"💡 **오늘의 Mini 챌린지:** {st.session_state.today_challenge}")
st.markdown("---")

# 5. 메인 기능: AI 분리배출 검색기
st.subheader("🔍 무엇이든 물어보세요!")
search_query = st.text_input(
    "분리수거 방법이 궁금한 품목을 입력해주세요.",
    placeholder="예: 배달 떡볶이 용기, 깨진 접시, 컵라면 용기, 영수증 등"
)

if search_query:
    with st.spinner("🔄 올바른 분리배출 방법을 분석 중입니다..."):
        # 줄바꿈 문법 에러를 방지하기 위해 프롬프트를 직관적으로 구성
        prompt = (
            f"사용자가 입력한 품목: '{search_query}'\n\n"
            "이 품목에 대한 올바른 분리배출 방법을 한국어로 친절하게 알려주세요.\n"
            "출력할 때는 반드시 아래의 마크다운 표 양식을 채워서 먼저 보여주고, 그 아래에 주의사항을 작성하세요.\n\n"
            "### 📌 분리배출 요약 테이블\n"
            "| 항목 | 내용 |\n"
            "| --- | --- |\n"
            "| **분류 카테고리** | 플라스틱, 일반쓰레기, 대형폐기물 등 |\n"
            "| **라벨/이물질 제거 여부** | 필수 제거, 해당 없음 등 |\n"
            "| **세척 필요 여부** | 깨끗이 세척 필요, 세척 불가능 등 |\n\n"
            "### ⚠️ 핵심 주의사항 및 팁\n"
            "- 주의사항 내용을 여기에 작성하세요."
        )
        
        try:
            response = model.generate_content(prompt)
            st.success("✅ 분석 완료!")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"❌ AI 분석 중 오류가 발생했습니다: {e}")

# 6. 자주 찾는 품목 퀵 가이드
st.markdown("---")
st.subheader("📋 자주 찾는 품목 퀵 가이드")
st.write("검색하기 번거롭다면? 많은 분들이 헷갈려하는 대표 품목들을 모았어요.")

tab1, tab2, tab3, tab4 = st.tabs(["🥤 페트병", "📦 택배 박스", "🍜 컵라면 용기", "🥛 우유팩"])

with tab1:
    st.markdown("**비닐 라벨은 떼고, 압착해서 플라스틱으로!**")
    st.markdown("- **내용물:** 깨끗이 비우기\n- **라벨:** 비닐류로 따로 분리배출\n- **뚜껑:** 닫아서 배출해도 되나, 가급적 부피를 줄여 압착하기")

with tab2:
    st.markdown("**테이프와 송장은 무조건 쓰레기통으로!**")
    st.markdown("- **종이 상자:** 송장 스티커, 박스 테이프를 완전히 제거한 뒤 접어서 종이로 배출\n- **아이스팩:** 젤 형태는 **일반쓰레기**, 물 형태는 물을 버린 후 비닐로 배출")

with tab3:
    st.markdown("**오염이 심하면 일반쓰레기입니다!**")
    st.markdown("- **하얀색 스티로폼 용기:** 국물 자국이 안 지워지면 **일반쓰레기**\n- **깨끗이 씻긴 용기:** 스티로폼(재활용)으로 배출")

with tab4:
    st.markdown("**일반 종이류와 섞이지 않게 따로!**")
    st.markdown("- **방법:** 내용물을 비우고 물로 헹군 뒤, 펼쳐서 말리기\n- **배출:** 종이팩 전용 수거함에 배출 (없다면 종이류와 구분하여 묶어서 배출)")

st.markdown("---")
st.caption("Re-Mind App | Gemini 2.5 Flash-Lite 기반 스마트 분리수거 도우미")
