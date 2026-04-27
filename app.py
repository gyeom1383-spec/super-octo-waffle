import streamlit as st
import requests

st.set_page_config(page_title="국어 서술형 답안 연습", page_icon="✏️")

st.title("✏️ 국어 서술형 답안 연습")
st.caption("답안을 작성한 뒤 제출하면 AI 피드백을 받을 수 있어요.")

st.divider()

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
황순원의 단편소설 소나기의 한 장면입니다.
조약돌은 소녀가 소년에게 보내는 관심과 호감, 즉 소녀의 마음을 상징합니다.

[학생 답변]
{answer}

[피드백 지침]
- 100자 이내로 간결하게
- 잘된 점 + 보완할 점
- 핵심 개념 한 줄 정리로 마무리
- 친절한 존댓말 사용"""

        api_key = st.secrets["GEMINI_API_KEY"]
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        res = requests.post(url, json=payload)
        data = res.json()

        if "candidates" in data:
            feedback = data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            feedback = f"오류 내용: {data}"

    st.success("✅ 피드백")
    st.markdown(feedback)
