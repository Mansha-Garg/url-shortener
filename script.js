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