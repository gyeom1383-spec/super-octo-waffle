import streamlit as st
import requests
import time

# 페이지 설정 (아이콘과 제목에 한글 사용)
st.set_page_config(page_title="소나기 속 숨은 의미 찾기", page_icon="🌧️", layout="centered")

# 문제 데이터 (기존 내용 유지)
QUESTIONS = [
    {
        "id": 1,
        "label": "개인 문항 1번",
        "tag": "소재의 상징",
        "context": """[관련 장면]
그러다가 소녀가 물속에서 무엇을 하나 집어낸다. 하얀 조약돌이었다. 그러고는 벌떡 일어나 팔짝팔짝 징검다리를 뛰어 건너간다.
다 건너가더니 홱 이리로 돌아서며,
"이 바보."
조약돌이 날아왔다.
소년은 저도 모르게 벌떡 일어섰다.
단발머리를 나풀거리며 소녀가 막 달린다. 갈밭 사잇길로 들어섰다. 뒤에는 청량한 가을 햇살 아래 빛나는 갈꽃뿐.
소년은 이 갈꽃이 아주 뵈지 않게 되기까지 그대로 서 있었다. 문득 소녀가 던진 조약돌을 내려다보았다. 물기가 걷혀 있었다. 소년은 조약돌을 집어 주머니에 넣었다.""",
        "excerpt": """그러다가 소녀가 물속에서 무엇을 하나 집어낸다. 하얀 조약돌이었다. 그러고는 벌떡 일어나 팔짝팔짝 징검다리를 뛰어 건너간다.<br>
다 건너가더니 홱 이리로 돌아서며,<br>
"이 바보."<br>
<u>조약돌</u>이 날아왔다.<br>
소년은 저도 모르게 벌떡 일어났다.""",
        "question": "다음 장면에서 밑줄 친 소재가 의미하는 바를 작성해 봅시다.",
        "hint": "교과서 27~28페이지를 확인하세요.",
        "placeholder": "조약돌은 [누가] [누구에게] 느끼는 [감정/마음]을 상징한다.",
        "answer_frame": "조약돌은 [누가] [누구에게] 느끼는 [감정/마음]을 상징한다.",
        "key_answer": "조약돌은 소녀가 소년에게 보내는 관심, 호감, 애정을 상징함. 소년이 조약돌을 주머니에 넣고 소중히 간직하는 장면과 연결됨.",
    },
    # ... (중략: QUESTIONS 2~6번 데이터는 기존과 동일하게 유지하시면 됩니다)
]

# (코드 간결화를 위해 QUESTIONS 리스트의 나머지는 생략했으나, 실제 코드에서는 그대로 유지하세요)

if "page" not in st.session_state:
    st.session_state.page = "main"
if "current_q" not in st.session_state:
    st.session_state.current_q = None
if "completed" not in st.session_state:
    st.session_state.completed = set()
if "feedbacks" not in st.session_state:
    st.session_state.feedbacks = {}

def show_main():
    st.title("🌧️ 소나기 속 숨은 의미 찾기")
    st.caption("소나기 속 장면들을 다시 읽고, 숨겨진 의미를 찾아보세요. 내 생각을 쓰면 인공지능 선생님이 함께 고민해드려요! 🌧️")
    st.divider()

    completed_count = len(st.session_state.completed)
    st.markdown(f"**진행 현황: {completed_count} / {len(QUESTIONS)} 문항 완료**")
    st.progress(completed_count / len(QUESTIONS))
    st.divider()

    st.markdown("**📝 개인 문항**")
    for q in QUESTIONS[:2]:
        is_done = q["id"] in st.session_state.completed
        label = f"{'✅ ' if is_done else ''}{q['label']} | {q['tag']}"
        if st.button(label, key=f"q_{q['id']}", use_container_width=True):
            st.session_state.current_q = q["id"]
            st.session_state.page = "question"
            st.rerun()

    st.divider()
    st.markdown("**👥 모둠 문항**")
    for q in QUESTIONS[2:]:
        is_done = q["id"] in st.session_state.completed
        label = f"{'✅ ' if is_done else ''}{q['label']} | {q['tag']}"
        if st.button(label, key=f"q_{q['id']}", use_container_width=True):
            st.session_state.current_q = q["id"]
            st.session_state.page = "question"
            st.rerun()

