async function loginUser(event) {
    event.preventDefault()
    
    const data = {
        email: document.getElementById("email").value,
        password: document.getElementById("password").value,
    };

    try {
        let response = await fetch("/api/token", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            let errorData = await response.json();
            throw new Error(errorData.detail || "Login failed");
        }

        let token = await response.json();

        document.cookie = `token=${token.access_token}; path=/; Secure; SameSite=Strict`;
        window.location.href = "/";
    } catch (error) {
        console.error("Login error:", error);
        alert(error.message);
    }
}
