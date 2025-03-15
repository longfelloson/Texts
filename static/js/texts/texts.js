document.addEventListener("DOMContentLoaded", async function () {
    const response = await fetch("/api/texts");
    const texts = await response.json();
    const parentDiv = document.getElementById("texts");

    for (let i = 0; i < texts.length; i++) {
        let link = `/texts/${texts[i].id}`;
        let fullLink = `${window.location.origin}/texts/${texts[i].id}`;

        let textDiv = document.createElement("div");
        textDiv.className = "text";
        textDiv.innerHTML = `<a href="${link}" class="header">${texts[i].header}</a>`;

        let textLinkIcon = document.createElement("img");
        textLinkIcon.src = "/static/img/link.svg";
        textLinkIcon.className = "link-logo";
        textLinkIcon.addEventListener("click", () => copyTextLink(fullLink));

        textDiv.appendChild(textLinkIcon);
        parentDiv.appendChild(textDiv);
    }
});

async function copyTextLink(fullLink) {
    await navigator.clipboard.writeText(fullLink);
    alert("Copied");
}
