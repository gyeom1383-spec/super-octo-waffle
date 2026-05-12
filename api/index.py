import sys
import os

try:
    from flask import Flask, render_template, request, jsonify
    import requests
    import json
    import gspread
    from google.oauth2.service_account import Credentials
    from datetime import datetime
except ImportError as e:
    from flask import Flask
    app = Flask(__name__)

    @app.route("/")
    def error():
        return f"Import 오류: {str(e)}", 500

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    app.template_folder = os.path.join(BASE_DIR, 'templates')
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'))

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
    {
        "id": 2,
        "label": "개인 문항 2번",
        "tag": "소재의 상징",
        "context": """[관련 장면]
다음 날부터 좀 더 늦게 개울가로 나왔다. 소녀의 그림자가 뵈지 않았다. 다행이었다.
그러나 이상한 일이었다. 소녀의 그림자가 뵈지 않는 날이 계속될수록 소년의 가슴 한구석에는 어딘가 허전함이 자리 잡는 것이었다. 주머니 속 조약돌을 주무르는 버릇이 생겼다.
그러한 어떤 날, 소년은 전에 소녀가 앉아 물장난을 하던 징검다리 한가운데에 앉아 보았다. 물속에 손을 잠갔다. 세수를 하였다. 물속을 들여다보았다. 검게 탄 얼굴이 그대로 비치었다. 싫었다.""",
        "excerpt": """다음 날부터 좀 더 늦게 개울가로 나왔다. 소녀의 그림자가 뵈지 않았다. 다행이었다.<br>
그러나 이상한 일이었다. 소녀의 그림자가 뵈지 않는 날이 계속될수록 소년의 가슴 한구석에는 어딘가 허전함이 자리 잡는 것이었다. <u>주머니 속 조약돌을 주무르는 버릇</u>이 생겼다.""",
        "question": "다음 장면에서 밑줄 친 소재가 의미하는 바를 작성해 봅시다.",
        "hint": "교과서 28페이지를 확인하세요.",
        "placeholder": "조약돌은 [누가] [누구에게] 느끼는 [감정/마음]을 상징한다.",
        "answer_frame": "조약돌은 [누가] [누구에게] 느끼는 [감정/마음]을 상징한다.",
        "key_answer": "조약돌은 소년이 소녀에 대해 느끼는 그리움, 애틋함, 마음속 깊이 자리 잡은 감정을 상징함. 소녀가 보이지 않을수록 조약돌을 주무르는 버릇이 생겼다는 행동 묘사와 연결됨.",
    },
    {
        "id": 3,
        "label": "모둠 문항 1번",
        "tag": "인물의 심리",
        "context": """[관련 장면]
논 사잇길로 들어섰다. 벼 가을걷이하는 곁을 지났다.
허수아비가 서 있었다. 소년이 새끼줄을 흔들었다. 참새가 몇 마리 날아간다. '참, 오늘은 일찍 집으로 돌아가 텃논의 참새를 봐야 할걸.' 하는 생각이 든다.
"아, 재밌다!"
소녀가 허수아비 줄을 잡더니 흔들어 댄다. 허수아비가 대고 우쭐거리며 춤을 춘다. 소녀의 왼쪽 볼에 살포시 보조개가 패었다.
저만치 허수아비가 또 서 있다. 소녀가 그리로 달려간다. 그 뒤를 소년도 달렸다. 오늘 같은 날은 일찌감치 집으로 돌아가 집안일을 도와야 한다는 생각을 잊어버리기라도 하려는 듯이.
소녀의 곁을 스쳐 그냥 달린다. 메뚜기가 따끔따끔 얼굴에 와 부딪힌다. 쪽빛으로 한껏 갠 가을 하늘이 소년의 눈앞에서 맴을 돈다. 어지럽다. 저놈의 독수리, 저놈의 독수리, 저놈의 독수리가 맴을 돌고 있기 때문이다.
돌아다보니 소녀는 지금 자기가 지나쳐 온 허수아비를 흔들고 있다. 좀 전 허수아비보다 더 우쭐거린다.""",
        "excerpt": """논 사잇길로 들어섰다. 벼 가을걷이하는 곁을 지났다.<br>
허수아비가 서 있었다. 소년이 새끼줄을 흔들었다. 참새가 몇 마리 날아간다. '참, 오늘은 일찍 집으로 돌아가 텃논의 참새를 봐야 할걸.' 하는 생각이 든다.<br>
"아, 재밌다!"<br>
ⓐ <u>소녀가 허수아비 줄을 잡더니 흔들어 댄다.</u> 허수아비가 대고 우쭐거리며 춤을 춘다. 소녀의 왼쪽 볼에 살포시 보조개가 패었다.<br>
저만치 허수아비가 또 서 있다. 소녀가 그리로 달려간다. 그 뒤를 소년도 달렸다. 오늘 같은 날은 일찌감치 집으로 돌아가 집안일을 도와야 한다는 생각을 잊어버리기라도 하려는 듯이.<br>
소녀의 곁을 스쳐 그냥 달린다. 메뚜기가 따끔따끔 얼굴에 와 부딪힌다. 쪽빛으로 한껏 갠 가을 하늘이 소년의 눈앞에서 맴을 돈다. 어지럽다. 저놈의 독수리, 저놈의 독수리, 저놈의 독수리가 맴을 돌고 있기 때문이다.<br>
ⓑ <u>돌아다보니 소녀는 지금 자기가 지나쳐 온 허수아비를 흔들고 있다. 좀 전 허수아비보다 더 우쭐거린다.</u>""",
        "question": "ⓐ와 ⓑ를 중심으로 소녀의 심리가 어떻게 변했는지 작성해 봅시다.",
        "hint": "교과서 31페이지를 확인하세요.",
        "placeholder": "ⓐ에서 소녀는 [심리 상태]였는데, ⓑ에서는 [심리 상태]로 변했다.",
        "answer_frame": "ⓐ에서 소녀는 [심리 상태]였는데, ⓑ에서는 [심리 상태]로 변했다.",
        "key_answer": "ⓐ에서 소녀는 허수아비를 처음 발견한 신선함과 즐거움을 느끼고 있었으나, ⓑ에서는 소년과 함께하는 시간이 더욱 신나고 흥겨운 상태로 고조됨.",
    },
    {
        "id": 4,
        "label": "모둠 문항 2번",
        "tag": "소재의 의미 비교",
        "context": """[관련 장면 — 지문1]
다시 소년은 꽃 한 옴큼을 꺾어 왔다. 싱싱한 꽃가지만 골라 소녀에게 건넨다.
그러나 소녀는,
"하나두 버리지 말어."

[관련 장면 — 지문2]
소녀가 속삭이듯이, 이리 들어와 앉으라고 했다. 괜찮다고 했다. 소녀가 다시 들어와 앉으라고 했다. 할 수 없이 뒷걸음질을 쳤다. 그 바람에 소녀가 안고 있는 꽃묶음이 우그러들었다. 그러나 소녀는 상관없다고 생각했다.

[맥락]
지문1의 꽃은 소년이 소녀에게 마음을 전하는 매개체이며, 지문2의 꽃묶음이 우그러지는 장면은 소나기라는 시련 속에서도 소녀가 소년과의 추억(꽃)보다 소년 자체를 더 소중히 여김을 보여줌.""",
        "excerpt": """[지문1]<br>
소녀가 산을 향해 달려갔다. 이번은 소년이 뒤따라 달리지 않았다. 그러고도 곧 소녀보다 더 많은 꽃을 꺾었다.<br>
"이게 들국화, 이게 싸리꽃, 이게 도라지꽃……."<br>
"도라지꽃이 이렇게 예쁜 줄은 몰랐네. 난 보랏빛이 좋아! …… 근데 이 양산 같이 생긴 노란 꽃이 뭐지?"<br>
"마타리꽃."<br>
소녀는 마타리꽃을 양산 받듯이 해 보인다. 약간 상기된 얼굴에 살폿한 보조개를 떠올리며.<br>
다시 소년은 꽃 한 옴큼을 꺾어 왔다. <u>ⓐ싱싱한 꽃가지만 골라 소녀에게 건넨다.</u><br>
그러나 소녀는,<br>
"하나두 버리지 말어."<br><br>
[지문2]<br>
수숫단 속은 비는 안 새었다. 그저 어둡고 좁은 게 안됐다. 앞에 나앉은 소년은 그냥 비를 맞아야만 했다. 그런 소년의 어깨에서 김이 올랐다.<br>
소녀가 속삭이듯이, 이리 들어와 앉으라고 했다. 괜찮다고 했다. 소녀가 다시 들어와 앉으라고 했다. 할 수 없이 뒷걸음질을 쳤다. <u>ⓑ그 바람에 소녀가 안고 있는 꽃묶음이 우그러들었다.</u>""",
        "question": "지문1의 ⓐ와 지문2의 ⓑ의 의미를 비교하여 서술해 봅시다.",
        "hint": "[힌트 1] [지문1]은 교과서 32페이지, [지문2]는 36페이지를 확인하세요.\n[힌트 2] ⓐ(싱싱한 꽃)를 건네는 행동에는 소년의 어떤 마음이 담겨 있는지, ⓑ(우그러진 꽃)의 모습은 앞으로 두 사람에게 일어날 사건을 어떻게 미리 보여주는지 생각해 보세요.",
        "placeholder": "ⓐ는 [                ] 의미를 지니지만, 이와 대조적으로 ⓑ는 [                ] 것을 암시한다.",
        "answer_frame": "ⓐ는 [                ] 의미를 지니지만, 이와 대조적으로 ⓑ는 [                ] 것을 암시한다.",
        "key_answer": "ⓐ는 소녀를 향한 소년의 맑고 순수한 사랑(호감)을 의미하는 반면, ⓑ는 꽃이 망가지는 모습을 통해 두 사람에게 닥칠 시련이나 슬픈 결말(이별)을 암시하여, 밝고 어두운 두 분위기가 서로 대조를 이룸.",
    },
    {
        "id": 5,
        "label": "모둠 문항 3번",
        "tag": "인물의 심리",
        "context": """[관련 장면]
이날 밤, 소년은 몰래 덕쇠 할아버지네 호두밭으로 갔다.
낮에 봐 두었던 나무로 올라갔다. 그리고 봐 두었던 가지를 향해 작대기를 내리쳤다. 호두 송이 떨어지는 소리가 별나게 크게 들렸다. 가슴이 선뜩했다. 그러나 다음 순간, 굵은 호두야 많이 떨어져라, 많이 떨어져라, 저도 모를 힘에 이끌려 마구 작대기를 내리치는 것이었다.
돌아오는 길에는 열이틀 달이 지우는 그늘만 골라 짚었다. 그늘의 고마움을 처음 느꼈다.
불룩한 주머니를 어루만졌다. 호두 송이를 맨손으로 깠다가는 옴이 오르기 쉽다는 말 같은 건 아무렇지도 않았다. 그저 근동에서 제일가는 이 덕쇠 할아버지네 호두를 어서 소녀에게 맛보여야 한다는 생각만이 앞섰다.
그러다, 아차, 하는 생각이 들었다. 소녀더러 병이 좀 낫거들랑 이사 가기 전에 한번 개울가로 나와 달라는 말을 못 해 둔 것이었다. 바보 같은 것, 바보 같은 것.""",
        "excerpt": """이날 밤, 소년은 몰래 덕쇠 할아버지네 호두밭으로 갔다.<br>
낮에 봐 두었던 나무로 올라갔다. 그리고 봐 두었던 가지를 향해 작대기를 내리쳤다. 호두 송이 떨어지는 소리가 별나게 크게 들렸다. 가슴이 선뜩했다. 그러나 다음 순간, 굵은 호두야 많이 떨어져라, 많이 떨어져라, 저도 모를 힘에 이끌려 마구 작대기를 내리치는 것이었다.<br>
<u>돌아오는 길에는 열이틀 달이 지우는 그늘만 골라 짚었다. 그늘의 고마움을 처음 느꼈다.</u>""",
        "question": "소년이 그늘만 짚어 돌아온 이유를 작성해 봅시다.",
        "hint": "교과서 40페이지를 확인해보세요.",
        "placeholder": "소년이 그늘만 짚어 돌아온 것은 [이유]이기 때문이다.",
        "answer_frame": "소년이 그늘만 짚어 돌아온 것은 [이유]이기 때문이다.",
        "key_answer": "소년은 덕쇠 할아버지네 호두밭에서 몰래 호두를 딴 것이므로 달빛에 들킬까 봐 그늘만 골라 걸어온 것임. 소녀에게 호두를 주고 싶은 마음이 간절했지만 남의 밭에서 딴 것이기에 들키지 않으려는 조마조마한 심리가 담겨 있음.",
    },
    {
        "id": 6,
        "label": "모둠 문항 4번",
        "tag": "인물의 심리",
        "context": """[관련 장면]
소녀가 분홍 스웨터 앞자락을 내려다본다. 거기에 검붉은 진흙물 같은 게 들어 있었다.
소녀가 가만히 보조개를 떠올리며,
"이게 무슨 물 같니?"
소년은 스웨터 앞자락만 바라다보고 있었다.
"내 생각해 냈다. 그날 도랑 건널 때 네게 업힌 일 있지? 그때 네 등에서 옮은 물이다."
소년은 얼굴이 확 달아오름을 느꼈다.

[결말 장면]
"글쎄 말이지. 이번 앤 꽤 여러 날 앓는 걸 약두 변변히 못 써 봤다더군. 지금 같애서는 윤 초시네두 대가 끊긴 셈이지……. 그런데 참 이번 계집애는 어린것이 여간 잔망스럽지가 않어. 글쎄 죽기 전에 이런 말을 했다지 않어? 자기가 죽거든 자기 입던 옷을 꼭 그대루 입혀서 묻어 달라구……."

[맥락]
소녀가 입던 분홍 스웨터에는 소년과 함께 소나기를 맞으며 도랑을 건널 때 묻은 흙탕물 얼룩이 남아 있음.""",
        "excerpt": """"글쎄 말이지. 이번 앤 꽤 여러 날 앓는 걸 약두 변변히 못 써 봤다더군. 지금 같애서는 윤 초시네두 대가 끊긴 셈이지……. 그런데 참 이번 계집애는 어린것이 여간 잔망스럽지가 않어. 글쎄 죽기 전에 이런 말을 했다지 않어? 자기가 죽거든 <u>자기 입던 옷을 꼭 그대루 입혀서 묻어 달라</u>구……." """,
        "question": "소녀가 입던 옷을 그대로 입혀서 묻어 달라고 한 이유를 작성해 봅시다.",
        "hint": "교과서 42페이지를 확인하세요.",
        "placeholder": "소녀가 입던 옷을 그대로 입혀 달라고 한 것은 [이유]이기 때문이다.",
        "answer_frame": "소녀가 입던 옷을 그대로 입혀 달라고 한 것은 [이유]이기 때문이다.",
        "key_answer": "소녀가 입던 옷(분홍 스웨터)에는 소년과 함께 소나기를 맞으며 도랑을 건널 때 묻은 흙탕물 얼룩이 있음. 소녀는 그 얼룩, 즉 소년과의 소중한 추억을 간직한 채 떠나고 싶었던 것임.",
    },
]

