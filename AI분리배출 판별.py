
import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# 1. 페이지 기본 설정 및 테마
st.set_page_config(
    page_title="에코스캔 (EcoScan) - AI 분리배출 가이드",
    page_icon="♻️",
    layout="centered"
)

# 스타일 개선 (CSS)
st.markdown("""
    <style>
    .main-title { font-size: 2.2rem; font-weight: bold; color: #2E7D32; text-align: center; margin-bottom: 5px; }
    .sub-title { font-size: 1.1rem; color: #555; text-align: center; margin-bottom: 25px; }
    .result-box { background-color: #F1F8E9; padding: 20px; border-radius: 10px; border-left: 5px solid #4CAF50; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">♻️ 에코스캔 (EcoScan)</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">사진을 찍거나 업로드하면 AI가 올바른 분리배출 방법을 알려드려요!</div>', unsafe_allow_html=True)

# 2. API 키 설정 및 클라이언트 초기화
# Streamlit Secrets 또는 로컬 환경 변수에서 키를 가져옵니다.
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("🔑 GEMINI_API_KEY가 설정되지 않았습니다. Streamlit Cloud의 Secrets 설정을 확인해주세요.")
    st.stop()

# Gemini 설정
genai.configure(api_key=api_key)

# 3. 세션 상태 초기화 (최근 분석 기록용)
if "history" not in st.session_state:
    st.session_state.history = []

# 4. 화면 레이아웃 구성
uploaded_file = st.file_uploader("쓰레기나 물품 사진을 업로드하세요 (JPG, PNG, JPEG)", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    try:
        # 이미지 열기
        image = Image.open(uploaded_file)
        
        # 이미지 화면 표시
        st.image(image, caption="📸 업로드된 이미지", use_container_width=True)
        
        # 분석 버튼
        if st.button("✨ 분리배출 방법 알아보기", type="primary", use_container_width=True):
            with st.spinner("AI가 이미지를 분석하여 분리배출 가이드를 작성 중입니다..."):
                try:
                    # gemini-2.5-flash-lite 모델 호출
                    model = genai.GenerativeModel('gemini-2.5-flash-lite')
                    
                    # 프롬프트 엔지니어링
                    prompt = """
                    당신은 대한민국 환경부 가이드라인을 완벽하게 숙지한 '분리배출 및 환경 전문가'입니다.
                    제공된 이미지 속 물체를 분석하여 다음 양식에 맞추어 친절하고 명확하게 답변해 주세요.
                    
                    [출력 양식]
                    ### 🔍 판별 결과: [물품 이름]
                    
                    * **분리수거 카테고리:** [예: 플라스틱, 캔류, 일반쓰레기, 대형폐기물 등]
                    * **배출 방법 안내:**
                      1. [비운다, 헹군다 등 구체적인 단계별 행동 요령 안내]
                      2. [부속품 분리 여부 등 포함]
                    * **💡 환경을 위한 꿀팁:** [해당 품목을 버릴 때 주의할 점이나 재활용률을 높이는 유용한 팁 1가지]
                    """
                    
                    response = model.generate_content([prompt, image])
                    result_text = response.text
                    
                    # 결과 출력
                    st.success("분석이 완료되었습니다!")
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.markdown(result_text)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # 기록에 추가 (최근 5개만 유지)
                    st.session_state.history.insert(0, result_text.split("\n")[0].replace("### 🔍 판별 결과: ", ""))
                    if len(st.session_state.history) > 5:
                        st.session_state.history.pop()
                        
                except Exception as e:
                    st.error(f"❌ AI 분석 중 오류가 발생했습니다: {e}")
                    st.info("API 호출 제한이나 일시적인 네트워크 오류일 수 있습니다. 잠시 후 다시 시도해주세요.")

    except Exception as img_err:
        st.error(f"이미지를 처리하는 동안 오류가 발생했습니다: {img_err}")

# 5. 사이드바 - 최근 분석 기록 및 안내
with st.sidebar:
    st.header("🍀 에코스캔 안내")
    st.write("혼란스러운 분리수거, 이제 사진 한 장으로 해결하세요! 플라스틱 테이프 제거, 음료수 병 헹구기 등 사소한 실천이 지구를 살립니다.")
    st.write("---")
    st.subheader("🕒 최근 확인한 품목")
    if st.session_state.history:
        for item in st.session_state.history:
            st.write(f"- {item}")
    else:
        st.write("아직 분석한 항목이 없습니다.")
