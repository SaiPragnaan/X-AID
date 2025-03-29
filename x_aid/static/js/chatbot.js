console.log("hi");

const messageList = document.querySelector(".chat-container");
const messageForm = document.querySelector(".message-form");
const messageInput = document.querySelector(".input-query");

messageForm.addEventListener("submit", (evt) => {
    evt.preventDefault();
    const message = messageInput.value.trim();
    // console.log(message)
    if (message.length == 0) {
        return;
    }
    const messageItem = document.createElement("div");
    messageItem.classList.add("chat-message", "user-message");
    messageItem.innerHTML = `
        <p>${message}</p>
    `;
    messageList.appendChild(messageItem);
    messageInput.value = "";

    const getFacts = async () => {
        let reponse = await fetch("/chatbot/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector(
                    "[name=csrfmiddlewaretoken]"
                ).value,
            },
            body: JSON.stringify({ message: message }),
        });
        console.log(reponse);
        data = await reponse.json();
        const reply = data.reply;
        const messageItem = document.createElement("div");
        messageItem.classList.add("chat-message", "bot-message");
        messageItem.innerHTML = `
            <p>${reply}</p>
        `;
        messageList.appendChild(messageItem);
    };
    getFacts();
});

