import streamlit as st
import requests

st.set_page_config(page_title="소나기 속 숨은 의미 찾기", page_icon="🌧️", layout="centered")

SONAGI = """
소년은 개울가에서 소녀를 보자 곧 윤 초시네 증손녀딸이라는 걸 알 수 있었다. 소녀는 개울에다 손을 잠그고 물장난을 하고 있는 것이다. 서울서는 이런 개울물을 보지 못하기나 한 듯이.
벌써 며칠째 소녀는 학교서 돌아오는 길에 물장난이었다. 그런데 어제까지는 개울 기슭에서 하더니 오늘은 징검다리 한가운데 앉아서 하고 있다.
소년은 개울둑에 앉아 버렸다. 소녀가 비키기를 기다리자는 것이다.
요행 지나가는 사람이 있어 소녀가 길을 비켜 주었다.

다음 날은 좀 늦게 개울가로 나왔다.
이날은 소녀가 징검다리 한가운데 앉아 세수를 하고 있었다. 분홍 스웨터 소매를 걷어 올린 팔과 목덜미가 마냥 희었다.
한참 세수를 하고 나더니 이번에는 물속을 빤히 들여다본다. 얼굴이라도 비추어 보는 것이리라. 갑자기 물을 움켜 낸다. 고기 새끼라도 지나가는 듯.
소녀는 소년이 개울둑에 앉아 있는 걸 아는지 모르는지 그냥 날쌔게 물만 움켜 낸다. 그러나 번번이 허탕이다. 그대로 재미있는 양, 자꾸 물만 움킨다. 어제처럼 개울을 건너는 사람이 있어야 길을 비킬 모양이다.
그러다가 소녀가 물속에서 무엇을 하나 집어낸다. 하얀 조약돌이었다. 그러고는 벌떡 일어나 팔짝팔짝 징검다리를 뛰어 건너간다.
다 건너가더니 홱 이리로 돌아서며,
"이 바보."
조약돌이 날아왔다.
소년은 저도 모르게 벌떡 일어섰다.
단발머리를 나풀거리며 소녀가 막 달린다. 갈밭 사잇길로 들어섰다. 뒤에는 청량한 가을 햇살 아래 빛나는 갈꽃뿐.
소년은 이 갈꽃이 아주 뵈지 않게 되기까지 그대로 서 있었다. 문득 소녀가 던진 조약돌을 내려다보았다. 물기가 걷혀 있었다. 소년은 조약돌을 집어 주머니에 넣었다.

다음 날부터 좀 더 늦게 개울가로 나왔다. 소녀의 그림자가 뵈지 않았다. 다행이었다.
그러나 이상한 일이었다. 소녀의 그림자가 뵈지 않는 날이 계속될수록 소년의 가슴 한구석에는 어딘가 허전함이 자리 잡는 것이었다. 주머니 속 조약돌을 주무르는 버릇이 생겼다.
그러한 어떤 날, 소년은 전에 소녀가 앉아 물장난을 하던 징검다리 한가운데에 앉아 보았다. 물속에 손을 잠갔다. 세수를 하였다. 물속을 들여다보았다. 검게 탄 얼굴이 그대로 비치었다. 싫었다.
소년은 두 손으로 물속의 얼굴을 움키었다. 몇 번이고 움키었다. 그러다가 깜짝 놀라 일어나고 말았다. 소녀가 이리 건너오고 있지 않느냐.
숨어서 내 하는 꼴을 엿보고 있었구나. 소년은 달리기 시작했다. 디딤돌을 헛짚었다. 한 발이 물속에 빠졌다. 더 달렸다.
몸을 가릴 데가 있어 줬으면 좋겠다. 이쪽 길에는 갈밭도 없다. 메밀밭이다. 전에 없이 메밀꽃 내가 짜릿하니 코를 찌른다고 생각됐다. 미간이 아찔했다. 찝찔한 액체가 입술에 흘러들었다. 코피였다. 소년은 한 손으로 코피를 훔쳐내면서 그냥 달렸다. 어디선가, 바보, 바보, 하는 소리가 자꾸만 뒤따라오는 것 같았다.

토요일이었다.
개울가에 이르니 며칠째 보이지 않던 소녀가 건너편 가에 앉아 물장난을 하고 있었다.
모르는 체 징검다리를 건너기 시작했다. 소녀의 맑고 검은 눈과 마주쳤다.
"비단조개."
"이름두 참 곱다."
갈림길에 왔다.
소녀가 걸음을 멈추며,
"너, 저 산 너머에 가 본 일 있니?"
"우리, 가 보지 않을래? 시골 오니까 혼자서 심심해 못 견디겠다."
논 사잇길로 들어섰다. 벼 가을걷이하는 곁을 지났다.
"아, 재밌다!"
소녀가 허수아비 줄을 잡더니 흔들어 댄다. 소녀의 왼쪽 볼에 살포시 보조개가 패었다.
논이 끝난 곳에 도랑이 하나 있었다. 소녀가 먼저 뛰어 건넜다.
소년이 무밭으로 들어가, 무 두 밑을 뽑아 왔다. 소녀에게 한 밑 건넨다.
소녀도 따라 했다. 그러나 세 입도 못 먹고,
"아, 맵고 지려."
하며 집어 던지고 만다.

산이 가까워졌다. 단풍이 눈에 따가웠다.
소년이 꽃을 꺾어 소녀에게 건넨다.
소녀가 비탈진 곳으로 가다 미끄러졌다. 소년이 손을 잡아 이끌어 올렸다. 소녀의 오른쪽 무릎에 핏방울이 내맺혔다. 소년은 저도 모르게 생채기에 입술을 가져다 대고 빨기 시작했다.
"저기 송아지가 있다. 그리 가 보자."
소년이 고삐를 바투 잡아 쥐고 등을 긁어 주는 척 후딱 올라탔다.
"어서들 집으루 가거라. 소나기가 올라."
먹장구름이 머리 위에 와 있다. 삽시간에 주위가 보랏빛으로 변했다.
산을 내려오는데 굵은 빗방울이 쏟아졌다. 소녀는 입술이 파랗게 질려 있었다. 소년이 무명 겹저고리를 벗어 소녀의 어깨를 싸 주었다.
소년이 수숫단 속을 비집어 소녀를 들였다. 앞에 나앉은 소년은 그냥 비를 맞아야만 했다.
수숫단 속을 벗어 나왔다. 도랑 있는 곳까지 와 보니, 엄청나게 물이 불어 있었다. 소년이 등을 돌려 댔다. 소녀가 순순히 업혔다. 소녀는 어머나 소리를 지르며 소년의 목을 그러안았다.
개울가에 다다르기 전에 가을 하늘은 구름 한 점 없이 쪽빛으로 개어 있었다.

그다음 날은 소녀의 모양이 뵈지 않았다. 매일같이 개울가로 달려와 봐도 뵈지 않았다.
그날도 소년은 주머니 속 흰 조약돌만 만지작거리며 개울가로 나왔다. 그랬더니 이쪽 개울둑에 소녀가 앉아 있는 게 아닌가.
"그동안 앓았다."
"그날 소나기 맞은 것 때메?"
소녀가 가만히 고개를 끄덕였다.
소녀가 분홍 스웨터 앞자락을 내려다본다. 거기에 검붉은 진흙물 같은 게 들어 있었다.
"내 생각해 냈다. 그날 도랑 건널 때 네게 업힌 일 있지? 그때 네 등에서 옮은 물이다."
소년은 얼굴이 확 달아오름을 느꼈다.
갈림길에서 소녀는 대추 한 줌을 내어 준다.
"그리구 저, 우리 이번에 제사 지내구 나서 좀 있다 집을 내주게 됐다."
"왜 그런지 난 이사 가는 게 싫어졌다."
전에 없이 소녀의 까만 눈에 쓸쓸한 빛이 떠돌았다.
소년은 그날 밤 몰래 덕쇠 할아버지네 호두밭으로 가 호두를 땄다. 소녀에게 맛보여야 한다는 생각만이 앞섰다.

어른들의 말이, 내일 소녀네가 양평읍으로 이사 간다는 것이었다.
그날 밤, 소년은 자리에 누워서도 같은 생각뿐이었다. 내일 소녀네가 이사하는 걸 가 보나 어쩌나.
마을 갔던 아버지가 돌아와서 말했다.
"윤 초시 댁두 말이 아니여. 그 많던 전답을 다 팔아 버리구, 대대루 살아오던 집마저 남의 손에 넘기더니, 또 악상까지 당하는 걸 보면……."
"증손이라곤 계집애 그 애 하나뿐이었지요?"
"그렇지. 이번 앤 꽤 여러 날 앓는 걸 약두 변변히 못 써 봤다더군. 지금 같애서는 윤 초시네두 대가 끊긴 셈이지……. 그런데 참 이번 계집애는 어린것이 여간 잔망스럽지가 않어. 글쎄 죽기 전에 이런 말을 했다지 않어? 자기가 죽거든 자기 입던 옷을 꼭 그대루 입혀서 묻어 달라구……."
"""

