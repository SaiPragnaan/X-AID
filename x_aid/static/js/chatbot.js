const messageList = document.querySelector(".chat-container");
const messageForm = document.querySelector(".message-form");
const messageInput = document.querySelector(".input-query");
const imageInput = document.querySelector("#image-upload");
const imagePreviewContainer = document.querySelector("#image-preview");
const previewImg = document.getElementById("preview-img");

const scrollToBottom = () => {
    if (!messageList) return;
    messageList.scrollTo({ top: messageList.scrollHeight, behavior: "smooth" });
};

window.onload = () => setTimeout(scrollToBottom, 200);

messageForm.addEventListener("submit", (evt) => {
    evt.preventDefault();

    const message = messageInput.value.trim();
    const imageFile = imageInput.files.length > 0 ? imageInput.files[0] : null;
    if (!message && !imageFile) return;

    if (message) {
        appendUserMessage(message);
        sendMessageToServer(message);
    }

    if (imageFile) {
        const reader = new FileReader();
        reader.onload = (e) => {
            appendUserImage(e.target.result);
            sendImageToServer(imageFile);
        };
        reader.readAsDataURL(imageFile);
    }

    messageInput.value = "";
    imageInput.value = "";
    imagePreviewContainer.style.display = "none";
});

const appendUserMessage = (message) => {
    const messageItem = document.createElement("div");
    messageItem.classList.add("chat-message", "user-message");
    messageItem.innerHTML = `<p class="message-content">${message}</p>`;
    messageList.appendChild(messageItem);
    setTimeout(scrollToBottom, 100);
};

const appendUserImage = (imageSrc) => {
    const messageItem = document.createElement("div");
    messageItem.classList.add("chat-message", "user-message");
    messageItem.innerHTML = `<img src="${imageSrc}" class="message-image user-image" alt="User Image"/>`;
    messageList.appendChild(messageItem);
    setTimeout(scrollToBottom, 100);
};

const appendBotMessage = (reply) => {
    const messageItem = document.createElement("div");
    messageItem.classList.add("chat-message", "bot-message");
    messageItem.innerHTML = `<p class="message-content">${reply}</p>`;
    messageList.appendChild(messageItem);
    setTimeout(scrollToBottom, 100);
};

const appendBotImage = (imageSrc) => {
    const messageItem = document.createElement("div");
    messageItem.classList.add("chat-message", "bot-message");
    messageItem.innerHTML = `<img src="${imageSrc}" class="message-image bot-image" alt="Bot Image"/>`;
    messageList.appendChild(messageItem);
    setTimeout(scrollToBottom, 100);
};

const sendMessageToServer = async (message) => {
    let response = await fetch("/chatbot/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
        },
        body: JSON.stringify({ message: message }),
    });
    let replyData = await response.json();
    if (replyData.reply) appendBotMessage(replyData.reply);
};

const sendImageToServer = async (file) => {
    const formData = new FormData();
    formData.append("image", file);
    formData.append("csrfmiddlewaretoken", document.querySelector("[name=csrfmiddlewaretoken]").value);

    let response = await fetch("/chatbot/", { method: "POST", body: formData });
    let replyData = await response.json();
    if (replyData.bot_reply) appendBotMessage(replyData.bot_reply);
    if (replyData.bot_image) appendBotImage(replyData.bot_image);
};

imageInput.addEventListener("change", function () {
    if (this.files && this.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) {
            previewImg.src = e.target.result;
            imagePreviewContainer.style.display = "block";
        };
        reader.readAsDataURL(this.files[0]);
        setTimeout(() => messageInput.focus(), 100);
    } else {
        imagePreviewContainer.style.display = "none";
    }
});