def get_sheets():
    gcp_info = {
        "type": os.environ.get("GCP_TYPE"),
        "project_id": os.environ.get("GCP_PROJECT_ID"),
        "private_key_id": os.environ.get("GCP_PRIVATE_KEY_ID"),
        "private_key": os.environ.get("GCP_PRIVATE_KEY").replace("\\n", "\n"),
        "client_email": os.environ.get("GCP_CLIENT_EMAIL"),
        "client_id": os.environ.get("GCP_CLIENT_ID"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_x509_cert_url": os.environ.get("GCP_CERT_URL"),
    }
    creds = Credentials.from_service_account_info(
        gcp_info,
        scopes=[
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
    )
    client = gspread.authorize(creds)
    return client.open("26년 용화중_상징적 의미 추론하기(소나기)").sheet1


def log_to_sheets(student_class, student_group, question_label, student_answer, feedback):
    for attempt in range(3):
        try:
            sheet = get_sheets()
            sheet.append_row([
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                student_class,
                student_group,
                question_label,
                student_answer,
                feedback
            ])
            break
        except Exception:
            continue


@app.route("/")
def index():
    return render_template("index.html", questions=QUESTIONS)


@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.json
    q_id = data.get("question_id")
    answer = data.get("answer")
    student_class = data.get("student_class")
    student_group = data.get("student_group")

    q = next((q for q in QUESTIONS if q["id"] == q_id), None)
    if not q:
        return jsonify({"error": "문항을 찾을 수 없습니다."}), 404

    api_key = os.environ.get("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite-preview-06-17:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}

    prompt = f"""너는 대한민국 중학교 1학년 국어 선생님이야.
반드시 한국어(한글)로만 대답해야 해.
중국어, 일본어, 영어 알파벳 등 다른 언어는 절대 쓰면 안 돼.

[문제]: {q['question']}
[정답 방향]: {q['key_answer']}
[학생 답변]: {answer}

아래 두 부분으로만 피드백을 작성해줘.

[선생님의 다정한 피드백 💌]
잘한 부분을 구체적으로 칭찬하고, 보완할 점을 지문 표현을 따옴표로 인용하며 힌트로 알려줘. 정답은 직접 말하지 마. 2~3문장.

[한 걸음 더 나아가기 위한 나의 미션 🐾]
- 내가 잘한 점:
- 나의 다음 행동:
- 힌트가 되는 지문:"""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "maxOutputTokens": 600,
            "temperature": 0.3
        }
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=55)
        if res.status_code == 200:
            result = res.json()
            feedback_text = result["candidates"][0]["content"]["parts"][0]["text"]
            log_to_sheets(student_class, student_group, q["label"], answer, feedback_text)
            return jsonify({"feedback": feedback_text})
        else:
            return jsonify({"error": "API 오류가 발생했습니다."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
