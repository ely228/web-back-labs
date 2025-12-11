function loadBoxes() {
    fetch("/lab9/api/boxes", { method: "POST" })
    .then(r => r.json())
    .then(data => {
        document.getElementById("remaining").innerText = data.remaining;
        const field = document.getElementById("field");
        field.innerHTML = "";

        data.boxes.forEach(box => {
            const img = document.createElement("img");
            img.src = box.opened ? box.gift_img : box.box_img;
            img.style.position = "absolute";
            img.style.left = box.x + "px";
            img.style.top = box.y + "px";
            img.style.width = "140px";
            img.style.transition = "all 0.4s";

            if (box.premium && !box.opened) {
                img.style.border = "4px solid gold";
                img.style.borderRadius = "12px";
                img.style.boxShadow = "0 0 15px gold";
            }

            if (!box.opened) {
                img.style.cursor = "pointer";
                img.onclick = () => openBox(box.id, img);
                img.onmouseover = () => img.style.transform = "scale(1.1) rotate(5deg)";
                img.onmouseout = () => img.style.transform = "scale(1) rotate(0)";
            } else {
                img.style.cursor = "default";
            }

            field.appendChild(img);
        });

        const btn = document.getElementById("ded-moroz-btn");
        if (data.is_authenticated) {
            btn.style.display = "block";
        } else {
            btn.style.display = "none";
        }
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
        imgElement.style.transform = "scale(1.4)";
        setTimeout(() => imgElement.style.transform = "scale(1)", 500);
        document.getElementById("message").innerText = data.text;
        setTimeout(loadBoxes, 700);
    });
}

function resetBoxes() {
    fetch("/lab9/api/reset", { method: "POST" })
    .then(r => r.json())
    .then(data => {
        document.getElementById("message").innerText = data.success || data.error;
        loadBoxes();
    });
}

window.onload = loadBoxes;