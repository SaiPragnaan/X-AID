console.log("hello");

document.addEventListener("DOMContentLoaded", function () {
    let body = document.querySelector("body");
    let modeBtn = document.querySelector("#mode-toggle");

    let currMode = localStorage.getItem("theme");
    if (!currMode || currMode === "auto") {
        currMode = "dark";
        localStorage.setItem("theme", "dark");
    }
    body.classList.add(currMode);

    modeBtn.addEventListener("click", () => {
        currMode = currMode === "light" ? "dark" : "light";
        if (currMode === "light") {
            modeBtn.setAttribute("class", "fa-solid fa-circle-half-stroke");
        } else {
            modeBtn.setAttribute("class", "fa-solid fa-moon");
        }
        // modeBtn.classList.remove("fa-solid fa-circle-half-stroke", "fa-solid fa-moon");
        body.classList.remove("dark", "light");
        body.classList.add(currMode);
        localStorage.setItem("theme", currMode);
    });
});

window.addEventListener("scroll", () => {
    if (window.scrollY < 0) {
        window.scrollTo(0, 0);
    }
});

document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.querySelector(".search-input");
    const chatMessages = document.querySelectorAll(".message-content");

    searchInput.addEventListener("input", function () {
        const query = searchInput.value.toLowerCase().trim();

        chatMessages.forEach((message) => {
            let text = message.textContent;
            let lowerText = text.toLowerCase();

            if (query.length > 0 && lowerText.includes(query)) {
                // Replace matching text with a highlighted span
                let highlightedText = text.replace(
                    new RegExp(query, "gi"),
                    (match) => `<span class="highlight">${match}</span>`
                );
                message.innerHTML = highlightedText;
            } else {
                // Reset to original text if query is empty
                message.innerHTML = text;
            }
        });
    });
});