QUESTIONS = [
    {
        "id": 1,
        "tag": "소재의 상징",
        "excerpt": """그러다가 소녀가 물속에서 무엇을 하나 집어낸다. 하얀 조약돌이었다. 그러고는 벌떡 일어나 팔짝팔짝 징검다리를 뛰어 건너간다.
다 건너가더니 홱 이리로 돌아서며,
"이 바보."
**조약돌**이 날아왔다.
소년은 저도 모르게 벌떡 일어났다.""",
        "question": "다음 장면에서 밑줄 친 소재가 의미하는 바를 작성하시오.",
        "hint": "교과서 27~28페이지를 확인하세요.",
        "placeholder": "조약돌은 [누가] [누구에게] 느끼는 [감정/마음]을 상징한다.",
        "answer_frame": "조약돌은 [누가] [누구에게] 느끼는 [감정/마음]을 상징한다.",
        "key_answer": "조약돌은 소녀가 소년에게 보내는 관심, 호감, 애정을 상징함. 소년이 조약돌을 주머니에 넣고 소중히 간직하는 장면과 연결됨.",
    },
    {
        "id": 2,
        "tag": "인물의 심리",
        "excerpt": "※ 문항 준비 중입니다.",
        "question": "※ 문항 준비 중입니다.",
        "hint": "교과서 xx페이지를 확인하세요.",
        "placeholder": "답안을 입력하세요.",
        "answer_frame": "",
        "key_answer": "",
    },
    {
        "id": 3,
        "tag": "인물의 심리",
        "excerpt": "※ 문항 준비 중입니다.",
        "question": "※ 문항 준비 중입니다.",
        "hint": "교과서 xx페이지를 확인하세요.",
        "placeholder": "답안을 입력하세요.",
        "answer_frame": "",
        "key_answer": "",
    },
    {
        "id": 4,
        "tag": "서술 방식",
        "excerpt": "※ 문항 준비 중입니다.",
        "question": "※ 문항 준비 중입니다.",
        "hint": "교과서 xx페이지를 확인하세요.",
        "placeholder": "답안을 입력하세요.",
        "answer_frame": "",
        "key_answer": "",
    },
    {
        "id": 5,
        "tag": "배경의 기능",
        "excerpt": "※ 문항 준비 중입니다.",
        "question": "※ 문항 준비 중입니다.",
        "hint": "교과서 xx페이지를 확인하세요.",
        "placeholder": "답안을 입력하세요.",
        "answer_frame": "",
        "key_answer": "",
    },
    {
        "id": 6,
        "tag": "주제 파악",
        "excerpt": "※ 문항 준비 중입니다.",
        "question": "※ 문항 준비 중입니다.",
        "hint": "교과서 xx페이지를 확인하세요.",
        "placeholder": "답안을 입력하세요.",
        "answer_frame": "",
        "key_answer": "",
    },
]

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
    st.caption("소나기 속 장면들을 다시 읽고, 숨겨진 의미를 찾아보세요. 내 생각을 쓰면 AI 선생님이 함께 고민해드려요! 🌧️")
    st.divider()

    completed_count = len(st.session_state.completed)
    st.markdown(f"**진행 현황: {completed_count} / {len(QUESTIONS)} 문항 완료**")
    st.progress(completed_count / len(QUESTIONS))
    st.divider()

    cols = st.columns(2)
    for i, q in enumerate(QUESTIONS):
        col = cols[i % 2]
        with col:
            is_done = q["id"] in st.session_state.completed
            label = f"{'✅ ' if is_done else ''}{q['id']}번 | {q['tag']}"
            if st.button(label, key=f"q_{q['id']}", use_container_width=True):
                st.session_state.current_q = q["id"]
                st.session_state.page = "question"
                st.rerun()

