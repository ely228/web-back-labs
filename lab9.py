from flask import Blueprint, render_template, session, jsonify, request
from flask_login import login_required, current_user
import random

lab9 = Blueprint('lab9', __name__)

if not hasattr(lab9, "boxes"):
    lab9.boxes = []
    used = set()
    for i in range(10):
        while True:
            x = random.randint(60, 1080)
            y = random.randint(80, 520)
            if all(abs(x - ux) > 160 or abs(y - uy) > 180 for ux, uy in used):
                lab9.boxes.append({
                    "id": i,
                    "x": x,
                    "y": y,
                    "opened": False,
                    "box_img": f"/static/lab9/box{i+1}.jpg",
                    "gift_img": f"/static/lab9/gift{i+1}.jpg",
                    "text": f"Поздравление №{i+1}! С Новым годом и счастья!",
                    "premium": i >= 7 
                })
                used.add((x, y))
                break

@lab9.route("/lab9/")
def lab():
    session.setdefault("opened_count", 0)
    return render_template("lab9/index.html")

@lab9.route("/lab9/api/boxes", methods=["POST"])
def get_boxes():
    remaining = sum(1 for b in lab9.boxes if not b["opened"])
    return jsonify({
        "boxes": [
            {
                "id": b["id"],
                "x": b["x"],
                "y": b["y"],
                "opened": b["opened"],
                "box_img": b["box_img"],
                "gift_img": b["gift_img"],
                "premium": b["premium"]
            } for b in lab9.boxes
        ],
        "remaining": remaining,
        "is_authenticated": current_user.is_authenticated
    })

@lab9.route("/lab9/api/open", methods=["POST"])
def open_box():
    if session.get("opened_count", 0) >= 3:
        return jsonify({"error": "Можно открыть только 3 подарка!"})

    data = request.get_json()
    box_id = data["id"]
    box = lab9.boxes[box_id]

    if box["opened"]:
        return jsonify({"error": "Коробка уже открыта!"})

    if box["premium"] and not current_user.is_authenticated:
        return jsonify({"error": "Этот подарок доступен только авторизованным пользователям!"})

    box["opened"] = True
    session["opened_count"] = session.get("opened_count", 0) + 1

    return jsonify({
        "text": box["text"],
        "gift": box["gift_img"]
    })

@lab9.route("/lab9/api/reset", methods=["POST"])
@login_required 
def reset_boxes():
    for box in lab9.boxes:
        box["opened"] = False
    session["opened_count"] = 0
    return jsonify({"success": "Дед Мороз наполнил все коробки заново!"})