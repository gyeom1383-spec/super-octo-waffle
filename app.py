import streamlit as st
from google import genai

st.set_page_config(page_title="국어 서술형 답안 연습", page_icon="✏️")

# Gemini API 설정
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.title("✏️ 국어 서술형 답안 연습")
st.caption("답안을 작성한 뒤 제출하면 AI 피드백을 받을 수 있어요.")

st.divider()

# 문항
st.markdown("#### 문제")
st.markdown(
    """다음 장면에서 밑줄 친 소재가 의미하는 바를 작성하시오.

---

> 그러다가 소녀가 물속에서 무엇을 하나 집어낸다. 하얀 조약돌이었다. 그러고는 벌떡 일어나 팔짝팔짝 징검다리를 뛰어 건너간다.  
> 다 건너가더니 홱 이리로 돌아서며,  
> "이 바보."  
> **조약돌**이 날아왔다.  
> 소년은 저도 모르게 벌떡 일어났다.
"""
)

st.info("💡 힌트: 교과서 27~28페이지를 확인하세요.")

st.divider()

# 답안 입력
answer = st.text_area(
    "📝 내 답안",
    placeholder="이 장면에서 조약돌은 ~ 을/를 의미한다.",
    height=120,
)

if st.button("제출하기", type="primary", disabled=not answer.strip()):
    with st.spinner("AI가 피드백을 작성 중입니다..."):

        prompt = f"""당신은 중학교 1학년 국어 교사입니다. 학생이 소설 속 소재의 상징적 의미를 묻는 서술형 문제에 답했습니다.

[문제]
다음 장면에서 밑줄 친 '조약돌'이 의미하는 바를 작성하시오.

[작품 맥락]
황순원의 단편소설 「소나기」의 한 장면입니다. 소녀가 소년에게 조약돌을 던지는 행동이 묘사되어 있습니다.
조약돌은 소녀가 소년에게 보내는 관심과 호감의 표현, 즉 소녀의 마음(애정, 장난기 어린 관심)을 상징합니다.

[학생 답변]
"{answer}"

[피드백 지침]
- 100자 이내로 간결하게 작성
- 잘된 점 한 가지 + 보완할 점(있다면) 한 가지
- 핵심 개념(소재의 상징적 의미)을 한 줄로 정리하며 마무리
- 친절한 존댓말 사용
- 정답/오답을 직접 언급하지 말고 방향을 안내하는 방식으로"""

        response = client.models.generate_content(
            model="gemini-1.5-flash-latest",
            contents=prompt
        )
        feedback = response.text

    st.success("✅ 피드백")
    st.markdown(feedback)
