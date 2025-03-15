async function addText(event) {
    event.preventDefault();

    let data = {
        body: document.getElementById("body").value.trim(),
        header: document.getElementById("text-header").value.trim(),
        expires_at: document.getElementById("expires-at").value || null,
    };

    for (let key in data) {
        if (!data[key] && key !== "expires_at") {
            alert(`Please fill the ${key} of the text`);
            return;
        }
    }

    try {
        const response = await fetch("/api/texts", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });

        let response_json = await response.json();

        if (!response.ok) {
            let errorMessage = Array.isArray(response_json.detail)
                ? response_json.detail.map(e => e.msg).join("\n")
                : response_json.detail || "An error occurred";
            throw new Error(errorMessage);
        }

        alert(response_json.msg);
        document.querySelector("form").reset();
    } catch (error) {
        console.error(error);
        alert(error.message);
    }
}
