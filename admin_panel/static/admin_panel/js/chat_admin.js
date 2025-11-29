document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('adminChatMessages');
    if (chatMessages) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    const textarea = document.querySelector('textarea');
    if (textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 120) + 'px';
        });

        textarea.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                const form = document.getElementById('adminChatForm');
                if (form) {
                    form.requestSubmit();
                }
            }
        });
    }

    const form = document.getElementById('adminChatForm');
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
                    const messagesContainer = document.getElementById('adminChatMessages');
                    const messageHtml = `
                        <div class="message admin-message">
                            <div class="message-bubble">
                                <div>${escapeHtml(messageText)}</div>
                                <div class="message-time">
                                    Вы • ${new Date().toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'})}, ${new Date().toLocaleDateString('ru-RU')}
                                </div>
                            </div>
                        </div>
                    `;
                    messagesContainer.insertAdjacentHTML('beforeend', messageHtml);
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;

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
