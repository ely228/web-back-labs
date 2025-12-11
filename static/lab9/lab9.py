from flask import Blueprint, render_template, request, session, jsonify
import random

lab9 = Blueprint('lab9', __name__)

if not hasattr(lab9, "boxes"):
    lab9.boxes = []
    used_positions = set()
    box_width = 160
    box_height = 180

    for i in range(10):
        while True:
            x = random.randint(50, 1100)
            y = random.randint(80, 520)
            overlap = False
            for ux, uy in used_positions:
                if abs(x - ux) < box_width and abs(y - uy) < box_height:
                    overlap = True
                    break
            if not overlap:
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
                used_positions.add((x, y))
                break

@lab9.route("/lab9/")
def lab():
    session.setdefault("opened_count", 0)
    return render_template("lab9/index.html")

@lab9.route("/lab9/api/boxes", methods=["POST"])
def get_boxes():
    remaining = len([b for b in lab9.boxes if not b["opened"]])
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
        "remaining": remaining
    })

@lab9.route("/lab9/api/open", methods=["POST"])
def open_box():
    data = request.json
    box_id = data["id"]
    if session.get("opened_count", 0) >= 3:
        return jsonify({"error": "Можно открыть только 3 подарка!"})
    box = lab9.boxes[box_id]
    if box["opened"]:
        return jsonify({"error": "Коробка уже открыта!"})
    if box["premium"] and "user" not in session:
        return jsonify({"error": "Этот подарок только для авторизованных пользователей!"})
    box["opened"] = True
    session["opened_count"] += 1
    return jsonify({
        "text": box["text"],
        "gift": box["gift_img"]
    })

@lab9.route("/lab9/api/reset", methods=["POST"])
def reset_boxes():
    if "user" not in session:
        return jsonify({"error": "Только для авторизованных пользователей!"})
    for box in lab9.boxes:
        box["opened"] = False
    session["opened_count"] = 0
    return jsonify({"success": "Все коробки наполнены заново!"})