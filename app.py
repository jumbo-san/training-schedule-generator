from flask import Flask, render_template, request

app = Flask(__name__)

# -------------------------
# BMI 計算と体格分類
# -------------------------
def calculate_bmi(height_cm, weight_kg):
    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)

def classify_body(bmi):
    if bmi < 18.5:
        return "軽め"
    elif bmi < 25:
        return "標準"
    else:
        return "重め"

# -------------------------
# 宅トレ用メニュー
# -------------------------
MENU = {
    "胸": {
        "軽め": "膝つきプッシュアップ",
        "標準": "プッシュアップ",
        "重め": "膝つきプッシュアップ"
    },
    "脚": {
        "軽め": "スクワット",
        "標準": "ワイドスクワット",
        "重め": "スクワット"
    },
    "背中": {
        "軽め": "バックエクステンション",
        "標準": "タオルローイング",
        "重め": "バックエクステンション"
    }
}

# -------------------------
# 回数（目的別）
# -------------------------
def get_reps(goal):
    if goal == "筋肥大":
        return "8〜12回"
    elif goal == "ダイエット":
        return "15〜20回"
    else:
        return "10〜15回"

# -------------------------
# セット数（頻度別）
# -------------------------
def get_sets(frequency):
    f = int(frequency)
    if f == 1:
        return "1〜2セット"
    elif f == 2:
        return "2セット"
    elif f == 3:
        return "3セット"
    elif f == 4:
        return "3セット"
    else:
        return "3〜4セット"

# -------------------------
# ルーティング
# -------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    menu_result = None

    if request.method == "POST":
        goal = request.form["goal"]
        frequency = request.form["frequency"]
        parts = request.form.getlist("parts")
        height = float(request.form["height"])
        weight = float(request.form["weight"])

        bmi = calculate_bmi(height, weight)
        body_type = classify_body(bmi)

        reps = get_reps(goal)
        sets = get_sets(frequency)

        week_menu = []
        for part in parts:
            exercise = MENU[part][body_type]
            week_menu.append({
                "part": part,
                "exercise": exercise,
                "reps": reps,
                "sets": sets
            })

        menu_result = [week_menu for _ in range(4)]

    return render_template("index.html", menu=menu_result)


if __name__ == "__main__":
    app.run()
