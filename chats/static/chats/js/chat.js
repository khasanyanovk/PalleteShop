document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chatMessages');
    if (chatMessages) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    const urlParams = new URLSearchParams(window.location.search);
    const prefillMessage = urlParams.get('message');

    const textarea = document.querySelector('textarea');
    if (textarea) {
        if (prefillMessage) {
            textarea.value = decodeURIComponent(prefillMessage);
            textarea.style.height = 'auto';
            textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
            window.history.replaceState({}, document.title, window.location.pathname);
        }
        
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 120) + 'px';
        });
        
        textarea.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                const form = document.getElementById('chatForm');
                if (form) {
                    form.requestSubmit();
                }
            }
        });
    }
    
    const form = document.getElementById('chatForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            const textarea = form.querySelector('textarea');
            const messageText = textarea.value.trim();
            
            if (!messageText) return;
            
            fetch(form.action || window.location.href, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const messagesContainer = document.getElementById('chatMessages');
                    const messageHtml = `
                        <div class="message user-message">
                            <div class="message-bubble">
                                <div>${escapeHtml(messageText)}</div>
                                <div class="message-time">
                                    ${new Date().toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'})}, ${new Date().toLocaleDateString('ru-RU')}
                                    <i class="bi bi-check2 message-status"></i>
                                </div>
                            </div>
                        </div>
                    `;
                    messagesContainer.insertAdjacentHTML('beforeend', messageHtml);
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                    
                    // Clear textarea
                    textarea.value = '';
                    textarea.style.height = 'auto';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                if (typeof showToast === 'function') {
                    showToast('Ошибка при отправке сообщения', 'error');
                }
            });
        });
    }
});

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML.replace(/\n/g, '<br>');
}

setInterval(function() {
    const lastMessage = document.querySelector('.message:last-child');
    const chatId = document.querySelector('[data-chat-id]');
    
    if (lastMessage && chatId) {

    }
}, 10000);
