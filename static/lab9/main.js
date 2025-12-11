function loadBoxes() {
    fetch("/lab9/api/boxes", { method: "POST" })
    .then(r => r.json())
    .then(data => {
        let field = document.getElementById("field");
        field.innerHTML = "";
        document.getElementById("remaining").innerText = data.remaining;
        data.boxes.forEach(box => {
            let img = document.createElement("img");
            img.src = box.opened ? box.gift_img : box.box_img;
            img.style.position = "absolute";
            img.style.left = box.x + "px";
            img.style.top = box.y + "px";
            img.style.width = "130px";
            img.style.cursor = box.opened ? "default" : "pointer";
            img.onclick = () => {
                if (!box.opened) openBox(box.id, img);
            };
            field.append(img);
        });
    });
}

function openBox(id, imgElement) {
    fetch("/lab9/api/open", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id })
    })
    .then(r => r.json())
    .then(data => {
        if (data.error) {
            document.getElementById("message").innerText = data.error;
            return;
        }
        imgElement.src = data.gift;
        document.getElementById("message").innerText = data.text;
        loadBoxes();
    });
}

window.onload = loadBoxes;