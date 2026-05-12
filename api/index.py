from flask import Flask, render_template, request, jsonify
import requests
import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os

app = Flask(__name__, template_folder='../templates')

QUESTIONS = [
    {
        "id": 1,
        "label": "개인 문항 1번",
        "tag": "소재의 상징",
        "question": "다음 장면에서 밑줄 친 소재가 의미하는 바를 작성해 봅시다.",
        "excerpt": """그러다가 소녀가 물속에서 무엇을 하나 집어낸다. 하얀 조약돌이었다.<br>
다 건너가더니 홱 이리로 돌아서며,<br>
"이 바보."<br>
<u>조약돌</u>이 날아왔다.<br>
소년은 저도 모르게 벌떡 일어났다.""",
        "hint": "교과서 27~28페이지를 확인하세요.",
        "placeholder": "조약돌은 [누가] [누구에게] 느끼는 [감정/마음]을 상징한다.",
        "answer_frame": "조약돌은 [누가] [누구에게] 느끼는 [감정/마음]을 상징한다.",
        "key_answer": "조약돌은 소녀가 소년에게 보내는 관심, 호감, 애정을 상징함.",
    },
    {
        "id": 2,
        "label": "개인 문항 2번",
        "tag": "소재의 상징",
        "question": "다음 장면에서 밑줄 친 소재가 의미하는 바를 작성해 봅시다.",
        "excerpt": """소녀의 그림자가 뵈지 않는 날이 계속될수록 소년의 가슴 한구석에는 어딘가 허전함이 자리 잡는 것이었다.<br>
<u>주머니 속 조약돌을 주무르는 버릇</u>이 생겼다.""",
        "hint": "교과서 28페이지를 확인하세요.",
        "placeholder": "조약돌은 [누가] [누구에게] 느끼는 [감정/마음]을 상징한다.",
        "answer_frame": "조약돌은 [누가] [누구에게] 느끼는 [감정/마음]을 상징한다.",
        "key_answer": "조약돌은 소년이 소녀에 대해 느끼는 그리움, 애틋함을 상징함.",
    },
    {
        "id": 3,
        "label": "모둠 문항 1번",
        "tag": "인물의 심리",
        "question": "ⓐ와 ⓑ를 중심으로 소녀의 심리가 어떻게 변했는지 작성해 봅시다.",
        "excerpt": """ⓐ <u>소녀가 허수아비 줄을 잡더니 흔들어 댄다.</u> 허수아비가 대고 우쭐거리며 춤을 춘다.<br>
ⓑ <u>돌아다보니 소녀는 지금 자기가 지나쳐 온 허수아비를 흔들고 있다. 좀 전 허수아비보다 더 우쭐거린다.</u>""",
        "hint": "교과서 31페이지를 확인하세요.",
        "placeholder": "ⓐ에서 소녀는 [심리 상태]였는데, ⓑ에서는 [심리 상태]로 변했다.",
        "answer_frame": "ⓐ에서 소녀는 [심리 상태]였는데, ⓑ에서는 [심리 상태]로 변했다.",
        "key_answer": "ⓐ에서 소녀는 허수아비를 처음 발견한 즐거움을 느꼈으나, ⓑ에서는 소년과 함께하는 시간 속에서 흥겨움이 더욱 고조됨.",
    },
    {
        "id": 4,
        "label": "모둠 문항 2번",
        "tag": "소재의 의미 비교",
        "question": "지문1의 ⓐ와 지문2의 ⓑ의 의미를 비교하여 서술해 봅시다.",
        "excerpt": """[지문1] 다시 소년은 꽃 한 옴큼을 꺾어 왔다. <u>ⓐ싱싱한 꽃가지만 골라 소녀에게 건넨다.</u><br>
[지문2] 할 수 없이 뒷걸음질을 쳤다. <u>ⓑ그 바람에 소녀가 안고 있는 꽃묶음이 우그러들었다.</u>""",
        "hint": "[힌트 1] 지문1은 교과서 32페이지, 지문2는 36페이지를 확인하세요.\n[힌트 2] ⓐ와 ⓑ의 꽃 상태가 어떻게 다른지 생각해보세요.",
        "placeholder": "ⓐ는 [                ] 의미를 지니지만, 이와 대조적으로 ⓑ는 [                ] 것을 암시한다.",
        "answer_frame": "ⓐ는 [                ] 의미를 지니지만, 이와 대조적으로 ⓑ는 [                ] 것을 암시한다.",
        "key_answer": "ⓐ는 소녀를 향한 소년의 순수한 호감을 의미하는 반면, ⓑ는 두 사람에게 닥칠 슬픈 결말을 암시함.",
    },
    {
        "id": 5,
        "label": "모둠 문항 3번",
        "tag": "인물의 심리",
        "question": "소년이 그늘만 짚어 돌아온 이유를 작성해 봅시다.",
        "excerpt": """이날 밤, 소년은 몰래 덕쇠 할아버지네 호두밭으로 갔다.<br>
<u>돌아오는 길에는 열이틀 달이 지우는 그늘만 골라 짚었다. 그늘의 고마움을 처음 느꼈다.</u>""",
        "hint": "교과서 40페이지를 확인해보세요.",
        "placeholder": "소년이 그늘만 짚어 돌아온 것은 [이유]이기 때문이다.",
        "answer_frame": "소년이 그늘만 짚어 돌아온 것은 [이유]이기 때문이다.",
        "key_answer": "소년은 남의 호두밭에서 몰래 호두를 딴 것이므로 달빛에 들킬까 봐 그늘만 골라 걸어온 것임.",
    },
    {
        "id": 6,
        "label": "모둠 문항 4번",
        "tag": "인물의 심리",
        "question": "소녀가 입던 옷을 그대로 입혀서 묻어 달라고 한 이유를 작성해 봅시다.",
        "excerpt": """자기가 죽거든 <u>자기 입던 옷을 꼭 그대루 입혀서 묻어 달라</u>구…….""",
        "hint": "교과서 42페이지를 확인하세요.",
        "placeholder": "소녀가 입던 옷을 그대로 입혀 달라고 한 것은 [이유]이기 때문이다.",
        "answer_frame": "소녀가 입던 옷을 그대로 입혀 달라고 한 것은 [이유]이기 때문이다.",
        "key_answer": "소녀가 입던 옷에는 소년과 함께 소나기를 맞으며 도랑을 건널 때 묻은 흙탕물 얼룩이 있음. 소녀는 소년과의 소중한 추억을 간직한 채 떠나고 싶었던 것임.",
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
