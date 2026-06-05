const CHAT_API = 'http://localhost:8000/api';

async function sendQuestion() {
    const input = document.getElementById('chat-input');
    const messages = document.getElementById('chat-messages');
    const question = input.value.trim();

    if (!question) return;

    messages.innerHTML += `
        <div class="chat-message user">
            🙋 ${question}
        </div>
    `;
    input.value = '';
    messages.scrollTop = messages.scrollHeight;

    const loadingId = 'loading-' + Date.now();
    messages.innerHTML += `
        <div class="chat-message bot" id="${loadingId}">
            🤖 מחשב תשובה...
        </div>
    `;
    messages.scrollTop = messages.scrollHeight;

    try {
        const res = await fetch(`${CHAT_API}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: question })
        });

        const data = await res.json();
        document.getElementById(loadingId).innerHTML = `🤖 ${data.answer}`;

    } catch (e) {
        document.getElementById(loadingId).innerHTML =
            '🤖 שגיאה בחיבור ל-API.';
        console.error('Error:', e);
    }

    messages.scrollTop = messages.scrollHeight;
}

document.addEventListener('DOMContentLoaded', () => {
    // Enter key
    document.getElementById('chat-input').addEventListener('keypress', e => {
        if (e.key === 'Enter') sendQuestion();
    });

    // כפתור שלח
    document.getElementById('send-btn').addEventListener('click', () => {
        sendQuestion();
    });
});