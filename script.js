const urlInput = document.getElementById("url");
const aliasInput = document.getElementById("alias");
const shortenBtn = document.getElementById("shortenBtn");

const result = document.getElementById("result");
const shortUrl = document.getElementById("shortUrl");
const copyBtn = document.getElementById("copyBtn");


shortenBtn.addEventListener("click", async function () {

    const url = urlInput.value.trim();
    const alias = aliasInput.value.trim();

    if (url === "") {
        alert("Please enter a URL.");
        return;
    }

    shortenBtn.textContent = "SHORTENING...";
    shortenBtn.disabled = true;

    try {

        const response = await fetch("/shorten", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                url: url,
                alias: alias
            })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.error);
            return;
        }

        const shortenedUrl =
            window.location.origin + "/" + data.code;

        shortUrl.textContent = shortenedUrl;
        shortUrl.href = shortenedUrl;
        result.classList.remove("hidden");

    } catch (error) {

        alert("Something went wrong. Please try again.");

    } finally {

        shortenBtn.textContent = "SHORTEN →";
        shortenBtn.disabled = false;

    }
});


copyBtn.addEventListener("click", async function () {

    await navigator.clipboard.writeText(shortUrl.textContent);

    copyBtn.textContent = "COPIED ✓";

    setTimeout(function () {
        copyBtn.textContent = "COPY";
    }, 1500);

});
async function loadRecentLinks() {
    const recentLinks = document.getElementById("recentLinks");

    try {
        const response = await fetch("/links");
        const links = await response.json();

        if (links.length === 0) {
            recentLinks.innerHTML =
                '<p class="empty-state">No routes created yet.</p>';
            return;
        }

        recentLinks.innerHTML = "";

        links.forEach(function (link) {
            const card = document.createElement("div");
            card.className = "recent-card";

            const shortUrl = window.location.origin + "/" + link.code;

            card.innerHTML = `
                <div>
                    <div class="recent-code">/${link.code}</div>
                    <div class="recent-url">${link.url}</div>
                </div>

                <button class="recent-copy">COPY</button>
            `;

            const copyButton = card.querySelector(".recent-copy");

            copyButton.addEventListener("click", async function () {
                await navigator.clipboard.writeText(shortUrl);

                copyButton.textContent = "COPIED ✓";

                setTimeout(function () {
                    copyButton.textContent = "COPY";
                }, 1500);
            });

            recentLinks.appendChild(card);
        });

    } catch (error) {
        recentLinks.innerHTML =
            '<p class="empty-state">Could not load recent routes.</p>';
    }
}

loadRecentLinks();