def show_question(q):
    if st.button("← 목록으로 돌아가기"):
        st.session_state.page = "main"
        st.rerun()

    st.divider()
    st.markdown(f"### {q['id']}번 문항 | {q['tag']}")
    st.markdown(f"**{q['question']}**")
    st.divider()

    if q["excerpt"] != "※ 문항 준비 중입니다.":
        st.markdown(f"> {q['excerpt'].replace(chr(10), chr(10)+'> ')}")
    else:
        st.info("※ 이 문항은 준비 중입니다.")

    st.info(f"💡 힌트: {q['hint']}")
    st.divider()

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
        if q["key_answer"] == "":
            st.warning("이 문항은 아직 준비 중입니다.")
        else:
            with st.spinner("AI가 피드백을 작성 중입니다..."):
                prompt = f"""당신은 중학교 1학년 국어 교사입니다. 아래는 황순원의 단편소설 「소나기」 전문입니다. 이 작품을 완전히 숙지한 후 학생의 서술형 답안에 피드백을 작성해 주세요.

[작품 전문]
{SONAGI}

[문제]
{q['question']}

[지문]
{q['excerpt']}

[핵심 개념]
- 상징: 추상적인 개념(감정, 생각)을 구체적인 사물로 표현하는 방법
- 이 문항의 핵심: 작품 속 소재나 표현이 어떤 추상적 의미를 나타내는지 추론하는 것

[채점 기준]
{q['key_answer']}

[답안 작성 프레임]
{q['answer_frame']}

[학생 답변]
{answer}

[피드백 작성 원칙 — 반드시 준수]
- 절대로 정답을 직접 알려주지 말 것
- 학생이 스스로 답을 찾아갈 수 있도록 추론 과정을 안내할 것
- 아래 순서로 피드백을 구성할 것:
  1. 학생 답변에서 잘된 점 또는 방향이 맞는 부분 언급
  2. 장면 속 인물의 행동과 감정에 주목하도록 질문 형식으로 유도
  3. 답안 작성 프레임을 제시하며 다시 써볼 수 있도록 안내
- 이름이나 호칭 없이 피드백 내용만 작성
- 200자 이내로 간결하게
- 친절한 존댓말 사용"""

                api_key = st.secrets["GEMINI_API_KEY"]
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
                payload = {"contents": [{"parts": [{"text": prompt}]}]}
                res = requests.post(url, json=payload)
                data = res.json()

                if "candidates" in data:
                    feedback = data["candidates"][0]["content"]["parts"][0]["text"]
                    st.session_state.feedbacks[q["id"]] = feedback
                    st.session_state.completed.add(q["id"])
                    st.success("✅ 피드백")
                    st.markdown(feedback)
                else:
                    st.error(f"오류 내용: {data}")

if st.session_state.page == "main":
    show_main()
elif st.session_state.page == "question":
    q = next((q for q in QUESTIONS if q["id"] == st.session_state.current_q), None)
    if q:
        show_question(q)
