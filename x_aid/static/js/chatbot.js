const messageList = document.querySelector(".chat-container");
const messageForm = document.querySelector(".message-form");
const messageInput = document.querySelector(".input-query");
const imageInput = document.querySelector("#image-upload");

const scrollToBottom = () => {
    let chatContainer = document.querySelector(".chat-container");
    if (!chatContainer) return;

    chatContainer.scrollTo({
        top: chatContainer.scrollHeight,
        behavior: "smooth",
    });
};

messageForm.addEventListener("submit", (evt) => {
    evt.preventDefault();

    const message = messageInput.value.trim();
    const imageFile = imageInput.files.length > 0 ? imageInput.files[0] : null;
    if (message.length === 0 && !imageFile) {
        return;
    }

    if (message.length > 0) {
        appendUserMessage(message);
        sendMessageToServer(message);
    }

    if (imageFile) {
        console.log("hi1");
        const reader = new FileReader();
        reader.onload = (e) => {
            console.log("hi2");
            appendUserImage(e.target.result);
            sendImageToServer(imageFile);
        };
        reader.readAsDataURL(imageFile);
    }

    messageInput.value = "";
    imageInput.value = "";
});

appendUserMessage = (message) => {
    const messageItem = document.createElement("div");
    messageItem.classList.add("chat-message", "user-message");
    messageItem.innerHTML = `<p  class="message-content">${message}</p>`;
    messageList.appendChild(messageItem);
    setTimeout(scrollToBottom, 100);
};

appendUserImage = (imageSrc) => {
    console.log("hi3");
    const messageItem = document.createElement("div");
    messageItem.classList.add("chat-message", "user-message");
    messageItem.innerHTML = `<img src="${imageSrc}" class="message-image user-image" alt="User Image"/>`;
    messageList.appendChild(messageItem);
    setTimeout(scrollToBottom, 100);
};

appendBotMessage = (reply) => {
    const messageItem = document.createElement("div");
    messageItem.classList.add("chat-message", "bot-message");
    messageItem.innerHTML = `<p class="message-content">${reply}</p>`;
    messageList.appendChild(messageItem);
    setTimeout(scrollToBottom, 100);
};

appendBotImage = (imageSrc) => {
    const messageItem = document.createElement("div");
    messageItem.classList.add("chat-message", "bot-message");
    messageItem.innerHTML = `<img src="${imageSrc}" class="message-image bot-image" alt="Bot Image"/>`;
    messageList.appendChild(messageItem);
    setTimeout(scrollToBottom, 100);
};

sendMessageToServer = async (message) => {
    let response = await fetch("/chatbot/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
                .value,
        },
        body: JSON.stringify({ message: message }),
    });

    let replyData = await response.json();
    if (replyData.reply) {
        appendBotMessage(replyData.reply);
    }
};

sendImageToServer = async (file) => {
    console.log("hi4");
    const formData = new FormData();
    formData.append("image", file);
    formData.append(
        "csrfmiddlewaretoken",
        document.querySelector("[name=csrfmiddlewaretoken]").value
    );

    let response = await fetch("/chatbot/", {
        method: "POST",
        body: formData,
    });

    let replyData = await response.json();
    if (replyData.bot_reply) {
        appendBotMessage(replyData.bot_reply);
    }
    if (replyData.bot_image) {
        appendBotImage(replyData.bot_image);
    }
};