def show_question(q):
    if st.button("← 목록으로 돌아가기"):
        st.session_state.page = "main"
        st.rerun()

    st.divider()
    st.markdown(f"### {q['label']} | {q['tag']}")
    st.markdown(f"**{q['question']}**")
    st.divider()

    st.markdown(q["excerpt"], unsafe_allow_html=True)

    hints = q['hint'].split('\n')
    for h in hints:
        if h.strip():
            st.info(h.strip(), icon="💡")

    st.divider()

    st.markdown("**✏️ 답안 작성틀**")
    st.markdown(
        f"""
        <div style="font-size: 1rem; padding: 1rem; border-radius: 0.5rem; background-color: rgba(151, 166, 195, 0.15);">
            {q['answer_frame']}
        </div>
        <br>
        """,
        unsafe_allow_html=True
    )

    prev_feedback = st.session_state.feedbacks.get(q["id"], None)

    answer = st.text_area(
        "📝 내 답안",
        placeholder=q["placeholder"],
        height=120,
        key=f"answer_{q['id']}"
    )

    if prev_feedback:
        st.success("✅ 이전 피드백")
        st.markdown(prev_feedback)
        st.divider()

    if st.button("제출하기", type="primary", disabled=not answer.strip()):
        with st.spinner("선생님이 꼼꼼하게 읽어보고 있어요..."):

            api_key = st.secrets["GROQ_API_KEY"]
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            # 외국어 배제를 위한 극단적인 프롬프트 수정
            prompt = f"""당신은 국어 선생님입니다. 아래 지시사항을 반드시 지켜서 학생의 답안에 피드백을 주세요.

[중요 규칙: 언어 사용 제한]
1. 오직 '한국어(한글)'만 사용하세요. 
2. 영어 알파벳(A, B, C...), 한자(漢字), 일본어 등 모든 외국어 문자를 절대 쓰지 마세요.
3. '피드백', '미션' 같은 외래어는 허용하지만, 영어 철자나 한자를 직접 적는 것은 절대 금지합니다.
4. 문학 용어(복선, 암시 등) 대신 쉬운 우리말 풀이를 사용하세요.

[문제 정보]
- 관련 장면: {q['context']}
- 문제: {q['question']}
- 채점 기준: {q['key_answer']}

[학생 답변]
{answer}

[피드백 작성 양식]
1. [선생님의 다정한 피드백] 
   - 학생이 쓴 표현을 직접 언급하며 칭찬하기.
   - 부족한 부분은 지문의 구체적인 문장을 인용하여 고쳐 쓸 방법 알려주기.
2. [한 걸음 더 나아가기 위한 나의 미션]
   - 잘한 점, 다음 행동, 다시 읽을 지문을 아주 쉽게 적기.

모든 답변은 반드시 한글로만 작성해야 합니다."""

            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": "당신은 한국어만 사용하는 교사입니다. 어떠한 경우에도 영어 철자나 한자를 사용하지 마세요. 오직 한글 자모로만 이루어진 글자만 사용하세요."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1000,
                "temperature": 0.3 # 일관성을 위해 온도를 낮춤
            }

            max_retries = 3
            feedback = None

            for attempt in range(max_retries):
                res = requests.post(url, headers=headers, json=payload)
                
                if res.status_code == 200:
                    data = res.json()
                    if "choices" in data:
                        feedback = data["choices"][0]["message"]["content"]
                        break
                elif res.status_code in [503, 429]:
                    if attempt < max_retries - 1:
                        time.sleep(3)
                        continue
                else:
                    st.error("오류가 발생했습니다. 잠시 후 다시 시도해주세요.")
                    break

            if feedback:
                st.session_state.feedbacks[q["id"]] = feedback
                st.session_state.completed.add(q["id"])
                st.success("✅ 선생님의 피드백이 도착했습니다!")
                st.markdown(feedback)

# 페이지 라우팅
if st.session_state.page == "main":
    show_main()
elif st.session_state.page == "question":
    q = next((q for q in QUESTIONS if q["id"] == st.session_state.current_q), None)
    if q:
        show_question(q)
