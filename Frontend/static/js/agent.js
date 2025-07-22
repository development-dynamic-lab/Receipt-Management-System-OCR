
document.addEventListener('DOMContentLoaded', function () {
    const userInput = document.querySelector('#user-input');
    const sendButton = document.querySelector('.send-button');
    const chatScreen = document.querySelector('.chat-screen');

    sendButton.addEventListener('click', async function () {
        const message = userInput.value.trim();
        if (message) {
            addMessageToChat(message, 'human');
            userInput.value = '';

            let ai_response = await send_to_ai(message);
            let renderedResponse = formatResponse(ai_response);
            addMessageToChat(renderedResponse, 'ai');
        }
    });

    function addMessageToChat(message, sender) {
        const mainWrap = document.createElement('div');
        mainWrap.classList.add('main-wrap', sender);

        const img = document.createElement('img');
        img.src = sender === 'ai' ? '../static//images/ai_logo.png' : '../static/images/human_logo.png';
        img.width = 50;
        img.height = 50;
        img.alt = `${sender} logo`;

        const responseBox = document.createElement('div');
        responseBox.classList.add('response-box', `${sender}-response`);
        responseBox.innerHTML = message;

        if (sender === 'ai') {
            mainWrap.appendChild(img);
            mainWrap.appendChild(responseBox);
        } else {
            mainWrap.appendChild(responseBox);
            mainWrap.appendChild(img);
        }

        chatScreen.appendChild(mainWrap);
        chatScreen.scrollTop = chatScreen.scrollHeight;
    }

    function formatResponse(response) {
        if (Array.isArray(response)) {
            return response.map(item => {
                const fields = Object.entries(item)
                    .map(([key, value]) => `${key}: ${String(value)}`)
                    .join(', ');
                return `🧾 ${fields}`;
            }).join('<br><br>');
        }

        if (typeof response === 'object' && response !== null) {
            const fields = Object.entries(response)
                .map(([key, value]) => `${key}: ${String(value)}`)
                .join(', ');
            return `🧾 ${fields}`;
        }

        return String(response);
    }

    async function send_to_ai(message) {
        try {
            const response = await fetch('/api/get_ai_response', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_input: message }),
            });

            if (response.ok) {
                const data = await response.json();
                return data.botResponse;
            } else {
                return "⚠️ Error: Unable to get response from AI.";
            }
        } catch (error) {
            console.error("Error in send_to_ai:", error);
            return "⚠️ Oops, something went wrong!";
        }
    }
});
