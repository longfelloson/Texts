document.addEventListener("DOMContentLoaded", async function displayText() {
    const textId = window.location.pathname.split("/").pop();

    try {
        const response = await fetch("/api/texts/" + textId);
        
        if (!response.ok) {
            const errorData = await response.json();
            alert(errorData[0].msg)
            return;
        }

        const text = await response.json();
        const textDiv = document.getElementById("text");

        const textHeaderSpan = document.createElement("span");
        textHeaderSpan.className = "header";
        textHeaderSpan.innerText = text.header;

        const textBodySpan = document.createElement("span");
        textBodySpan.className = "body";
        textBodySpan.innerText = text.body;

        const textDeleteButton = document.createElement("button");
        textDeleteButton.className = "delete"
        textDeleteButton.innerHTML = "DELETE";
        textDeleteButton.addEventListener("click", () => deleteText(textId));

        textDiv.appendChild(textHeaderSpan);
        textDiv.appendChild(textBodySpan);
        textDiv.appendChild(textDeleteButton);
    } catch (error) {
        alert("No text available.");
        console.error(error);
    }
});


async function deleteText(textId) {
    try {
        await fetch("/api/texts/" + textId, {
            method: "DELETE",
            headers: {"Content-Type": "application/json"},
        })
        window.location.href = "/texts"
    } catch {
        alert("Oops... Try later!")
    }
}