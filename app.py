import time

MAX_RETRIES = 3

response_text = None

for attempt in range(MAX_RETRIES):

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.8,
                max_output_tokens=500,
            )
        )

        response_text = response.text
        break

    except Exception as e:

        error_str = str(e)

        # 503 오류면 잠시 기다렸다 재시도
        if "503" in error_str or "UNAVAILABLE" in error_str:

            if attempt < MAX_RETRIES - 1:
                wait_time = 2 * (attempt + 1)

                st.warning(
                    f"서버가 혼잡해요 😢 {wait_time}초 후 다시 시도합니다..."
                )

                time.sleep(wait_time)

            else:
                response_text = """
지금 AI 서버 사용량이 많아서 답변이 지연되고 있어요 😢

잠시 후 다시 시도해주세요.
"""

        else:
            response_text = f"""
⚠️ 오류가 발생했어요.

오류 내용:
{error_str}
"""
            break

# 최종 출력
st.markdown(response_text)

# 기록 저장
st.session_state.messages.append({
    "role": "assistant",
    "content": response_text
})
